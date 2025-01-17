import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    lower_brown = np.array([95, 50, 50])  # Dolna granica koloru w przestrzeni HSV
    upper_brown = np.array([115, 255, 255])  # Górna granica koloru w przestrzeni HSV

    lower_color1 = np.array([6, 130, 25])  # Lower limit for RGB(105, 64, 47)
    upper_color1 = np.array([16, 255, 255])  # Upper limit for RGB(105, 64, 47)

    lower_color2 = np.array([16, 80, 45])  # Lower limit for RGB(159, 111, 63)
    upper_color2 = np.array([26, 255, 255])  # Upper limit for RGB(159, 111, 63)

    lower_color3 = np.array([2, 8, 61])  # Lower limit for RGB(175, 156, 151)
    upper_color3 = np.array([12, 108, 161])  # Upper limit for RGB(175, 156, 151)

    mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
    mask_color1 = cv2.inRange(hsv, lower_color1, upper_color1)
    mask_color2 = cv2.inRange(hsv, lower_color2, upper_color2)
    mask_color3 = cv2.inRange(hsv, lower_color3, upper_color3)

    result_brown = cv2.bitwise_and(frame, frame, mask=mask_brown)
    result_color1 = cv2.bitwise_and(frame, frame, mask=mask_color1)
    result_color2 = cv2.bitwise_and(frame, frame, mask=mask_color2)
    result_color3 = cv2.bitwise_and(frame, frame, mask=mask_color3)

    combined_result = cv2.bitwise_or(result_brown, cv2.bitwise_or(result_color1, cv2.bitwise_or(result_color2, result_color3)))

    cv2.imshow('Oryginal',frame)
    cv2.imshow('Combined Results', combined_result)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()