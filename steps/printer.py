from supy import utils,analysisStep

class l2JetPrinter(analysisStep) :
    def __init__(self, collection='') :
        self.collection = collection
        self.leavesToPrint=['E',
                            'eta',
                            'phi',
                            'RoIWord',
                            'InputType',
                            'OutputType',
                            ]
        
    def uponAcceptance (self,eventVars) :
        jets = eventVars[self.collection]
        print self.collection
        for i,j in enumerate(jets) :
            print "[%d] "%i \
                  + " ".join(["%s : %s"%(a, getattr(j,a)) for a in self.leavesToPrint])
