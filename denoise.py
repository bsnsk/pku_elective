#coding:utf-8
import sys,os
from PIL import Image,ImageDraw

#---------------------This file is from http://dream-people.iteye.com/blog/378907-----------------
#--------------------- Modified by bsnsk ---------------------------------------------------------

t2val = {}
def twoValue(image,G):
    for y in xrange(0,image.size[1]):
        for x in xrange(0,image.size[0]):
            g = image.getpixel((x,y))
            t2val[(x, y)] = 1 if g > G else 0

# denoise
# G: two-value threshold
# N: desnoising rate
# Z: denoising times
def clearNoise(image, N, Z):

    neighbor_dirs = [
        (-1, -1), (-1, 1), (-1, 0),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    for i in xrange(0,  Z):
        t2val[(0,0)] = 1
        t2val[(image.size[0] - 1,image.size[1] - 1)] = 1

        for x in xrange(1,image.size[0] - 1):
            for y in xrange(1,image.size[1] - 1):
                nearDots = 0
                L = t2val[(x,y)]
                for (dx, dy) in neighbor_dirs:
                    if L == t2val[(x + dx, y + dy)]:
                        nearDots += 1
                if nearDots < N:
                    t2val[(x,y)] = 1

def saveImage(filename,size):
    image = Image.new("1",size)
    draw = ImageDraw.Draw(image)

    for x in xrange(0,size[0]):
        for y in xrange(0,size[1]):
            draw.point((x,y),t2val[(x,y)])

    image.save(filename)


def process(img_in, img_out):
    image = Image.open("%s" % img_in).convert("L")
    twoValue(image, 100)
    clearNoise(image, 3, 4)
    saveImage("%s" % img_out, image.size)
