from . import models as M


class DB(object):
    def __init__(self):
        self.session = M.DBSession()

    def flush(self):
        self.session.flush()

    def create_submission(self, data):
        """Create and persist a new Submission.

        You should validate ``data`` before calling this method.

        """
        submission = M.Submission(data=data)

        env_data = data['environment']
        env = self.get_environment(uuid=env_data.get('uuid'))
        if not env:
            env = M.Environment(**env_data)

        submission.environment = env
        self.session.add(submission)
        return submission

    def get_submission(self, id_):
        """Fetch a single Submission by id.

        """
        return self.session.query(M.Submission).get(int(id_))

    def get_submissions_query(self, service=None):
        """Return query for Submissions.

        :param service: Only include submissions that contain this service

        """
        q = self.session.query(M.Submission)

        if service:
            q = q.filter(
                M.Submission._service_names.contains([service]))

        q = q.order_by(M.Submission.created_at.desc())
        return q

    def get_environment(self, **kw):
        """Return an Environment that matches the criteria specified
        by ``**kw``.

        """
        return self.session.query(M.Environment) \
            .filter_by(**kw) \
            .first()
