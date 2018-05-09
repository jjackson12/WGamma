from ROOT import *
import sys 
from getMCbgWeights import *
import re
import os

observable = sys.argv[1]

bkgDir = "../HgammaCondor/smallified_bkg"

weightDict = getMCbgWeightsDict(bkgDir)
sampleEvents   = getMCbgSampleEvents(bkgDir)



dataFile = TFile("../HgammaCondor/smallified_data2/smallified_singlePhoton2016.root")
data = dataFile.Get("ntuplizer/tree")




nBins = 1000


histRanges = {}

histRanges["ph_pt"] = (0, 1200)
histRanges["jetAK8_pt"] = (0, 1200)
histRanges["ph_eta"] = (-3.,3.)
histRanges["ph_phi"] = (-3.14,3.14)
histRanges["jetAK8_eta"] = (-3.,3.)
histRanges["jetAK8_phi"] = (-3.14,3.14)


dataHist = TH1F("dataHist", "dataHist", nBins, histRanges[observable][0], histRanges[observable][1])
data.Draw("%s>>dataHist" % observable)



#TH1
#TGraphASimErrors (good for asymmetrical errors)
#TEfficiencyPlot: 
#Preffered: TH1::Divide, with Sumw()

#THStack.GetStack().Last() = Total Histogram
#TH1.Sumw2 CALL ITERATIVELY ON EACH BKG HISTOGRAM
#TH1.Divide(denominator) (Clone original histogram)



lumi = 35900
xSects = getMCbgSampleXsects()

fileDict = {}
bkgHists = {}
iterTrees = {}

for bkgFile in os.listdir(bkgDir):
    print("\n\nprocessing background: %s\n" % bkgFile)
    bkg = re.search(r'(.*)smallified_(.*).root',bkgFile).groups()[1]
    fileDict[bkg] = TFile("%s/%s" % (bkgDir, bkgFile))
    iterTrees[bkg] = fileDict[bkg].Get("ntuplizer/tree")
    histLabel = "%s_%s" % (bkg, observable)

    bkgHists[bkg]=TH1F(histLabel, histLabel, nBins, histRanges[observable][0], histRanges[observable][1])
    #iterTree.Draw('%s>>%s' % (observable, histLabel), str(weight))
    iterTrees[bkg].Draw('%s>>%s' % (observable, histLabel))
    efficiency = iterTrees[bkg].GetEntries()/fileDict[bkg].Get("ntuplizer/hCounter").GetBinContent(1)
    weight = lumi*xSects["%s.root"%bkg]/sampleEvents["%s.root"%bkg]
    print("weight calc = %s"%weight)
    weight =  weightDict["%s.root"%bkg][0]
    print("weight comp  = %s"%weight)
    bkgHists[bkg].Scale(weightDict["%s.root"%bkg][0])
    #bkgHists[bkg].Scale(weight)
    bkgHists[bkg].Sumw2()
    print("(From drawn Hist:) N = %s" % str(bkgHists[bkg].GetSumOfWeights()/efficiency))
    print("(From Direct Calculation:) N = %s" % str(lumi*xSects["%s.root" % bkg]))

#bkgHists[bkg].Scale(weight) 

histStack = THStack()
colors = [kRed,kBlue,kBlack,kGreen,kOrange,kYellow,kBlue-1,kRed+1,kGreen+2,kPink,kViolet,kAzure,kTeal,kTeal+3]
for bkgHist in bkgHists.itervalues():
    #bkgHist.Sumw2()
    color = colors.pop()
    bkgHist.SetLineColor(color)
    bkgHist.SetFillColor(color)
    histStack.Add(bkgHist)



ratioPlot = dataHist.Clone("ratioPlot")

ratioPlot.SetNameTitle("ratioPlot","Ratio of Data to MC Background Predictions")
ratioPlot.Divide(histStack.GetStack().Last()) 
ratioPlot.SetMinimum(0.8)
ratioPlot.SetMaximum(1.35)
#ratioPlot.Sumw2()
#ratioPlot.Draw()
ratioBins = 10
binRatio = int(ratioPlot.GetNbinsX()/ratioBins)
#ratioPlot.RebinX(10)

can = TCanvas("can","MC Background vs. Data",800,800)

# Upper histogram plot is pad1
pad1 = TPad("pad1", "pad1", 0, 0.4, 1, 1.0)
#pad1.SetBottomMargin(0)  # joins upper and lower plot
pad1.SetGridx()
pad1.Draw()
# Lower ratio plot is pad2
can.cd()  # returns to main canvas before defining pad2
pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
#pad2.SetTopMargin(0)  # joins upper and lower plot
#pad2.SetBottomMargin(0.2)
pad2.SetGridx()
pad2.Draw()

pad1.cd()

histStack.Draw()
dataHist.Draw("SAME")
leg = TLegend(0.7,0.7,0.9,0.9)
for h in bkgHists.values():
    print("Adding legend element for %s" % h.GetName())
    leg.AddEntry(h,h.GetName().replace("_"+observable,""),"f")
leg.AddEntry(dataHist,"data","p")
leg.Draw("SAME")
pad1.SetLogy()

pad2.cd()
ratioPlot.Draw()
pad2.SetLogy()
#ratioPlot.Draw("ep")
can.SetTitle(observable)
can.Print('bkgSanityCheck/bkg_vs_data_%s.png'%observable,'png')

outFile = TFile("bkgSanityCheck/bkg_vs_data_%s.root" % observable,"RECREATE")
outFile.cd()
can.Write()
outFile.Close()
