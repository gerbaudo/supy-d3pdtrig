
   mkdir MyRootCoreDir
   cd MyRootCoreDir
   source ~/script/bash/setup_atlas.sh 
   asetup AtlasP1HLT,17.1.4.5,here

   svn co svn+ssh://svn.cern.ch/reps/atlasoff/PhysicsAnalysis/D3PDTools/RootCore/tags/RootCore-00-01-00 RootCore
   svn co svn+ssh://svn.cern.ch/reps/atlasgrp/Institutes/LIP/RootCore/TriggerEff/trunk TriggerEff
   svn co svn+ssh://svn.cern.ch/reps/atlasoff/DataQuality/GoodRunsLists/tags/GoodRunsLists-00-00-94 GoodRunsLists
   svn co svn+ssh://svn.cern.ch/reps/atlasoff/Trigger/TrigAnalysis/TrigRootAnalysis/tags/TrigRootAnalysis-00-00-08  TrigRootAnalysis
   cd RootCore/
   ./configure
   cd ..
   source RootCore/scripts/setup.sh
   $ROOTCOREDIR/scripts/find_packages.sh
   $ROOTCOREDIR/scripts/compile.sh
