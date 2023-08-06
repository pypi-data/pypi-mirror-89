# video-latency-test #

This project provides software for a simple video latency test,
utilizing the Linux framebuffer for video output and OpenCV for camera capture.

[![CircleCI](https://circleci.com/bb/pseudodesign/video-latency-test.svg?style=shield&circle-token=f44332ba64c8bb34b5379ad07c5de2af70104a2d)](https://circleci.com/bb/pseudodesign/video-latency-test)
[![codecov](https://codecov.io/bb/pseudodesign/video-latency-test/branch/master/graph/badge.svg?token=T4EX0YF66K)](https://codecov.io/bb/pseudodesign/video-latency-test)

## Usage

Run `video-latency-test` from the commandline.

```
root@raspberrypi4-64:~# video-latency-test -h
usage: video-latency-test [-h] [--frames FRAMES] [--hue HUE] [--csv CSV]
                          output_fb cv2_cap

Run a video latency test

positional arguments:
  output_fb        The name of the framebuffer to use, e.g. fb0
  cv2_cap          Index of the cv2 capture device, e.g. 0

optional arguments:
  -h, --help       show this help message and exit
  --frames FRAMES  Number of frames to capture for the test
  --hue HUE        Hue threshold (uses hue values of 0-180)
  --csv CSV        Location to save a CSV log of captured data

```
## Implementation

The `video-latency-test` executable accepts a VideoOutputInterface object, and a VideoCapture object,
then measures the latency between setting a color on the VideoOutputInterface and detecting
that color on the VideoCaptureInterface.  The base implementation, using a Linux Framebuffer
for the output and a USB camera for the input, is shown in the diagram below.

![video-latency-test-workflow](docs/images/video-latency-test-workflow.png "Video Latency Test Workflow")

### Video Output

#### Interface

#### Framebuffer Implementation

### Video Capture

#### Interface

#### Framebuffer Implementation

### Frame Types

Frame types provide a method of generating frames written to the Video Output device, 
along with a method of validating those frames from the Video Capture device.

#### Interface

#### Solid Colors