import base64
import unittest
from unittest.mock import MagicMock, patch

from main import deident_text

class TestCreateDLPJob(unittest.TestCase):
    
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
