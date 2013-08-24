
from supy.samples import SampleHolder

baseDir = '/afs/cern.ch/work/m/marcoag/public/'
prefix = 'data12_8TeV.00200967.physics_JetTauEtmiss.merge.NTUP_TRIG.'
fnamesList=('['
            +'"'+baseDir+'/'+prefix+'f434_m1114._0030.1",'
            +'"'+baseDir+'/'+prefix+'f434_m1114._0031.1",'
            +'"'+baseDir+'/'+prefix+'f434_m1114._0032.1",'
            +'"'+baseDir+'/'+prefix+'f434_m1114._0033.1",'
            +'"'+baseDir+'/'+prefix+'f434_m1114._0034.1",'
            +'"'+baseDir+'/'+prefix+'f434_m1114._0035.1",'
            +'"'+baseDir+'/'+prefix+'f434_m1114._0036.1",'
            +'"'+baseDir+'/'+prefix+'f434_m1114._0037.1",'
            +'"'+baseDir+'/'+prefix+'f434_m1114._0038.1",'
            +'"'+baseDir+'/'+prefix+'f434_m1114._0039.1",'
            +']')
def getMarcoSamples(skim='', run=None) :
    marcoSamples = SampleHolder()
    marcoSamples.add('marcoSamples', fnamesList, lumi = 100.0)
    return marcoSamples
