#!/usr/bin/env python

import supy
import calculables,steps,samples, ROOT as r

GeV=1.0e+3
TeV=1.0e+3*GeV

class example_trig(supy.analysis) :
    def otherTreesToKeepWhenSkimming(self) : return []
    def parameters(self) :
        return {'minJetPt' : 10.0,
                'grlFile' : "data11_7TeV.periodAllYear_DetStatus-v36-pro10_CoolRunQuery-00-04-08_SMjets.xml",
                'L2jetChain' : 'L2_[0-9]*j.*',
                'L2multiJetChain' : 'L2_[5-9]+j.*(em|had)$',
                }

    def listOfSteps(self,config) :
        pars = self.parameters()
        outList=[
            supy.steps.printer.progressPrinter(),
            steps.filters.triggers(["EF_5j55_a4tchad_L2FS"]).invert(),
            steps.filters.triggers(["EF_5j55_a4tchad_L2FSPS"]),
            #--steps.filters.triggers(["EF_mu18_medium",]),
            #supy.steps.printer.printstuff(["EF_mu18_medium",]),
            #--supy.steps.filters.multiplicity("vx_Indices",min=1),
            #--supy.steps.filters.multiplicity("IndicesOfflineJets",min=1),
            #--supy.steps.filters.multiplicity("IndicesOfflineBadJets",max=0),
            #--supy.steps.histos.multiplicity(var = "vx_Indices", max = 20),
            steps.filters.goodRun().onlyData(),
            supy.steps.histos.multiplicity(var="IndicesL2Jets",max=20),
            steps.trigger.jetPt(collection="RunNumber"),
            #supy.steps.printer.printstuff(['PassedTriggers',]),
            steps.trigger.triggerCounts(pattern=r'%s'%pars['L2multiJetChain']),
            steps.trigger.triggerCounts(pattern=r'.*5j55.*'),
            #supy.steps.filters.multiplicity(min = 4, var = "jet_Indices"),
            #supy.steps.histos.multiplicity(var = "jet_Indices", max = 20),
            #supy.steps.histos.eta(var = "jet_P4", N = 20, low = -2., up = +2., indices = "jet_Indices"),
            #supy.steps.histos.value(var = "jet_M01" , N = 50, low = 0., up = 1.0e+3*GeV),
            #supy.steps.filters.value(var = "jet_M01", min = 1.0*TeV),
            #supy.steps.other.skimmer()
            ]
        return outList
    
    def listOfCalculables(self,config) :
        pars = self.parameters()
        listOfCalculables = supy.calculables.zeroArgs(supy.calculables)
        listOfCalculables += [calculables.TrigD3PD.Tdt(),]
        listOfCalculables += [calculables.TrigD3PD.TriggerBit("EF_mu18_medium"),
                              calculables.TrigD3PD.TriggerBit("EF_5j55_a4tchad_L2FSPS"),
                              calculables.TrigD3PD.TriggerBit("EF_5j55_a4tchad_L2FS"),
                              ]
        listOfCalculables += [calculables.TrigD3PD.Grlt(pars['grlFile']),
                              calculables.TrigD3PD.isGoodRun(runN='RunNumber',lbn='lbn'),
                              calculables.TrigD3PD.PassedTriggers(),
                              ]
        listOfCalculables += [calculables.vertex.Indices(collection=('vx_',''),
                                                         zPosMax=100, nTracksMin=4),]
        listOfCalculables += [calculables.jet.IndicesL1(collection=("trig_L1_jet_", "")),
                              calculables.jet.IndicesL2(collection=("trig_L2_jet_", ""), minEt=10.*GeV),
                              calculables.jet.IndicesEf(collection=("trig_EF_jet_emscale_", ""), minEt=10.*GeV),
                              calculables.jet.IndicesOffline(collection=("jet_AntiKt4TopoEMJets_", "")),
                              calculables.jet.IndicesOfflineBad(),
                              ]
        return listOfCalculables

    def listOfSampleDictionaries(self) :
        protocol="root://xrootd-disk.pic.es/"
        basedir="/pnfs-disk/pic.es/at3/projects/TOPD3PD/2011/Skimming/DPD_prod01_02_October11"
        exampleDict = supy.samples.SampleHolder()
#        exampleDict.add("Pythia_ttbar_bWincbHminus",
#                '["/tmp/gerbaudo/eos/NTUP_TRIG.742401._000002.root.1"]',
#                        lumi = 1.0e+3 ) #/pb
# get these files from
# eos ls /eos/atlas/atlasdatadisk/data11_7TeV/NTUP_TRIG/r3408_r3410_p661/data11_7TeV.00191628.physics_EnhancedBias.merge.NTUP_TRIG.r3408_r3410_p661_tid742401_00
# (these are the suspicious eventd from Brian's email)
        exampleDict.add("Pythia_ttbar_bWincbHminus",
                        'utils.fileListFromDisk(location = "/tmp/gerbaudo/eos/*.root", isDirectory = False)',
                        #'[""]',
                        lumi = 1.0e+3 ) #/pb
        return [exampleDict]

    def listOfSamples(self,config) :
        return (supy.samples.specify(names = "Pythia_ttbar_bWincbHminus", color = r.kBlack, markerStyle = 20,
                                     nFilesMax = 10,
                                     nEventsMax=-1,)
                #supy.samples.specify(names = "Zmumu_skimMu", color = r.kRed, effectiveLumi = 10.0e+3) +
                #supy.samples.specify(names = "ttbar_skimMu", color = r.kViolet, effectiveLumi = 10.0e+3)
                )

    def conclude(self,pars) :
        #make a pdf file with plots from the histograms created above
        org = self.organizer(pars)
        org.scale(lumiToUseInAbsenceOfData=1000.)
        supy.plotter( org,
                      pdfFileName = self.pdfFileName(org.tag),
                      #samplesForRatios = ("Example_Skimmed_900_GeV_Data","Example_Skimmed_900_GeV_MC"),
                      #sampleLabelsForRatios = ("data","sim"),
                      ).plotAll()
