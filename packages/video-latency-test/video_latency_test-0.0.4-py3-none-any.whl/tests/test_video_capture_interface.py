from unittest import TestCase
from unittest.mock import patch
from video_latency_test.video_capture import VideoCaptureInterface


class TestVideoOutputInterface(TestCase):
    def setUp(self) -> None:
        self.video_capture = VideoCaptureInterface()

    def test_get_next_frame_raises_not_implemented_error(self) -> None:
        with self.assertRaises(NotImplementedError):
            self.video_capture.get_next_frame()

    def test_get_resolution_method_raises_not_implemented_error(self) -> None:
        with self.assertRaises(NotImplementedError):
            self.video_capture.get_resolution()

    @patch("logging.debug")
    def test_start_method_logs_to_debug_log(self, mock_debug_log) -> None:
        self.video_capture.start()
        mock_debug_log.assert_called_once()
