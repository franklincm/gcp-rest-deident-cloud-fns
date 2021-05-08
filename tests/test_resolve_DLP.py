import base64
import unittest
import pytest
from unittest.mock import MagicMock, Mock, patch

from main import resolve_DLP


class TestCreateDLPJob(unittest.TestCase):
    def job_result(self):
        jr = MagicMock()
        jr.name = MagicMock()
        jr.name.return_value = "test"
        jr.inspect_details.result.info_type_stats = [
            MagicMock(),
            MagicMock(),
            MagicMock(),
        ]
        jr.inspect_details.requested_options.job_config.storage_config.cloud_storage_options.file_set.url = (
            "test-file.txt"
        )
        return jr

    @patch("main.pubsub.PublisherClient.publish")
    @patch("main.StorageClient")
    @patch("main.DlpServiceClient.get_dlp_job")
    def test_resolve_DLP(self, mocked_dlp, mocked_storage, mocked_publisher):
        mocked_dlp.return_value = self.job_result()
        mocked_storage.return_value = MagicMock()
        mocked_publisher.return_value = MagicMock()

        data = {"attributes": {"DlpJobName": "test"}}

        resolve_DLP(data, None)

        mocked_dlp.assert_called_with(request={"name": "test"})
        mocked_publisher.assert_called_with(
            "projects/gcp-rest-deident/topics/new-sensitive-doc", b"test-file.txt"
        )
