from base import (
    UnitTestBase,
)


class SubmissionTest(UnitTestBase):
    def setUp(self):
        from cloudbenchmarksorg import models as M
        super(SubmissionTest, self).setUp()
        self.submission = M.Submission(data=self.submission_data)

    def test_cloud_name(self):
        s = self.submission
        self.assertEqual(s.cloud_name, 'gce-us-central-1')

        s.data['environment']['region'] = ''
        self.assertEqual(s.cloud_name, 'gce')

        s.data['environment']['cloud'] = 'hpcloud'
        self.assertEqual(s.cloud_name, 'hpcloud')

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
