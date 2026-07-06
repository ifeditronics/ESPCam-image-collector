import cv2
import numpy as np

img = np.zeros((480, 640, 3), dtype=np.uint8)

while True:
    cv2.imshow("Test Window", img)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()