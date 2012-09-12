from supy.samples import SampleHolder
from supy.sites import eos


eosBaseDir='/eos/atlas/user/g/gerbaudo/trigger/skim'
skims = ['EF_A4_OR_A10','L1_RD0_FILLED', 'L1_4J15']
lumiPerRun = {208184:105.2, 208258:92.55, 208261:103.1, 208354:133.2, # D4, D5
              208485:142.2, 208662:149.0, # D6, D7
              }

def skimmedPeriodD(skim='') :
    assert skim in skims,"periodD: this skim is not available :%s"%skim
    periodD = SampleHolder()
    fileListCmd = '+'.join(['%s%s")'%(eos(),"%s/SUSYD3PD.%d.skim.%s"%(eosBaseDir,run,skim)) for run in lumiPerRun.keys()])
    periodD.add("periodD.%s"%skim, fileListCmd, lumi = sum(lumiPerRun.values()))
    return periodD

# might want to define per-run samples?
##for r in runs :
##    for d in ['EF_A4_OR_A10','L1_RD0_FILLED'] :
##        exampleDict.add("%d.%s"%(r,d),
##                        '%s%s")'%(supy.sites.eos(),
##                                  "%s/SUSYD3PD.%d.skim.%s"%(eosBaseDir,r,d)),
##                        lumi=lumiPerRun[r])
