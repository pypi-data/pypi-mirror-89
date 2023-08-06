from nptyping import NDArray, UInt8
from typing import Any
import logging


class VideoCaptureInterface:
    def get_next_frame(self) -> NDArray[(Any, Any, 4), UInt8]:
        """
        Blocks while retrieving the next frame
        Image is an array of the format (width, height, [B, G, R, A])
        :return: an image
        """
        raise NotImplementedError()

    def get_resolution(self) -> (int, int):
        """
        Return the resolution of the interface
        :return: width, height
        """
        raise NotImplementedError()

    def start(self) -> None:
        """
        Prepare the interface for use
        :return:
        """
        logging.debug("The start method is undefined for this class")
