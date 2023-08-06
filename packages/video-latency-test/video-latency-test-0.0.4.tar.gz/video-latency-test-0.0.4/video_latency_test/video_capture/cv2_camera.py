"""
Opens a cv2 camera.  See documentation here:

https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
"""
from typing import Any
from nptyping import NDArray, UInt8
from .interface import VideoCaptureInterface
from cv2 import VideoCapture, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FRAME_WIDTH


class Cv2Camera(VideoCaptureInterface):

    def __init__(self, image_source: int):
        """
        Create a Cv2 Camera Source
        :param image_source:
        """
        self.image_source = image_source
        self.cv2_capture = None

    def get_next_frame(self) -> NDArray[(Any, Any, 4), UInt8]:
        if not self.cv2_capture:
            raise RuntimeError("Cannot interact with device unless it has been started")
        _ret, frame = self.cv2_capture.read()
        return frame

    def get_resolution(self) -> (int, int):
        if not self.cv2_capture:
            raise RuntimeError("Cannot interact with device unless it has been started")
        width = self.cv2_capture.get(CAP_PROP_FRAME_WIDTH)
        height = self.cv2_capture.get(CAP_PROP_FRAME_HEIGHT)
        return width, height

    def start(self) -> None:
        self.cv2_capture = VideoCapture(self.image_source)
