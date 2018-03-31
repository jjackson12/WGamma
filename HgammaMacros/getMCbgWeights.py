from ROOT import *

# janky methods for mapping the samples cross sections, the sample's small3 tree, and the sample's treeChecker tree
# John Hakala 5/11/2016

def getDDPrefix():
  return "ddTree_"

def getSmallPrefix():
  return "smallified_"

#TODO: Set to 1 for now
def getMCbgSampleKfactors():
  sampleXsects = {}
  sampleXsects[   "gJets100To200.root"   ]   = 1.6*0.8
  sampleXsects[   "gJets200To400.root"   ]   = 1.6*0.8
  sampleXsects[   "gJets400To600.root"   ]   = 1.4*0.8
  sampleXsects[   "gJets600ToInf.root"   ]   = 1.0*0.8
  sampleXsects[   "qcd300to500.root"     ]   = .7 *0.8
  sampleXsects[   "qcd500to700.root"     ]   = .7 *0.8
  sampleXsects[   "qcd700to1000.root"    ]   = .7 *0.8
  sampleXsects[   "qcd1000to1500.root"   ]   = .7 *0.8
  sampleXsects[   "qcd1500to2000.root"   ]   = .7 *0.8
  sampleXsects[   "qcd2000toInf.root"    ]   = .7 *0.8
  #sampleXsects[   "qcd200to300.root"     ]  = 1   
  #sampleXsects[   "dyJetsQQ-180.root"    ]  = 1.23  
  #sampleXsects[ "wJetsQQ-180.root" ]        = 1.21*0.8 
  return sampleXsects

#TODO: Update list
def getMCbgSampleXsects():
  kFactors = getMCbgSampleKfactors()
  sampleXsects = {}
  sampleXsects[   "gJets100To200.root"   ]   = 9238
  sampleXsects[   "gJets200To400.root"   ]   = 2305
  sampleXsects[   "gJets400To600.root"   ]   = 274.4
  sampleXsects[   "gJets600ToInf.root"   ]   = 93.46 
  sampleXsects[   "qcd300to500.root"     ]   = 347700     
  sampleXsects[   "qcd500to700.root"     ]   = 32100      
  sampleXsects[   "qcd700to1000.root"    ]    = 6831       
  sampleXsects[   "qcd1000to1500.root"   ]    = 1207       
  sampleXsects[   "qcd1500to2000.root"   ]    = 119.9      
  sampleXsects[   "qcd2000toInf.root"    ]    = 25.24      
  #sampleXsects[   "qcd200to300.root"     ]   = 1712000    
  #sampleXsects[   "dyJetsQQ-180.root"    ]    = 1187  
  #sampleXsects[ "wJetsQQ-180.root" ] = 95.14 
  return sampleXsects

#NOTE: "small3Dir" is the directory in which all of the background root files are held.
def getMCbgSampleEvents(small3Dir):
  sampleXsects=getMCbgSampleXsects()
  sampleEvents = {}
  for key in sampleXsects:
    mcBGfileName = "%s/%s%s" % (small3Dir, getSmallPrefix(), key)
    #print "the small3 input filename is: %s" % mcBGfileName
    mcBGfile = TFile( mcBGfileName )
    #print mcBGfile
    hCounter = mcBGfile.Get("ntuplizer/hCounter")
    nEvents = hCounter.GetBinContent(1)
    sampleEvents[key]=nEvents;
  return sampleEvents

def getSignalsToInclude():
  return [  "sig_m750.root",
            "sig_m850.root",
            "sig_m1000.root",
            "sig_m1150.root",
            "sig_m1300.root",
            "sig_m1450.root",
            "sig_m1600.root",
            "sig_m1750.root",
            "sig_m1900.root",
            "sig_m2050.root",
            "sig_m2450.root",
            "sig_m2850.root",
            "sig_m3250.root",
          ]

def getWeightsDict(bkgSmall3Dir):
  sampleKfactors = getMCbgSampleKfactors() 
  sampleXsects   = getMCbgSampleXsects() 
  sampleEvents   = getMCbgSampleEvents(bkgSmall3Dir)

  lumi = 35900

  sampleWeights = {}
  for key in sampleXsects:
    expectedEvents = lumi*sampleXsects[key]
    weight = sampleKfactors[key]*expectedEvents/sampleEvents[key]
    sampleWeights[key] = (weight, "bkg")
  signalWeight = .5
  #for signalToInclude in getSignalsToInclude():
  #  sampleWeights[signalToInclude] = signalWeight
  sampleWeights["data2016SinglePhoton.root"] = (1 , "data")
  sampleWeights[ "sig_m750.root"   ] = (.8*0.4, "sig")
  sampleWeights[ "sig_m850.root"   ] = (.8*0.4, "sig")
  sampleWeights[ "sig_m1000.root"  ] = (.7*0.4, "sig")
  sampleWeights[ "sig_m1150.root"  ] = (.7*0.4, "sig")
  sampleWeights[ "sig_m1300.root"  ] = (.7*0.4, "sig")
  sampleWeights[ "sig_m1450.root"  ] = (.6*0.4, "sig")
  sampleWeights[ "sig_m1600.root"  ] = (.6*0.4, "sig")
  sampleWeights[ "sig_m1750.root"  ] = (.6*0.4, "sig")
  sampleWeights[ "sig_m1900.root"  ] = (.5*0.4, "sig")
  sampleWeights[ "sig_m2050.root"  ] = (.5*0.4, "sig")
  sampleWeights[ "sig_m2450.root"  ] = (.5*0.4, "sig")
  sampleWeights[ "sig_m2850.root"  ] = (.4*0.4, "sig")
  sampleWeights[ "sig_m3250.root"  ] = (.4*0.4, "sig")
  return sampleWeights

