import cv2
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
        except ValueError:
            return 'The Camera is failed to initial...'

