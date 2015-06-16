import json
import os
import unittest


class SubmissionValidatorTest(unittest.TestCase):
    def test_example_validates(self):
        here = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(here, 'data', 'submission.json')) as f:
            submission = json.load(f)

        from cloudbenchmarksorg.validators import validate_submission
        self.assertIsNone(validate_submission(submission))
