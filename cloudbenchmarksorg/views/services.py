from pyramid.view import view_config

from ..db import DB


@view_config(route_name='service', request_method='GET',
             renderer='services/show.mako')
def services_show(request):
    """List submissions for a service.

    GET /services/:name

    """
    service_name = request.matchdict['name']

    db = DB()
    query = db.get_submissions_query(service=service_name)
    return {
        'submissions': query,
    }
