from supy import analysisStep

class triggers(analysisStep) :
    def select(self,ev) : return len(filter(lambda t: ev[t] == True, self.triggers))
    def __init__(self, triggers = []) :
        self.triggers = triggers
        self.moreName = '_'.join([t for t in self.triggers])
class goodRun(analysisStep) :
    def select(self,ev) :
        return ev[self.var]
    def __init__(self, var='isGoodRun') :
        self.var = var
