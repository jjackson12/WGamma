from os import path, makedirs, getcwd
from glob import glob
from runHgammaSelector import processHg
from pprint import pprint

debug = False
first = True

#for variation in [("nom", 0), ("up", 1), ("down", -1)]:
for variation in [("nom", 0)]:
  baseDir = path.join(getcwd(), "organize_smallifications")
  categories = ["backgrounds", "signals", "data"]
  #categories = ["signals"]
  catDirs = {}
  for category in categories:
    catDirs[category] = path.join(baseDir, category)
  
  pprint(catDirs)
  
  outDir = baseDir.replace("smallifications", "DDs_btag-%s" % variation[0])
  if not path.exists(outDir):
    makedirs(outDir)
  print "catDirs", catDirs
  for catDir in catDirs:
    catOutDir = path.join(outDir, catDir)
    inputFiles = glob("%s/%s/*.root" % (baseDir, catDir))
    
    if not path.exists(catOutDir):
      makedirs(catOutDir)
    for inputFile in inputFiles:
      if first:
        print "about to call the first processHg" 
        processHg(inputFile, inputFile.replace("smallified", "ddTree").replace("smallifications", "DDs_btag-%s" % variation[0]), False, False, variation[1])
        first = False
      elif not debug:
        processHg(inputFile, inputFile.replace("smallified", "ddTree").replace("smallifications", "DDs_btag-%s" % variation[0]), True, True, variation[1])
