import json

from pyramid import testing

from base import (
    UnitTestBase,
    IntegrationTestBase,
)


class UnitTest(UnitTestBase):
    def test_show_service_succeeds(self):
        """Test showing submissions for a service"""
        from cloudbenchmarksorg.views.services import services_show
        from cloudbenchmarksorg.db import DB

        # load a test row
        db = DB()
        submission = db.create_submission(self.submission_data)
        db.flush()

        request = testing.DummyRequest()
        request.matchdict['name'] = submission._service_names[0]
        response = services_show(request)
        submissions = json.loads(response['submissions'])
        self.assertEqual(submissions[0]['id'], submission.id)
        self.assertEqual(submissions[0]['rank'], 1)

    def test_services_index(self):
        """Test listing all services"""
        from cloudbenchmarksorg.views.services import services_index
        from cloudbenchmarksorg.db import DB

        # load a test row
        db = DB()
        submission = db.create_submission(self.submission_data)
        db.flush()

        request = testing.DummyRequest()
        response = services_index(request)
        q = response['services']
        self.assertEqual(
            [row.service for row in q],
            sorted(submission._service_names))


class IntegrationTest(IntegrationTestBase):
    def test_show_service(self):
        """ GET Service

        GET /services/:name 200

        """
        # load a test submission first
        self.app.post_json('/submissions', self.submission_data)
        self.app.get('/services/cassandra')

    def test_services_index(self):
        """ GET Services

        GET /services 200

        """
        # load a test submission first
        self.app.post_json('/submissions', self.submission_data)
        self.app.get('/services')
