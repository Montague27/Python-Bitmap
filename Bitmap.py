from tkinter import *
from PIL import Image
import time

im = Image.open('E4.png')
width, height = im.size

map_sea = (24, 66, 76)
map_land = (198, 224, 190)
black = (0, 0, 0)
white = (255, 255, 255)

prvs = []
rgbs = [map_land, black] #排除計算範圍的RGB色碼
rgb_im = im.convert('RGB')

def nearby_color(xy, color):
    x, y = xy
    e,s,w,n = (x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)
    ne,nw,se,sw = (x + 1, y - 1), (x - 1, y - 1), (x + 1, y + 1), (x - 1, y + 1)
    direction = [e, s, w, n, ne, nw, se, sw]  
    for xy in direction:
        x, y = xy
        if -1 < x < width and -1 < y < height:
            rgb = rgb_im.getpixel((x, y))
            if rgb == color:
                return True
    return False

def nearby_rgb(xy):
    x, y = xy
    e,s,w,n = (x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)
    ne,nw,se,sw = (x + 1, y - 1), (x - 1, y - 1), (x + 1, y + 1), (x - 1, y + 1)
    direction = [e, s, w, n, ne, nw, se, sw]
    for xy in direction:
        x, y = xy
        if -1 < x < width and -1 < y < height:
            rgb = rgb_im.getpixel((x, y))
            if rgb not in rgbs:
                return rgb
    return None
    
def find_pos(xy, color):
    posall = [xy]
    for i in range(500): #搜索深度 視乎地圖大細
        x, y = posall[-1]
        e,s,w,n = (x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)
        direction = [e, s, w, n]
        for xy in direction:
            x, y = xy
            if -1 < x < width and -1 < y < height:
                if xy not in posall:
                    rgb = rgb_im.getpixel((x, y))
                    if rgb == black:
                        if nearby_color(xy, color):
                            posall.append(xy)
    return posall

def get_pos():
    for y in range(height):
        for x in range(width):
            xy = x, y
            rgb = rgb_im.getpixel(xy)
            if rgb != map_sea and rgb == black:
                nearby_color = nearby_rgb(xy)
                if nearby_color is not None:
                    if nearby_color not in rgbs:
                        rgbs.append(nearby_color)
                        pos = find_pos(xy, nearby_color)
                        prvs.append(pos)
                        
class MainGame(Frame):
    def __init__(self, parent): 
        Frame.__init__(self, parent)  
        self.parent = parent        
        self.initUI()
        
    def initUI(self):
        self.parent.title('Python')
        self.pack(fill = BOTH, expand = 1)
        self.canvas = Canvas(self)
        for prv in prvs:
            self.canvas.create_polygon(prv, outline = 'black', fill = '#CCCCFF')

        self.canvas.pack()

#計算所需運行時間 可移除        
times= time.time()
get_pos()
print(time.time() - times)

#顯示地圖
root = Tk()
root.geometry('600x600+0+0')
main = MainGame(root)
