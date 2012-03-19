This project is a satellite of <supy> for D3PD format TTrees.
See <github.com/elaird/supy>.
The goal of this package is to perform a fast analysis of the ATLAS trigger D3PD files.

-----------
| License |
-----------
GPLv3 (http://www.gnu.org/licenses/gpl.html)

---------------
| Quick Start |
---------------

 execute the commands in 'do.sh'                    #1) set up the required external packages
Then:
git clone git://github.com/<user>/supy-d3pdtrig.git #2) get this package
cd supy-d3pdtrig
git submodule update --init                         #3) checkout supy dependence
source env.sh                                       #4) set PATH and PYTHONPATH
supy   analyses/example_trig.py --loop 1            #5) Run the example (need input files):

----------------
| Dependencies |
----------------
ROOT (>=5.27.06) and python (2.x, x>=6) are required.
See <github.com/elaird/supy>