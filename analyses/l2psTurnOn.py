
import supy
import calculables,steps,samples, ROOT as r
import re

GeV=1.0e+3
TeV=1.0e+3*GeV

class l2psTurnOn(supy.analysis) :
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
            supy.steps.filters.label('5jets'),
            steps.histos.attribute(attrName='et', coll=refJetColl, nTh=4, title="E_{T} %dth jet "%(4+1)+"("+refJetColl+"); E_{T}; events",xLo=0.0,xUp=200.0*GeV),
            steps.histos.turnOnJet(trigger='L2_5j15_a4TTem', jetColl=refJetColl, nTh=4),
            steps.histos.turnOnJet(trigger='L2_5j15_a4TTem_5j50_a4cchad', jetColl=refJetColl, nTh=4),
            steps.histos.turnOnJet(trigger='L2_5j15_a4TTem_5j55_a4cchad', jetColl=refJetColl, nTh=4),
            steps.histos.turnOnJet(trigger='EF_5j55_a4tchad_L2FS', jetColl=refJetColl, nTh=4),
            steps.histos.turnOnJet(trigger='EF_5j55_a4tchad_L2FSPS', jetColl=refJetColl, nTh=4),
            steps.histos.turnOnJet(trigger='EF_5j60_a4tchad_L2FS', jetColl=refJetColl, nTh=4),
            steps.histos.turnOnJet(trigger='EF_5j60_a4tchad_L2FSPS', jetColl=refJetColl, nTh=4),
            supy.steps.filters.label('6jets'),
            steps.histos.attribute(attrName='et', coll=refJetColl, nTh=5, title="E_{T} %dth jet "%(5+1)+"("+refJetColl+"); E_{T}; events",xLo=0.0,xUp=200.0*GeV),            
            steps.histos.turnOnJet(trigger='L2_5j15_a4TTem', jetColl=refJetColl, nTh=5),
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
            emjb(jetColl='L2JetsNONEA4TT', label='L2FS', multi=6, minEt=10.*GeV),
            emjb(jetColl='L2JetsNONEA4TT', label='L2FS', multi=6, minEt=15.*GeV),
            emjb(jetColl='OfflineJets', label='Offline', multi=4, minEt=90.*GeV),
            emjb(jetColl='OfflineJets', label='Offline', multi=5, minEt=80.*GeV),
            ]
        return listOfCalculables

    def listOfSampleDictionaries(self) :
        protocol="root://xrootd-disk.pic.es/"
        basedir="/pnfs-disk/pic.es/at3/projects/TOPD3PD/2011/Skimming/DPD_prod01_02_October11"
        castorBaseDir="/castor/cern.ch/grid/atlas/tzero/prod1/perm/data12_8TeV/express_express"
        castorDefaultOpt ='fileExt="NTUP_TRIG",pruneList=False'

        lumiPerRun = {202668:26.0, 202712:29.85, 202740:7.28, 202798:52.6, # B1
                      202987:14.02, 202991:40.15, 203027:89.29, 203258:119.4, #B2
                      208184:105.2, 208258:92.55, 208261:103.1, 208354:133.2, # D4, D5
                      208485:142.2, 208662:149.0, # D6, D7
                      }
        exampleDict = supy.samples.SampleHolder()
        exampleDict.add("PeriodB_L1_4J15",
                        'utils.fileListFromTextFile('
                        +'fileName="/afs/cern.ch/work/g/gerbaudo/public/trigger/MyRootCoreDir/supy-d3pdtrig/data/periodB.txt"'
                        #+'fileName="/afs/cern.ch/work/g/gerbaudo/public/trigger/MyRootCoreDir/supy-d3pdtrig/data/periodB_test.txt"'
                        +')',
                        lumi= sum(lumiPerRun.keys())
                        )
        exampleDict.add("PeriodD_L1_4J15",
                        'utils.fileListFromTextFile('
                        +'fileName="/afs/cern.ch/work/g/gerbaudo/public/trigger/MyRootCoreDir/supy-d3pdtrig/data/periodD.txt"'
                        +')',
                        lumi= sum(lumiPerRun[r] for r in [208184,208258,208261,208354,208485,208662])
                        )
        exampleDict.add("PeriodD_208354",
                        #'utils.fileListFromDisk('
                        #+'location="/tmp/gerbaudo/dq2/user.tdoherty.SUSYD3PD.208354.skim.L1_4J15.2860.ANALY_RAL/*root*"'
                        #+', isDirectory = False'
                        'utils.fileListFromTextFile('
                        +'fileName="/afs/cern.ch/user/g/gerbaudo/work/public/trigger/MyRootCoreDir/supy-d3pdtrig/data/test.txt"'
                        +')',
                        lumi=lumiPerRun[208184]
                        )

        return [exampleDict]

    def listOfSamples(self,config) :
        nEventsMax=-1 #10000
        return (
            supy.samples.specify(names="PeriodD_L1_4J15", color = r.kBlack, nEventsMax=nEventsMax, nFilesMax=-1)
            #supy.samples.specify(names="PeriodD_208354", color = r.kBlack, nEventsMax=nEventsMax, nFilesMax=-1)
            )

    def conclude(self,pars) :
        #make a pdf file with plots from the histograms created above
        org = self.organizer(pars)
        supy.plotter( org,
                      pdfFileName = self.pdfFileName(org.tag),
                      doLog = False,
                      blackList = ['num_.*', 'den_.*'],
                      ).plotAll()
