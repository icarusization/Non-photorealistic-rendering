from math import sqrt
import Image, ImageDraw

# Function: Bezier2  ------  Used for creating a Bezier curve with given points set and width, color.
#
# Function Parameter:
#     draw: The call of drawing on the image;
#     points: The points set like points = ((150, 100), (100, 200), (685, 300));
#     line_width, line_color: Relative parameter about the line;
#     loop: The times it uses Two Time Interpolation to insert points (>=4 is often enough)
#     pk{}: This is the set of all points if it is useful for you;
# Return: get_points()---the list of each points, [[x,y],...]
#
# Function Implementation:
#     m = Image.new('RGB', (1024, 1024), (255, 255, 255))
#     draw = ImageDraw.Draw(im)
#     points = ((150, 100), (100, 200), (685, 300),(300,120),(400,280))
#     b = Bezier2(draw, points, 1, (0, 0, 255), 4)
#     b.render()
#     del draw
#     im.show()


class Bezier2(object):
    def __init__(self, points, line_color, loop):
        self.points = points
        self.len = len(points)
        self.line_color = line_color
        self.loop = loop
        self.current_point = (0, 0)
        self.pk = {}
        if loop>12:
            print "Too much loops when plotting a stroke!"
            exit()

    def moveto(self, p):
        self.current_point = p

    def lineto(self, p):
        self.current_point = p

    def get_points(self):
        axis_line = []
        for i in range(len(self.pk)):
            if not [self.pk[i][0], self.pk[i][1]] in axis_line:
                axis_line.append([self.pk[i][0], self.pk[i][1]])
        return axis_line;

    def render(self):
        NO = self.len                   # The num of points in set self.points
        KT = self.loop                  # This is the loop times for Two Time Interpolation
        m = NO - 1
        p = {}
        for i in range(0, NO, 2):
            p[i] = self.points[i]
        if not(NO % 2): p[m] = self.points[m]

        for i in range(1, NO-1, 2):
            l1 = 1.0 * (self.points[i-1][0] - self.points[i][0])
            ll = 1.0 * (self.points[i-1][1] - self.points[i][1])
            l1 = sqrt(l1 * l1 + ll * ll)

            l2 = 1.0 * (self.points[i+1][0] - self.points[i][0])
            ll = 1.0 * (self.points[i+1][1] - self.points[i][1])
            l2 = sqrt(l2 * l2 + ll * ll)

            p[i] = (
                ((l1 + l2) * (l1 + l2) * self.points[i][0] - l2 * l2 * self.points[i-1][0] - l1 * l1 * self.points[i+1]
                [0]) / (2 * l1 * l2),
                ((l1 + l2) * (l1 + l2) * self.points[i][1] - l2 * l2 * self.points[i-1][1] - l1 * l1 * self.points[i+1]
                [1]) / (2 * l1 * l2)
            )

        self.pk = {}  # pk[129][2]
        for i in range(m + 1):
            self.pk[i] = p[i]

        pt = {}
        for k in range(KT + 1):
            for i in range(0, m + 1, 2):
                pt[2 * i] = self.pk[i]
            if not (NO % 2): pt[2*m] = self.pk[m]
            for i in range(m):
                pt[2 * i + 1] = (
                    int(self.pk[i][0] + self.pk[i + 1][0]) >> 1,
                    int(self.pk[i][1] + self.pk[i + 1][1]) >> 1
                )
            for i in range(1, m):
                pt[2 * i] = (
                    int(pt[2 * i - 1][0] + pt[2 * i + 1][0]) >> 1,
                    int(pt[2 * i - 1][1] + pt[2 * i + 1][1]) >> 1
                )
            for i in range(2 * m + 1):
                self.pk[i] = pt[i]

            if k == KT:
                break
            m <<= 1
        self.moveto(self.pk[0])
        for i in range(1, 2 * m + 1):
            self.lineto(self.pk[i])


if __name__ == '__main__':
    im = Image.new('RGB', (400, 400), (255, 255, 255))
    points = [(200, 100), (233,130), (265,131), (266, 130), (300,100)]
    b = Bezier2(points, (0, 0, 255), 7)
    b.render()
    r_points=b.get_points()
    for i in range(len(r_points)):
        im.putpixel(r_points[i],(0, 0, 0))

    for i in range(19):
        k = 20 * (i + 1)
        for j in range(400):
            im.putpixel((k, j), (0, 0, 0))
            im.putpixel((j, k), (0, 0, 0))
    im.show()