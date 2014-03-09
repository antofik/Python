import cv
import cv2


WIDTH = 640
HEIGHT = 480
DEPTH = 8
CHANNELS = 3

cam1 = cv2.VideoCapture(1)
cam2 = cv2.VideoCapture(0)
cv2.namedWindow("capture", cv.CV_WINDOW_AUTOSIZE)

def combine_images(image, image1, image2):
    cv.SetImageROI(image, (0, 0, WIDTH, HEIGHT))
    cv.Copy(image1, image)
    cv.SetImageROI(image, (WIDTH,0,WIDTH*2,HEIGHT))
    cv.Copy(image2, image)
    cv.ResetImageROI(image)

frame = cv.CreateImage((WIDTH*2, HEIGHT), DEPTH, CHANNELS)
while True:
    ok, frame1 = cam1.read()
    if not ok:
        print 'Error connecting to cam 1'
        break
    ok, frame2 = cam2.read()
    if not ok:
        print 'Error connecting to cam 2'
        break

    img1 = cv.fromarray(frame1)
    img2 = cv.fromarray(frame2)
    combine_images(frame, img1, img2)
    cv.ShowImage("capture", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
    if key == 13:
        cv2.imwrite('frame1.png', frame1)
        cv2.imwrite('frame2.png', frame2)
        print 'Screenshot are ready'

    