import base64
import unittest
from unittest.mock import MagicMock, patch

from main import resolve_DLP

class TestCreateDLPJob(unittest.TestCase):

    @patch("main.pubsub.PublisherClient")
    @patch("main.StorageClient")
    @patch("main.DlpServiceClient.get_dlp_job")
    def test_resolve_DLP(self, mocked_dlp, mocked_storage, mocked_publisher):
        mocked_dlp.get_dlp_job.return_value = MagicMock()
        mocked_storage.get_bucket.return_value = MagicMock()

        data = {
            "attributes" : {
                "DlpJobName" : "test"
            }
        }
        
        resolve_DLP(data, None)
        
        mocked_dlp.assert_called()
