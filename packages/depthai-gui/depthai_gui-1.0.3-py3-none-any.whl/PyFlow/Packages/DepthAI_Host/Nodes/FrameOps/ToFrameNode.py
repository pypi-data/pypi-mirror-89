import numpy as np

from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from common import HostNode


class ToFrameNode(HostNode):
    def __init__(self, name):
        super(ToFrameNode, self).__init__(name)
        self.data = self.createInputPin('data', 'AnyPin')
        self.data.enableOptions(PinOptions.AllowAny)
        self.out = self.createOutputPin('out', 'AnyPin')
        self.out.enableOptions(PinOptions.AllowAny)
        self.out.enableOptions(PinOptions.AllowMultipleConnections)

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addOutputDataType('AnyPin')
        helper.addOutputStruct(StructureType.Multi)
        return helper

    @staticmethod
    def category():
        return 'FrameOps'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Description in rst format."

    def run(self, device):
        while self._running:
            data = self.queue.get()
            frame = data['data'].getData().reshape((3, 300, 300)).transpose(1, 2, 0).astype(np.uint8)
            frame = np.ascontiguousarray(frame)
            self.send("out", frame)
