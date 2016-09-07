#coding=utf8
import cv2, time

print('Press Esc to exit')
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
imgWindow = cv2.namedWindow('FaceDetect', cv2.WINDOW_NORMAL)

def detect_face():

    faces = []
    img = cv2.imread('img.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.3, 5)

    if faces:
        for x, y, w, h in faces:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.imshow('FaceDetect', img)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    detect_face()