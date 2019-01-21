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

import csv

""" Project managment part  """

"""Tworzenie plikow z odczytami zawierajacymi wszystkie odczyty z danego taksonu otrzymanych z roznych zestawow danych dla jednej stacji"""

#def create_folder_all(station_name):
#    base_cwd = os.getcwd()
#    os.chdir(os.getcwd()+"/"+station_name+"/")
#    os.system("mkdir all_"+station_name)
#    os.chdir(base_cwd)



#Index,Station identifier [TARA_station#],Taxon ,Reads number
#0,TARA_031,taxa_1,3000
#1,TARA_032,taxa_1,400
#2,TARA_033,taxa_1,40000
#3,TARA_034,taxa_1,1
#4,TARA_035,taxa_1,100
#5,TARA_036,taxa_1,25000



class Project_managment:

    def __init__(self,station_name_list):

        self.station_name_list = station_name_list.split(',')
        self.base_cwd = os.getcwd()

    def fromcsv2dict(self,file):
        reader = csv.reader(file)
        dict =  {}
        for row in reader:
            splited_row = row.split("\t")
            dict[splited_row[1]] = splited_row[2]
        return dict


    def get_species_results_from_site(self,sample_site):

        os.chdir(self.base_cwd+"/"+str(sample_site)+"/")
        thedir = str(sample_site)
        directories =  [ name for name in os.listdir(thedir) if os.path.isdir(os.path.join(thedir, name)) ]
        list_of_dict = []
        cwd = os.getcwd()
        for directory in directories:
            os.chdir(cwd+"/"+directory+"/")
            files = glob.glob("*_species_level_table.csv"")
            for file in files:
                #?Tu czy na pewno tak?
                unique_names.add(self.fromcsv2dict(file))
        os.chdir(self.base_cwd)
        return list_of_dict


    def get_fourth_taxa_level_from_site(self,sample_site):

        os.chdir(self.base_cwd+"/"+str(sample_site)+"/")
        thedir = str(sample_site)
        directories =  [ name for name in os.listdir(thedir) if os.path.isdir(os.path.join(thedir, name)) ]
        list_of_dict = []
        cwd = os.getcwd()
        for i in directories:
            os.chdir(cwd+"/"+i+"/")
            files = glob.glob("*_species_level_table.csv"")
            for file in files:
                unique_names.add(self.fromcsv2dict(file))
        os.chdir(self.base_cwd)
        return list_of_dict








class Concatenate:

    def __init__(self,station_name):

        self.base_cwd = os.getcwd()
        self.station_name = station_name


    def fromcsv2dict(self,file):
        reader = csv.reader(file)
        dict =  {}
        for row in reader:
            splited_row = row.split("\t")
            dict[splited_row[1]] = splited_row[2]
        return dict

    def get_species_results_from_site(self):

        os.chdir(self.base_cwd+"/"+self.station_name+"/")
        thedir = self.station_name
        directories =  [ name for name in os.listdir(thedir) if os.path.isdir(os.path.join(thedir, name)) ]
        list_of_dict = []
        cwd = os.getcwd()
        for i in directories:
            os.chdir(cwd+"/"+i+"/")
            files = glob.glob("*_species_level_table.csv"")
            for file in files:
                unique_names.add(self.fromcsv2dict(file))
        os.chdir(self.base_cwd)
        return list_of_dict





    def get_unique_among_folders(self):
#        base_cwd = os.getcwd()
        os.chdir(self.base_cwd+"/"+self.station_name+"/")
        thedir = self.station_name
        directories =  [ name for name in os.listdir(thedir) if os.path.isdir(os.path.join(thedir, name)) ]
        unique_names = set()
        cwd = os.getcwd()
        for i in directories:
            os.chdir(cwd+"/"+i+"/")
            files = glob.glob("extracted_reads_*")
            for file in files:
                unique_names.add(file)
        os.chdir(self.base_cwd)
        return unique_names

    def concatenate(self):

        unique_names = get_unique_among_folders(self.station_name)
        os.chdir(os.getcwd()+"/"+self.station_name+"/")
        thedir = self.station_name
        directories =  [ name for name in os.listdir(thedir) if os.path.isdir(os.path.join(thedir, name)) ]
        reads_in_memory = {}
        for name in unique_names:
            reads_in_memory[name] = []
        cwd = os.getcwd()
        for i in directories:
            os.chdir(cwd+"/"+i+"/")
            files = glob.glob("extracted_reads_*")
            if files == 0:
                print "   [ERROR] There is no files. Check folders"
            for file in files:
                for record in SeqIO.parse(file, ext):
                    reads_in_memory[file].append(record)
        os.chdir(self.base_cwd)
        os.chdir(os.getcwd()+"/"+self.station_name+"/")
        for key in reads_in_memory:
            SeqIO.write(reads_in_memory[key], "all_"+key, ext)
            print "Writing "+key


if __name__ == "__main__":

    import os
    from time import gmtime, strftime
    import sys
    import argparse
    import glob
    from Bio import SeqIO

    description = """

Version 1.0

If you have any questions, please do not hesitate to contact me
email address: michal.karlicki@gmail.com
"""

    epilog = """

"""


    parser = argparse.ArgumentParser(
                    description=description,
                    formatter_class=argparse.RawDescriptionHelpFormatter,
                    epilog=epilog)



    parser.add_argument('extension', metavar='extension', type=str)
    parser.add_argument('station_name', metavar='station_name', type=str)



    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    start = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    concatenate(args.extension,args.station_name)
    end = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    print "Starting time: "+start
    print "Ending time: "+end