"""
This implementation reads/writes to a linux framebuffer
"""


from .interface import VideoOutputInterface
from pathlib import Path
from nptyping import NDArray, UInt8
from typing import Any


class Framebuffer(VideoOutputInterface):
    def __init__(self, fb: str):
        """
        Create a video_output implementation for a linux framebuffer
        :param fb: Name of the framebuffer, e.g. "fb0"
        """
        self.fb = fb

    def get_resolution(self) -> (int, int):
        """
        Retrive the resolution from the `virtual_size` node
        :return: width, height
        """
        with open(self.sysfs_path.joinpath("virtual_size")) as fpt:
            data = fpt.read().split(",")
        return int(data[0]), int(data[1])

    def send_image(self, image: NDArray[(Any, Any, 4), UInt8]) -> None:
        """
        Transmit the provided image on the video interface
        Image is an array of the format (width, height, [B, G, R, A])
        :param image:
        :return:
        """
        with open(self.dev_node_path, 'wb') as fpt:
            fpt.write(bytes(image))

    @property
    def dev_node_path(self) -> Path:
        """
        The location of the device node, e.g. "/dev/fb0"
        :return:
        """
        return Path(f"/dev/{self.fb}")

    @property
    def sysfs_path(self) -> Path:
        """
        Returns the sysfs path for this fb
        :return:
        """
        return Path(f"/sys/class/graphics/{self.fb}")
