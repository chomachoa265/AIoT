import cv2
import numpy as np


def file2img(file):
    #read image file string data
    filestr = file.read()
    #convert string data to numpy array
    file_bytes = np.fromstring(filestr, np.uint8)
    # convert numpy array to image
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    return img


# 待優化

def cropImage(img):
    imgCopy = img.copy()
    for i in range(2):
        for j in range(2):
            gray = cv2.cvtColor(imgCopy, cv2.COLOR_BGR2GRAY)
            gray = cv2.medianBlur(gray, 3)
            ret, thresh = cv2.threshold(gray, 1, 255, 0)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            maxArea = -1
            bestCnt = None

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > maxArea:
                    maxArea = area
                    bestCnt = cnt

            approx = cv2.approxPolyDP(bestCnt, 0.01*cv2.arcLength(bestCnt, True), True)
            far = approx[np.product(approx, 2).argmax()][0]
            x = far[0]
            y = far[1]
            imgCopy = imgCopy[:y, :x]
            imgCopy = cv2.flip(imgCopy, 0)
        imgCopy = cv2.flip(imgCopy, 1)
    return imgCopy