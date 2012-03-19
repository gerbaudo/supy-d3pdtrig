import collections, re
import supy
import ROOT as r

class triggerCounts(supy.analysisStep) :
    "histogram the counts for each trigger; based on susycaf.steps.trigger.triggerScan"
    def __init__(self, pattern = r'.*', passedTriggers = 'PassedTriggers') :
        self.pattern = pattern
        self.passedTriggers = passedTriggers
        self.moreName = self.pattern
        self.counts = collections.defaultdict(int)
        self.triggerNames = collections.defaultdict(set)
    def varsToPickle(self) :
        return ['counts','triggerNames']
    def uponAcceptance(self, eventVars) :
        for key in eventVars[self.passedTriggers]:
            if not re.match(self.pattern,key): continue
            self.counts[key] += 1
    def mergeFunc(self, products) :
        def update(a,b) : a.update(b); return a;
        self.counts = reduce(update, products["counts"], dict())
        names = sorted(self.counts.keys())
        hist = r.TH1D('triggerCounts',
                      "Trigger counts;;events",
                      len(names), 0, len(names))
        for i,name in enumerate(names) :
            hist.GetXaxis().SetBinLabel(i+1,name)
            hist.SetBinContent(i+1, self.counts[name])
        hist.Write()
            
            
         