def getMCbgWeightsDict(bkgSmall3Dir):
 weights = getWeightsDict(bkgSmall3Dir) 
 nonMCbgs = getSignalsToInclude()
 nonMCbgs.append("data2016SinglePhoton.root")
 for nonMCbg in nonMCbgs:
   weights.pop(nonMCbg)
 return weights

def getMCbgOrderedList():
  return [ 
    #"dyJetsQQ-180.root"   ,
    #"wJetsQQ-180.root"    ,
    "qcd2000toInf.root"     ,
    "qcd1500to2000.root"    ,
    "qcd1000to1500.root"    ,
    "qcd700to1000.root"     ,
    "qcd500to700.root"      ,
    "qcd300to500.root"      ,
    #"qcd200to300.root"      ,
    "gJets600ToInf.root"    ,
    "gJets400To600.root"    ,
    "gJets200To400.root"    ,
    "gJets100To200.root"   
  ]

def getMCbgColors():
  color = TColor()
  sampleColors = {}
  #sampleColors["QCD_HT100to200.root"       ] = color.GetColor(.1, 0.3, 0.25)
  sampleColors["gJets100To200.root" ] = color.GetColor(.475*1.1, .6*1.2, 1.0)
  sampleColors["gJets200To400.root" ] = color.GetColor(.475, .6, 1.0)
  sampleColors["gJets400To600.root" ] = color.GetColor(.35, .5, 0.85)
  sampleColors["gJets600ToInf.root" ] = color.GetColor(.225, .3, 0.7) 
  #sampleColors["qcd200to300.root"   ] = color.GetColor(.31*1.2, 1.0, 0.425*1.2)
  sampleColors["qcd300to500.root"   ] = color.GetColor(.31, .95, 0.425)
  sampleColors["qcd500to700.root"   ] = color.GetColor(.28, .9, 0.4)
  sampleColors["qcd700to1000.root"  ] = color.GetColor(.25, .8, 0.375)
  sampleColors["qcd1000to1500.root" ] = color.GetColor(.22, .7, 0.35)
  sampleColors["qcd1500to2000.root" ] = color.GetColor(.19, .6, 0.325)
  sampleColors["qcd2000toInf.root"  ] = color.GetColor(.16, .5, 0.3)
  #sampleColors["dyJetsQQ-180.root"  ] = color.GetColor(.6, .2, .2)
  #sampleColors["wJetsQQ-180.root"   ] = color.GetColor(.85, .85, 0.3)
  return sampleColors

def getMCbgLabels():
  color = TColor()
  legendLabels = {}
  legendLabels["gJets100To200.root" ] = "#gamma#plusjets[100,200]"
  legendLabels["gJets200To400.root" ] = "#gamma#plusjets[200,400]"
  legendLabels["gJets400To600.root" ] = "#gamma#plusjets[400,600]"
  legendLabels["gJets600ToInf.root" ] = "#gamma#plusjets[600,#infty]"
  #legendLabels["qcd200to300.root"   ] = "QCD[200,300]"
  legendLabels["qcd300to500.root"   ] = "QCD[300,500]"
  legendLabels["qcd500to700.root"   ] = "QCD[500,700]"
  legendLabels["qcd700to1000.root"  ] = "QCD[700,1000]"
  legendLabels["qcd1000to1500.root" ] = "QCD[1000,1500]"
  legendLabels["qcd1500to2000.root" ] = "QCD[1500,2000]"
  legendLabels["qcd2000toInf.root"  ] = "QCD[2000,#infty]"
  #legendLabels["dyJetsQQ-180.root"  ] = "DY#plusjets[180,#infty]"
  #legendLabels["wJetsQQ-180.root"   ] = "W#plusjets[600,#infty]"
  #legendLabels["QCD_HT100to200"       ] = "QCD[100,200]"
  return legendLabels

def getSmall3ddTreeDict(ddDir):
  s3dd = {}
  
  #s3dd["QCD_HT100to200.root"       ] = "%s/ddTree_QCD_HT100to200.root"%ddDir
  #s3dd["gJets100To200" ] = "%s/ddTree_GJets100-200"  % ddDir
  s3dd["gJets200To400.root" ] = "%s/ddTree_gJets200To400"  % ddDir
  s3dd["gJets400To600.root" ] = "%s/ddTree_gJets400To600"  % ddDir
  s3dd["gJets600ToInf.root" ] = "%s/ddTree_gJets600ToInf"  % ddDir
  #s3dd["qcd200to300.root"   ] = "%s/ddTree_qcd200to300"    % ddDir
  s3dd["qcd300to500.root"   ] = "%s/ddTree_qcd300to500"    % ddDir
  s3dd["qcd500to700.root"   ] = "%s/ddTree_qcd500to700"    % ddDir
  s3dd["qcd700to1000.root"  ] = "%s/ddTree_qcd700to1000"   % ddDir
  s3dd["qcd1000to1500.root" ] = "%s/ddTree_qcd1000to1500"  % ddDir
  s3dd["qcd1500to2000.root" ] = "%s/ddTree_qcd1500to2000"  % ddDir
  s3dd["qcd2000toInf.root"  ] = "%s/ddTree_qcd2000toInf"   % ddDir
  #s3dd["dyJetsQQ-180.root"  ] = "%s/ddTree_dyJetsQQ-180"   % ddDir
  #s3dd["wJetsQQ-180.root"   ] = "%s/ddTree_wJetsQQ-180"    % ddDir

  return s3dd
