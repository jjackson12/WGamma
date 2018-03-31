from glob import glob
from pprint import pprint

def parseConfigs(show = False):
  configFiles =  glob("../HgammaCondor/singlePhoton_Apr21.ini")
  configsDict={}

  from ConfigParser import RawConfigParser
  parsers = []
  for configFile in configFiles:
    parsers.append(RawConfigParser())
    parsers[-1].optionxform = str
    parsers[-1].read(configFile)
    values = dict(parsers[-1].items('ShortNames')).values()
    configsDict[configFile] = values
  if show:
    pprint(configsDict)
  return configsDict

def findAllMatches(show=False):
  datasetsDict = parseConfigs()
  for key in datasetsDict:
    if "ext" in key:
      del datasetsDict[key]
  matchingFiles = {}
  for datasetsArray in datasetsDict.values():
    for dataset in datasetsArray:
      if not "ext" in dataset:
        if "qcd" in dataset: ## fixme
          dataset = dataset.replace("qcdHT", "qcd")
        matchingFiles[dataset] = glob("../HgammaCondor/smallified_%s*.root" % dataset)
  if show:
    pprint(matchingFiles)
  return matchingFiles
  
def haddTogetherAllDatasets(outDir, haddDatasets = True, mergeData = True, show = False): 
  from commands import getoutput
  from os import makedirs, path
  filesDict = findAllMatches()
  if not path.exists(outDir):
    makedirs(outDir)
  for dataset in filesDict:
    if filesDict[dataset]:
      incantation = "hadd %s/smallified_%s.root %s" % (outDir, dataset, " ".join(filesDict[dataset]))
      if haddDatasets:
        if show:
          print incantation
        print getoutput(incantation)
  if mergeData:
    from shutil import move
    singlePhotons = []
    singleMuons = []
    for smallification in glob("%s/*" % outDir):
      if "2016" in smallification:
        if "singlePhoton" in smallification:
          singlePhotons.append(smallification)
        if "singleMuon" in smallification:
          singleMuons.append(smallification)
    if show: 
      print "singlePhotons:"
      pprint(singlePhotons)
      print "singleMuons:"
      pprint(singleMuons)
    singlePhotonDir = path.join(outDir, "singlePhotonFrags")
    singleMuonDir = path.join(outDir, "singleMuonFrags")
    if not path.exists(singlePhotonDir):
      makedirs(singlePhotonDir)
    if not path.exists(singleMuonDir):
      makedirs(singleMuonDir)
    for sp in singlePhotons:
      move (sp, path.join(singlePhotonDir, path.basename(sp)))
    for sm in singleMuons:
      move (sm, path.join(singleMuonDir, path.basename(sm)))
    incantationPhotons = "hadd %s/smallified_data2016SinglePhoton.root %s" % (outDir, " ".join(glob("%s/*.root"%singlePhotonDir)))
    incantationMuons = "hadd %s/smallified_data2016SingleMuon.root %s" % (outDir, " ".join(glob("%s/*.root"%singleMuonDir)))
    if show:
      print getoutput(incantationPhotons)
      print getoutput(incantationMuons)

haddTogetherAllDatasets("smallifications_May2", True, True, True)
