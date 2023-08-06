from pyfakefs.fake_filesystem_unittest import TestCase
from unittest.mock import MagicMock
from video_latency_test.video_output import Framebuffer
from pathlib import Path
import numpy


class TestFramebuffer(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs()
        self.fb = "fb0"
        self.video_output = Framebuffer(self.fb)
        self.mock_image = MagicMock()

    def test_get_resolution_returns_width_and_height_from_sysfs(self) -> None:
        virtual_size_node = Path(f"/sys/class/graphics/{self.fb}/virtual_size")
        self.fs.create_file(virtual_size_node, contents='800,600')
        width, height = self.video_output.get_resolution()
        self.assertEqual(800, width)
        self.assertEqual(600, height)

    def test_send_image_writes_image_to_framebuffer_device(self):
        framebuffer_dev_node = f"/dev/{self.fb}"
        self.fs.create_file(framebuffer_dev_node)
        test_image = numpy.random.randint(0, numpy.iinfo('uint8').max, size=(800, 600, 3), dtype='uint8')
        self.video_output.send_image(test_image)
        with open(framebuffer_dev_node, 'rb') as fpt:
            data = fpt.read()
        retrieved_image = numpy.reshape(numpy.frombuffer(data, dtype='uint8'), (800, 600, 3))
        self.assertTrue((retrieved_image == test_image).all())
