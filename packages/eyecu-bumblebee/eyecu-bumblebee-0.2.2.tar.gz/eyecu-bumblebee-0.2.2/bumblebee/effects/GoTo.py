import cv2

from ..sources import FileStream
from ..interfaces import IEffect


class GoTo(IEffect):

    def __init__(self, src: FileStream):
        super().__init__(src)
        self.src = src



    def __call__(self,frame_number : int,*args,**kwargs):
        self.src.cap.set(cv2.CAP_PROP_POS_FRAMES,float(frame_number))