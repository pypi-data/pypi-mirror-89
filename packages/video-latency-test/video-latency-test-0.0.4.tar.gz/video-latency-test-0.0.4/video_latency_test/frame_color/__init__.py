"""
Provides the FrameColor class and a few base-color examples.
"""
import numpy as np
from nptyping import NDArray
from typing import Any
import cv2
import logging


class FrameColor:
    def __init__(self, color: [int, int, int]):
        """
        A helper class for generating and testing frame colors
        :param color: A BRG array indicating the color
        """
        self.color_bgr = np.array(color, dtype='uint8')
        self.color_hue = cv2.cvtColor(
            np.array([[self.color_bgr]], dtype='uint8'),
            cv2.COLOR_BGR2HSV,
        )[0][0][0]

    def matches(self, frame: NDArray[Any, Any, 4], hue_threshold: int = 20) -> bool:
        """
        Return ``True`` if the provided frame matches this frame color
        :param frame:
        :param hue_threshold: an integer between 0 and 179
        :return:
        """
        downscaled_frame_size = (3, 3)
        # Determine our color boundary
        low_hue = self.color_hue - hue_threshold
        high_hue = self.color_hue + hue_threshold
        # Downscale the frame
        downscaled_frame = cv2.resize(frame, downscaled_frame_size)
        logging.debug(f"Downscaled Frame BGRA: {downscaled_frame}")
        # Convert to HSV
        downscaled_frame = cv2.cvtColor(
            cv2.cvtColor(downscaled_frame, cv2.COLOR_BGRA2BGR),
            cv2.COLOR_BGR2HSV
        )
        logging.debug(f"Downscaled Frame HSV: {downscaled_frame}")
        output_mask = np.zeros(downscaled_frame_size, dtype='uint8')
        logging.debug(f"Attempting to match hue between {low_hue} and {high_hue}")
        # Find matching pixels
        if low_hue < 0:
            output_mask |= cv2.inRange(
                downscaled_frame,
                np.array([low_hue % 180, 0 , 0], dtype='uint8'),
                np.array([180, 255, 255], dtype='uint8')
            )
            low_hue = 0
        if high_hue > 180:
            output_mask |= cv2.inRange(
                downscaled_frame,
                np.array([0, 0, 0], dtype='uint8'),
                np.array([high_hue % 180, 255, 255], dtype='uint8')
            )
            high_hue = 180
        output_mask |= cv2.inRange(
            downscaled_frame,
            np.array([low_hue, 0, 0], dtype='uint8'),
            np.array([high_hue, 255, 255], dtype='uint8')
        )
        expected = np.full(downscaled_frame_size, 255, dtype='uint8')
        return np.array_equal(output_mask, expected)

    def fb(self, width: int, height: int) -> NDArray[Any, Any, 4]:
        """
        Return a numpy frame of this class's color
        :param width:
        :param height:
        :return:
        """
        return np.full((width, height, 4),
                       [self.color_bgr[0], self.color_bgr[1], self.color_bgr[2], 255],
                       dtype="uint8")


BLUE = FrameColor([255, 0, 0])
GREEN = FrameColor([0, 255, 0])
RED = FrameColor([0, 0, 255])
PURPLE = FrameColor([0x99, 0, 0x99])
ORANGE = FrameColor([0, 69, 255])
