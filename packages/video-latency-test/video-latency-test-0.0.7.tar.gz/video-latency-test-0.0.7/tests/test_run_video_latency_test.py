from unittest import TestCase
from unittest.mock import MagicMock, call, ANY, patch
from video_latency_test import run_video_latency_test
from func_timeout import func_set_timeout, FunctionTimedOut, func_timeout


@patch("video_latency_test.frame_color")
class TestRunVideoLatencyTest(TestCase):

    # This field doesn't need to be realistic, but long enough the allow the
    # library to trigger its timeout
    FRAME_CAPTURE_TIMEOUT_SECONDS = 0.5

    def setUp(self) -> None:
        self.test_video_output = MagicMock()
        self.test_video_capture = MagicMock()
        self.test_video_output.get_resolution.return_value = (800, 600)

    def test_run_app_starts_video_output_before_it_is_used(self, patched_frame_colors):
        run_video_latency_test(self.test_video_output, self.test_video_capture, num_frames=1)
        self.test_video_output.assert_has_calls([
            call.start(),
            call.get_resolution(),
            call.send_image(ANY)
        ])

    def test_run_app_transmits_blue_red_frames(self, patched_frame_color):
        expected_fbs = [
            patched_frame_color.BLUE.fb(800, 600),
            patched_frame_color.RED.fb(800, 600)
        ]
        iterations = 3
        run_video_latency_test(self.test_video_output, self.test_video_capture, num_frames=len(expected_fbs) * iterations)
        calls = [call.send_image(expected_fbs[c % len(expected_fbs)]) for c in range(len(expected_fbs)*iterations)]
        calls.insert(0, call.start())
        calls.insert(1, call.get_resolution())
        self.test_video_output.assert_has_calls(calls)

    @func_set_timeout(FRAME_CAPTURE_TIMEOUT_SECONDS*2)
    def test_frame_detection_times_out_after_provided_time(self, patched_frame_color):
        patched_frame_color.BLUE.matches.return_value = False
        with self.assertRaises(FunctionTimedOut):
            run_video_latency_test(
                self.test_video_output,
                self.test_video_capture,
                capture_timeout_seconds=self.FRAME_CAPTURE_TIMEOUT_SECONDS
            )

    def test_runs_forever_when_num_frames_is_zero(self, patched_frame_color):
        with self.assertRaises(FunctionTimedOut):
            # Running for a half second should be long enough to demonstrate running forever
            func_timeout(.5,
                         run_video_latency_test,
                         args=(self.test_video_output, self.test_video_capture, 0)
                         )

    def test_does_not_run_forever_when_num_frames_is_finite(self, patched_frame_color):
        # We should be able to run 30 mocked frames in this time
        func_timeout(.5,
                     run_video_latency_test,
                     args=(self.test_video_output, self.test_video_capture, 30)
                     )

    def test_hue_threshold_is_passed_to_color_matches_call(self, patched_frame_color):
        run_video_latency_test(self.test_video_output, self.test_video_capture, num_frames=1, hue_threshold="hue_threshold")
        patched_frame_color.BLUE.matches.assert_called_once_with(ANY, "hue_threshold")
