import Image, ImageDraw
Iterative = 24
Iterative2 = Iterative * Iterative
Iterative3 = Iterative2 * Iterative


def Draw_HermiteCurve(x1, y1, x2, y2, xr1, yr1, xr2, yr2,draw):
    oldx = x1
    oldy = y1
    m1 = Iterative3
    m2 = m3 = m4 = 0

    for i in range(Iterative):
        k1 = (i << 1) + 1
        k2 = (k1 + i) * i + k1
        k1 *= Iterative
        k2 -= k1
        m4 += k2
        k1 = k2 - k1
        m3 += k1 + Iterative2
        k2 += k1
        m2 -= k2
        m1 += k2
        x = (int)((x1 * m1 + x2 * m2 + xr1 * m3 +xr2 * m4) / Iterative3)
        y = (int)((y1 * m1 + y2 * m2 + yr1 * m3 +yr2 * m4) / Iterative3)
        draw.line(((oldx, oldy), (x, y)), fill=255)
        oldx = x
        oldy = y;

if __name__ == '__main__':
    im = Image.new('RGB', (400, 400), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    Draw_HermiteCurve(100,200,300,200,5,-5,8,8,draw)

    for i in range(19):
        k = 20 * (i + 1)
        for j in range(400):
            im.putpixel((k, j), (0, 0, 0))
            im.putpixel((j, k), (0, 0, 0))
    im.show()