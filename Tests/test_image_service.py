import unittest
import os
import shutil # For cleaning up temp folder
from unittest.mock import patch, MagicMock, mock_open
import requests # For requests.exceptions
from Services.ImageService import ImageService

class TestImageService(unittest.TestCase):

    def setUp(self):
        self.image_service = ImageService()
        self.temp_folder = "temp_test_images" # Use a dedicated test temp folder
        # Ensure clean state for temp_test_images
        if os.path.exists(self.temp_folder):
            shutil.rmtree(self.temp_folder)
        # The service itself creates the folder if it doesn't exist via os.makedirs(exist_ok=True)

    def tearDown(self):
        # Clean up the test temp folder after each test
        if os.path.exists(self.temp_folder):
            shutil.rmtree(self.temp_folder)

    @patch('requests.get')
    @patch('os.makedirs') # Mock makedirs to check its call, though exist_ok=True handles it.
    @patch('builtins.open', new_callable=mock_open)
    def test_save_photo_from_web_success_with_filename(self, mock_file_open, mock_os_makedirs, mock_requests_get):
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"image_data"
        mock_response.raise_for_status = MagicMock()
        mock_requests_get.return_value = mock_response

        url = "http://example.com/image.jpg"
        file_name = "my_image"
        expected_file_path = os.path.join(self.temp_folder, f"{file_name}.jpg")

        # Act
        result_path = self.image_service.SavePhotofromWeb(url, file_name, temp_folder=self.temp_folder)

        # Assert
        mock_os_makedirs.assert_called_once_with(self.temp_folder, exist_ok=True)
        mock_requests_get.assert_called_once_with(url)
        mock_response.raise_for_status.assert_called_once()
        mock_file_open.assert_called_once_with(expected_file_path, "wb")
        mock_file_open().write.assert_called_once_with(b"image_data")
        self.assertEqual(result_path, expected_file_path)
        # Check if file actually created (by open) is not directly testable with mock_open easily for existence.
        # The mock assertions cover the behavior.

    @patch('requests.get')
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('uuid.uuid4') # Mock uuid to control generated filename
    def test_save_photo_from_web_success_no_filename(self, mock_uuid, mock_file_open, mock_os_makedirs, mock_requests_get):
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"image_data_png"
        mock_response.raise_for_status = MagicMock()
        mock_requests_get.return_value = mock_response

        mock_uuid_value = MagicMock()
        mock_uuid_value.hex = "testuuid" # uuid4().hex[:8] is used in some versions, here it's str(uuid4())[:8]
        mock_uuid.return_value = mock_uuid_value # If code uses str(uuid.uuid4())

        # If the code uses str(uuid.uuid4())[:8], then mock str(uuid_obj)
        # The actual code is: file_name = str(uuid.uuid4())[:8]
        # So, we need uuid4() to return an object whose string representation starts with what we want.
        class MockUUID:
            def __str__(self):
                return "testuuid12345" # Needs to be at least 8 chars
        mock_uuid.return_value = MockUUID()


        url = "http://example.com/another_image.png"
        # file_name is None or empty, so it will be auto-generated
        expected_generated_name = "testuuid" # First 8 chars of str(MockUUID())
        expected_file_path = os.path.join(self.temp_folder, f"{expected_generated_name}.png")

        # Act
        result_path = self.image_service.SavePhotofromWeb(url, None, temp_folder=self.temp_folder)

        # Assert
        mock_os_makedirs.assert_called_once_with(self.temp_folder, exist_ok=True)
        mock_requests_get.assert_called_once_with(url)
        mock_file_open.assert_called_once_with(expected_file_path, "wb")
        mock_file_open().write.assert_called_once_with(b"image_data_png")
        self.assertEqual(result_path, expected_file_path)

    @patch('requests.get')
    @patch('os.makedirs')
    def test_save_photo_from_web_download_error(self, mock_os_makedirs, mock_requests_get):
        # Arrange
        mock_requests_get.side_effect = requests.exceptions.RequestException("Download failed")
        url = "http://example.com/image_fails.jpg"
        file_name = "failure_image"

        # Act
        with patch('builtins.print') as mock_print:
            result_path = self.image_service.SavePhotofromWeb(url, file_name, temp_folder=self.temp_folder)

        # Assert
        mock_os_makedirs.assert_called_once_with(self.temp_folder, exist_ok=True)
        mock_requests_get.assert_called_once_with(url)
        self.assertIsNone(result_path)
        mock_print.assert_any_call(f"Error downloading image: Download failed")


    @patch('requests.get')
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists') # Mock os.path.exists
    def test_save_photo_from_web_file_already_exists(self, mock_os_path_exists, mock_file_open, mock_os_makedirs, mock_requests_get):
        # Arrange
        # os.path.exists is called twice:
        # 1. For the temp_folder: We want this to be False so os.makedirs is called.
        # 2. For the file_path: We want this to be True to simulate file exists.
        mock_os_path_exists.side_effect = [
            False, # For os.path.exists(self.temp_folder)
            True   # For os.path.exists(expected_file_path)
        ]

        url = "http://example.com/existing.jpg"
        file_name = "existing_image"
        expected_file_path_to_check = os.path.join(self.temp_folder, f"{file_name}.jpg")

        # Act
        result_path = self.image_service.SavePhotofromWeb(url, file_name, temp_folder=self.temp_folder)

        # Assert
        mock_os_makedirs.assert_called_once_with(self.temp_folder, exist_ok=True)

        # Check calls to os.path.exists
        self.assertEqual(mock_os_path_exists.call_count, 2)
        mock_os_path_exists.assert_any_call(self.temp_folder) # First call
        mock_os_path_exists.assert_any_call(expected_file_path_to_check) # Second call

        # requests.get and open should NOT be called if file exists
        mock_requests_get.assert_not_called()
        mock_file_open.assert_not_called()

        # The function should return None or the path, depending on desired behavior for "already exists".
        # Current code returns None if it doesn't attempt download, or path if it does.
        # The code structure: if not os.path.exists(file_path): try download...
        # So if it *does* exist, it skips the block and returns None implicitly at the end of function.
        self.assertIsNone(result_path)


    def test_save_photo_folder_creation(self):
        # This test is more of an integration test for directory creation.
        # It relies on the actual os.makedirs behavior.
        # Arrange
        if os.path.exists(self.temp_folder): # Clean up if setUp didn't catch it or failed
            shutil.rmtree(self.temp_folder)
        self.assertFalse(os.path.exists(self.temp_folder))

        # Mock requests.get to prevent actual download, just focus on folder creation
        with patch('requests.get') as mock_requests_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.content = b"dummy"
            mock_requests_get.return_value = mock_response

            # Act
            # Call with a non-existent folder, SavePhotofromWeb should create it.
            self.image_service.SavePhotofromWeb("http://example.com/img.gif", "testimg", temp_folder=self.temp_folder)

        # Assert
        self.assertTrue(os.path.exists(self.temp_folder))
        # Also check if the file was "created" (mocked open would be better for unit, but here testing folder)
        self.assertTrue(os.path.exists(os.path.join(self.temp_folder, "testimg.gif")))


if __name__ == '__main__':
    unittest.main()
