import json

from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config

from ..db import DB


@view_config(route_name='environments', request_method='GET',
             renderer='environments/index.mako')
def environments_index(request):
    """List all environments.

    GET /environments

    """
    db = DB()
    q = db.get_environment_names()
    return {
        'environments': q,
    }


@view_config(route_name='environment', request_method='GET',
             renderer='environments/show.mako')
def environments_show(request):
    """List submissions for an environment.

    GET /environments/:name

    """
    env_name = request.matchdict['name']

    db = DB()
    # Query by calculated name first, then by provider_type if
    # we didn't get a match
    environment = db.get_environment(name=env_name)
    if not environment:
        environment = db.get_environment(provider_type=env_name)

    if not environment:
        return HTTPNotFound()

    submissions = db.get_submissions_json(environment_id=environment.id)
    return {
        'submissions': json.dumps(submissions),
    }
