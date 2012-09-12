from supy.samples import SampleHolder
from supy.sites import eos


eosBaseDir='/eos/atlas/user/g/gerbaudo/trigger/skim'
skims = ['L1_4J15']
lumiPerRun = {202668:26.0, 202712:29.85, 202740:7.28, 202798:52.6, # B1
              202965:24.7, 202987:14.02, 202991:40.15, 203027:89.29, 203258:119.4, #B2
              }

def skimmedPeriodB(skim='') :
    assert skim in skims,"periodB: this skim is not available :%s"%skim
    periodB = SampleHolder()
    fileListCmd = '+'.join(['%s%s")'%(eos(),"%s/SUSYD3PD.%d.skim.%s"%(eosBaseDir,run,skim)) for run in lumiPerRun.keys()])
    periodB.add("periodB.%s"%skim, fileListCmd, lumi = sum(lumiPerRun.values()))
    return periodB
