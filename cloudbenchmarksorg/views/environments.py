from pyramid.view import view_config

from ..db import DB


@view_config(route_name='environment', request_method='GET',
             renderer='environments/show.mako')
def environments_show(request):
    """List submissions for an environment.

    GET /environments/:name

    """
    env_name = request.matchdict['name']

    db = DB()
    environment = db.get_environment(name=env_name)
    return {
        'environment': environment,
    }
