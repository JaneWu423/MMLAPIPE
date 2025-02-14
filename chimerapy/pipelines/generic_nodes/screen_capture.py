import typing

import cv2
import imutils
import numpy as np

import chimerapy.engine as cpe
from chimerapy.orchestrator import source_node

if typing.TYPE_CHECKING:
    from mss.base import MSSBase


@source_node(name="CPPipelines_ScreenCapture")
class ScreenCapture(cpe.Node):
    """A generic video screen capture node using mss

    Parameters
    ----------
    name : str, optional (default: 'ScreenCaptureNode')
        The name of the node
    scale: float, optional (default: 0.5)
        The scale of the screen capture
    fps: int, optional (default: 30)
        The frame rate of the screen capture (unused, not guaranteed)
    frame_key: str, optional (default: 'frame')
        The key to use for the frame in the data chunk
    monitor: int, optional (default: 0)
        The monitor to capture
    save_name: str, optional (default: 0)
         If a string is provided, save the video (prefixed with this name)
    """

    def __init__(
        self,
        scale: float = 0.5,
        fps: int = 30,
        frame_key: str = "frame",
        monitor: int = 0,
        name="ScreenCaptureNode",
        save_name: typing.Optional[str] = None,
    ):
        self.scale = scale
        self.fps = fps
        self.frame_key = frame_key
        self.capture = None
        self.monitor = monitor
        self.save_name = save_name
        super().__init__(name=name)

    def setup(self):
        self.capture = None

    def _get_capture(self) -> "MSSBase":
        import mss

        if self.capture is None:
            self.capture = mss.mss()
        return self.capture

    def step(self) -> cpe.DataChunk:
        img = self._get_capture().grab(self.capture.monitors[self.monitor])
        arr = np.array(img)
        arr = cv2.cvtColor(arr, cv2.COLOR_BGRA2BGR)
        arr = imutils.resize(arr, width=int(arr.shape[1] * self.scale))

        if self.save_name:
            self.save_video(self.save_name, arr, self.fps)

        data_chunk = cpe.DataChunk()
        data_chunk.add(self.frame_key, arr, "image")

        return data_chunk
