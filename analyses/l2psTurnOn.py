
import supy
import calculables,steps,samples, ROOT as r
import re

GeV=1.0e+3
TeV=1.0e+3*GeV

class l2psTurnOn(supy.analysis) :
    def otherTreesToKeepWhenSkimming(self) : return []
    def parameters(self) :
        efJetCalibTag='AntiKt4_topo_calib_EMJES'
        return {'minJetEt' : 30.0*GeV,
                'maxJetEta' : 3.2,
                'minNofflineJets' : 5,
                'grlFile' : "data/data12_8TeV.periodAllYear_DetStatus-v51-pro13-04_CoolRunQuery-00-04-08_All_Good.xml",
                'L2jetChain' : 'L2_[0-9]*j.*',
                'L2multiJetChain' : 'L2_[4-9]+j.*(em|had)$',
                'refTrigger' : 'EF_4j80_a4tchad_L2FS',
                'skim' : 'L1_4J15',
                'offJetColl' : 'OfflineJets',
                'efJetCalibTag' : efJetCalibTag,
                'efJetColl' : "EfJets%s"%efJetCalibTag,
                'l2psJetColl' : 'L2JetsA4TTA4CC_JES',
                'l15JetColl' : 'L2JetsNONEA4TT',
                'l2coneJetColl': 'L2JetsA4TTL2CONE',
                }


    def listOfSteps(self,config) :
        pars = self.parameters()
        refTrigger = pars['refTrigger']
        offJetColl = pars['offJetColl']
        refJetColl = offJetColl
        outList=[
            supy.steps.printer.progressPrinter(),
            supy.steps.filters.multiplicity("IndicesOfflineBadJets",max=0),
            supy.steps.filters.multiplicity("vxp_Indices",min=1),
            supy.steps.filters.multiplicity(refJetColl, min=1),
            steps.filters.goodRun().onlyData(),
            steps.filters.triggers([refTrigger]),
            #supy.steps.printer.printstuff(['PassedTriggers',]),
            #supy.steps.printer.printstuff(['EmulatedL1_6j10','EmulatedL2FS_6j10']),
            steps.filters.triggers(['EmulatedOffline_4j90']), # make sure we are on the 4j55 plateau
            supy.steps.filters.label('5jets'),
            steps.histos.attribute(attrName='et', coll=refJetColl, nTh=4, title="E_{T} %dth jet "%(4+1)+"("+refJetColl+"); E_{T}; events",xLo=0.0,xUp=200.0*GeV),
            steps.histos.turnOnJet(trigger='L2_5j15_a4TTem', jetColl=refJetColl, nTh=4),
            steps.histos.turnOnJet(trigger='L2_5j15_a4TTem_5j50_a4cchad', jetColl=refJetColl, nTh=4),
            steps.histos.turnOnJet(trigger='L2_5j15_a4TTem_5j55_a4cchad', jetColl=refJetColl, nTh=4),
            steps.histos.turnOnJet(trigger='EF_5j55_a4tchad_L2FS', jetColl=refJetColl, nTh=4),
            steps.histos.turnOnJet(trigger='EF_5j55_a4tchad_L2FSPS', jetColl=refJetColl, nTh=4),
            steps.histos.turnOnJet(trigger='EF_5j60_a4tchad_L2FS', jetColl=refJetColl, nTh=4),
            steps.histos.turnOnJet(trigger='EF_5j60_a4tchad_L2FSPS', jetColl=refJetColl, nTh=4),
            #steps.histos.turnOnJet(trigger='EF_5j60_a4tchad_L2FS', jetColl=refJetColl, nTh=4),
            steps.histos.turnOnJet(trigger='EF_5j60_a4tclcw_L2FS', jetColl=refJetColl, nTh=4),
            steps.histos.turnOnJet(trigger='EmulatedL1_5j10', jetColl=refJetColl, emulated=True, nTh=4),
            steps.histos.turnOnJet(trigger='EmulatedL1_6j10', jetColl=refJetColl, emulated=True, nTh=5),
            steps.histos.turnOnJet(trigger='EmulatedL1_6j15', jetColl=refJetColl, emulated=True, nTh=5),
            # - 5th jet : 5j15L2FS vs. 4j15L2FS + 5j50L2FSPS
            steps.histos.turnOnJet(trigger='EmulatedL2FS_5j15', jetColl=refJetColl, emulated=True, nTh=4),
            steps.histos.turnOnJet(trigger='EmulatedL2FS_4j15_L2PS_5j50', jetColl=refJetColl, emulated=True, nTh=4),
            supy.steps.filters.label('6jets'),
            steps.histos.attribute(attrName='et', coll=refJetColl, nTh=5, title="E_{T} %dth jet "%(5+1)+"("+refJetColl+"); E_{T}; events",xLo=0.0,xUp=200.0*GeV),
            steps.histos.turnOnJet(trigger='L2_5j15_a4TTem', jetColl=refJetColl, nTh=5),
            # - 6th jet : 6j15L2FS vs. 4j15L2FS + 6j50L2FSPS
            # - 6th jet : 6j15L2FS vs. 5j15L2FS + 6j50L2FSPS
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EmulatedL2FS_6j10', emulated=True, nTh=5),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EmulatedL2FS_6j15', emulated=True, nTh=5),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EmulatedL2FS_4j15_L2PS_6j50', emulated=True, nTh=5),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EmulatedL2FS_5j15_L2PS_6j50', emulated=True, nTh=5),
            steps.histos.turnOnJet(trigger='L2_5j15_a4TTem_6j45_a4cchad', jetColl=refJetColl, nTh=5),
            steps.histos.turnOnJet(trigger='L2_6j15_a4TTem_6j50_a4cchad', jetColl=refJetColl, nTh=5),
            steps.histos.turnOnJet(trigger='EF_6j45_a4tchad_L2FS_5L2j15', jetColl=refJetColl, nTh=5),
            steps.histos.turnOnJet(trigger='EF_6j50_a4tchad_L2FS_5L2j15', jetColl=refJetColl, nTh=5),
            steps.histos.turnOnJet(trigger='EF_6j50_a4tchad_L2FSPS_5L2j15', jetColl=refJetColl, nTh=5),
            steps.histos.turnOnJet(trigger='EF_6j55_a4tchad_L2FS_5L2j15', jetColl=refJetColl, nTh=5),
            steps.histos.turnOnJet(trigger='EF_6j55_a4tchad_L2FSPS', jetColl=refJetColl, nTh=5),
            supy.steps.filters.label('7jets'),
            steps.histos.attribute(attrName='et', coll=refJetColl, nTh=6, title="E_{T} %dth jet "%(6+1)+"("+refJetColl+"); E_{T}; events",xLo=0.0,xUp=200.0*GeV),
            steps.histos.turnOnJet(trigger='L2_5j15_a4TTem', jetColl=refJetColl, nTh=6),
            steps.histos.turnOnJet(trigger='L2_5j15_a4TTem_7j35_a4cchad', jetColl=refJetColl, nTh=6),
            steps.histos.turnOnJet(trigger='L2_7j15_a4TTem_7j50_a4cchad', jetColl=refJetColl, nTh=6),
            steps.histos.turnOnJet(trigger='EF_7j40_a4tchad_L2FS_5L2j15', jetColl=refJetColl, nTh=6),
            steps.histos.turnOnJet(trigger='EF_7j40_a4tchad_L2FSPS_5L2j15', jetColl=refJetColl, nTh=6),
            steps.histos.turnOnJet(trigger='EF_7j45_a4tchad_L2FS_5L2j15', jetColl=refJetColl, nTh=6),
            steps.histos.turnOnJet(trigger='EF_7j55_a4tchad_L2FSPS', jetColl=refJetColl, nTh=6),
            supy.steps.filters.label('8jets'),
            steps.histos.attribute(attrName='et', coll=refJetColl, nTh=7, title="E_{T} %dth jet "%(7+1)+"("+refJetColl+"); E_{T}; events",xLo=0.0,xUp=200.0*GeV),
            steps.histos.turnOnJet(trigger='L2_5j15_a4TTem', jetColl=refJetColl, nTh=7),
            steps.histos.turnOnJet(trigger='L2_5j15_a4TTem_8j30_a4cchad', jetColl=refJetColl, nTh=7),
            steps.histos.turnOnJet(trigger='EF_8j35_a4tchad_L2FS_5L2j15', jetColl=refJetColl, nTh=7),
            steps.histos.turnOnJet(trigger='EF_8j35_a4tchad_L2FSPS_5L2j15', jetColl=refJetColl, nTh=7),

            steps.trigger.triggerCounts(triggers=[]
                                        +[
            'L2_5j15_a4TTem','L2_5j15_a4TTem_5j50_a4cchad','L2_5j15_a4TTem_5j55_a4cchad',
            'EF_5j55_a4tchad_L2FSPS','EF_5j55_a4tchad_L2FS','EF_5j55_a4tchad_L2FSPS','EF_5j60_a4tchad_L2FS','EF_5j60_a4tchad_L2FSPS',
            'L2_5j15_a4TTem_6j45_a4cchad','L2_6j15_a4TTem_6j50_a4cchad',
            'EF_6j45_a4tchad_L2FS_5L2j15','EF_6j50_a4tchad_L2FS_5L2j15','EF_6j50_a4tchad_L2FSPS_5L2j15',
            'EF_6j55_a4tchad_L2FS_5L2j15','EF_6j55_a4tchad_L2FSPS',
            'L2_5j15_a4TTem_7j35_a4cchad','L2_7j15_a4TTem_7j50_a4cchad',
            'EF_7j40_a4tchad_L2FS_5L2j15','EF_7j40_a4tchad_L2FSPS_5L2j15','EF_7j45_a4tchad_L2FS_5L2j15','EF_7j55_a4tchad_L2FSPS',
            'L2_5j15_a4TTem_8j30_a4cchad',
            'EF_8j35_a4tchad_L2FS_5L2j15','EF_8j35_a4tchad_L2FSPS_5L2j15',
            ]
                                        ),

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
        listOfCalculables += [calculables.jet.IndicesL1(), calculables.jet.L1Jets(),]
        listOfCalculables += [calculables.jet.IndicesL2(minEt=minEt, maxEta=maxEta, input='A4TT', output='A4CC_JES'), # A4CC HAD JES
                              calculables.jet.L2Jets(indices="IndicesL2JetsA4TTA4CC_JES"),
                              calculables.jet.IndicesL2(input='NONE', output='A4TT'),     # L1.5 EM
                              calculables.jet.L2Jets(indices="IndicesL2JetsNONEA4TT"),
                              calculables.jet.L2JetsCalibL15(collection='L2JetsNONEA4TT'),
                              calculables.jet.IndicesEf(minEt=minEt, maxEta=maxEta, calibTag='AntiKt4_topo_calib_EMJES'),
                              calculables.jet.EfJets(indices='IndicesEfJetsAntiKt4_topo_calib_EMJES'),
                              ]
        listOfCalculables += [calculables.jet.IndicesOffline(minEt=minEt, maxEta=maxEta),
                              calculables.jet.OfflineJets(),
                              calculables.jet.IndicesOfflineBad(),
                              ]
        emjb = calculables.TrigD3PD.EmulatedMultijetTriggerBit
        listOfCalculables += [
            emjb(jetColl='L1Jets', label='L1', multi=5, minEt=10.*GeV),
            emjb(jetColl='L1Jets', label='L1', multi=6, minEt=10.*GeV),
            emjb(jetColl='L1Jets', label='L1', multi=6, minEt=15.*GeV),
            emjb(jetColl='L2JetsNONEA4TT', label='L2FS', multi=4, minEt=15.*GeV),
            emjb(jetColl='L2JetsNONEA4TT', label='L2FS', multi=5, minEt=15.*GeV),
            emjb(jetColl='L2JetsNONEA4TT', label='L2FS', multi=6, minEt=10.*GeV),
            emjb(jetColl='L2JetsNONEA4TT', label='L2FS', multi=6, minEt=15.*GeV),
            emjb(jetColl='L2JetsA4TTA4CC_JES', label='L2PS', multi=5, minEt=50.*GeV),
            emjb(jetColl='L2JetsA4TTA4CC_JES', label='L2PS', multi=6, minEt=50.*GeV),
            emjb(jetColl='OfflineJets', label='Offline', multi=4, minEt=90.*GeV),
            emjb(jetColl='OfflineJets', label='Offline', multi=5, minEt=80.*GeV),
            ]
        tb = calculables.TrigD3PD.TriggerBit
        listOfCalculables += [tb('L2_4j15_a4TTem'), tb('L2_5j15_a4TTem'),
                              ]
        tba = calculables.TrigD3PD.TriggerBitAnd
        listOfCalculables += [
            tba(bit1='EmulatedL2FS_4j15', bit2='EmulatedL2PS_5j50', label='L2FS_4j15_L2PS_5j50'),
            tba(bit1='EmulatedL2FS_4j15', bit2='EmulatedL2PS_6j50', label='L2FS_4j15_L2PS_6j50'),
            tba(bit1='EmulatedL2FS_5j15', bit2='EmulatedL2PS_6j50', label='L2FS_5j15_L2PS_6j50'),
            ]

        return listOfCalculables

    def listOfSampleDictionaries(self) :
        skim = self.parameters()['skim']
        return [samples.skimmedPeriodD(skim=skim, run=208258)]

    def listOfSamples(self,config) :
        test = False #True
        nEventsMax= 100000 if test else None
        nFilesMax=100 if test else None
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
