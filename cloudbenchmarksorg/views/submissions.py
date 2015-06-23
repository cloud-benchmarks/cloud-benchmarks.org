from pyramid.httpexceptions import (
    HTTPNotFound,
)
from pyramid.view import view_config

from .. import validators
from ..db import DB


@view_config(route_name='submissions', request_method='POST',
             renderer='json')
def submissions_post(request):
    """Post a new submission.

    POST /submissions

    """
    data = request.json_body
    errors = validators.validate_submission(data)
    if errors:
        request.response.status = 400
        return {
            "errors": [
                e.message for e in errors
            ],
        }

    db = DB()
    db.create_submission(data)
    return {}


@view_config(route_name='submissions', request_method='GET',
             renderer='submissions/index.mako')
def submissions_get(request):
    """List submissions.

    GET /submissions

    """
    db = DB()
    submissions_query = db.get_submissions_query()
    return {
        'submissions_query': submissions_query,
    }


@view_config(route_name='submission', request_method='GET',
             renderer='submissions/show.mako')
def submission_show(request):
    """Show a submission.

    GET /submissions/:id

    """
    submission_id = request.matchdict['id']

    db = DB()
    submission = db.get_submission(submission_id)
    if not submission:
        return HTTPNotFound()

    return {
        'submission': submission,
    }
