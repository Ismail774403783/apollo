from functools import wraps


from flask import render_template, session
from flask.ext.login import user_logged_out
from flask.ext.mongoengine import MongoEngineSessionInterface
from flask.ext.security import MongoEngineUserDatastore

from .. import factory, models
from ..core import db, menu, security

from . import assets
from .helpers import gen_page_list, set_request_presets


def create_app(settings_override=None, register_security_blueprint=True):
    """Returns the frontend application instance"""
    app = factory.create_app(__name__, __path__, settings_override)

    # Init assets
    assets.init_app(app)

    menu.init_app(app)

    userdatastore = MongoEngineUserDatastore(db, models.User, models.Role)

    security.init_app(app, userdatastore,
                      register_blueprint=register_security_blueprint)
    app.session_interface = MongoEngineSessionInterface(db)

    # Register custom error handlers
    if not app.debug:
        for e in [500, 404, 403]:
            app.errorhandler(e)(handle_error)

    @app.before_first_request
    def create_user_roles():
        userdatastore.find_or_create_role('clerk')
        userdatastore.find_or_create_role('manager')
        userdatastore.find_or_create_role('analyst')
        userdatastore.find_or_create_role('admin')

    # register deployment selection middleware
    app.before_request(set_request_presets)

    # add Jinja2 filters
    app.jinja_env.filters.update(pagelist=gen_page_list)

    # Login and logout signal handlers
    user_logged_out.connect(lambda app, user: session.clear())

    return app


def handle_error(e):
    code = getattr(e, 'code', 500)
    return render_template('{code}.html'.format(code=code)), code


def route(bp, *args, **kwargs):
    def decorator(f):
        @bp.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return f

    return decorator
