import sqlalchemy as sa

from . import models as M


class DB(object):
    def __init__(self):
        self.session = M.DBSession()

    def flush(self):
        self.session.flush()

    def get_services(self):
        """Return query of distinct services across all submissions.

        """
        return self.session.query(
            sa.distinct(
                sa.func.jsonb_array_elements_text(
                    M.Submission._service_names)
            ).label('service')
        ).order_by('service')

    def create_submission(self, data, sanitize=False):
        """Create and persist a new Submission.

        You should validate ``data`` before calling this method.

        """
        existing = self.get_submission_by_tag(
            data['action']['action']['tag'])
        if existing:
            return existing

        submission = M.Submission(data=data)
        if sanitize:
            submission.sanitize()

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

    def get_submission_by_tag(self, tag):
        """Fetch a single Submission by tag.

        """
        return self.session.query(M.Submission) \
            .filter(M.Submission.data[(
                'action', 'action', 'tag')].astext == tag) \
            .first()

    def get_submissions_json(self, *args, **kw):
        """Same as `get_submissions_query` but with
        results as json.

        """
        results = []
        for s, asc_rank, desc_rank in self.get_submissions_query(*args, **kw):
            d = s.to_json()
            d['rank'] = asc_rank if s.sort_direction == 'asc' else desc_rank
            results.append(d)
        return results

    def get_submissions_query(self, service=None, environment_id=None):
        """Return a query result iterable where each result contains:

            (Submission, asc_rank, desc_rank)

        Rankings are among other Submissions with the same benchmark_name.

        :param service: Only include submissions that contain this service
        :param environment_id: Only include submissions for the Environment
            with this id

        """
        q = self.session.query(
            M.Submission,
            sa.func.rank().over(
                partition_by=M.Submission.benchmark_name,
                order_by=M.Submission._result_value).label('asc_rank'),
            sa.func.rank().over(
                partition_by=M.Submission.benchmark_name,
                order_by=M.Submission._result_value.desc()).label('desc_rank'),
        )

        if service:
            q = q.filter(
                M.Submission._service_names.contains([service]))

        if environment_id:
            q = q.filter_by(environment_id=environment_id)

        q = q.order_by(M.Submission.created_at.desc())
        return q

    def get_related_submissions(self, submission):
        """Return query of Submissions related to (same benchmark name),
        but not including ``submission``.

        """
        order_by = M.Submission._result_value
        minmax = sa.func.min
        if submission.result.get('direction') == 'desc':
            order_by = order_by.desc()
            minmax = sa.func.max

        # subquery to get best result per distinct environment name
        sub = self.session.query(
            M.Environment.name.label('envname'),
            minmax(M.Submission._result_value).label('result')) \
            .filter(M.Submission.environment_id == M.Environment.id) \
            .filter(M.Submission.benchmark_name == submission.benchmark_name) \
            .group_by('envname').subquery()

        return self.session.query(M.Submission) \
                .join(M.Environment,
                    M.Submission.environment_id == M.Environment.id) \
                .join(sub, sa.and_(
                    M.Submission._result_value == sub.c.result,
                    M.Environment.name == sub.c.envname)) \
                .filter(M.Submission.id != submission.id) \
                .filter(M.Submission._result_value != None) \
                .order_by(order_by)  # noqa

    def get_environment(self, **kw):
        """Return an Environment that matches the criteria specified
        by ``**kw``.

        """
        return self.session.query(M.Environment) \
            .filter_by(**kw) \
            .first()

    def get_environment_names(self):
        """Return query of distinct environment names across all
        submissions.

        """
        return self.session.query(
            sa.distinct(M.Environment.name).label('name')
        ).order_by('name')
