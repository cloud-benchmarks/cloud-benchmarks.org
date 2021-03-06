import json

from pyramid import testing

from base import (
    UnitTestBase,
    IntegrationTestBase,
)


class UnitTest(UnitTestBase):
    def test_show_environment_succeeds(self):
        """Test showing submissions for an environment"""
        from cloudbenchmarksorg.views.environments import environments_show
        from cloudbenchmarksorg.db import DB

        # load a test row
        db = DB()
        submission = db.create_submission(self.submission_data)
        db.flush()

        # query by calculated env name
        request = testing.DummyRequest()
        request.matchdict['name'] = submission.environment.name
        response = environments_show(request)
        submissions = json.loads(response['submissions'])
        self.assertEqual(
            submissions[0]['environment']['uuid'],
            submission.environment.uuid
        )

        # query by provider_type
        request = testing.DummyRequest()
        request.matchdict['name'] = submission.environment.provider_type
        response = environments_show(request)
        submissions = json.loads(response['submissions'])
        self.assertEqual(
            submissions[0]['environment']['uuid'],
            submission.environment.uuid
        )

    def test_environments_index(self):
        """Test showing submissions for an environment"""
        from cloudbenchmarksorg.views.environments import environments_index
        from cloudbenchmarksorg.db import DB

        # load a test row
        db = DB()
        submission = db.create_submission(self.submission_data)
        db.flush()

        request = testing.DummyRequest()
        response = environments_index(request)
        names = [row.name for row in response['environments']]
        self.assertEqual(
            names,
            [submission.environment.name]
        )


class IntegrationTest(IntegrationTestBase):
    def test_show_environment(self):
        """ GET Environment

        GET /environments/:name 200

        """
        # load a test submission first
        self.app.post_json('/submissions', self.submission_data)
        self.app.get('/environments/gce-us-central-1')

    def test_environments_index(self):
        """ GET Environments

        GET /environments 200

        """
        # load a test submission first
        self.app.post_json('/submissions', self.submission_data)
        self.app.get('/environments')
