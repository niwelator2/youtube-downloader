from io import StringIO
import sys
import unittest
import os

from click import progressbar
from main import (
    download_single_video,
    display_message,
    on_progress,
    clean_video_title,
    show_error_message,
    start_download_playlist_threaded_inner,
)


class TestAutomation(unittest.TestCase):
    def test_download_single_video_automation_mp4(self):
        """
        Test the download of a single video in the automation MP4 format.

        This function tests the functionality of the `download_single_video` function in the case of downloading a single video in the automation MP4 format. It sets up the necessary variables, such as the video link, download type, save directory, current video, and downloaded titles. Then, it calls the `download_single_video` function with these variables.

        After the download is complete, the function asserts that the downloaded video file exists in the specified save directory with the correct video title.

        Parameters:
            self (object): The instance of the test class.

        Returns:
            None
        """
        video_link = "https://music.youtube.com/watch?v=RhmHSAClG1c"
        download_type = "MP4"
        save_directory = "test/unitytest"
        current_video = 1
        downloaded_titles = set()

        download_single_video(
            video_link, download_type, save_directory, current_video, downloaded_titles
        )

        self.assertTrue(
            os.path.exists(
                os.path.join(save_directory, clean_video_title("Video_Title.mp4"))
            )
        )

    def test_download_single_video_automation_mp3(self):
        """
        Test the download of a single video in the automation MP3 format.

        This function tests the functionality of the `download_single_video` function in the case of downloading a single video in the automation MP4 format. It sets up the necessary variables, such as the video link, download type, save directory, current video, and downloaded titles. Then, it calls the `download_single_video` function with these variables.

        After the download is complete, the function asserts that the downloaded video file exists in the specified save directory with the correct video title.

        Parameters:
            self (object): The instance of the test class.

        Returns:
            None
        """
        video_link = "https://music.youtube.com/watch?v=RhmHSAClG1c"
        download_type = "MP3"
        save_directory = "test/unitytest"
        current_video = 1
        downloaded_titles = set()

        download_single_video(
            video_link, download_type, save_directory, current_video, downloaded_titles
        )

        self.assertTrue(
            os.path.exists(
                os.path.join(save_directory, clean_video_title("Video_Title.mp3"))
            )
        )

    def test_download_playlist_video_automation_mp3(self):

        video_link = "https://music.youtube.com/playlist?list=RDCLAK5uy_nZiG9ehz_MQoWQxY5yElsLHCcG0tv9PRg"
        download_type = "MP3"
        save_directory = "test/unitytest"
        current_video = 1
        downloaded_titles = set()

        start_download_playlist_threaded_inner(
            video_link, download_type, save_directory, current_video, downloaded_titles
        )

        self.assertTrue(
            os.path.exists(
                os.path.join(save_directory, clean_video_title("Video_Title.mp3"))
            )
        )

    def test_display_message_automation(self):

        message = "Test message"
        video_title = "Test Video"

        # Redirect sys.stdout to capture print output
        captured_output = StringIO()
        sys.stdout = captured_output

        display_message(message, video_title)

        # Restore sys.stdout
        sys.stdout = sys.__stdout__

        self.assertIn("Test Video: Test message", captured_output.getvalue())

    def test_on_progress_automation(self):
        # Test on_progress function with automation
        # Mock stream object
        class MockStream:
            filesize = 1000

        # Mock chunk and bytes_remaining
        chunk = b"chunk"
        bytes_remaining = 500

        # Call the function to be tested
        on_progress(MockStream(), chunk, bytes_remaining, 1)

        # Assertions based on expected behavior
        # Check if the progress bar is updated correctly
        self.assertEqual(progressbar.get(), 50.0)

    def test_clean_video_title_automation(self):
        # Test cleaning video title with automation
        title = "Test Video #1"
        cleaned_title = clean_video_title(title)

        # Assertions based on expected behavior
        # Check if special characters are replaced with underscores
        self.assertEqual(cleaned_title, "Test_Video_1")

    def test_show_error_message_automation(self):
        # Test showing an error message with automation
        error_message = "Test error message"

        # Redirect sys.stdout to capture print output
        captured_output = StringIO()
        sys.stdout = captured_output

        # Call the function to be tested
        show_error_message(error_message)

        # Restore sys.stdout
        sys.stdout = sys.__stdout__

        # Assertions based on expected behavior
        # Check if the error message was displayed correctly
        self.assertIn("Test error message", captured_output.getvalue())


if __name__ == "__main__":
    unittest.main()
