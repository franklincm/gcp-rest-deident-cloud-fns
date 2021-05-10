import base64
import pytest
import unittest
from unittest.mock import MagicMock, patch

from main import deident_text


class TestCreateDLPJob(unittest.TestCase):
    def mock_blob(self, filename):
        mblob = MagicMock()
        mblob.download_as_bytes = MagicMock()
        mblob.download_as_bytes.return_value = b"teststuff"
        return mblob

    def mock_bucket(self):
        mbucket = MagicMock(get_blob=self.mock_blob)
        # mbucket.get_blob = MagicMock()
        # mbucket.get_blob.return_value = self.mock_blob()
        return mbucket

    @patch("main.StorageClient")
    @patch("main.DlpServiceClient.deidentify_content")
    def test_deident_text(self, mocked_dlp, mocked_storage):
        mocked_dlp.deidentify_content.return_value = []
        mocked_storage().get_bucket.return_value = self.mock_bucket()

        file_name = "test_file.txt"
        file_name_utf = file_name.encode(encoding="UTF-8")
        file_name_base64 = base64.b64encode(file_name_utf)

        data = {"data": file_name_base64}

        deident_text(data, None)

        parent = "projects/gcp-rest-deident"

        inspect_config = {
            "info_types": [
                {"name": "FIRST_NAME"},
                {"name": "PHONE_NUMBER"},
                {"name": "EMAIL_ADDRESS"},
                {"name": "US_SOCIAL_SECURITY_NUMBER"},
            ],
            "min_likelihood": "POSSIBLE",
            "limits": {"max_findings_per_request": 0},
        }

        deidentify_config = {
            "info_type_transformations": {
                "transformations": [
                    {
                        "primitive_transformation": {
                            "character_mask_config": {
                                "masking_character": "#",
                                "number_to_mask": 25,
                            }
                        }
                    }
                ]
            }
        }

        contentItem = {"byte_item": {"type_": "TEXT_UTF8", "data": b"teststuff"}}

        mocked_dlp.assert_called_with(
            request = {
                "parent" : parent,
                "deidentify_config" : deidentify_config,
                "inspect_config" : inspect_config,
                "item" : contentItem
            }
        )

        mocked_storage.assert_called()
