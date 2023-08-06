from unittest import TestCase
from unittest.mock import patch, MagicMock, call
from video_latency_test.video_capture import Cv2Camera
from cv2 import CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT


class TestCv2CameraCapture(TestCase):
    def setUp(self) -> None:
        self.framebuffer_number = 0
        self.video_capture = Cv2Camera(self.framebuffer_number)
        self.video_capture.cv2_capture = MagicMock()

    def test_get_next_frame(self) -> None:
        self.video_capture.cv2_capture.read.return_value = (True, "Test Frame")
        frame = self.video_capture.get_next_frame()
        self.video_capture.cv2_capture.read.assert_called_once()
        self.assertEqual("Test Frame", frame)

    def test_get_next_frame_raises_runtime_error_when_not_started(self) -> None:
        self.video_capture.cv2_capture = None
        with self.assertRaises(RuntimeError):
            self.video_capture.get_next_frame()

    def test_get_resolution_uses_the_opencv_get_prop_function(self) -> None:
        self.video_capture.cv2_capture.get.side_effect = [800, 600]
        self.assertEqual((800, 600), self.video_capture.get_resolution())
        self.video_capture.cv2_capture.get.assert_has_calls(
            [call(CAP_PROP_FRAME_WIDTH), call(CAP_PROP_FRAME_HEIGHT)], any_order=True
        )

    def test_get_resolution_raises_runtime_error_when_not_started(self) -> None:
        self.video_capture.cv2_capture = None
        with self.assertRaises(RuntimeError):
            self.video_capture.get_resolution()

    @patch("video_latency_test.video_capture.cv2_camera.VideoCapture")
    def test_start_method_opens_video_capture(self, mock_video_capture) -> None:
        self.video_capture.start()
        mock_video_capture.assert_called_once_with(self.framebuffer_number)
