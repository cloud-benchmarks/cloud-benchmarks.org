from . import models as M


class DB(object):
    def __init__(self):
        self.session = M.DBSession()

    def flush(self):
        self.session.flush()

    def create_submission(self, data):
        """Create and persist a new Submission.

        Validate ``data`` before calling this method.

        """
        s = M.Submission(data=data)
        self.session.add(s)
        return s

    def get_submissions_query(self):
        """Return query for Submissions.

        """
        q = self.session.query(M.Submission) \
                .order_by(M.Submission.created_at.desc())
        return q
