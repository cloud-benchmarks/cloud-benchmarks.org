from base import (
    UnitTestBase,
)


class DBTest(UnitTestBase):
    def test_get_submissions_query(self):
        from cloudbenchmarksorg.db import DB

        # load a test row
        db = DB()
        submission = db.create_submission(self.submission_data)
        db.flush()

        q = db.get_submissions_query(service='cassandra')
        sub, a_rank, d_rank = q.first()

        self.assertEqual(q.count(), 1)
        self.assertEqual(sub.id, submission.id)
        self.assertEqual(a_rank, 1)
        self.assertEqual(d_rank, 1)

        q = db.get_submissions_query(service='non-existent')
        self.assertEqual(q.count(), 0)

    def test_get_submission_by_tag(self):
        from cloudbenchmarksorg.db import DB

        # load a test row
        db = DB()
        submission = db.create_submission(self.submission_data)
        db.flush()

        existing = db.get_submission_by_tag(
            submission.data['action']['action']['tag'])

        self.assertEqual(existing, submission)

        existing = db.get_submission_by_tag('foo')
        self.assertIsNone(existing)

    def test_get_services(self):
        from cloudbenchmarksorg.db import DB

        # load a test row
        db = DB()
        submission = db.create_submission(self.submission_data)
        db.flush()

        q = db.get_services()
        services = [row.service for row in q]
        self.assertEqual(services, sorted(submission._service_names))

    def test_get_environment_names(self):
        from cloudbenchmarksorg.db import DB

        # load a test row
        db = DB()
        submission = db.create_submission(self.submission_data)
        db.flush()

        q = db.get_environment_names()
        names = [row.name for row in q]
        self.assertEqual(names, [submission.environment.name])

    def test_get_related_submissions(self):
        from cloudbenchmarksorg.db import DB

        def make_related_result(env, result):
            import copy
            import uuid
            d = copy.deepcopy(self.submission_data)
            d['environment']['provider_type'] = env
            d['environment']['uuid'] = str(uuid.uuid4())
            d['action']['output']['meta']['composite']['value'] = result
            d['action']['action']['tag'] = str(uuid.uuid4())
            return d

        # load test submissions
        db = DB()
        submission_gce = db.create_submission(self.submission_data)
        submission_azure = db.create_submission(
            make_related_result('azure', 99999.0))
        submission_ec2 = db.create_submission(
            make_related_result('ec2', 199999.0))
        db.flush()

        q = db.get_related_submissions(submission_gce)
        self.assertEqual(
            [submission_ec2, submission_azure],
            list(q)
        )
