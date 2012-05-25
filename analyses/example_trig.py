#!/usr/bin/env python

import supy
import calculables,steps,samples, ROOT as r
import re

GeV=1.0e+3
TeV=1.0e+3*GeV

class example_trig(supy.analysis) :
    def otherTreesToKeepWhenSkimming(self) : return []
    def parameters(self) :
        return {'minJetEt' : 10.0*GeV,
                'grlFile' : "data11_7TeV.periodAllYear_DetStatus-v36-pro10_CoolRunQuery-00-04-08_SMjets.xml",
                'L2jetChain' : 'L2_[0-9]*j.*',
                'L2multiJetChain' : 'L2_[4-9]+j.*(em|had)$',
                }

    def listOfSteps(self,config) :
        pars = self.parameters()
        outList=[
            supy.steps.printer.progressPrinter(),
            supy.steps.histos.multiplicity(var='IndicesL2JetsA4TTA4CC_JES', max=20),
            #supy.steps.printer.printstuff(["IndicesL2JetsA4TTA4CC_JES",]),
            #steps.trigger.triggerCounts(pattern=r'.*5j55.*'),
            steps.trigger.triggerCounts(pattern=r'%s'%pars['L2multiJetChain']),
            supy.steps.histos.value(var='averageIntPerXing', N=50+1, low=0.5, up=50.5),
            supy.steps.filters.multiplicity("vxp_Indices",min=1),
            supy.steps.filters.multiplicity("IndicesOfflineJets",min=1),
            supy.steps.filters.multiplicity("IndicesOfflineBadJets",max=0),
            #steps.filters.triggers(["EF_4j55_a4tchad_L2FS"]),
            supy.steps.histos.multiplicity(var='IndicesL2JetsA4TTA4CC_JES', max=20),
            supy.steps.histos.multiplicity(var='IndicesL2JetsNON_L15L2CONE', max=20),
            supy.steps.histos.multiplicity(var='IndicesEfJetsAntiKt4_topo_calib_EMJES', max=20),
            steps.histos.attribute(attrName='E',coll='L2JetsNON_L15L2CONE', nX=100,xLo=-10.0*GeV,xUp=1000.0*GeV,title="L2Cone: E; E [MeV]; jets"),
            steps.histos.attribute(attrName='nLeadingCells',coll='L2JetsNON_L15L2CONE', nX=100,xLo=+0.0,xUp=500.0,title="L2Cone: nLeadingCells;N;jets"),
            steps.histos.attribute(attrName='hecf',coll='L2JetsNON_L15L2CONE', nX=100,xLo=-0.5,xUp=+1.5,title="L2Cone: hecf; hecf; jets"),
            steps.histos.attribute(attrName='jetQuality',coll='L2JetsNON_L15L2CONE', nX=100,xLo=-0.5,xUp=+1.5,title="L2Cone: jetQuality; jets"),
            steps.histos.attribute(attrName='emf',coll='L2JetsNON_L15L2CONE', nX=100,xLo=-0.5,xUp=+1.5,title="L2Cone: emf; emf; jets"),
            steps.histos.attribute(attrName='jetTimeCells',coll='L2JetsNON_L15L2CONE', nX=100,xLo=-50.0,xUp=+50.0,title="L2Cone: jetTimeCells;t [ns];jets"),
            steps.histos.attribute(attrName='jetTimeCells',coll='L2JetsNON_L15L2CONE', nX=100,xLo=-10.0,xUp=+10.0,title="L2Cone: jetTimeCells;t [ns];jets"),

            #steps.filters.triggers(["EF_4j55_a4tchad_L2FS", "EF_4j55_a4tchad_L2FSPS",]),
            #steps.filters.triggers(["EF_5j55_a4tchad_L2FS"]),
            #steps.filters.triggers(["EF_5j55_a4tchad_L2FSPS"]).invert(),

            #--supy.steps.histos.multiplicity(var = "vx_Indices", max = 20),
            #--steps.filters.goodRun().onlyData(),
            #supy.steps.histos.multiplicity(var="IndicesL2Jets",max=20),
            #steps.trigger.jetPt(collection="RunNumber"),
            steps.histos.deltaEta(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL1Jets',
                                  title='#Delta #eta matched (EfJetsAntiKt4, L1); #Delta #eta; jets'),
            steps.histos.deltaEta(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsNON_L15L2CONE',
                                  title='#Delta #eta matched (EfJetsAntiKt4, L2CONE); #Delta #eta; jets'),
            steps.histos.deltaEta(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsA4TTL2CONE',
                                  title='#Delta #eta matched (EfJetsAntiKt4, A4TTL2CONE); #Delta #eta; jets'),
            steps.histos.deltaEta(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsNONEA4TT',
                                  title='#Delta #eta matched (EfJetsAntiKt4, A4TT); #Delta #eta; jets'),
            steps.histos.deltaEta(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsNONEA10TT',
                                  title='#Delta #eta matched (EfJetsAntiKt4, A10TT); #Delta #eta; jets'),
            steps.histos.deltaEta(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsA4TTA4CC_JES',
                                  title='#Delta #eta matched (EfJetsAntiKt4, A4CC); #Delta #eta; jets'),

            steps.histos.deltaPhi(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL1Jets',
                                  title='#Delta #phi matched (EfJetsAntiKt4, L1); #Delta #phi; jets'),
            steps.histos.deltaPhi(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsNON_L15L2CONE',
                                  title='#Delta #phi matched (EfJetsAntiKt4, L2CONE); #Delta #phi; jets'),
            steps.histos.deltaPhi(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsA4TTL2CONE',
                                  title='#Delta #phi matched (EfJetsAntiKt4, ATTL2CONE); #Delta #phi; jets'),
            steps.histos.deltaPhi(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsNONEA4TT',
                                  title='#Delta #phi matched (EfJetsAntiKt4, A4TT); #Delta #phi; jets'),
            steps.histos.deltaPhi(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsNONEA10TT',
                                  title='#Delta #phi matched (EfJetsAntiKt4, A10TT); #Delta #phi; jets'),
            steps.histos.deltaPhi(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsA4TTA4CC_JES',
                                  title='#Delta #phi matched (EfJetsAntiKt4, A4CC); #Delta #phi; jets'),

            steps.histos.deltaR(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL1Jets',
                                  title='#Delta R matched (EfJetsAntiKt4, L1); #Delta R; jets'),
            steps.histos.deltaR(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsNON_L15L2CONE',
                                  title='#Delta R matched (EfJetsAntiKt4, L2CONE); #Delta R; jets'),
            steps.histos.deltaR(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsA4TTL2CONE',
                                  title='#Delta R matched (EfJetsAntiKt4, A4TTL2CONE); #Delta R; jets'),
            steps.histos.deltaR(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsNONEA4TT',
                                  title='#Delta R matched (EfJetsAntiKt4, A4TT); #Delta R; jets'),
            steps.histos.deltaR(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsNONEA10TT',
                                  title='#Delta R matched (EfJetsAntiKt4, A10TT); #Delta R; jets'),
            steps.histos.deltaR(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsA4TTA4CC_JES',
                                  title='#Delta R matched (EfJetsAntiKt4, A4CC); #Delta R; jets'),

            #steps.histos.deltaEt(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL1Jets',
            #                      title='#Delta E_{T} matched (EfJetsAntiKt4, L1); #Delta E_{T}; jets'),
            #steps.histos.deltaEt(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsNON_L15L2CONE',
            #                      title='#Delta E_{T} matched (EfJetsAntiKt4, L2CONE); #Delta E_{T}; jets'),
            #steps.histos.deltaEt(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsA4TTL2CONE',
            #                      title='#Delta E_{T} matched (EfJetsAntiKt4, A4TTL2CONE); #Delta E_{T}; jets'),
            #steps.histos.deltaEt(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsNONEA4TT',
            #                      title='#Delta E_{T} matched (EfJetsAntiKt4, A4TT); #Delta E_{T}; jets'),
            #steps.histos.deltaEt(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsNONEA10TT',
            #                      title='#Delta E_{T} matched (EfJetsAntiKt4, A10TT); #Delta E_{T}; jets'),


            steps.histos.deltaEtFrac(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsNONEA4TT',
                                     title='#Delta E_{T}/E_{T} matched (EfJetsAntiKt4, A4TT); #Delta E_{T}/E_{T}; jets'),
            steps.histos.deltaEtFrac(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL1Jets',
                                     title='#Delta E_{T}/E_{T} matched (EfJetsAntiKt4, L1); #Delta E_{T}/E_{T}; jets'),
            steps.histos.deltaEtFrac(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsNON_L15L2CONE',
                                     title='#Delta E_{T}/E_{T} matched (EfJetsAntiKt4, L2CONE); #Delta E_{T}/E_{T}; jets'),
            steps.histos.deltaEtFrac(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsA4TTL2CONE',
                                     title='#Delta E_{T}/E_{T} matched (EfJetsAntiKt4, A4TTL2CONE); #Delta E_{T}/E_{T}; jets'),
            steps.histos.deltaEtFrac(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsNONEA4TT',
                                     title='#Delta E_{T}/E_{T} matched (EfJetsAntiKt4, A4TT); #Delta E_{T}/E_{T}; jets'),
            steps.histos.deltaEtFrac(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsNONEA10TT',
                                     title='#Delta E_{T}/E_{T} matched (EfJetsAntiKt4, A10TT); #Delta E_{T}/E_{T}; jets'),
            steps.histos.deltaEtFrac(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsA4TTA4CC_JES',
                                     title='#Delta E_{T}/E_{T} matched (EfJetsAntiKt4, A4CC); #Delta E_{T}/E_{T}; jets'),

            steps.histos.etaPhiMap(coll='L1Jets', title="L1 jets #phi vs. #eta"),
            steps.histos.etaPhiMap(coll='L2JetsNON_L15L2CONE', title="L2 cone jets #phi vs. #eta"),
            steps.histos.etaPhiMap(coll='L2JetsA4TTL2CONE', title="L2 cone (A4TT seeded) jets #phi vs. #eta"),
            steps.histos.etaPhiMap(coll='L2JetsNONEA4TT', title="L2 A4TT jets #phi vs. #eta"),
            steps.histos.etaPhiMap(coll='L2JetsNONEA10TT', title="L2 A10TT jets #phi vs. #eta"),
            steps.histos.etaPhiMap(coll='EfJetsAntiKt4_topo_calib_EMJES', title="Ef jets #phi vs. #eta"),


            steps.histos.deltaEtaVsEtaMap(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsNON_L15L2CONE',
                                          title='#Delta #eta matched (EfJetsAntiKt4, NON_L15L2CONE); #eta; #Delta E_{T}/E_{T}'),
            steps.histos.deltaEtaVsEtaMap(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsA4TTA4CC_JES',
                                          title='#Delta #eta matched (EfJetsAntiKt4, A4CC); #eta; #Delta E_{T}/E_{T}'),

            steps.histos.deltaEtFracVsEtaMap(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsNON_L15L2CONE',
                                             title='#Delta E_{T}/E_{T} matched (EfJetsAntiKt4, NON_L15L2CONE); #eta; #Delta E_{T}/E_{T}'),
            steps.histos.deltaEtFracVsEtaMap(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsA4TTA4CC_JES',
                                             title='#Delta E_{T}/E_{T} matched (EfJetsAntiKt4, A4CC); #eta; #Delta E_{T}/E_{T}'),
            ]
        return outList

    def listOfCalculables(self,config) :
        pars = self.parameters()
        minEt = pars['minJetEt']
        listOfCalculables = supy.calculables.zeroArgs(supy.calculables)
        listOfCalculables += supy.calculables.zeroArgs(calculables)
        #listOfCalculables += supy.calculables.zeroArgs(calculables.vertex)
        listOfCalculables += [calculables.TrigD3PD.Tdt(),]
        #listOfCalculables += [calculables.TrigD3PD.Tdt(treeName = "TrigConfTree", dirName = "susyMeta"),]
        listOfCalculables += [calculables.TrigD3PD.TriggerBit("EF_mu18_medium"),
                              calculables.TrigD3PD.TriggerBit("EF_4j55_a4tchad_L2FS"),
                              calculables.TrigD3PD.TriggerBit("EF_4j55_a4tchad_L2FSPS"),
                              calculables.TrigD3PD.TriggerBit("EF_5j55_a4tchad_L2FS"),
                              calculables.TrigD3PD.TriggerBit("EF_5j55_a4tchad_L2FSPS"),
                              #calculables.TrigD3PD.TriggerBit("EF_6j55_a4tchad_L2FS"),
                              #calculables.TrigD3PD.TriggerBit("EF_6j55_a4tchad_L2FSPS"),
                              calculables.TrigD3PD.TriggerBit("L1_4J15"),
                              ]
        listOfCalculables += [#calculables.TrigD3PD.Grlt(pars['grlFile']),
                              #calculables.TrigD3PD.isGoodRun(runN='RunNumber',lbn='lbn'),
                              #calculables.TrigD3PD.PassedTriggers(),
                              ]
        listOfCalculables += [calculables.vertex.Indices(collection=('vxp_',''),
                                                         zPosMax=100, nTracksMin=4),]
        listOfCalculables += [calculables.jet.IndicesL1(collection=("trig_L1_jet_", "")),
                              calculables.jet.L1Jets(),

                              calculables.jet.IndicesL2(minEt=minEt, input='NON_L15', output='L2CONE'),# regular L2
                              calculables.jet.IndicesL2(minEt=minEt, input='A4TT', output='L2CONE'),   # L2 seeded by L1.5
                              calculables.jet.IndicesL2(minEt=minEt, input='NONE', output='A4TT'),     # L1.5 EM
                              calculables.jet.IndicesL2(minEt=minEt, input='NONE', output='A10TT'),     # L1.5 EM
                              calculables.jet.IndicesL2(minEt=minEt, input='NONE', output='A4TT_JES'), # L1.5 HAD JES
                              calculables.jet.IndicesL2(minEt=minEt, input='A4TT', output='A4CC_JES'), # A4CC HAD JES
                              calculables.jet.L2Jets(indices="IndicesL2JetsNON_L15L2CONE"),
                              calculables.jet.L2Jets(indices="IndicesL2JetsA4TTL2CONE"),
                              calculables.jet.L2Jets(indices="IndicesL2JetsNONEA4TT"),
                              calculables.jet.L2Jets(indices="IndicesL2JetsNONEA10TT"),
                              calculables.jet.L2Jets(indices="IndicesL2JetsNONEA4TT_JES"),
                              calculables.jet.L2Jets(indices="IndicesL2JetsA4TTA4CC_JES"),

                              calculables.jet.IndicesEf(minEt=minEt, calibTag='AntiKt4_topo_calib_EMJES'),
                              calculables.jet.EfJets(indices='IndicesEfJetsAntiKt4_topo_calib_EMJES'),

                              calculables.jet.MatchedJets(coll1='EfJetsAntiKt4_topo_calib_EMJES',
                                                          otherColls=['L1Jets']),
                              calculables.jet.MatchedJets(coll1='EfJetsAntiKt4_topo_calib_EMJES',
                                                          otherColls=['L2JetsNON_L15L2CONE']),
                              calculables.jet.MatchedJets(coll1='EfJetsAntiKt4_topo_calib_EMJES',
                                                          otherColls=['L2JetsA4TTL2CONE']),
                              calculables.jet.MatchedJets(coll1='EfJetsAntiKt4_topo_calib_EMJES',
                                                          otherColls=['L2JetsNONEA4TT']),
                              calculables.jet.MatchedJets(coll1='EfJetsAntiKt4_topo_calib_EMJES',
                                                          otherColls=['L2JetsNONEA10TT']),

                              calculables.jet.MatchedJets(coll1='EfJetsAntiKt4_topo_calib_EMJES',
                                                          otherColls=['L2JetsA4TTA4CC_JES']),

                              calculables.jet.MatchedJets(coll1='EfJetsAntiKt4_topo_calib_EMJES',
                                                          otherColls=['L2JetsNON_L15L2CONE', 'L2JetsA4TTL2CONE']),
                              calculables.jet.MatchedJets(coll1='EfJetsAntiKt4_topo_calib_EMJES',
                                                          otherColls=['L2JetsNONEA4TT', 'L2JetsNONEA10TT']),
                              calculables.jet.IndicesOffline(minEt=minEt),
                              calculables.jet.OfflineJets(),
                              calculables.jet.IndicesOfflineBad(),
                              ]
        return listOfCalculables

    def listOfSampleDictionaries(self) :
        protocol="root://xrootd-disk.pic.es/"
        basedir="/pnfs-disk/pic.es/at3/projects/TOPD3PD/2011/Skimming/DPD_prod01_02_October11"
        # need export STAGE_SVCCLASS=atlcal for this castor area
        castorBdirX="/castor/cern.ch/grid/atlas/tzero/prod1/perm/data12_8TeV/express_express"
        castorBdirJ="/castor/cern.ch/grid/atlas/tzero/prod1/perm/data12_8TeV/physics_JetTauEtmiss"
        castorDefaultOpt ='fileExt="NTUP_TRIG",pruneList=False'
        eosMyBDir="/eos/atlas/user/g/gerbaudo/trigger"

        exampleDict = supy.samples.SampleHolder()

