"""
This test is more implementation than unit level, but is helpful to demonstrate
intended functionality.
"""

from unittest import TestCase
from video_latency_test import frame_color


class TestFrameColors(TestCase):
    AVAILABLE_COLORS = [
        frame_color.BLUE,
        frame_color.GREEN,
        frame_color.RED,
        frame_color.PURPLE,
    ]

    def test_generated_frames_match_only_correct_color(self):
        for test_color in self.AVAILABLE_COLORS:
            frame = test_color.fb(640, 480)
            for comparison_color in self.AVAILABLE_COLORS:
                self.assertEqual(
                    test_color is comparison_color,
                    comparison_color.matches(frame)
                )

    def test_generated_frames_always_match_when_hue_threshold_is_high(self):
        for test_color in self.AVAILABLE_COLORS:
            frame = test_color.fb(640, 480)
            for comparison_color in self.AVAILABLE_COLORS:
                self.assertTrue(comparison_color.matches(frame, 179))
