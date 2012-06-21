#!/usr/bin/env python

import supy
import calculables,steps,samples, ROOT as r
import re

GeV=1.0e+3
TeV=1.0e+3*GeV

class jetMichaelTests(supy.analysis) :
    def otherTreesToKeepWhenSkimming(self) : return []
    def parameters(self) :
        return {'minJetEt' : 30.0*GeV,
                'maxJetEta' : 3.2,
                'minNofflineJets' : 5,
                'grlFile' : "data/data12_8TeV.periodAllYear_DetStatus-v45-pro13_CoolRunQuery-00-04-08_SMjets.xml",
                'L2jetChain' : 'L2_[0-9]*j.*',
                'L2multiJetChain' : 'L2_[4-9]+j.*(em|had)$',
                'refTrigger' : "EF_5j55_a4tchad_L2FS",
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
            steps.filters.goodRun().onlyData(),
            steps.filters.triggers([refTrigger]),
            steps.histos.attribute(attrName='et', coll=refJetColl, nTh=4, title="E_{T} %dth jet "%(4+1)+"("+refJetColl+"); E_{T}; events",xLo=0.0,xUp=200.0*GeV),
            steps.histos.attribute(attrName='et', coll=refJetColl, nTh=5, title="E_{T} %dth jet "%(5+1)+"("+refJetColl+"); E_{T}; events",xLo=0.0,xUp=200.0*GeV),
            steps.histos.turnOnJet(trigger='EF_5j55_a4tchad_L2FSPS', jetColl=refJetColl, nTh=4),
            steps.histos.turnOnJet(trigger='EF_5j55_a4tchad_L2FSPS', jetColl=refJetColl, nTh=5),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EmulatedL2PS_5j75', emulated=True, nTh=4),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EmulatedEF_5j50_L2PS_5j75', emulated=True, nTh=4),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EmulatedEF_5j55_L2PS_5j75', emulated=True, nTh=4),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EmulatedEF_5j60_L2PS_5j75', emulated=True, nTh=4),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EmulatedEF_5j65_L2PS_5j75', emulated=True, nTh=4),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EmulatedEF_5j70_L2PS_5j75', emulated=True, nTh=4),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EmulatedEF_5j75_L2PS_5j75', emulated=True, nTh=4),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EmulatedEF_5j80_L2PS_5j75', emulated=True, nTh=4),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EmulatedEF_5j85_L2PS_5j75', emulated=True, nTh=4),
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
        listOfCalculables += [tb("EF_5j55_a4tchad_L2FS"),
                              tb("EF_5j55_a4tchad_L2FSPS"),
                              ]
        listOfCalculables += [calculables.TrigD3PD.PassedTriggers(),
                              #calculables.TrigD3PD.PassedTriggers(r'.*PS.*'),
                              ]
        listOfCalculables += [calculables.vertex.Indices(collection=('vxp_',''),
                                                         zPosMax=100, nTracksMin=4),]
        listOfCalculables += [calculables.jet.IndicesL2(minEt=minEt, maxEta=maxEta, input='A4TT', output='A4CC_JES'), # A4CC HAD JES
                              calculables.jet.L2Jets(indices="IndicesL2JetsA4TTA4CC_JES"),
                              calculables.jet.IndicesEf(minEt=minEt, maxEta=maxEta, calibTag='AntiKt4_topo_calib_EMJES'),
                              calculables.jet.EfJets(indices='IndicesEfJetsAntiKt4_topo_calib_EMJES'),
                              ]
        listOfCalculables += [calculables.jet.IndicesOffline(minEt=minEt, maxEta=maxEta),
                              calculables.jet.OfflineJets(),
                              calculables.jet.IndicesOfflineBad(),
                              ]
        emjb = calculables.TrigD3PD.EmulatedMultijetTriggerBit
        listOfCalculables += [
            emjb(jetColl='L2JetsA4TTA4CC_JES', label='L2PS', multi=5, minEt=75.*GeV),
            emjb(jetColl='EfJetsAntiKt4_topo_calib_EMJES', label='EF', multi=5, minEt=50.*GeV),
            emjb(jetColl='EfJetsAntiKt4_topo_calib_EMJES', label='EF', multi=5, minEt=55.*GeV),
            emjb(jetColl='EfJetsAntiKt4_topo_calib_EMJES', label='EF', multi=5, minEt=60.*GeV),
            emjb(jetColl='EfJetsAntiKt4_topo_calib_EMJES', label='EF', multi=5, minEt=65.*GeV),
            emjb(jetColl='EfJetsAntiKt4_topo_calib_EMJES', label='EF', multi=5, minEt=70.*GeV),
            emjb(jetColl='EfJetsAntiKt4_topo_calib_EMJES', label='EF', multi=5, minEt=75.*GeV),
            emjb(jetColl='EfJetsAntiKt4_topo_calib_EMJES', label='EF', multi=5, minEt=80.*GeV),
            emjb(jetColl='EfJetsAntiKt4_topo_calib_EMJES', label='EF', multi=5, minEt=85.*GeV),
            ]
        tba = calculables.TrigD3PD.TriggerBitAnd
        listOfCalculables += [
            tba(bit1='EmulatedL2PS_5j75', bit2='EmulatedEF_5j50', label='EF_5j50_L2PS_5j75'),
            tba(bit1='EmulatedL2PS_5j75', bit2='EmulatedEF_5j55', label='EF_5j55_L2PS_5j75'),
            tba(bit1='EmulatedL2PS_5j75', bit2='EmulatedEF_5j60', label='EF_5j60_L2PS_5j75'),
            tba(bit1='EmulatedL2PS_5j75', bit2='EmulatedEF_5j65', label='EF_5j65_L2PS_5j75'),
            tba(bit1='EmulatedL2PS_5j75', bit2='EmulatedEF_5j70', label='EF_5j70_L2PS_5j75'),
            tba(bit1='EmulatedL2PS_5j75', bit2='EmulatedEF_5j75', label='EF_5j75_L2PS_5j75'),
            tba(bit1='EmulatedL2PS_5j75', bit2='EmulatedEF_5j80', label='EF_5j80_L2PS_5j75'),
            tba(bit1='EmulatedL2PS_5j75', bit2='EmulatedEF_5j85', label='EF_5j85_L2PS_5j75'),
            ]
        return listOfCalculables

    def listOfSampleDictionaries(self) :
        protocol="root://xrootd-disk.pic.es/"
        basedir="/pnfs-disk/pic.es/at3/projects/TOPD3PD/2011/Skimming/DPD_prod01_02_October11"
        castorBaseDir="/castor/cern.ch/grid/atlas/tzero/prod1/perm/data12_8TeV/express_express"
        castorDefaultOpt ='fileExt="NTUP_TRIG",pruneList=False'

        lumiPerRun = {202668:26.0, 202712:29.85, 202740:7.28, 202798:52.6, # B1
                      202987:14.02, 202991:40.15, 203027:89.29, 203258:119.4, #B2
                      }
        exampleDict = supy.samples.SampleHolder()
        exampleDict.add("PeriodB_L1_4J15",
                        'utils.fileListFromTextFile('
                        +'fileName="/afs/cern.ch/work/g/gerbaudo/public/trigger/MyRootCoreDir/supy-d3pdtrig/data/periodB.txt"'
                        #+'fileName="/afs/cern.ch/work/g/gerbaudo/public/trigger/MyRootCoreDir/supy-d3pdtrig/data/periodB_test.txt"'
                        +')',
                        lumi= sum(lumiPerRun.keys())
                        )
        return [exampleDict]

    def listOfSamples(self,config) :
        nEventsMax=-1 #1000
        return (
            supy.samples.specify(names="PeriodB_L1_4J15", color = r.kBlack, nEventsMax=nEventsMax, nFilesMax=-1)
            )

    def conclude(self,pars) :
        #make a pdf file with plots from the histograms created above
        org = self.organizer(pars)
        supy.plotter( org,
                      pdfFileName = self.pdfFileName(org.tag),
                      doLog = False,
                      blackList = ['num_.*', 'den_.*'],
                      ).plotAll()
