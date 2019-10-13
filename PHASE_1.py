from hilbertcurve.hilbertcurve import HilbertCurve as HC
import math
from PIL import Image, ImageOps
import numpy as np

#note: img_pth = image path

def GetImage():
    im_pth = str(input("Enter file path (eg BATMAN.JPG): "))
    im = Image.open(im_pth)
    return im

def ImageToRGB(im):

    old_size = im.size  # old_size[0] is in (width, height) format
    old_resolution = old_size[0]*old_size[1]

    N=2
    p = math.ceil(math.log(old_resolution,2)/2)

    desired_size = 2**p

    PaddingColour1 = PaddingColour(im, p, N)
    new_im = Image.new("RGB", (desired_size, desired_size), PaddingColour1) ##third thing - colour - here it's left blank so that automatically makes the padding area black
    new_im.paste(im, ((desired_size-old_size[0])//2,(desired_size-old_size[1])//2))
    pix = new_im.load()

    C = [0]*((4**p)*3)

    hilbert_curve = HC(p, N)
    
    
    for i in range(4**p):
        coords = hilbert_curve.coordinates_from_distance(i)
        C[3*i], C[3*i+1], C[3*i+2] = pix[coords[0], (desired_size - coords[1] - 1)]
    return (C, p, N, new_im)

#missing_R = int()
def PaddingColour(im, p, N):
    pix_val = list(im.getdata())
    first_pix_R = pix_val[0][0]
    last_pix_R = pix_val[-1][0]

    R = first_pix_R + 1
    if R == last_pix_R or R > 255:
        R = 0

    PaddingColour1 = (R , 100, 100)   
    return PaddingColour1


def RGBToImage (C, p, N):
    desired_size = 2**p
    im2 = Image.new("RGB", (desired_size , desired_size) , (255,255,255))
    hilbert_curve = HC(p, N)
    for i in range(4**p):
        coords = hilbert_curve.coordinates_from_distance(i)     #coords becomes a tuple, with an x and y value (in that order - which is why you take x coord = coords[0] and raw y = coords[1] - but then you have to change y to flip it and asjust it because the y axis goes from 0 to 99 and not 1 to 100)
        im2.putpixel((coords[0], (desired_size - coords[1] - 1)), (C[3*i],C[3*i+1],C[3*i+2]))
    pix = im2.load()
    PaddingColour2 = pix[0, 0]
    return [PaddingColour2, im2]

def RemovePadding (im, PaddingColour):
    i = 0
    P = list(im.getdata())#im.getdata() ouputs a series of tuples containing R, G, B values; NOT INDIVIDUAL R, G, B COMPONENTS
    while P[i] == PaddingColour:
        i += 1
    sideLength = len(P)**(1/2)
    top = math.floor(i/sideLength)
    left = int(i%sideLength)

    j = len(P)
    while P[j-1] == PaddingColour:
        j -= 1
    bottom = math.ceil(j/sideLength)
    right = int(j%sideLength)

    im_noPadding = im.crop((left, top, right, bottom))
    im_noPadding.show()

    








