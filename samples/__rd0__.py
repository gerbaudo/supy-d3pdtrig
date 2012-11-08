
from supy.samples import SampleHolder
from supy.sites import eos

# skims created by Rajiv from the MinBias stream with condition
#   "EF_j15_a4tchad = 1 OR EF_j25_a4tchad = 1 OR EF_j35_a4tchad = 1 OR EF_rd0_filled_NoAlg = 1"

def minbiasPeriodD() :
    eosBaseDir='/eos/atlas/user/g/gerbaudo/trigger/skim'
    skims = ['subraman.207447_490.skim.EFRDO','subraman.208123_208179.skim.EFRDO','subraman.208184_208189.skim.EFRDO']
    lumiPerRun = {207447:172.1,207490:117.2 # D1
                  ,208123:70.3,208126:26.4 # D3
                  ,208179:7.5,208184:105.2,208189:45.2 # D4
                  }
    rd0 = SampleHolder()
    lumi = sum(lumiPerRun.values())
    fileListCmd = '+'.join(['%s%s")'%(eos(),"%s/%s"%(eosBaseDir,skim)) for skim in skims])
    rd0.add("periodDrd0", fileListCmd, lumi = lumi)
    return rd0
