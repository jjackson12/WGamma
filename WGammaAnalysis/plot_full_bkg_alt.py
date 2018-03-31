from ROOT import *
import sys 
from getMCbgWeights import *
import re
import os

observable = sys.argv[1]

bkgDir = "../HgammaCondor/smallified_bkg"

weightDict = getMCbgWeightsDict(bkgDir)


#def saveHist(iFile, oVar):
#    print("%s>>%s" % (observable, oVar)) 
#    f = TFile(iFile)
#    tree = f.Get("ntuplizer/tree")
#    tree.Draw("%s>>%s" % (observable, oVar))
#    print("%s>>%s" % (observable, oVar))
#    return 5
dataFile = TFile("../HgammaCondor/smallified_data2/smallified_singlePhoton2016.root")
data = dataFile.Get("ntuplizer/tree")

data.Draw("%s>>dataHist" % observable)
#dataHist = gDirectory.Get("dataHist")
#test = saveHist("../HgammaCondor/smallified_data2/smallified_singlePhoton2016.root",'dataHist')

nBins = dataHist.GetNbinsX()
xMax = dataHist.GetXaxis().GetXmax()
xMin = dataHist.GetXaxis().GetXmin()
bkgHist = TH1F("hist","MC Background",nBins,int(xMin),int(xMax))


histsToAdd = {}
bkgFiles = {}


#TODO: I'm going to have to rebin each histogram to line up!
for bkgFile in os.listdir(bkgDir):
    print("processing background: %s\n" % bkgFile)
    bkg = re.search(r'(.*)smallified_(.*).root',bkgFile).groups()[1]
    bkgFiles[bkg] = TFile("%s/%s" % (bkgDir, bkgFile))
    print("file","%s/%s" % (bkgDir, bkgFile))
    iterTree = bkgFiles[bkg].Get("ntuplizer/tree")
    histName = "%s_%s" % (bkg, observable)
    histsToAdd[bkg] = TH1F(histName, histName, nBins, xMin, xMax)
    iterTree.Draw('%s>>%s' % (observable, histName))


for bkg in histsToAdd.keys():
    weight = weightDict["%s.root"%bkg][0]
    oldBins = histsToAdd[bkg].GetNbinsX()
    nGroup = int(round(oldBins/nBins))
    print("weight: %s\n"% str(weight))
    histsToAdd[bkg].GetXaxis().SetRange(int(xMin),int(xMax))
    histsToAdd[bkg].Rebin(nGroup)
    bkgHist.Add(histsToAdd[bkg],weight)

can = TCanvas("mc_vs_data","MC Background vs. Data")
can.cd()
dataHist.Draw()

bkgHist.Draw("SAME")

can.Print('bkg_vs_data.png','png')



