from base import UnitTestBase


class SubmissionValidatorTest(UnitTestBase):
    def test_example_validates(self):
        from cloudbenchmarksorg.validators import validate_submission
        self.assertIsNone(validate_submission(self.submission_data))
