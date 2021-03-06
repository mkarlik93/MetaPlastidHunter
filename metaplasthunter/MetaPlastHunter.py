#!/usr/bin/env python

###############################################################################
#                                                                             #
#    Entry point for MetaPlastHunter                                          #
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

import logging
import argparse
import os
import sys
from time import gmtime, strftime
import multiprocessing as mp
from bin.external import Mapping_runner, SAM2coverage
from bin.taxonomic_assignment import Taxonomic_assignment_Runner
from bin.settings import Settings_loader_yaml
from bin.cov import Coverage_utilities

#logging.basicConfig(level=debug[args.verbosity], format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger("MetaPlastHunter")


#TODO - sprawdzanie poprawnosci plikow i kompletnosci

class Run:

    """


    Main class for running MetaPlastHunter RC

    MPH for read classification


    """

    def __init__(self,input,input2,output,settings,threads,mapping):

        self.list_sra = ""
        self.station_name = ""
        self.settings = settings
        self.threads = threads
        self.input = input
        self.input2 = input2
        self.output = output
        self.mapping = mapping


    def assign_taxnomomy_to_SAM(self):

        logger.info( " [%s] Testing settings file " % (strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())))
#        Settings_loader_yaml(self.settings).yaml_check_settings_file()
        logger.info( " [%s] Starting assign taxa to SAM file " % (strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())))
        SAM2coverage(self.input, self.output, self.settings).process()
        logger.info("     [%s] Taxonomic assignment based on SAM file" % (strftime("%a, %d %b %Y %H:%M:%S +2", gmtime())))
        Taxonomic_assignment_Runner(self.input, self.output,self.settings).process()

    def taxonomic_assigment(self):
        #Ta tez
        logger.info( "     [%s] Testing settings file " % (strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())))
        Settings_loader_yaml(self.settings).yaml_check_settings_file_classification()
        logger.info("     [%s] Mapping and generating SAM file" % (strftime("%a, %d %b %Y %H:%M:%S +2", gmtime())))
        Mapping_runner(self.input,self.input2,self.output, self.settings,self.threads,self.mapping).process()
        logger.info("     [%s] Taxonomic assignment based on SAM file" % (strftime("%a, %d %b %Y %H:%M:%S +2", gmtime())))
        Taxonomic_assignment_Runner(self.input,self.output, self.settings).process()

    def check(self):

        logger.info("     [%s] Testing settings file " % (strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())))
        Settings_loader_yaml(self.settings).yaml_check_settings_file_classification()
        logger.info("      [%s] Checking empirical threshold file and update if nessecary" %  (strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())))
        Coverage_utilities(self.settings).add_empirical_threshold()

def main():

    description = """

Version %s


MetaPlastHunter -


 The efficient and accurate plastid reads classification pipeline.

Quantitative aproach for eukaryotic metagenomics.

Available workflows:

[--taxonomic_classification/-C] Searching, Classification, Visualization

[--sam_assign, -A]   Sequence alignment file (SAM) classification

[--check]   Check settings and calculate empirical threshold if nessecary


Obligatory arguments:

Settings - inpute file

Facultative arguments:

threads

If you have any questions, please do not hesitate to contact me
email address: %s

Please cite:

Karlicki & Karnkowska, 2019

https://jgi.doe.gov/data-and-tools/bbtools/bb-tools-user-guide/bbmap-guide/

SILVA


This sofware has been written by %s.
""" % (__version__, __email__, __author__)

    epilog = """
"""

    parser = argparse.ArgumentParser(
                    description=description,
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                    epilog=epilog)

    parser.add_argument('--taxonomic_classification','-C',action='store_true')
    parser.add_argument('--rapid_classification', '-Acc',action='store_true')
    parser.add_argument('--settings','-S', metavar='settings', type=str)
    parser.add_argument('--sam_assign','-A',action='store_true')
    parser.add_argument('--in_1', metavar='input',type=str)
    parser.add_argument('--in_2',nargs='?',type=str, default="")
    parser.add_argument('--output','-O',type=str)
    parser.add_argument('--threads','-T',nargs='?', type=int,default=mp.cpu_count())
    parser.add_argument('--mapping','-M',nargs='?',type=bool,default=False)
    parser.add_argument('--check',action='store_true')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    start = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

    if os.path.exists(args.in_1) is True:

        pass

    else:

        logger.error("There is no such a file under given path!")

    if os.path.exists(args.in_2) is True and args.in_2 is not None:
        pass

    if args.in_1 == args.in_2:
        logger.error("input__1 and input__2 seems to be indentical")
        sys.exit()

#    else:
#        logger.error("There is no such a file under given path!")

    process = Run(os.path.abspath(args.in_1),os.path.abspath(args.in_2), args.output, args.settings,args.threads,args.mapping)

    if args.check:

        process.check()

    if args.taxonomic_classification:

        process.taxonomic_assigment()

    elif args.rapid_classification:

        process.rapid_taxonomic_assignment()

    elif args.sam_assign:

        process.assign_taxnomomy_to_SAM()

    else:

        logger.error("      Please specify pipeline")
        sys.exit()

    end = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())


    logger.info("Starting time: "+start)
    logger.info("Ending time: "+end)



if __name__ == "__main__":

    main()
