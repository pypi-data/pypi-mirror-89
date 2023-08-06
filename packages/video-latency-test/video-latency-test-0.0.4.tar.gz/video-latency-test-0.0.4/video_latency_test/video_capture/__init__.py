"""
This module provides an interface for pushing frames to a video output device.

The interface is defined in VideoOutputInterface; other classes are implementations of that interface.
"""

from .interface import VideoCaptureInterface
from .cv2_camera import Cv2Camera
