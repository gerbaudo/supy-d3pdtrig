#!/usr/bin/env python

import supy
import calculables,steps,samples, ROOT as r

GeV=1.0e+3
TeV=1.0e+3*GeV

class display_L2FSPS(supy.analysis) :
    def otherTreesToKeepWhenSkimming(self) : return []
    def parameters(self) :
        return {'minJetEt' : 10.0*GeV,
                'L2jetChain' : 'L2_[0-9]*j.*',
                'L2multiJetChain' : 'L2_[5-9]+j.*(em|had)$',
                }

    def listOfSteps(self,config) :
        pars = self.parameters()
        outList=[
            supy.steps.printer.progressPrinter(),
            steps.filters.triggers(["EF_5j55_a4tchad_L2FS"]),
            steps.filters.triggers(["EF_5j55_a4tchad_L2FSPS"]).invert(),
            steps.displayer.displayer(doL1Jets=True, doL2Jets=True, doEfJets = True, doOfflineJets=True),
            ]
        return outList
    
    def listOfCalculables(self,config) :
        pars = self.parameters()
        minEt = pars['minJetEt']
        listOfCalculables = supy.calculables.zeroArgs(supy.calculables)
        listOfCalculables += [calculables.TrigD3PD.Tdt(),
                              calculables.TrigD3PD.PassedTriggers(),
                              ]
        listOfCalculables += [calculables.TrigD3PD.TriggerBit("EF_5j55_a4tchad_L2FSPS"),
                              calculables.TrigD3PD.TriggerBit("EF_5j55_a4tchad_L2FS"),
                              ]
        listOfCalculables += [calculables.jet.IndicesL1(collection=("trig_L1_jet_", "")),
                              calculables.jet.L1Jets(),

                              calculables.jet.L2Jets(indices="IndicesL2JetsNON_L15L2CONE"),
                              calculables.jet.L2Jets(indices="IndicesL2JetsNONEA4TT"),
                              calculables.jet.L2Jets(indices="IndicesL2JetsNONEA4TT_JES"),
                              calculables.jet.L2Jets(indices="IndicesL2JetsNONEA4CC_JES"),
                              calculables.jet.IndicesL2(minEt=minEt, input='NON_L15', output='L2CONE'),# regular L2
                              calculables.jet.IndicesL2(minEt=minEt, input='NONE', output='A4TT'),     # L1.5 EM
                              calculables.jet.IndicesL2(minEt=minEt, input='NONE', output='A4TT_JES'), # L1.5 HAD JES
                              calculables.jet.IndicesL2(minEt=minEt, input='NONE', output='A4CC_JES'), # A4CC HAD JES

                              calculables.jet.IndicesEf(minEt=minEt, calibTag='AntiKt4_topo_calib_EMJES'),
                              calculables.jet.EfJets(indices='IndicesEfJetsAntiKt4_topo_calib_EMJES'),

                              calculables.jet.MatchedJets(coll1='EfJetsAntiKt4_topo_calib_EMJES',
                                                          otherColls=['L2JetsNONEA4CC_JES','L2JetsNONEA4TT']),
                              calculables.jet.IndicesOffline(minEt=minEt),
                              calculables.jet.OfflineJets(),
                              ]
        return listOfCalculables

    def listOfSampleDictionaries(self) :
        exampleDict = supy.samples.SampleHolder()
        # get these files from
        # eos ls /eos/atlas/atlasdatadisk/data11_7TeV/NTUP_TRIG/r3408_r3410_p661/data11_7TeV.00191628.physics_EnhancedBias.merge.NTUP_TRIG.r3408_r3410_p661_tid742401_00
        # (these are the suspicious events from Brian's email)
        #exampleDict.add("Pythia_ttbar_bWincbHminus",
        #                'utils.fileListFromDisk(location = "/tmp/gerbaudo/eos/NTUP*.root*", isDirectory = False)',
        #                lumi = 1.0e+3 ) #/pb
        # this file is from Bertrand's D3PD
        # dq2-ls -f user.chapleau.valid1.105204.TTbar_FullHad_McAtNlo_Jimmy.recon.AOD.e825_s1310_s1300_r3391.NTUP_TRIG.JetOnly.v1/
        exampleDict.add("Pythia_ttbar_bWincbHminus",
                        'utils.fileListFromDisk(location = "/tmp/gerbaudo/dq2/user.chapleau.001130.EXT0._00082.NTUP.root", isDirectory = False)',
                        lumi = 1.0e+3 ) #/pb
        exampleDict.add("ttbar-00-01-28",
                        '%s%s")'%(supy.sites.eos(), "/eos/atlas/user/g/gerbaudo/trigger/bugfixCheck/TrigT2CaloJet-00-01-28"),
                        lumi = 1.0e3)
        exampleDict.add("ttbar-00-01-29",
                        '%s%s")'%(supy.sites.eos(), "/eos/atlas/user/g/gerbaudo/trigger/bugfixCheck/TrigT2CaloJet-00-01-29"),
                        lumi = 1.0e3)
        return [exampleDict]

    def listOfSamples(self,config) :
        return (#supy.samples.specify(names = "Pythia_ttbar_bWincbHminus", color = r.kBlack, markerStyle = 20,
                #                     #nFilesMax = 100,
                #                     #nEventsMax=10,
                #                     )
                supy.samples.specify(names = "ttbar-00-01-29", color = r.kBlack, markerStyle = 20,
                                     nFilesMax = 1,
                                     nEventsMax=1000,
                                     )
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
