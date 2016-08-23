# This file is used to test the strokes class.

import Image
import Strokes
import time


def initial_stroke(m_s):                       # Create a stroke with parameters set below.
    length = 100
    width = 20
    color = (100, 100, 200)
    m_s.length = length
    m_s.width = width
    m_s.lists = []
    return m_s

im = Image.new("RGB", (400, 400), (255, 255, 255))
for i in range(19):
    k = 20*(i+1)
    for j in range(400):
        im.putpixel((k, j),(0, 0, 0))
        im.putpixel((j, k), (0, 0, 0))

s = Strokes.Stroke()
s = initial_stroke(s)

# Here you can revise these parameters according to the introduction in the Strokes Class.
s.distort = 0.2
s.shake = 0.3
s.tapering = 0.5
s.ColorVariability = 0.3
s.ShadeVariability = 0.3
c = Strokes.Color(21, 190, 4)
s.color = c

points = s.draw_strokes(im, 0, 50, 40, 50, 10, s.color)
for i in range(len(points)):
    p = points[i]
    c = p[2]
    im.putpixel((200-s.length/2+p[0],200+p[1]),c.get_color())
im.show()