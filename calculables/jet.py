import supy
from math import cosh

GeV = 1000.

def l1jetAttributes() :
    return ["n", "eta", "phi", "et4x4", "et6x6", "et8x8", ]
def l1jetCollection() :
    return (("trig_L1_jet_", ""))
def l2jetAttributes() :
    return ["n", "E", "eta", "phi", "RoIWord", "ehad0", "eem0",
            "nLeadingCells", "hecf", "jetQuality", "emf", "jetTimeCells",]
def l2jetCollection() :
    return ("trig_L2_jet_", "")

def efJetAttributes() :
    return ["E", "pt", "m", "eta", "phi", ]
def efJetCollection() :
    return ("trig_EF_jet_emscale_", "")
#___________________________________________________________
class IndicesL1(supy.wrappedChain.calculable) :
    "Build L1 jet indices; filter objects as needed"
    def __init__(self, collection = l1jetCollection()):
        self.fixes = collection
        self.stash(l1jetAttributes())
    @property
    def name(self):
        return 'IndicesL1Jets'
    def update(self, _) :
        self.value = range(self.source[self.n])
        # example filter:
        #self.value = [j for j in range(self.source[self.n]) if self.source[self.eta] > etamin]
class L1Jet(object) :
    def __init__(self, eta=0., phi=0., et4x4=0., et6x6=0., et8x8=0.):
        self.eta = eta
        self.phi = phi
        self.et4x4 = et4x4
        self.et6x6 = et6x6
        self.et8x8 = et8x8

class L1Jets(supy.wrappedChain.calculable) :
    def __init__(self, collection = l1jetCollection()):
        self.fixes = collection
        self.stash(l1jetAttributes())
    @property
    def name(self):
        return 'L1Jets'
    def update(self, _) :
        self.value = [L1Jet(eta, phi, et4x4, et6x6, et8x8)
                      for eta, phi, et4x4, et6x6, et8x8 in
                      zip(self.source[self.eta], self.source[self.phi],
                          self.source[self.et4x4], self.source[self.et6x6], self.source[self.et8x8])]
#___________________________________________________________
# todo: subdivide the L2 jets in categories (cone, L1.5, L2PS)
class IndicesL2(supy.wrappedChain.calculable) :
    def __init__(self, collection = l2jetCollection(), minEt = None):
        self.minEt = minEt
        self.fixes = collection
        self.stash(l2jetAttributes())
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
class L2Jet(object) :
    def __init__(self, E=0., eta=0., phi=0., ehad0=0., eem0=0., nLeadingCells=0.,
                 hecf=0., jetQuality=0., emf=0., jetTimeCells=0.):
        self.E = E
        self.eta = eta
        self.phi = phi
        self.ehad0 = ehad0
        self.eem0 = eem0
        self.nLeadingCells = nLeadingCells
        self.hecf = hecf
        self.jetQuality = jetQuality
        self.emf = emf
        self.jetTimeCells = jetTimeCells
        
class L2Jets(supy.wrappedChain.calculable) :
    def __init__(self, collection = l2jetCollection()):
        self.fixes = collection
        self.stash(l2jetAttributes())
    @property
    def name(self):
        return 'L2Jets'
    def update(self, _) :
        self.value = [L2Jet(E, eta, phi, ehad0, eem0, nLeadingCells,
                            hecf, jetQuality, emf, jetTimeCells)
                      for E, eta, phi, ehad0, eem0, nLeadingCells,\
                      hecf, jetTimeCells, emf, jetTimeCells in
                      zip(self.source[self.E], self.source[self.eta],
                          self.source[self.phi], self.source[self.ehad0],
                          self.source[eem0], self.source[nLeadingCells],
                          self.source[self.hecf], self.source[self.jetTimeCells],
                          self.source[self.emf], self.source[self.jetTimeCells])]

#___________________________________________________________
class IndicesEf(supy.wrappedChain.calculable) :
    def __init__(self, collection = efJetCollection(), minEt = None):
        self.minEt = minEt
        self.fixes = collection
        self.stash(efJetAttributes())
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

class EfJet(object) :
    def __init__(self, E=0., pt=0., m=0., eta=0., phi=0.) :
        self.E = E
        self.pt = pt
        self.m = m
        self.eta = eta
        self.phi = phi
        
class EfJets(supy.wrappedChain.calculable) :
    def __init__(self, collection = efJetCollection(), minimumPt=10.*GeV):
        self.fixes = collection
        self.stash(efJetAttributes())
        self.minimumPt = minimumPt
    @property
    def name(self):
        return 'EfJets'
    def update(self, _) :
        self.value = [EfJet(E, pt, m, eta, phi)
                      for E, pt, m, eta, phi in
                      zip(self.source[self.E], self.source[self.pt],
                          self.source[self.m],
                          self.source[self.eta], self.source[self.phi],)
                      if pt>self.minimumPt]

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

