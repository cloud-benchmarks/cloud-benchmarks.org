from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('submissions', '/submissions')
    config.add_route('submission', '/submissions/{id}')
    config.add_route('submission_svg', '/submissions/{id}/svg')
    config.add_route('environment', '/environments/{name}')
    config.add_route('services', '/services')
    config.add_route('service', '/services/{name}')

    config.scan()
    return config.make_wsgi_app()
