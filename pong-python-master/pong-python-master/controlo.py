import cv2
import numpy as np

class VisionControl:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise Exception("Não foi possível abrir a câmara.")

    def get_position(self):
        ret, frame = self.cap.read()
        if not ret:
            return None

        # Espelhar imagem (mais natural)
        frame = cv2.flip(frame, 1)

        # Converter para HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Intervalos de cor vermelha (duas gamas)
        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])

        # Máscara combinada
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = mask1 + mask2

        # Filtragem
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # Encontrar contornos
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cx = None
        if contours:
            c = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(c)
            if area > 800:
                (x, y, w, h) = cv2.boundingRect(c)
                cx = x + w // 2
                # Mostrar resultado
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(frame, (cx, y + h // 2), 5, (255, 0, 0), -1)

        # Mostrar janelas
        cv2.imshow("Camera", frame)
        cv2.imshow("Mask", mask)
        cv2.waitKey(1)

        # Posição normalizada (0–1)
        if cx is not None:
            width = frame.shape[1]
            return cx / width
        return None

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
