from . import models as M


class DB(object):
    def create_submission(self, data):
        """Create and persist a new Submission.

        Validate ``data`` before calling this method.

        """
        s = M.Submission(data=data)
        M.DBSession.add(s)
        return s
