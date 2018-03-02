# -*- coding: utf-8 -*-
from operator import itemgetter

from flask_babelex import lazy_gettext as _
from lxml import etree
from lxml.builder import E, ElementMaker
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_utils import ChoiceType
from slugify import slugify_unicode
from unidecode import unidecode

from apollo.core import db
from apollo.dal.models import Resource

NSMAP = {
    None: 'http://www.w3.org/2002/xforms',
    'h': 'http://www.w3.org/1999/xhtml',
    'ev': 'http://www.w3.org/2001/xml-events',
    'xsd': 'http://www.w3.org/2001/XMLSchema',
    'jr': 'http://openrosa.org/javarosa'
}

HTML_E = ElementMaker(namespace=NSMAP['h'], nsmap=NSMAP)
EVT_E = ElementMaker(namespace=NSMAP['ev'], nsmap=NSMAP)
SCHEMA_E = ElementMaker(namespace=NSMAP['xsd'], nsmap=NSMAP)
ROSA_E = ElementMaker(namespace=NSMAP['jr'], nsmap=NSMAP)


class Form(Resource):
    FORM_TYPES = (
        ('CHECKLIST', _('Checklist Form')),
        ('INCIDENT', _('Incident Form'))
    )

    __mapper_args__ = {'polymorphic_identity': 'form'}
    __tablename__ = 'form'

    id = db.Column(
        db.Integer, db.Sequence('form_id_seq'), primary_key=True)
    name = db.Column(db.String, nullable=False)
    prefix = db.Column(db.String, nullable=False)
    form_type = db.Column(ChoiceType(FORM_TYPES), nullable=False)
    require_exclamation = db.Column(db.Boolean, default=True)
    data = db.Column(JSONB)
    version_identifier = db.Column(db.String)
    deployment_id = db.Column(
        db.Integer, db.ForeignKey('deployment.id', ondelete='CASCADE'),
        nullable=False)
    form_set_id = db.Column(
        db.Integer, db.ForeignKey('form_set.id'), nullable=False)
    resource_id = db.Column(
        db.Integer, db.ForeignKey('resource.resource_id'))
    quality_checks = db.Column(JSONB)
    party_mappings = db.Column(JSONB)
    calculate_moe = db.Column(db.Boolean)
    accreditated_voters_tag = db.Column(db.String)
    quality_checks_enabled = db.Column(db.Boolean, default=False)
    invalid_votes_tag = db.Column(db.String)
    registered_votes_tag = db.Column(db.String)
    blank_votes_tag = db.Column(db.String)

    deployment = db.relationship('Deployment', backref='forms')
    form_set = db.relationship('FormSet', backref='forms')

    def _populate_field_cache(self):
        self._field_cache = {
            f['tag']: f for g in self.data['groups'] for f in g['fields']
        }

    def _populate_group_cache(self):
        self._group_cache = {
            g['name']: g for g in self.data['groups']
        }

    def get_form_type_display(self):
        d = dict(Form.FORM_TYPES)
        return d[self.form_type]

    @property
    def tags(self):
        if not hasattr(self, '_field_cache'):
            self._populate_field_cache()

        return sorted(self._field_cache.keys())

    def get_field_by_tag(self, tag):
        if not hasattr(self, '_field_cache'):
            self._populate_field_cache()

        return self._field_cache.get(tag)

    def to_xml(self):
        root = HTML_E.html()
        head = HTML_E.head(HTML_E.title(self.name))
        data = E.data(id='-1')
        model = E.model(E.instance(data))

        body = HTML_E.body()
        model.append(E.bind(nodeset='/data/form_id', readonly='true()'))
        model.append(E.bind(nodeset='/data/version_id', readonly='true()'))

        form_id = etree.Element('form_id')
        form_id.text = str(self.id)

        version_id = etree.Element('version_id')
        version_id.text = self.version_identifier

        data.append(form_id)
        data.append(version_id)

        data.append(E.device_id())
        data.append(E.phone_number())
        data.append(E.phone_number())

        device_id_bind = E.bind(nodeset='/data/device_id')
        device_id_bind.attrib['{{{}}}preload'.format(NSMAP['jr'])] = \
            'property'
        device_id_bind.attrib['{{{}}}preloadParams'.format(NSMAP['jr'])] = \
            'deviceid'

        subscriber_id_bind = E.bind(nodeset='/data/subscriber_id')
        subscriber_id_bind.attrib['{{{}}}preload'.format(NSMAP['jr'])] = \
            'property'
        subscriber_id_bind.attrib['{{{}}}preloadParams'.format(NSMAP['jr'])] = \
            'subscriberid'

        phone_number_bind = E.bind(nodeset='/data/phone_number')
        phone_number_bind.attrib['{{{}}}preload'.format(NSMAP['jr'])] = 'property'
        phone_number_bind.attrib['{{{}}}preloadParams'.format(NSMAP['jr'])] = 'phonenumber'

        model.append(device_id_bind)
        model.append(subscriber_id_bind)
        model.append(phone_number_bind)

        for group in self.data['groups']:
            grp_element = E.group(E.label(group['name']))
            for field in group['fields']:
                data.append(etree.Element(field['tag']))
                path = '/data/{}'.format(field['tag'])

                # TODO: construct field data

            body.append(grp_element)

        head.append(model)
        root.append(head)
        root.append(body)

        return root


