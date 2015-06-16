from . import models as M


class DB(object):
    def __init__(self):
        self.session = M.DBSession()

    def create_submission(self, data):
        """Create and persist a new Submission.

        Validate ``data`` before calling this method.

        """
        s = M.Submission(data=data)
        self.session.add(s)
        return s
