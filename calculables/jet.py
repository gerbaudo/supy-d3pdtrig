import supy
from math import cosh

class IndicesL1(supy.wrappedChain.calculable) :
    def __init__(self, collection = ("trig_L1_jet_", "")):
        self.fixes = collection
        self.stash(["n", "eta", "phi", "et4x4", "et6x6", "et8x8",
                    "RoIWord",
                    ])
    @property
    def name(self):
        return 'IndicesL1Jets'
    def update(self, _) :
        self.value = range(self.source[self.n])
#___________________________________________________________
class IndicesL2(supy.wrappedChain.calculable) :
    def __init__(self, collection = ("trig_L2_jet_", ""), minEt = None):
        self.minEt = minEt
        self.fixes = collection
        self.stash(["n", "E", "eta", "phi", "RoIWord", "ehad0", "eem0",
                    "nLeadingCells", "hecf", "jetQuality", "emf", "jetTimeCells",
                    ])
        self.moreName = ""
        if minEt!=None: self.moreName += "et>%.1f"%minEt
    @property
    def name(self):
        return 'IndicesL2Jets'
    def update(self, _) :
        energies = self.source[self.E]
        etas = self.source[self.eta]
        self.value = []
        for i in range(self.source[self.n]):
            if self.minEt and energies.at(i)/cosh(etas.at(i)) < self.minEt: continue
            self.value.append(i)
#___________________________________________________________
class IndicesEf(supy.wrappedChain.calculable) :
    def __init__(self, collection = ("trig_EF_jet_emscale_", ""), minEt = None):
        self.minEt = minEt
        self.fixes = collection
        self.stash(["E", "pt", "m", "eta", "phi", ])
        self.moreName = ""
        if minEt!=None: self.moreName += "et>%.1f"%minEt
    @property
    def name(self):
        return 'IndicesEfJets'
    def update(self, _) :
        energies = self.source[self.E]
        etas = self.source[self.eta]
        self.value = []
        for i in range(energies.size()):
            if self.minEt and energies.at(i)/cosh(etas.at(i)) < self.minEt: continue
            self.value.append(i)
#___________________________________________________________
class IndicesOffline(supy.wrappedChain.calculable) :
    def __init__(self, collection = ("jet_AntiKt4TopoEM_", ""), minEt = None):
        self.minEt = minEt
        self.fixes = collection
        self.stash(["n", "E", "pt", "m", "eta", "phi",
                    "isUgly", "isBadLoose"])
        self.moreName = ""
        if minEt!=None: self.moreName += "et>%.1f"%minEt
    @property
    def name(self):
        return 'IndicesOfflineJets'
    def update(self, _) :
        energies = self.source[self.E]
        etas = self.source[self.eta]
        self.value = []
        for i in range(self.source[self.n]):
            if self.minEt and energies.at(i)/cosh(etas.at(i)) < self.minEt: continue
            self.value.append(i)
#___________________________________________________________
class IndicesOfflineBad(supy.wrappedChain.calculable) :
    def __init__(self, collection = ("jet_AntiKt4TopoEMJets_","")) :
        self.fixes = collection
        self.stash(["isBadLoose"])
    def update(self, _) :
        self.value = []
        badLoose = self.source[self.isBadLoose]
        for i in range(badLoose.size()) :
            if badLoose.at(i)==1: self.value.append(i)
    @property
    def name(self):
        return "IndicesOfflineBadJets"

