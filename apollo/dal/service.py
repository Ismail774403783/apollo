# -*- coding: utf-8 -*-
from flask import abort
from flask_login import current_user


class Service(object):
    '''Database service wrapper class'''
    __model__ = None

    def _get_current_deployment(self):
        if current_user:
            deployment = current_user.deployment
        else:
            deployment = None

        return deployment

    def _isinstance(self, model, raise_error=True):
        rv = isinstance(model, self.__model__)
        if not rv and raise_error:
            error_msg = '{0} is not of type {1}'.format(model, self.__model__)
            raise ValueError(error_msg)

        return rv

    def save(self, model, commit=True):
        return model.save(commit)

    def find(self, **kwargs):
        return self.__model__.query.filter_by(**kwargs)

    def filter(self, *args):
        return self.__model__.query.filter(*args)

    def all(self):
        return self.__model__.query.all()

    def get(self, *args):
        return self.filter(*args).one_or_none()

    def get_or_404(self, *args):
        rv = self.get(*args)
        if rv is None:
            abort(404)

        return rv

    def fget_or_404(self, **kwargs):
        return self.find(**kwargs).first_or_404()

    def first(self, **kwargs):
        return self.filter(**kwargs).first()

    def new(self, **kwargs):
        return self.__model__(**kwargs)

    def create(self, **kwargs):
        return self.save(self.new(**kwargs))

    def update(self, model, commit=True, **kwargs):
        self._isinstance(model)
        return model.update(commit=commit, **kwargs)

    def delete(self, model, commit=True):
        self._isinstance(model)
        return model.delete(commit=commit)

    @property
    def query(self):
        return self.__model__.query
