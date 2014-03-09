from cv import *
from cv2 import *
import time
import numpy as np

X = 1
Y = 0
R = 2
G = 1
B = 0

def _dir(obj):
    print '*'*160
    for p in dir(obj):
        if not p.startswith('__'):
            try:
                value = unicode(getattr(obj, p))[:100]
                if value.startswith('<built-in method'):
                    value = getattr(obj, p).__doc__[:100]
                print '%s => %s' % (p, value)
            except:
                print p
    print '*'*160


class Curve:
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy
        self.next = None

    def set_ddiff(self, ddx, ddy):
        self.next = Curve(ddx,ddy)

    def delta(self, distance):
        ddx,ddy = self.next.delta(distance) if self.next else (0,0)
        return (self.dx + ddx)*distance, (self.dy + ddy)*distance

    def predict(self, point, distance):
        x,y = point
        dx,dy = self.delta(distance)
        return x+dx,y+dy


class CurveSegment:
    def __init__(self,x,y,dx,dy):
        self.start_point = (x,y)
        self.diff = Curve(dx,dy)
        self.next = []


class CurveDetector:
    def __init__(self):
        pass

    def detect(self, image, point):
        return []


class Figure:
    def __init__(self, start_point, start_segments):
        self.start_point = start_point
        self.start_segments = start_segments

class FigureDetector:
    def __init__(self, image):
        self.image = image
        self.height,self.width = image.shape
        self.detector = CurveDetector()

    def find_start_point(self):
        return self.width//2,self.height//2

    def get_segments_by_point(self, point):
        """
        Returns list of tuples (point,CurveSegment)
        """
        x,y = point
        return [((x+1,y+1), CurveSegment(x,y,1,1,))]

    def get_segments_by_segment(self, point, previous_segment):
        x,y = point
        return [((x+1,y+1), CurveSegment(x,y,1,1))]

    def detect(self):
        self.start = self.find_start_point()
        self.current = self.start
        self.items = self.get_segments_by_point(self.start)
        self.start_segments = [segment for (end_point,segment) in self.items]
        figure = Figure(self.start,self.start_segments)
        items = self.items
        while items:
            next = []
            for end_point, previous_segment in items:
                new_items = self.get_segments_by_segment(end_point, previous_segment)
                previous_segment.next = [segment for (_,segment) in new_items]
                next.append(new_items)
            items = next


class ImageTest:
    Image1 = r'data.png'
    Image2 = r'rose/frame2.png'

    def __init__(self):
        self.original1 = imread(ImageTest.Image1)
        self.original2 = imread(ImageTest.Image2)
        self.image1 = imread(ImageTest.Image1)
        self.image2 = imread(ImageTest.Image2)
        self.gray1 = cvtColor(self.image1,COLOR_BGR2GRAY)
        self.gray2 = cvtColor(self.image2,COLOR_BGR2GRAY)
        self.height, self.width, self.depth = self.image1.shape

    def run(self):
        image = self.gray1
        start = time.time()

        for x in range(self.width):
            for y in range(self.height):
                image[y][x] = 0 if image[y][x] > 128 else 255

        delta = (time.time() - start)
        print 'Processing took %s sec time' % delta
        self.result = image

    def show_results(self):
        imshow("Resulting image", self.result)
        waitKey(0)

test = ImageTest()
test.run()
test.show_results()