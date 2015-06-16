from pyramid import testing

from base import UnitTestBase


class TestViews(UnitTestBase):
    def test_post_submission_succeeds(self):
        """ Make sure we can post a new submission"""
        from cloudbenchmarksorg.views import submissions_post

        request = testing.DummyRequest(
            json_body=self.submission_data
        )

        response = submissions_post(request)
        self.assertEqual(response, {})

    def test_post_submission_fails(self):
        """ Make sure we can't post garbage data as a new submission"""
        from cloudbenchmarksorg.views import submissions_post

        request = testing.DummyRequest(
            json_body={}
        )

        response = submissions_post(request)
        self.assertTrue('errors' in response)
