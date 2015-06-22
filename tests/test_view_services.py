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
        self.assertEqual(
            response['submissions'].first().id,
            submission.id
        )


class IntegrationTest(IntegrationTestBase):
    def test_show_environment(self):
        """ GET Service

        GET /services/:name 200

        """
        # load a test submission first
        self.app.post_json('/submissions', self.submission_data)
        self.app.get('/services/cassandra')
