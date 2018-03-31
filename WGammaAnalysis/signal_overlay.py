from ROOT import *
import sys 
from getMCbgWeights import *
import re
import os


bkgDir = "../HgammaCondor/smallified_bkg"
signalDir = "../HgammaCondor/smallified_signal"

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
histRanges["jetAK8_puppi_softdrop_mass"] = (0,500)

#TODO: 750 isn't among my signal MC; do I do 700 and/or 800?
signalMasses = [600, 800,1000,2000,3500]


#weight calculation
weightDict = getMCbgWeightsDict(bkgDir)



observables = ["ph_pt","ph_eta","jetAK8_pt","jetAK8_eta","jetAK8_puppi_softdrop_mass"]


for observable in observables:
	print("plotting all for %s"%observable)

	#Data
	dataHist = TH1F("dataHist", "dataHist", nBins, histRanges[observable][0], histRanges[observable][1])
	data.Draw("%s>>dataHist" % observable)

	#Background
	fileDict = {}
	bkgHists = {}
	iterTrees = {}

	for bkgFile in os.listdir(bkgDir):
	    print("processing background: %s\n" % bkgFile)
	    bkg = re.search(r'(.*)smallified_(.*).root',bkgFile).groups()[1]
	    fileDict[bkg] = TFile("%s/%s" % (bkgDir, bkgFile))
	    iterTrees[bkg] = fileDict[bkg].Get("ntuplizer/tree")
	    histLabel = "%s_%s" % (bkg, observable)

	    bkgHists[bkg]=TH1F(histLabel, histLabel, nBins, histRanges[observable][0], histRanges[observable][1])
	    #iterTree.Draw('%s>>%s' % (observable, histLabel), str(weight))
	    iterTrees[bkg].Draw('%s>>%s' % (observable, histLabel))
	    efficiency = iterTrees[bkg].GetEntries()/fileDict[bkg].Get("ntuplizer/hCounter").GetBinContent(1)
	    weight =  weightDict["%s.root"%bkg][0]
	    bkgHists[bkg].Scale(weightDict["%s.root"%bkg][0])
	    #bkgHists[bkg].Scale(weight)
	    bkgHists[bkg].Sumw2()

	histStack = THStack()
	colors = [kRed,kBlue,kBlack,kGreen,kOrange,kYellow,kBlue-1,kRed+1,kGreen+2,kPink,kViolet,kAzure,kTeal,kTeal+3]
	for bkgHist in bkgHists.itervalues():
	    #bkgHist.Sumw2()
	    color = colors.pop()
	    bkgHist.SetLineColor(color)
	    bkgHist.SetFillColor(color)
	    histStack.Add(bkgHist)


	#Signal

	sigHists = {}
	def getSignalHist(mass):
	    fileName = "%s/smallified_WGammaSig_m%s.root"%(signalDir,mass)
	    name = "signal_m" + str(mass)
	    fileDict[name] = TFile(fileName)
	    iterTrees[name] = fileDict[name].Get("ntuplizer/tree")
	    histLabel = "%s_%s" % (name, observable)

	    sigHists[name]=TH1F(histLabel, histLabel, nBins, histRanges[observable][0], histRanges[observable][1])
	    #iterTree.Draw('%s>>%s' % (observable, histLabel), str(weight))
	    iterTrees[name].Draw('%s>>%s' % (observable, histLabel))
	    sigHists[name].SetLineColor(kRed)
	    return sigHists[name]



	cans = {}

	  
	for sigMass in signalMasses:
	    print("\nplotting signal mass %s\n"%sigMass)
	    cans[sigMass] = TCanvas("can","Signal overlay on Data",800,800)
	    cans[sigMass].cd()
	    signal = getSignalHist(sigMass)
	    signal.Scale(dataHist.GetSumOfWeights()/signal.GetSumOfWeights())
	    signal.Draw()
	    dataHist.Draw("SAME")
	    leg = TLegend(0.7,0.7,0.9,0.9)
	    leg.AddEntry(signal,"signal")
	    leg.AddEntry(dataHist,"data")
	    leg.Draw("SAME")
	    cans[sigMass].SetLogy()
	    
	    printName = 'signalOverlays/%s/signal_m%s_%s.png'%(observable,str(sigMass), observable)
	    cans[sigMass].Print(printName,'png')
	    outFile = TFile("signalOverlays/%s/signal_m%s_%s.root"%(observable,str(sigMass), observable),"RECREATE")
	    outFile.cd()
	    cans[sigMass].Write()
	    outFile.Close()
