# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 16:08:01 2017

@author: mykytayurtyn
"""

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

resdir = "results"
flines = {}

lblfile = "data/coco.names"

with open(lblfile) as lblf:
    labels = [line.rstrip('\n') for line in open(lblfile)]



for fpath, subdirs, files in os.walk(resdir):
    for f in files:
        filename, fileext = os.path.splitext(f)
        if(fileext <> ".txt"):
            continue
        f = os.path.join(fpath, f)
        with open(f) as fl:
            for l in fl:
                rl = l.split()
                fname = rl[0]
                lbl = rl[1]
                prob = float(rl[2])
                xa = int(rl[3])
                ya = int(rl[4])
                wa = int(rl[5])
                ha = int(rl[6])
                xb = float(rl[7])
                yb = float(rl[8])
                wb = float(rl[9])
                hb = float(rl[10])
                
                if(not fname in flines):
                    flines[fname] = {}
                    flines[fname]["wb"] = 0.00
                    #print flines
                    
                if(flines[fname]["wb"] < wb):
                    flines[fname] = {
                        "fname": fname,
                        "lbl": lbl,
                        "prob": prob,
                        "xa": xa,
                        "ya": ya,
                        "wa": wa,
                        "ha": ha,
                        "xb": xb,
                        "yb": yb,
                        "wb": wb,
                        "hb": hb
                    }

with open("cartruck.train.list", "w") as tl: 
    for x in flines:
        line = flines[x]
        if(line["lbl"] not in ("car", "truck") and line["wb"] < 0.4):
            continue    
        fname = line["fname"]
        
#        print labels
        lblidx = labels.index(line["lbl"])   

        
        tgtdir, tgtf = os.path.split(fname);

        # set target dir for labels        
        if(tgtdir.startswith("..")):
            tgtdir = tgtdir[3:]            
        tgtdir = os.path.join("labels", tgtdir)
        
        #set target label and boxfile
        tgtf, tgtfe = os.path.splitext(tgtf)        
        tgtf = tgtf + ".txt"
        tgtf = os.path.join(tgtdir, tgtf)
        
        mkdir_p(tgtdir)
        with open(tgtf, "w") as t:
            t.write("%s %f %f %f %f\n" % (lblidx, line["xb"], line["yb"], line ["wb"], line["hb"]))

        
        
        tl.write(fname)
        tl.write("\n")