# get these files from
# eos ls /eos/atlas/atlasdatadisk/data11_7TeV/NTUP_TRIG/r3408_r3410_p661/data11_7TeV.00191628.physics_EnhancedBias.merge.NTUP_TRIG.r3408_r3410_p661_tid742401_00
# (these are the suspicious eventd from Brian's email)
        exampleDict.add("foo",
                        '%s%s")'%(supy.sites.eos(), eosMyBDir+"/bugfixCheck/TrigT2CaloJet-00-01-29"),
                        lumi = 1.0e3)
        exampleDict.add("data12_8TeV.00200804",
                        'utils.fileListFromCastor('
                        +'location="'+castorBdirJ+'/00200804/data12_8TeV.00200804.physics_JetTauEtmiss.merge.NTUP_TRIG.x191_m1109"'
                        +'",'+castorDefaultOpt+')',
                        lumi = 0.03547) #/pb
        exampleDict.add("data12_8TeV.00200863",
                        'utils.fileListFromCastor('
                        +'location="'+castorBdirJ+'/00200863/data12_8TeV.00200863.physics_JetTauEtmiss.merge.NTUP_TRIG.f431_m1109"'
                        +'",'+castorDefaultOpt+')',
                        lumi = 3.505)
        exampleDict.add("data12_8TeV.00200913",
                        'utils.fileListFromCastor('
                        +'location="'+castorBdirJ+'/00200913/data12_8TeV.00200913.physics_JetTauEtmiss.merge.NTUP_TRIG.f431_m1109"'
                        +'",'+castorDefaultOpt+')',
                        lumi = 2.786)
        exampleDict.add("data12_8TeV.00200926",
                        'utils.fileListFromCastor('
                        +'location="'+castorBdirJ+'/00200926/data12_8TeV.00200926.physics_JetTauEtmiss.merge.NTUP_TRIG.f431_m1109"'
                        +'",'+castorDefaultOpt+')',
                        lumi = 9.226)
        exampleDict.add("data12_8TeV.00202609",
                        'utils.fileListFromCastor('
                        +'location="'+castorBdirJ+'/00202609/data12_8TeV.00202609.physics_JetTauEtmiss.merge.NTUP_TRIG.f441_m1129/'
                        +'",'+castorDefaultOpt+')',
                        lumi = 26.11)

        exampleDict.add("TrigT2CaloJet-00-01-29",
                        '%s%s")'%(supy.sites.eos(), eosMyBDir+"/bugfixCheck/TrigT2CaloJet-00-01-29"),
                        lumi = 1.0e3)
        exampleDict.add("TrigT2CaloJet-00-01-31",
                        '%s%s")'%(supy.sites.eos(), eosMyBDir+"/bugfixCheck/TrigT2CaloJet-00-01-31"),
                        lumi = 1.0e3)
        exampleDict.add("data12_8TeV.00202660",
                        'utils.fileListFromCastor('
                        +'location="%s"'%(castorBdirX+'/00202660/data12_8TeV.00202660.express_express.merge.NTUP_TRIG.x199_m1129/')
                        +','+castorDefaultOpt+')',
                        lumi = 2.178)
        exampleDict.add("data12_8TeV.00202668",
                        'utils.fileListFromCastor('
                        +'location="%s"'%(castorBdirX+'/00202668/data12_8TeV.00202668.express_express.merge.NTUP_TRIG.f443_m1139/')
                        +','+castorDefaultOpt+')',
                        lumi = 26.11)

        exampleDict.add("202668_L1_4J15",
                        '%s%s")'%(supy.sites.eos(), eosMyBDir+"/skim/SUSYD3PD.202668.skim.L1_4J15"),
                        lumi = 26.11)
        exampleDict.add("202712_L1_4J15",
                        '%s%s")'%(supy.sites.eos(), eosMyBDir+"/skim/SUSYD3PD.202712.skim.L1_4J15"),
                        lumi = 29.85)
        exampleDict.add("202712_L1_4J15_2",
                        '%s%s")'%(supy.sites.eos(), eosMyBDir+"/skim/SUSYD3PD.202712.skim.L1_4J15_2"),
                        lumi = 29.85)
        exampleDict.add("202740_L1_4J15",
                        '%s%s")'%(supy.sites.eos(), eosMyBDir+"/skim/SUSYD3PD.202740.skim.L1_4J15"),
                        lumi = 7.281)
        exampleDict.add("202798_L1_4J15",
                        (supy.utils.fileListFromEos,
                         dict(supy.sites.eosPars().items()
                              +{'location':eosMyBDir+"/skim/SUSYD3PD.202798.skim.L1_4J15"
                                }.items())),
                        lumi = 52.6)
        exampleDict.add("data12_8TeV.00203277",
                        'utils.fileListFromCastor('
                        +'location="%s"'%(castorBdirX+'/00203277/data12_8TeV.00203277.express_express.merge.NTUP_TRIG.f444_m1141/')
                        +','+castorDefaultOpt+')',
                        lumi = 99.3)
        exampleDict.add("data12_8TeV.00203335",
                        'utils.fileListFromCastor('
                        +'location="%s"'%(castorBdirX+'/00203335/data12_8TeV.00203335.express_express.merge.NTUP_TRIG.f446_m1146/')
                        +','+castorDefaultOpt+')',
                        lumi = 61.81)
        exampleDict.add("data12_8TeV.00203336",
                        'utils.fileListFromCastor('
                        +'location="%s"'%(castorBdirX+'/00203336/data12_8TeV.00203336.express_express.merge.NTUP_TRIG.f446_m1146/')
                        +','+castorDefaultOpt+')',
                        lumi = 61.25)
        return [exampleDict]

    def listOfSamples(self,config) :
        nEventsMax=1000 #10000
        return (
            #supy.samples.specify(names = "data12_8TeV.00200804", color = r.kBlack)
            #supy.samples.specify(names = "Zmumu_skimMu", color = r.kRed, effectiveLumi = 10.0e+3)
            #supy.samples.specify(names=['data12_8TeV.00202660', 'data12_8TeV.00202668',
            #                            'data12_8TeV.00202712', 'data12_8TeV.00202740', 'data12_8TeV.00202798',],
            #                     color = r.kBlack, nEventsMax=nEventsMax, nFilesMax=-1)

            supy.samples.specify(names="data12_8TeV.00203277", color = r.kBlack, nEventsMax=nEventsMax, nFilesMax=-1)
            +supy.samples.specify(names="data12_8TeV.00203335", color = r.kRed, nEventsMax=nEventsMax, nFilesMax=-1, markerStyle=r.kOpenCircle)
            +supy.samples.specify(names="data12_8TeV.00203336", color = r.kBlue, nEventsMax=nEventsMax, nFilesMax=-1)

            )

    def conclude(self,pars) :
        #make a pdf file with plots from the histograms created above
        org = self.organizer(pars)
        #org.scale(lumiToUseInAbsenceOfData=1000.)
        org.mergeSamples(targetSpec = {"name":"Period B (part)", "color":r.kBlack}, allWithPrefix="202")
        supy.plotter( org,
                      pdfFileName = self.pdfFileName(org.tag),
                      #linYafter = ("triggers", "L1_4J15"),
                      doLog = False,
                      #samplesForRatios = ("Example_Skimmed_900_GeV_Data","Example_Skimmed_900_GeV_MC"),
                      #sampleLabelsForRatios = ("data","sim"),
                      blackListRe = [re.compile(r'num_'), re.compile(r'den_')],
                      ).plotAll()