class FormBuilderSerializer(object):
    @classmethod
    def serialize_field(cls, field):
        data = {
            'label': field['tag'],
            'description': field['description'],
            'analysis': field.get('analysis_type')
        }

        if field.get('is_comment'):
            data['component'] = 'textarea'
        elif not field.get('options'):
            data['component'] = 'textInput'
            data['required'] = field.get('is_boolean', False)
            data['min'] = field.get('min', 0)
            data['max'] = field.get('max', 9999)
        else:
            sorted_options = sorted(field['options'].items(), key=itemgetter(1))
            data['options'] = [opt[0] for opt in sorted_options]
            if field.get('is_multi_choice'):
                data['component'] = 'checkbox'
            else:
                data['compoent'] = 'radio'

        return data

    @classmethod
    def serialize_group(cls, group):
        field_data = []

        field_data.append({
            'label': group['name'],
            'component': 'group'
        })

        field_data.extend([cls.serialize_field(f) for f in group['fields']])

        return field_data

    @classmethod
    def serialize(cls, form):
        group_data = []
        if form.data:
            for group in form.data['groups']:
                group_data.extend(cls.serialize_group(group))
        data = {'fields': group_data}
        return data

    @classmethod
    def deserialize(cls, form, data):
        groups = []
        current_group = None

        if len(data['fields']) > 0:
            if data['fields'][0]['component'] != 'group':
                raise ValueError('Fields specified outside of group')

        for f in data['fields']:
            if f['component'] == 'group':
                group = {
                    'name': f['label'],
                    'slug': unidecode(slugify_unicode(f['label'])),
                    'fields': []
                }
                current_group = group
                groups.append(group)
                continue

            field = {
                'tag': f['label'],
                'description': f['description']
            }

            if f['analysis']:
                field['analysis_type'] = f['analysis']

            if f['component'] == 'textarea':
                field['is_comment'] = True
                field['analysis_type'] = 'N/A'
            elif f['component'] == 'textInput':
                field['is_boolean'] = f['required']
                if f['min']:
                    field['min'] = f['min']
                if f['max']:
                    field['max'] = f['max']
            else:
                field['options'] = {
                    k: v for v, k in enumerate(f['options'], 1)}
                if f['component'] == 'checkbox':
                    field['is_multi_choice'] = True

            current_group['fields'].append(field)

            # invalidate the form cache
            if hasattr(form, '_field_cache'):
                delattr(form, '_field_cache')
            if hasattr(form, '_group_cache'):
                delattr(form, '_group_cache')
            if hasattr(form, '_schema_cache'):
                delattr(form, '_schema_cache')

        form.data = {'groups': groups}
        form.save()
