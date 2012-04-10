from math import fabs
from supy import wrappedChain

#for compatibility with old ntuples
class vxp_z(wrappedChain.calculable) :
    def update(self,_) :
        self.value = self.source["vx_z"]
class vxp_n(wrappedChain.calculable) :
    def update(self,_) :
        self.value = self.source["vx_n"]
class vxp_nTracks(wrappedChain.calculable) :
    def update(self,_) :
        self.value = self.source["vx_nTracks"]

#_________________________________________________
class Indices(wrappedChain.calculable) :
    def __init__(self, collection = None, zPosMax = None, nTracksMin = None) :
        self.fixes = collection
        self.stash(['n', 'z', 'nTracks'])
        self.zPosMax = zPosMax
        self.nTracksMin = nTracksMin
        self.moreName = ""
        if zPosMax!=None :
            self.moreName += "abs(z) <=%.1f"%zPosMax
        if nTracksMin!=None:
            self.moreName += "; nTracks >=%d"%nTracksMin
    def update(self,ignored) :
        z = self.source[self.z]
        nTracks = self.source[self.nTracks]
        self.value = []
        for i in range(int(self.source[self.n])) :
            if fabs(z.at(i))>self.zPosMax : continue
            if nTracks.at(i)<self.nTracksMin : continue
            self.value.append(i)
#_________________________________________________
