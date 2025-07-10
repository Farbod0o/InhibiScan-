import cv2
import numpy as np
path = "r3.jpg"
image = cv2.imread(path)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower_white = np.array([20, 100, 100])
upper_white = np.array([30, 255, 255])
mask = cv2.inRange(hsv, lower_white, upper_white)
pill_contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

centers = []
for contour in pill_contours:
    (x, y), radius = cv2.minEnclosingCircle(contour)
    print(radius)
    if radius > 40 and radius < 100 :
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(image, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        centers.append((int(x), int(y),int(radius)))

# cv2.imshow('image', image)
cv2.imwrite('pill.jpg', image)
image = cv2.imread(path)


print(centers)
gray_standard = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

gray=cv2.convertScaleAbs(np.min(image, axis=2))
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
gray = clahe.apply(gray_standard)

blurred = cv2.GaussianBlur(gray, (5, 5), 0)
_, threshold = cv2.threshold(blurred, 160, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('gray', gray)
cv2.imwrite('gray.jpg', gray)
cv2.imshow('threshold', threshold)
n = 0
for (x, y, r) in centers:
    rad = r
    last_ratio = 0
    n+=1
    print("-------------------------")
    print(n)
    while True:
        mask = np.zeros_like(gray)
        cv2.circle(mask, (x, y), r+5, 255, -1)
        white_pixels = np.sum(threshold[mask == 255] == 255)
        total_pixels = np.sum(mask == 255)
        ratio = white_pixels / total_pixels
        print(f"Ratio: {ratio}")
        if ratio<last_ratio:
            cv2.circle(image, (x,y), 2, (0, 0, 255), 3)
            cv2.putText(image, f"zone{n}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
            if last_ratio > 0.5:
                print("ok")
                cv2.circle(image, (x, y), r, (0, 255, 0), 2)
                cv2.circle(image, (x, y), rad, (0, 255, 0), 2)
                cv2.putText(image,f"radius:{r}pixel",(x,y+40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255))

            break
        last_ratio = ratio
        r += 1

cv2.imshow('image', image)
cv2.imwrite('imagef.jpg', image)
cv2.waitKey(0)
