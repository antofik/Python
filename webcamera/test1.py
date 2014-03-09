import cv

capture = cv.CaptureFromCAM(-1)
cv.NamedWindow("capture", cv.CV_WINDOW_AUTOSIZE)

i = 0
while True:
    frame = cv.QueryFrame(capture)
    cv.ShowImage("capture", frame)
    cv.WaitKey(10)
    #path = "capture%.4d.jpg" % i # Уникальное имя для каждого кадра
    #cv.SaveImage(path, frame)
    #i += 1