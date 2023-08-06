from unittest import TestCase
from unittest.mock import patch
from video_latency_test.video_output import VideoOutputInterface


class TestVideoOutputInterface(TestCase):
    def setUp(self) -> None:
        self.video_output = VideoOutputInterface()

    def test_send_image_method_raises_not_implemented_error(self) -> None:
        with self.assertRaises(NotImplementedError):
            self.video_output.send_image(None)

    def test_get_resolution_method_raises_not_implemented_error(self) -> None:
        with self.assertRaises(NotImplementedError):
            self.video_output.get_resolution()

    @patch("logging.debug")
    def test_start_method_logs_to_debug_log(self, mock_debug_log) -> None:
        self.video_output.start()
        mock_debug_log.assert_called_once()
