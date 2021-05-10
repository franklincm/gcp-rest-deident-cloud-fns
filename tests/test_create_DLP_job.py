import base64
import unittest
from unittest.mock import MagicMock, patch

from main import create_DLP_job


class TestCreateDLPJob(unittest.TestCase):
    @patch("main.DlpServiceClient.create_dlp_job")
    def test_create_DLP_job(self, mocked_dlp):
        mocked_dlp.create_dlp_job.return_value = []

        file_name = "some-file.txt"
        data = {"name": file_name}

        create_DLP_job(data, {})

        parent = "projects/gcp-rest-deident"
        inspect_job = {
            "inspect_config": {
                "info_types": [
                    {"name": "FIRST_NAME"},
                    {"name": "PHONE_NUMBER"},
                    {"name": "EMAIL_ADDRESS"},
                    {"name": "US_SOCIAL_SECURITY_NUMBER"},
                ],
                "min_likelihood": "POSSIBLE",
                "limits": {"max_findings_per_request": 0},
            },
            "storage_config": {
                "cloud_storage_options": {
                    "file_set": {"url": "gs://doc-staging-141223/some-file.txt"}
                }
            },
            "actions": [
                {"pub_sub": {"topic": "projects/gcp-rest-deident/topics/new-document"}}
            ],
        }

        mocked_dlp.assert_called_with(parent=(parent), inspect_job=(inspect_job))
