# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 19:25:36 2017

@author: mykytayurtyn
"""
from PIL import Image

import os
import errno

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


boxfile = "cartruck.box.list"

tsize = 128, 128

with open(boxfile) as bfile:
    
    for l in bfile:
        ls = l.split()
        
        fname = ls[0]
        cls = ls[1]
        x = float(ls[2])
        y = float(ls[3])
        w = float(ls[4])
        h = float(ls[5])
        
        tgtdir, tgtf = os.path.split(fname)

        if(tgtdir.startswith("..")):
            tgtdir = tgtdir[3:]            
        tgtdir = os.path.join("cropped", tgtdir)
        mkdir_p(tgtdir)

        tgtf = os.path.join(tgtdir, tgtf)  
            
        im = Image.open(fname)
        width, height = im.size
        left  = int((x - w/2.) * width);
        right = int((x + w/2.) * width);
        top   = int((y - h/2.) * height);
        bot   = int((y + h/2.) * height);
        
        print width, height
        print left, top, right, bot

        im = im.crop((left, top, right, bot))
#        im = im.thumbnail(tsize, Image.ANTIALIAS)
        im.save(tgtf, "JPEG")
        
        
        