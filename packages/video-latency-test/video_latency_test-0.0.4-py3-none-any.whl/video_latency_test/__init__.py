from .video_output import VideoOutputInterface, Framebuffer
from .video_capture import VideoCaptureInterface, Cv2Camera
from . import frame_color
from func_timeout import func_timeout
import logging
from datetime import datetime, timedelta
import collections
import itertools
import argparse
from pathlib import Path
import csv


def validate_frame(color: frame_color.FrameColor, capture_device: VideoCaptureInterface, hue_threshold: int) -> bool:
    """
    Capture frames on capture device until it matches color
    :param color:
    :param capture_device:
    :param hue_threshold: An integer between 0 and 179
    :return: True if frame matches provided color
    """
    logging.debug("Attempting to validate frame")
    while True:
        frame = capture_device.get_next_frame()
        if color.matches(frame, hue_threshold):
            return True
        logging.debug("Frame did not match; trying again")


class sliceable_deque(collections.deque):
    def __getitem__(self, index):
        if isinstance(index, slice):
            return type(self)(itertools.islice(self, index.start,
                                               index.stop, index.step))
        return collections.deque.__getitem__(self, index)


def _log_previous(previous_entries, number_to_average):
    e = previous_entries[len(previous_entries)-number_to_average:]
    print(f"Last {len(e)}: Min: {min(e):.2f}ms Avg: {sum(e)/len(e):.2f}ms Max: {max(e):.2f}ms")


def run_video_latency_test(output_device: VideoOutputInterface,
                           capture_device: VideoCaptureInterface,
                           num_frames: int = 30,
                           capture_timeout_seconds: float = 5,
                           hue_threshold: int = 20,
                           csv_log_file: Path = None):
    frame_colors = [
        frame_color.BLUE,
        frame_color.RED
    ]
    output_device.start()
    capture_device.start()
    fb_width, fb_height = output_device.get_resolution()
    run_forever = num_frames == 0
    f = 0
    previous_timestamps = sliceable_deque(maxlen=100)
    if csv_log_file:
        with open(csv_log_file, 'w') as fpt:
            csv_writer = csv.writer(fpt)
            csv_writer.writerow([f'Log started at {str(datetime.now())}'])
            csv_writer.writerow(['Frame Number', 'Latency (ms)'])
    while run_forever or num_frames > f:
        current_frame_color = frame_colors[f % len(frame_colors)]
        output_device.send_image(current_frame_color.fb(fb_width, fb_height))
        start = datetime.now()
        func_timeout(capture_timeout_seconds, validate_frame, (current_frame_color, capture_device, hue_threshold))
        stop = datetime.now()
        previous_timestamps.append((stop - start) / timedelta(milliseconds=1))
        f += 1
        if csv_log_file:
            with open(csv_log_file, 'a') as fpt:
                csv_writer = csv.writer(fpt)
                csv_writer.writerow([f, f"{previous_timestamps[-1]:.2f}"])
        if not f % 10:
            print(f"Last Frame Latency: {previous_timestamps[-1]:.2f}")
            if f > 10:
                _log_previous(previous_timestamps, 10)
            if f > 50:
                _log_previous(previous_timestamps, 50)
            if f > 100:
                _log_previous(previous_timestamps, 100)


def cmdline():
    parser = argparse.ArgumentParser(description="Run a video latency test")

    parser.add_argument('output_fb',
                        type=str,
                        help='The name of the framebuffer to use, e.g. fb0')

    parser.add_argument('cv2_cap',
                        type=int,
                        help='Index of the cv2 capture device, e.g. 0')

    parser.add_argument("--frames",
                        type=int,
                        default=30,
                        help="Number of frames to capture for the test")

    parser.add_argument("--hue",
                        type=int,
                        default=15,
                        help="Hue threshold (uses hue values of 0-180)")

    parser.add_argument("--csv",
                        type=str,
                        default=None,
                        help="Location to save a CSV log of captured data")

    args = parser.parse_args()

    if args.csv:
        args.csv = Path(args.csv)

    run_video_latency_test(
        Framebuffer(args.output_fb),
        Cv2Camera(args.cv2_cap),
        num_frames=args.frames,
        hue_threshold=args.hue,
        csv_log_file=args.csv,
    )


