from pyramid.httpexceptions import (
    HTTPFound,
)
from pyramid.view import view_config


@view_config(route_name='home')
def home(request):
    """Home page

    GET /

    """
    return HTTPFound(location='/submissions')
