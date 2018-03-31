from sys import argv
from ROOT import *

fileName = "bkgSanityCheck/bkg_vs_data_%s.root" % argv[1]
f = TFile(str(fileName))
f.Get("can").Draw()

