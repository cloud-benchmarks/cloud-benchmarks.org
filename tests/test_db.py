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
