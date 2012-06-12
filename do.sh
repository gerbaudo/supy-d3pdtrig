   mkdir MyRootCoreDir
   cd MyRootCoreDir
   source ~/script/bash/setup_atlas.sh 
   asetup AtlasP1HLT,17.1.4.5,here

   svn co svn+ssh://svn.cern.ch/reps/atlasoff/PhysicsAnalysis/D3PDTools/RootCore/tags/RootCore-00-01-17 RootCore
   svn co svn+ssh://svn.cern.ch/reps/atlasoff/DataQuality/GoodRunsLists/tags/GoodRunsLists-00-01-01 GoodRunsLists
   svn co svn+ssh://svn.cern.ch/reps/atlasoff/Trigger/TrigAnalysis/TrigRootAnalysis/tags/TrigRootAnalysis-00-01-01  TrigRootAnalysis
   cd RootCore/
   ./configure
   cd ..
   source RootCore/scripts/setup.sh
   $ROOTCOREDIR/scripts/find_packages.sh
   $ROOTCOREDIR/scripts/compile.sh
