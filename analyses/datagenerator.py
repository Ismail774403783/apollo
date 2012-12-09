from django.core.cache import cache
import networkx as nx
import numpy as np
import pandas as pd
from django_dag.models import Node, Edge
from core.models import *


def sub_location_types(location_id):
    '''Given the PK for a location, retrieve the types of locations
    lower than the specified one.'''

    # TODO: change this to something that allows for retrieval
    # of the node without ancestors without ambiguity
    if location_id == 0:
        return [LocationType.objects.latest(field_name='pk').get_ancestors()[-1].name]

    try:
        root_location = Location.objects.get(pk=location_id)
    except Location.DoesNotExist:
        return None

    children_nodes = root_location.type.get_children()

    if not children_nodes:
        return None

    return [x.name for x in children_nodes]


def make_histogram(options, dataset):
    temp = []

    for option in options:
        temp.append(dataset.count(option))

    return temp


def get_data_records(form, location_root=0):
    '''
    Given a form model instance and a location pk, generate a pandas DataFrame
    containing the submitted form values for locations below the specified
    location_root.
    '''
    # fields that can store multiple variables are to be handled differently
    multivariate_fields = FormField.objects.filter(group__form=form, allow_multiple=True).values_list('tag', flat=True)
    regular_fields = FormField.objects.filter(group__form=form, allow_multiple=False).values_list('tag', flat=True)
    all_fields = list(multivariate_fields) + list(regular_fields)

    # retrieve normal and reversed locations graphs
    locations_graph = get_locations_graph()
    locations_graph_reversed = get_locations_graph(reverse=True)
    location_types = sub_location_types(location_root)

    # if the location_root is defined, then we'll retrieve all sublocations based
    # on the location_root which will be used for retrieving submissions if not
    # we'll just use all locations in the graph
    if location_root:
        sub_location_ids = nx.dfs_tree(locations_graph_reversed, location_root).nodes()
    else:
        sub_location_ids = locations_graph.nodes()

    # in addition to retrieving field data, also retrieve the location_id
    submissions = list(Submission.objects.filter(location__pk__in=sub_location_ids, observer=None).data(all_fields).values(*(['location_id'] + all_fields)))

    for submission in submissions:
        '''
        Annotate the submissions with their ancestral location data as specified by `location_types`
        '''
        if location_types:
            ancestor_locations = get_location_ancestors_by_type(locations_graph, submission['location_id'], location_types)
            for ancestor_location in ancestor_locations:
                submission[ancestor_location['type']] = ancestor_location['name']

        # for numerical processing, we need to convert the responses into integers
        # note also that multivariates are converted into a list non numeric values
        # are represented as NaNs
        for _field in regular_fields:
            submission[_field] = int(submission[_field]) if submission[_field] else pd.np.nan
        for _field in multivariate_fields:
            submission[_field] = map(lambda x: int(x) if x else pd.np.nan, submission[_field].split(",") if submission[_field] else [])

    return (pd.DataFrame(submissions), regular_fields, multivariate_fields)


def generate_process_data(location_id, form):
    location_types = sub_location_types(location_id)

    if not location_types:
        return {}

    data_frame, univariate_fields, multivariate_fields = get_data_records(form, location_id)

    dataset = {}

    for location_type in location_types:
        location_data = {}

        df = data_frame.groupby(location_type)

        # add in the univariate fields
        for field in univariate_fields:
            field_data = {}

            regions = df[field].aggregate({'mean': np.mean,
                'std': lambda x: np.std(x)})

            global_mean = np.mean(data_frame[field])
            global_std = np.std(data_frame[field])

            field_data['regions'] = regions.to_dict()
            field_data['summary'] = {'mean': global_mean, 'std': global_std}

            location_data[field] = field_data

        dataset[location_type] = location_data

        # add in the multivariate fields
        for field in multivariate_fields:
            field_options = [ x.option for x in FormFieldOption.objects.filter(field__tag=field)]
            pass

    return dataset

def generate_results_data(location_root, form):
    pass


def generate_locations_graph():
    '''
    Creates a directed acyclical graph of the locations database
    This is more performant for performing tree lookups and is
    faster than the alternative of running several queries to
    retrieve this graph from the database
    '''
    nodes = Node.objects.filter(graph__name='location').values('pk', 'object_id')
    locations = Location.objects.filter(pk__in=[node['object_id'] for node in nodes]).values('pk', 'name', 'type__name')
    DG = nx.DiGraph()
    for location in locations:
        DG.add_node(location['pk'], name=location['name'], type=location['type__name'])
    edges = Edge.objects.filter(graph__name='location').values_list('node_from__object_id', 'node_to__object_id')
    for node_from, node_to in edges:
        DG.add_edge(node_from, node_to)
    return DG


def get_locations_graph(reverse=False):
    '''
    This provides a means of caching the generated
    graph and serving up the graph from the cache
    as needed.

    There's an optional parameter to retrieve the
    reversed version of the graph
    '''
    graph = cache.get('reversed_locations_graph') if reverse else cache.get('locations_graph')
    if not graph:
        if reverse:
            graph = generate_locations_graph().reverse()
            # cache for 30 days
            cache.set('reversed_locations_graph', graph, 3592000)
        else:
            graph = generate_locations_graph()
            # cache for 30 days
            # we compensate by invalidating the cache when any Location
            # object changes
            cache.set('locations_graph', graph, 3592000)
    return graph


def get_location_ancestors_by_type(graph, location_id, types=[]):
    '''
    This method provides a means of retrieving the ancestors of a particular location
    of specified types as defined in the LocationType model. It uses the depth-first-search
    algorithm in retrieving this subgraph
    '''
    nodes = graph.subgraph(nx.dfs_tree(graph, location_id).nodes()).nodes(data=True)
    return [node[1] for node in nodes if node[1]['type'] in types]