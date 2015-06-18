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

    def test_services(self):
        s = self.submission
        self.assertEqual(s.services, s.data['bundle']['services'])

    def test_charms(self):
        s = self.submission

        charms = sorted(list(s.charms()), key=lambda x: x.name)
        self.assertEqual(charms[0].name, 'cabs-collector')
        self.assertEqual(charms[0].count, 0)
        self.assertEqual(charms[1].name, 'cassandra')
        self.assertEqual(charms[1].count, 1)

        charms = list(s.charms(filtered=True))
        self.assertEqual(len(charms), 1)
        self.assertEqual(charms[0].name, 'cassandra')
        self.assertEqual(charms[0].count, 1)
