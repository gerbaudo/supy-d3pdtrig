
import supy
import calculables,steps,samples, ROOT as r
import re

GeV=1.0e+3
TeV=1.0e+3*GeV

nJet = 6 # 6,7,8
nThJet = '%dth'%(nJet)
plateauThresholds = {6:70.0*GeV, 7:55.0*GeV, 8:50.0*GeV}
plateauThreshold = plateauThresholds[nJet]

class debugL2PsInefficiency(supy.analysis) :
    def otherTreesToKeepWhenSkimming(self) : return []
    def parameters(self) :
        return {'minJetEt' : 30.0*GeV,
                'maxJetEta' : 3.2,
                'minNofflineJets' : 5,
                'grlFile' : "data/data12_8TeV.periodAllYear_DetStatus-v51-pro13-04_CoolRunQuery-00-04-08_All_Good.xml",
                'L2jetChain' : 'L2_[0-9]*j.*',
                'L2multiJetChain' : 'L2_[4-9]+j.*(em|had)$',
                'refTrigger' : "EF_4j55_a4tchad_L2FS", # Matthew used a 4j ref trig (prescaled?)(do not understand why not 5j)
                'refJetColl' : 'OfflineJets',
                'skim' : 'L1_4J15',
                }

    def listOfSteps(self,config) :
        pars = self.parameters()
        refTrigger = pars['refTrigger']
        refJetColl = pars['refJetColl']
        outList=[
            supy.steps.printer.progressPrinter(),
            supy.steps.filters.multiplicity("IndicesOfflineBadJets",max=0),
            supy.steps.filters.multiplicity("vxp_Indices",min=1),
            supy.steps.filters.multiplicity(refJetColl, min=1),
            steps.filters.goodRun().onlyData(),
            #steps.filters.triggers([refTrigger]),
            #supy.steps.printer.printstuff(['PassedTriggers',]),
            #supy.steps.printer.printstuff(['EmulatedL1_6j10','EmulatedL2FS_6j10']),
            steps.filters.triggers(['EmulatedOffline_4j90']), # make sure we are on the 4j55 plateau
            steps.filters.triggers(['EmulatedOffline_%dj%d'%(nJet,plateauThreshold/GeV)]), # make sure we are on the njXX plateau
            ]
        if nThJet=='6th' :
            outList+=[#steps.filters.triggers(['EF_6j55_a4tchad_L2FS_5L2j15']),
                      #steps.filters.triggers(['EF_6j55_a4tchad_L2FSPS']).invert(),
                      #supy.steps.printer.printstuff(['EF_6j55_a4tchad_L2FS_5L2j15','EF_6j55_a4tchad_L2FSPS','L2_5j15_a4TTem']),
                      steps.filters.triggers(['EF_6j50_a4tchad_L2FS_5L2j15']),
                      steps.filters.triggers(['EF_6j50_a4tchad_L2FSPS_5L2j15']).invert(),
                      #supy.steps.printer.printstuff(['EF_6j50_a4tchad_L2FS_5L2j15','EF_6j50_a4tchad_L2FSPS_5L2j15','L2_5j15_a4TTem']),
                      #supy.steps.printer.printstuff(['EmulatedL2FS_5j15','EmulatedL2FS_6j15','EmulatedL2PS_6j50']),
                      ]
        elif nThJet=='7th' :
            outList+=[steps.filters.triggers(['EF_7j40_a4tchad_L2FS_5L2j15']),
                      steps.filters.triggers(['EF_7j40_a4tchad_L2FSPS_5L2j15']).invert(),
                      supy.steps.printer.printstuff(['EF_7j40_a4tchad_L2FS_5L2j15','EF_7j40_a4tchad_L2FSPS_5L2j15','L2_5j15_a4TTem']),]
        elif nThJet=='8th' :
            outList+=[steps.filters.triggers(['EF_8j35_a4tchad_L2FS_5L2j15']),
                      steps.filters.triggers(['EF_8j35_a4tchad_L2FSPS_5L2j15']).invert(),
                      supy.steps.printer.printstuff(['EF_8j35_a4tchad_L2FS_5L2j15','EF_8j35_a4tchad_L2FSPS_5L2j15','L2_5j15_a4TTem']),]


        outList+=[
            #supy.steps.printer.printstuff(['RunNumber','EventNumber']),
            #supy.steps.printer.printstuff(['EmulatedL2FS_%dj%d'%(m,t) for m,t in [(6,50),(7,75),(8,30)]]),
            supy.steps.histos.multiplicity(var='L2JetsA4TTA4CC_JES'),
            supy.steps.histos.multiplicity(var='EfJetsAntiKt4_topo_calib_EMJES'),
            supy.steps.histos.multiplicity(var='UnmatchedJets', max=nJet),
            steps.histos.etaPhiMap(coll='UnmatchedJets', title="EF jets without L2PS match (%dj)"%nJet),
            ]
        return outList

    def listOfCalculables(self,config) :
        pars = self.parameters()
        minEt = pars['minJetEt']
        maxEta = pars['maxJetEta']
        listOfCalculables = supy.calculables.zeroArgs(supy.calculables)
        listOfCalculables += supy.calculables.zeroArgs(calculables)
        listOfCalculables += [calculables.TrigD3PD.Grlt(pars['grlFile']),
                              calculables.TrigD3PD.isGoodRun(runN='RunNumber',lbn='lbn'),
                              calculables.TrigD3PD.Tdt(treeName = "TrigConfTree", dirName = "susyMeta"),]
        tb = calculables.TrigD3PD.TriggerBit
        listOfCalculables += [tb("EF_4j55_a4tchad_L2FS"),
                              tb("EF_5j55_a4tchad_L2FS"),
                              tb("EF_5j55_a4tchad_L2FSPS"),
                              tb("EF_6j55_a4tchad_L2FS_5L2j15"),
                              tb("EF_6j55_a4tchad_L2FSPS"),
                              tb("EF_7j40_a4tchad_L2FS_5L2j15"),
                              tb("EF_7j40_a4tchad_L2FSPS_5L2j15"),
                              tb("EF_8j35_a4tchad_L2FS_5L2j15"),
                              tb("EF_8j35_a4tchad_L2FSPS_5L2j15"),
                              tb("L2_5j15_a4TTem"),
                              ]
        listOfCalculables += [calculables.TrigD3PD.PassedTriggers(),
                              # To be checked: not clear whether this has an effect on triggerCounts
                              #calculables.TrigD3PD.PassedTriggers([r'L1_[0-9]J.*'
                              #                                     ,r'.*PS.*'
                              #                                     ,r'L2.*a4TT.*'
                              #                                     ,r'L2.*a4cc.*'
                              #                                     ,r'EF.*L2FS.*'
                              #                                     ,r'EF.*L2PS.*'
                              #                                     ]),
                              ]
        listOfCalculables += [calculables.vertex.Indices(collection=('vxp_',''),
                                                         zPosMax=100, nTracksMin=4),]
        listOfCalculables += [calculables.jet.IndicesL2(maxEta=maxEta, input='NONE', output='A4TT'), # A4TT EM
                              calculables.jet.IndicesL2(minEt=plateauThreshold, maxEta=maxEta, input='A4TT', output='A4CC_JES'), # A4CC HAD JES
                              calculables.jet.L2Jets(indices="IndicesL2JetsNONEA4TT"),
                              calculables.jet.L2Jets(indices="IndicesL2JetsA4TTA4CC_JES"),
                              calculables.jet.IndicesEf(minEt=plateauThreshold, maxEta=maxEta, calibTag='AntiKt4_topo_calib_EMJES'),
                              calculables.jet.EfJets(indices='IndicesEfJetsAntiKt4_topo_calib_EMJES'),
                              calculables.jet.MatchedJets(coll1='EfJetsAntiKt4_topo_calib_EMJES',
                                                          otherColls=['L2JetsA4TTA4CC_JES']),
                              calculables.jet.UnmatchedJets(coll='EfJetsAntiKt4_topo_calib_EMJES'
                                                            +'Match'
                                                            +'L2JetsA4TTA4CC_JES'),
                              ]
        listOfCalculables += [calculables.jet.IndicesOffline(minEt=minEt, maxEta=maxEta),
                              calculables.jet.OfflineJets(),
                              calculables.jet.IndicesOfflineBad(),
                              ]
        emjb = calculables.TrigD3PD.EmulatedMultijetTriggerBit
        listOfCalculables += [
            emjb(jetColl='L1Jets', label='L1', multi=5, minEt=10.*GeV),
            emjb(jetColl='L1Jets', label='L1', multi=6, minEt=10.*GeV),
            emjb(jetColl='L2JetsNONEA4TT', label='L2FS', multi=4, minEt=15.*GeV),
            emjb(jetColl='L2JetsNONEA4TT', label='L2FS', multi=5, minEt=15.*GeV),
            emjb(jetColl='L2JetsNONEA4TT', label='L2FS', multi=6, minEt=15.*GeV),
            emjb(jetColl='L2JetsA4TTA4CC_JES', label='L2PS', multi=6, minEt=50.*GeV),
            emjb(jetColl='L2JetsA4TTA4CC_JES', label='L2PS', multi=6, minEt=55.*GeV),
            emjb(jetColl='OfflineJets', label='Offline', multi=4, minEt=90.*GeV),
            emjb(jetColl='OfflineJets', label='Offline', multi=5, minEt=80.*GeV),
            ]
        tba = calculables.TrigD3PD.TriggerBitAnd
        listOfCalculables += [
            tba(bit1='EmulatedL2PS_5j75', bit2='EF_5j55_a4tchad_L2FSPS', label='EF_5j55_L2FSPS_L2PS_5j75'),
            ]
        listOfCalculables += [emjb(jetColl='OfflineJets', label='Offline', multi=m, minEt=t)
                              for m,t in plateauThresholds.iteritems()]
        listOfCalculables += [emjb(jetColl='L2JetsA4TTA4CC_JES', label='L2FS', multi=m, minEt=t*GeV)
                              for m,t in [(6,50),(7,75),(8,30)]]
        return listOfCalculables

    def listOfSampleDictionaries(self) :
        skim = self.parameters()['skim']
        return [samples.skimmedPeriodD(skim=skim)]

    def listOfSamples(self,config) :
        test = False
        nEventsMax= 1000000 if test else -1
        nFilesMax=100 if test else -1
        skim = self.parameters()['skim']
        return ([] + supy.samples.specify(names="periodD.%s"%skim, nEventsMax=nEventsMax, nFilesMax=nFilesMax))

    def conclude(self,pars) :
        #make a pdf file with plots from the histograms created above
        org = self.organizer(pars)
        supy.plotter( org,
                      pdfFileName = self.pdfFileName(org.tag),
                      doLog = False,
                      blackList = ['num_.*', 'den_.*'],
                      ).plotAll()