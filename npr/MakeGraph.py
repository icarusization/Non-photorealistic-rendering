import Image

im = Image.open('paper.jpg')
im = im.resize((250*2,250*2))
im.save('paper2.jpg')