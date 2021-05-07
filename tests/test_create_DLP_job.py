import unittest
from unittest.mock import patch

from main import create_DLP_job

class TestCreateDLPJob(unittest.TestCase):
    @patch("main.dlp.create_dlp_job")
    def test_create_DLP_job(self, mocked_dlp):
        mocked_dlp.create_dlp_job.return_value = []

        file_name = "some-file.txt"
        data = {"name" : file_name}
    
        create_DLP_job(data, {})
        
        mocked_dlp.assert_called_once()
