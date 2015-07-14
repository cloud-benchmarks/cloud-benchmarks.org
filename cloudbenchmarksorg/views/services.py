import json

from pyramid.view import view_config

from ..db import DB


@view_config(route_name='services', request_method='GET',
             renderer='services/index.mako')
def services_index(request):
    """List all services (distinct services across all submissions).

    GET /services

    """
    db = DB()
    query = db.get_services()
    return {
        'services': query,
    }


@view_config(route_name='service', request_method='GET',
             renderer='services/show.mako')
def services_show(request):
    """List submissions for a service.

    GET /services/:name

    """
    service_name = request.matchdict['name']

    db = DB()
    submissions = db.get_submissions_json(service=service_name)

    return {
        'submissions': json.dumps(submissions),
    }
