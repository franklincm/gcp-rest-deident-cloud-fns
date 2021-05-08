import base64
import unittest
from unittest.mock import MagicMock, patch

from main import create_DLP_job
from main import resolve_DLP
from main import deident_text

class TestCreateDLPJob(unittest.TestCase):
    @patch("main.DlpServiceClient.create_dlp_job")
    def test_create_DLP_job(self, mocked_dlp):
        mocked_dlp.create_dlp_job.return_value = []

        file_name = "some-file.txt"
        data = {"name" : file_name}
    
        create_DLP_job(data, {})

        PROJECT_ID = "gcp-rest-deident"
        parent = f"projects/{PROJECT_ID}"
        
        mocked_dlp.assert_called()
        

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


    @patch("main.StorageClient")
    @patch("main.DlpServiceClient.deidentify_content")
    def test_deident_text(self, mocked_dlp, mocked_storage):
        mocked_dlp.deidentify_content.return_value = []
        mocked_storage.get_bucket.return_value = MagicMock()
        
        file_name = "test_file.txt"
        file_name_utf = file_name.encode(encoding="UTF-8")
        file_name_base64 = base64.b64encode(file_name_utf)

        data = {
            "data" : file_name_base64
        }
        
        deident_text(data, None)
        
        mocked_dlp.assert_called()
        mocked_storage.assert_called()
