from skimage import io,transform

class Canvas:
    def __init__(self):
        self.canvas=None
        self.paper=None
        self.width=None
        self.height=None
        self.palette=[]

    def set_canvas(self,width,height):
        self.width=width
        self.height=height

    def set_paper(self,paper):
        img=io.imread(paper)
        self.canvas=transform.resize(img, (self.height,self.width))
        #io.imshow(self.canvas)
        #io.show()

    def set_palettecolor(self,color):
        c=[color]
        self.palette.extend(c)

if __name__=='__main__':
    canvas=Canvas()
    canvas.set_canvas(600,400)
    canvas.set_paper('paper.jpg')
