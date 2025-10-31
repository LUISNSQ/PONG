import sys
import cv2
import numpy as np

class ControloVisao:
    def __init__(self,):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Erro ao abrir a câmara.")
            sys.exit(1)  # fecha o programa


        self.threshold_value = 0.5 # é apenas um valor inicial
        cv2.namedWindow("Camera")
        cv2.namedWindow("Threshold")

        #ajustado à luminosidade da sala
        base_lowH = 170
        base_highH = 180
        base_lowS = 90
        base_highS = 220
        base_lowV = 0 # aumentar se a luz for fraca
        base_highV = 255

        def none(x):
            pass

        cv2.createTrackbar("Threshold", "Threshold", 50, 100, none)
        cv2.createTrackbar("Low H", "Camera", base_lowH, 180, none)
        cv2.createTrackbar("High H", "Camera", base_highH, 180, none)
        cv2.createTrackbar("Low S", "Camera", base_lowS, 255, none)
        cv2.createTrackbar("High S", "Camera", base_highS, 255, none)
        cv2.createTrackbar("Low V", "Camera", base_lowV, 255, none)
        cv2.createTrackbar("High V", "Camera", base_highV, 255, none)

    def on_trackbar(self, value):
        self.threshold_value = value / 100.0

    def detetor(self):
        ret, frame = self.cap.read()
        if not ret:
            return None

        #frame_mirror = frame[:, ::-1, :]
        frame = cv2.flip(frame, 1) # espelha a imagem

        lh = cv2.getTrackbarPos("Low H", "Camera")
        hh = cv2.getTrackbarPos("High H", "Camera")
        ls = cv2.getTrackbarPos("Low S", "Camera")
        hs = cv2.getTrackbarPos("High S", "Camera")
        lv = cv2.getTrackbarPos("Low V", "Camera")
        hv = cv2.getTrackbarPos("High V", "Camera")


        #countours
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_red = np.array([lh, ls, lv])
        upper_red = np.array([hh, hs, hv])
        red = cv2.inRange(hsv, lower_red, upper_red)

        contours, _ = cv2.findContours(red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cx = None

        if contours:
            c = max(contours, key=cv2.contourArea)  # verifica qual é o maior contour
            area = cv2.contourArea(c)

            if area > 800:
               # cv2.drawContours(frame, contours =[c], contourIdx = -1, color =(0, 255, 0),thickness= 1)
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                m = cv2.moments(c)
                if m["m00"] != 0:
                    cX = int(m["m10"] / m["m00"])
                    cY = int(m["m01"] / m["m00"])
                    cx = cX

                    cv2.circle(img = frame, center = (cX, cY),radius = 5, color =(255, 0, 0), thickness =-1)
        #Threshold
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = gray / 255.0

        _, image_threshold = cv2.threshold(gray,
                                             self.threshold_value,
                                             1.0,
                                             cv2.THRESH_BINARY)
        cv2.imshow("Threshold", image_threshold)


        cv2.imshow("Camera", frame)
        cv2.waitKey(1)

        # Posição da Barra
        if cx is not None:
            width = frame.shape[1]
            return cx / width
        return None

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
