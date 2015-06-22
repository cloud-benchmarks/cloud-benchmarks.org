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

        self.assertEqual(q.count(), 1)
        self.assertEqual(q.first().id, submission.id)

        q = db.get_submissions_query(service='non-existent')
        self.assertEqual(q.count(), 0)
