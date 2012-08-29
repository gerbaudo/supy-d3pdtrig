
import supy
import calculables,steps,samples, ROOT as r
import re

GeV=1.0e+3
TeV=1.0e+3*GeV


class fatJetTurnOn(supy.analysis) :
    def otherTreesToKeepWhenSkimming(self) : return []
    def parameters(self) :
        return {'minJetEt' : 30.0*GeV,
                'maxJetEta' : 3.2,
                'minNofflineJets' : 5,
                'grlFile' : "data/data12_8TeV.periodAllYear_DetStatus-v51-pro13-04_CoolRunQuery-00-04-08_All_Good.xml",
                'L2jetChain' : 'L2_[0-9]*j.*',
                'L2multiJetChain' : 'L2_[4-9]+j.*(em|had)$',
                'refTrigger' : "L1_RD0_FILLED",
                'refJetColl' : 'OfflineJets',
                'offlineFatJetColl':'jet_AntiKt10LCTopo_'
                }

    def listOfSteps(self,config) :
        pars = self.parameters()
        refTrigger = pars['refTrigger']
        refJetColl = pars['refJetColl']
        offlineFatJetColl = pars['offlineFatJetColl']
        outList=[
            supy.steps.printer.progressPrinter(),
            supy.steps.filters.multiplicity("IndicesOfflineBadJets",max=0),
            supy.steps.filters.multiplicity("vxp_Indices",min=1),
            supy.steps.filters.multiplicity(refJetColl, min=1),
            steps.filters.goodRun().onlyData(),
            steps.filters.triggers([refTrigger]),
            #supy.steps.printer.printstuff(['PassedTriggers',]),
            steps.histos.attribute(attrName='et', coll=refJetColl, nTh=0, title="E_{T} %dth jet "%(0+1)+"("+refJetColl+"); E_{T}; events",xLo=0.0,xUp=200.0*GeV),            
            steps.histos.turnOnJet(trigger='EF_j35_a10tcem', jetColl=refJetColl, nTh=0,N=40,low=0.0,up=200.0,
                                   title="EF_j35_a10tcem efficiency; 1st AntiKt4TopoNewEM jet E_{T} [GeV];eff"),
            steps.histos.turnOnJet(trigger='EF_j35_a10tcem', jetColl='OfflineJetsA10', nTh=0,N=40,low=0.0,up=200.0,
                                   title="EF_j35_a10tcem efficiency; 1st AntiKt10LCTopo jet E_{T} [GeV];eff"),
            ]
        return outList

    def listOfCalculables(self,config) :
        pars = self.parameters()
        minEt = pars['minJetEt']
        maxEta = pars['maxJetEta']
        offlineFatJetColl = pars['offlineFatJetColl']
        listOfCalculables = supy.calculables.zeroArgs(supy.calculables)
        listOfCalculables += supy.calculables.zeroArgs(calculables)
        listOfCalculables += [calculables.TrigD3PD.Grlt(pars['grlFile']),
                              calculables.TrigD3PD.isGoodRun(runN='RunNumber',lbn='lbn'),
                              calculables.TrigD3PD.Tdt(treeName = "TrigConfTree", dirName = "susyMeta"),]
        tb = calculables.TrigD3PD.TriggerBit
        listOfCalculables += [tb('L1_RD0_FILLED'),
                              tb('EF_j35_a10tcem'),
                              ]
        listOfCalculables += [calculables.TrigD3PD.PassedTriggers(),]
        listOfCalculables += [calculables.vertex.Indices(collection=('vxp_',''),
                                                         zPosMax=100, nTracksMin=4),]
        listOfCalculables += [calculables.jet.IndicesOffline(minEt=minEt, maxEta=maxEta),
                              calculables.jet.OfflineJets(),
                              calculables.jet.IndicesOfflineBad(),
                              calculables.jet.IndicesOffline(collection=(offlineFatJetColl,''),maxEta=maxEta,minEt=minEt,
                                                             tag='A10',attributesToSkip=['isUgly','isBadLoose']),
                              calculables.jet.OfflineJets(collection=(offlineFatJetColl,''),indices='IndicesOfflineJetsA10',
                                                          attributesToSkip=['isUgly','isBadLoose']),
                              ]
        emjb = calculables.TrigD3PD.EmulatedMultijetTriggerBit
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
        exampleDict.add("test_L1_RD0_FILLED",
                        'utils.fileListFromTextFile('
                        +'fileName="/afs/cern.ch/user/g/gerbaudo/work/public/trigger/MyRootCoreDir/supy-d3pdtrig/data/test_L1_RD0_FILLED.txt"'
                        +')',
                        lumi=lumiPerRun[208261]
                        )

        return [exampleDict]

    def listOfSamples(self,config) :
        nEventsMax=-1 # 10000
        return (
            supy.samples.specify(names="test_L1_RD0_FILLED", color = r.kBlack, nEventsMax=nEventsMax, nFilesMax=-1)
            )

    def conclude(self,pars) :
        #make a pdf file with plots from the histograms created above
        org = self.organizer(pars)
        supy.plotter( org,
                      pdfFileName = self.pdfFileName(org.tag),
                      doLog = False,
                      blackList = ['num_.*', 'den_.*'],
                      ).plotAll()
