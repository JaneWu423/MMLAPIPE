from typing import Dict, List

import cv2

import chimerapy.engine as cpe
from chimerapy.orchestrator import sink_node

from .data import YOLOFrame


@sink_node(name="CPPipelines_HFDisplay")
class HFDisplay(cpe.Node):
    """A node that display results after applying Hugging Face models."""

    def __init__(
        self,
        frames_key: str = "frame",
        name: str = "DisplayNode",
    ) -> None:
        self.frames_key = frames_key
        super().__init__(name=name)

    def step(self, data_chunks: Dict[str, cpe.DataChunk]) -> cpe.DataChunk:
        print("reached here")
        for _, data_chunk in data_chunks.items():
            frame = data_chunk.get(self.frames_key)["value"]
            
            cv2.imshow(frame.src_id, frame.arr)
            cv2.waitKey(1)
        return 1

    def teardown(self) -> None:
        cv2.destroyAllWindows()