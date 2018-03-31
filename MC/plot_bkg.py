from ROOT import *
import sys
import os
import re
import time

#TODO: Might need to create this file
gROOT.Macro("rootLogon.C")

bkgPath = sys.argv[1]
maxNumber = sys.argv[2]
quantity = sys.argv[3]
intervals = 100

print("\nlooking at " + quantity  + " in "+bkgPath+" up to "+maxNumber+"\n\n")

numbers = []
n = 0;
while(n<int(maxNumber)):
    n+=intervals
    numbers.append(n)

for number in numbers:
#TODO: Test
    subFolderNumber = "000"+str(int(number)/1000)

    bkgFile = bkgPath + "/"+subFolderNumber+"/flatTuple_"+str(number)+".root"

    bkgFilePath = "/mnt/hadoop/store/user/johakala/"+bkgFile
    print("\n\nRunning on "+bkgFilePath+"\n\n")
    title = quantity + " for " + bkgFile[0:20] + "... number "+str(number)
    can = TCanvas(title,title)
    f = TFile(bkgFilePath)
    tree = f.Get("ntuplizer/tree")
    tree.Draw(quantity)
    time.sleep(3)

print("\ndone!\n")



