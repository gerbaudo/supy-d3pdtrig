import supy
from math import cosh
from T2L1_RoIParser import inputOutputJetCounter

GeV = 1000.

def l1jetAttributes() :
    return ["n", "eta", "phi", "et4x4", "et6x6", "et8x8", ]
def l1jetCollection() :
    return (("trig_L1_jet_", ""))
def l2jetAttributes() :
    return ["n", "E", "eta", "phi", "RoIWord", "ehad0", "eem0",
            "nLeadingCells", "hecf", "jetQuality", "emf", "jetTimeCells",
            "RoiWord"]
def l2jetCollection() :
    return ("trig_L2_jet_", "")
def efJetAttributes() :
    return ["E", "pt", "m", "eta", "phi", "calibtags",]
def efJetCollection() :
    return ("trig_EF_jet_emscale_", "")
def offlineJetAttributes() :
    return ["n", "E", "pt", "m", "eta", "phi",
            "isUgly", "isBadLoose"]
def offlineJetCollection() :
    return ("jet_AntiKt4TopoEMJets_", "")
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
                 hecf=0., jetQuality=0., emf=0., jetTimeCells=0., roiWord=0):
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
        self.roiWord = roiWord
    def et(self) :
        return self.E/cosh(self.eta)
    def inputOutputJetCounter(self) :
        return inputOutputJetCounter(self.roiWord)

        
class L2Jets(supy.wrappedChain.calculable) :
    def __init__(self, collection = l2jetCollection()):
        self.fixes = collection
        self.stash(l2jetAttributes())
    @property
    def name(self):
        return 'L2Jets'
    def update(self, _) :
        self.value = [L2Jet(E=E, eta=eta, phi=phi, ehad0=ehad0, eem0=eem0,
                            # nLeadingCells,
                            #hecf,
                            #jetQuality=jetQuality,
                            #emf=emf,
                            #jetTimeCells,
                            roiWord=roiWord)
                      for E, eta, phi, ehad0, eem0, roiWord in
                      zip(self.source[self.E], self.source[self.eta],
                          self.source[self.phi], self.source[self.ehad0],
                          self.source[self.eem0],
                          #self.source[self.jetQuality],
                          #self.source[self.nLeadingCells],
                          #self.source[self.hecf], self.source[self.jetTimeCells],
                          #self.source[self.emf],
                          self.source[self.RoIWord])]

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
    def __init__(self, E=0., pt=0., m=0., eta=0., phi=0., calibtag='') :
        self.E = E
        self.pt = pt
        self.m = m
        self.eta = eta
        self.phi = phi
        self.calibtag = calibtag
    def et(self) :
        return self.E/cosh(self.eta)
        
class EfJets(supy.wrappedChain.calculable) :
    def __init__(self, collection = efJetCollection(), minimumEt=10.*GeV):
        self.fixes = collection
        self.stash(efJetAttributes())
        self.minimumEt = minimumEt
    @property
    def name(self):
        return 'EfJets'
    def update(self, _) :
        self.value = [EfJet(E, pt, m, eta, phi)
                      for E, pt, m, eta, phi in
                      zip(self.source[self.E], self.source[self.pt],
                          self.source[self.m],
                          self.source[self.eta], self.source[self.phi],)
                      if E/cosh(eta)>self.minimumEt]
    def et(self) :
        return self.E/cosh(self.eta)

#___________________________________________________________
class IndicesOffline(supy.wrappedChain.calculable) :
    def __init__(self, collection = offlineJetCollection(), minEt = None):
        self.minEt = minEt
        self.fixes = collection
        self.stash(offlineJetAttributes())
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
    def __init__(self, collection = offlineJetCollection()) :
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
#___________________________________________________________
class OfflineJet(object) :
    def __init__(self, E=0., pt=0., m=0., eta=0., phi=0., isUgly=0., isBadLoose=0.) :
        self.E = E
        self.pt = pt
        self.m = m
        self.eta = eta
        self.phi = phi
        self.isUgly = isUgly
        self.isBadLoose = isBadLoose
    def et(self) :
        return self.E/cosh(self.eta)
#___________________________________________________________
class OfflineJets(supy.wrappedChain.calculable) :
    def __init__(self, collection = offlineJetCollection(), minimumEt=10.*GeV):
        self.fixes = collection
        self.stash(offlineJetAttributes())
        self.minimumEt = minimumEt
    @property
    def name(self):
        return 'OfflineJets'
    def update(self, _) :
        self.value = [OfflineJet(E, pt, m, eta, phi, isUgly, isBadLoose)
                      for E, pt, m, eta, phi, isUgly, isBadLoose in
                      zip(self.source[self.E], self.source[self.pt],
                          self.source[self.m],
                          self.source[self.eta], self.source[self.phi],
                          self.source[self.isUgly], self.source[self.isBadLoose])
                      if E/cosh(eta)>self.minimumEt]
    def et(self) :
        return self.E/cosh(self.eta)

