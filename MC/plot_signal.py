from ROOT import *
import sys
import os
import re

#TODO: Might need to create this file
gROOT.Macro("rootLogon.C")

quantity = sys.argv[1]
print("\nlooking at " + quantity + " in Signal\n\n")


for signalFile in os.listdir("Signal"):
    print("\n\nRunning on "+signalFile+"\n\n")
    mass = re.search(r'(.*)m(.*).root',signalFile).groups()[1]
    print("\n\n mass: "+mass+"\n\n")
    #title = quantity + "for signal at mass " + mas
    can = TCanvas(quantity + " for signal at mass " + mass + " GeV",quantity + " for signal at mass " + mass + "GeV")
    f = TFile("Signal/"+signalFile)
    tree = f.Get("ntuplizer/tree")
    tree.Draw(quantity)
    can.Print("signal_"+quantity+"_"+mass+".png",'png')

print("\ndone!\n")



