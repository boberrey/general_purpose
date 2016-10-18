#!/usr/bin/env python
""" 
Read in a pickled file and copy it as a csv

Inputs:
	pickled file

Outputs:
    csv

Ben Ober-Reynolds, boberrey@stanford.edu
20161018
"""

import pandas as pd
import argparse
import os
import sys

def main():
	################ Parse input parameters ################

	#set up command line argument parser
	parser = argparse.ArgumentParser(description='Script for converting a pickle file to csv')
	group = parser.add_argument_group('required arguments')
	group.add_argument('-p', '--pickle_file', required=True,
	                    help='The pickle file that you want to read')
	group = parser.add_argument_group('optional arguments')
	group.add_argument('-od','--output_directory', default="",
	                    help='output directory for the new csv. Default is same directory as pickle file.')
	group.add_argument('-fn','--filename', default="",
	                    help='filename for the new csv file. Default is the old file name.')
	if not len(sys.argv) > 1:
		parser.print_help()
		sys.exit()
	#parse command line arguments
	args = parser.parse_args()

	# Set path
	output_dir = ""
	if args.output_directory == "":
		output_dir = os.path.dirname(os.path.abspath(args.pickle_file))
	else:
		output_dir = args.output_directory

	# Prepare new file name
	filename = ""
	if args.filename == "":
		filename = os.path.splitext(os.path.basename(args.pickle_file))[0] + ".csv"
	else:
		filename = args.filename

	# Read data in
	df = pd.read_pickle(args.pickle_file)

	# Print data out
	df.to_csv(output_dir + "/" + filename)



if __name__ == '__main__':
    main()