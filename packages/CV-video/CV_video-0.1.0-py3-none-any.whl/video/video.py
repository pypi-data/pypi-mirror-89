
import threading
import sys
sys.path.append('/home/epc/Documents/ubt/documents/CenterNet-three_train/src/lib')
from home.epc.Documents.ubt.documents.Project.CenterNet-three_train.src.lib.detectors.detector_factory import detector_factory
from home.epc.Documents.ubt.documents.Project.CenterNet-three_train.src.lib.opts import opts
import cv2
import time

MODEL_PATH = '/home/epc/Documents/ubt/documents/Project/CenterNet-three_train/exp/ctdet/FullData/915/model_last.pth'
#MODEL_PATH = '/home/epc/Documents/ubt/documents/Project/CenterNet-three_train/models/1218model_last.pth'
TASK = 'ctdet' # or 'multi_pose' for human pose estimation
opt = opts().init('{} --load_model {}'.format(TASK, MODEL_PATH).split(' '))#paramter
opt.debug = 1
detector = detector_factory[opt.task](opt)
def Camera(path):
    while True:
        try:
            vc = cv2.VideoCapture(path)
            ret, frame = vc.read()
            if ret != True:
                vc = cv2.VideoCapture(path)
                ret, frame = vc.read()
                #continue
            # continue
            cv2.imshow('Camera{}', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            vc.release()
            cv2.destroyAllWindows()
        except:
            return 'The Camera is failed to initial...'

