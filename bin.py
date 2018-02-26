#!/usr/bin/env python
###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

__author__ = 'Michal Karlicki'
__copyright__ = 'Copyright 2018'
__credits__ = ['Michal Karlicki']
__license__ = 'GPL3'
__version__ = '1.0.0'
__maintainer__ = 'Michal Karlicki'
__email__ = 'michal.karlicki@gmail.com'
__status__ = 'Development'



from src import bbpipe
from src import krakenize
from src import kraken_output_analysis
from src import get_data

#LET's write whole main



class WholePipeline:

    def __init__(self,list_sra, station_name,settings,threads):
        self.list_sra = list_sra
        self.station_name = station_name
        self.settings = settings
        self.threads = threads

    def run(self):
        print "     [%s] Dowloading data" % (strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
        Pipeline_fetch(self.list_sra,self.station_name,self.settings).run()
        print "     [%s] Kraken classification" % (strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
        Pipeline_kraken(self.list_sra, self.station_name,self.settings,self.threads).run()
        print "     [%s] BBtools postprocessing" % (strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
        BBpipe(list_sra,station_name,settings).process()
        print "     [%s] Output analysis" % (strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
        Run_analysis(list_sra, station_name,4).process()

class Pipeline_without_downloading:

    def __init__(self,list_sra, station_name,settings,threads):

        self.list_sra = list_sra
        self.station_name = station_name
        self.settings = settings
        self.threads = threads

    def run(self):
#        list_sra_ids = sra_ids.split(",")

        #Do tworzenia folderow Just in case
#        try:
#            os.stat(station_name)
#        except:
#            os.mkdir(station_name)
#            for id in list_sra:
#                command_create_dir = "mkdir %s/%s" % (station_name,sra_id)



        print "     [%s] Kraken classification" % (strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
        Pipeline_kraken(self.list_sra, self.station_name,self.settings,self.threads).run()
        print "     [%s] BBtools postprocessing" % (strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
        BBpipe(list_sra,station_name,settings).process()
        print "     [%s] Output analysis" % (strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
        Run_analysis(list_sra, station_name,4).process()




if __name__ == "__main__":

    from time import gmtime, strftime
    import sys
    import os
    import argparse


    description = """

Version %s


The first version of mtp programme.

If you have any questions, please do not hesitate to contact me
email address: michal.karlicki@gmail.com


This sofware was written by %s.
""" % (__version__,__author__)

    epilog = """

"""


    parser = argparse.ArgumentParser(
                    description=description,
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                    epilog=epilog)


    parser.add_argument('-run_full_analysis','--full',action='store_true')
    parser.add_argument('-run_partial_analysis','--partial',action='store_true')
    parser.add_argument('sra_ids', metavar='sra_ids', type=str)
    parser.add_argument('station_name', metavar='station_name', type=str)
    parser.add_argument('database_dir', metavar='database_dir', type=str)
    parser.add_argument('threads', metavar='threads', type=int)


    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    start = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    if args.full:
        WholePipeline(args.list_sra, args.station_name,args.settings,args.threads).run()
    if args.partial:
        Pipeline_without_downloading(args.sra_ids, args.station_name,args.settings,args.threads).run()
    end = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    print "Starting time: "+start
    print "Ending time: "+end
