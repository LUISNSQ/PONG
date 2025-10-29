import sys
import cv2
import numpy as np

class ControloVisao:
    def __init__(self):   #
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Erro ao abrir a câmara.")
            sys.exit(1)  # fecha o programa

        self.threshold_value = 0.5 # é apenas um valor inicial
        cv2.namedWindow("Threshold")
        cv2.createTrackbar("Threshold", "Threshold", 50, 100, self.on_trackbar) # NAO CRIES A JANELA DENTRO DO LOOP

    def on_trackbar(self, value):
        self.threshold_value = value / 100.0

    def detetor(self):
        ret, frame = self.cap.read()
        if not ret:
            return None

        #frame_mirror = frame[:, ::-1, :]
        frame = cv2.flip(frame, 1) # espelha a imagem


        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        cima_red1 = np.array([0, 120, 70])
        baixo_red1 = np.array([10, 255, 255])
        cima_red2 = np.array([170, 120, 70])
        baixo_red2 = np.array([180, 255, 255])

        red1 = cv2.inRange(hsv, baixo_red1, cima_red1)
        red2 = cv2.inRange(hsv, baixo_red2, cima_red2)
        red = red1 + red2

        # Encontrar contornos
        contours, _ = cv2.findContours(red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cx = None
        if contours:
            c = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(c)
            if area > 800:
                (x, y, w, h) = cv2.boundingRect(c)
                cx = x + w // 2
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(frame, (cx, y + h // 2), 5, (255, 0, 0), -1)

        #Threshold
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = gray / 255.0

        _, image_thresholded = cv2.threshold(gray,
                                             self.threshold_value,
                                             1.0,
                                             cv2.THRESH_BINARY)
        cv2.imshow("Threshold", image_thresholded)

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
