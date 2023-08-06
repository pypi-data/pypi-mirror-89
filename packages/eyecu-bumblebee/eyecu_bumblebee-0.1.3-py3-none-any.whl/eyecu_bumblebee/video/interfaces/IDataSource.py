import cv2


class IDataSource():

    __ID__ = 1

    def read(self):
        ret, frame = self.cap.read()

        if not ret:
            raise Exception("Stream {} :> Cannot get data from source.")

        return frame


    def get_props(self):

        return (
            int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            3
        )