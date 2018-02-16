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

def fastq_dump_sra_file(station_name,sra_id):
    command_create_dir = "mkdir %s/%s" % (station_name,sra_id)
    os.system(command_create_dir)
    command = "/opt/sratoolkit.2.8.2-1-ubuntu64/bin/fastq-dump %s --skip-technical -I --split-3" % (sra_id)
    os.chdir("%s/%s/" % (station_name,sra_id))
    os.system(command)


class Pipeline_fetch:

    def __init__(self, list_sra, station_name):
        self.list_sra = list_sra
        self.station_name = station_name

    def create_station_dir(self):
        command  = "mkdir %s" % (self.station_name)
        os.system(command)
        print "Directory was created"

    def preprocess_sra_id(self):
        sra_ids = self.list_sra
        list_sra_ids = sra_ids.split(",")
        return list_sra_ids


    def multiprocess(self):
        sra_ids = self.list_sra
        list_sra_ids = sra_ids.split(",")
        for i in list_sra_ids:
                proc = Process(target=fastq_dump_sra_file, args=(self.station_name,i))
                proc.start()
                print "Downloading has started"

    def evaluation(self):
        cwd = os.getcwd()
        station_name = self.station_name
        sra_ids = self.list_sra
        list_sra_ids = sra_ids.split(",")
        os.chdir("%s/%s/" % (cwd,station_name))
        for i in list_sra_ids:
            os.chdir( "%s/%s/%s/" % (cwd,station_name,i))
            if len(glob.glob("*.fastq")) == 2:
                print "For "+str(i)+" everything is ok!"
            else:
                print "check it : "+str(i)
            os.chdir("%s/%s/" % (cwd,station_name))
        os.chdir(cwd)

    def fastqc_report(self):
        cwd = os.getcwd()
        station_name = self.station_name
        sra_ids = self.list_sra
        list_sra_ids = sra_ids.split(",")
        os.chdir("%s/%s/" % (cwd,station_name))
        for i in list_sra_ids:
            os.chdir( "%s/%s/%s/" % (cwd,station_name,i))
            if len(glob.glob("*.fastq")) == 2:
                for file in glob.glob("*.fastqc"):
                    command = "fastqc "+i
                    os.system(command)
                    print "For "+str(i)+" everything is ok!"
            else:
                print "check it : "+str(i)
            os.chdir("%s/%s/" % (cwd,station_name))
        os.chdir(cwd)


if __name__ == "__main__":

    from time import gmtime, strftime
    import sys
    import os
    import argparse
    from multiprocessing import Process
    import glob


    description = """

Version 1.01

Script designed for getting data from SRA repository and evaluation.

If you have any questions, please do not hesitate to contact me
email address: michal.karlicki@gmail.com
"""

    epilog = """

"""


    parser = argparse.ArgumentParser(
                    description=description,
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                    epilog=epilog)




    parser.add_argument('sra_ids', metavar='sra_ids', type=str)
    parser.add_argument('station_name', metavar='station_name', type=str)



    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    start = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    run = Pipeline_fetch(args.sra_ids,args.station_name)
    run.create_station_dir()
    run.multiprocess()
    run.evaluation()
    run.fastqc_report()
    end = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    print "Starting time: "+start
    print "Ending time: "+end