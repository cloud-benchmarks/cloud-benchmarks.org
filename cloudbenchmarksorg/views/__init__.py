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
            "errors": errors,
        }

    db = DB()
    db.create_submission(data)
    return {}
