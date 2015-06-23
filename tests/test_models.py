import responses

from base import (
    UnitTestBase,
)


class SubmissionTest(UnitTestBase):
    def setUp(self):
        from cloudbenchmarksorg import models as M
        super(SubmissionTest, self).setUp()
        self.submission = M.Submission(data=self.submission_data)

    def test_services_dict(self):
        s = self.submission
        self.assertEqual(s.services_dict, s.data['bundle']['services'])

    def test_services(self):
        s = self.submission

        services = sorted(list(s.services()), key=lambda x: x.charm_name)
        self.assertEqual(services[0].charm_name, 'cabs-collector')
        self.assertEqual(services[0].unit_count, 0)
        self.assertEqual(services[1].charm_name, 'cassandra')
        self.assertEqual(services[1].unit_count, 1)

        services = list(s.services(filtered=True))
        self.assertEqual(len(services), 1)
        self.assertEqual(services[0].charm_name, 'cassandra')
        self.assertEqual(services[0].unit_count, 1)

    def test_svg(self):
        from cloudbenchmarksorg.models.submission import SVG_URL
        with responses.RequestsMock() as req_mock:
            svg_data = 'svg data'
            content_type = 'image/svg+xml'

            req_mock.add(
                responses.POST, SVG_URL, body=svg_data,
                status=406, content_type=content_type,
            )
            self.assertIsNone(self.submission.svg)

            req_mock.reset()
            req_mock.add(
                responses.POST, SVG_URL, body=svg_data,
                status=200, content_type=content_type,
            )
            self.assertEqual(self.submission.svg, svg_data)
            # access again, make sure cached copy is used
            # (no second request)
            self.assertEqual(self.submission.svg, svg_data)
            self.assertEqual(len(req_mock.calls), 1)


class EnvironmentTest(UnitTestBase):
    def setUp(self):
        from cloudbenchmarksorg import models as M
        super(EnvironmentTest, self).setUp()
        self.env = M.Environment(**self.submission_data['environment'])

    def test_name(self):
        e = self.env
        self.assertEqual(e._parse_name(), 'gce-us-central-1')

        e.region = ''
        self.assertEqual(e._parse_name(), 'gce')

        e.cloud = 'hpcloud'
        self.assertEqual(e._parse_name(), 'hpcloud')
