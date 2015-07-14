import json

from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPServiceUnavailable,
)
from pyramid.response import Response
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
    db.create_submission(data, sanitize=True)
    return {}


@view_config(route_name='submissions', request_method='GET',
             renderer='submissions/index.mako')
def submissions_get(request):
    """List submissions.

    GET /submissions

    """
    db = DB()
    submissions = db.get_submissions_json()

    return {
        'submissions': json.dumps(submissions),
    }


@view_config(route_name='submission', request_method='GET',
             renderer='submissions/show.mako')
def submission_show(request):
    """Show a submission detail page.

    GET /submissions/:id

    """
    submission_id = request.matchdict['id']

    db = DB()
    submission = db.get_submission(submission_id)
    if not submission:
        return HTTPNotFound()

    related_submissions = db.get_related_submissions(submission)
    return {
        'submission': submission,
        'related_submissions': list(related_submissions),
    }


@view_config(route_name='submission_svg')
def submission_svg(request):
    """Return svg data for a submission.

    GET /submissions/:id.svg

    """
    submission_id = request.matchdict['id']

    db = DB()
    submission = db.get_submission(submission_id)

    if not submission:
        return HTTPNotFound()

    if not submission.svg:
        return HTTPServiceUnavailable("Unable to retrieve svg")

    return Response(
        body=submission.svg, charset='utf-8',
        content_type='image/svg+xml')


@view_config(route_name='submission_yaml')
def submission_yaml(request):
    """Return bundle yaml for a submission.

    GET /submissions/:id.yaml

    """
    submission_id = request.matchdict['id']

    db = DB()
    submission = db.get_submission(submission_id)

    if not submission:
        return HTTPNotFound()

    return Response(
        body=submission.bundle_yaml, charset='utf-8',
        content_type='text/yaml')
