#!/usr/bin/env python
""" 
Read in a pickled file and send it to stdout

Inputs:
	pickled file

Outputs:
   

Ben Ober-Reynolds, boberrey@stanford.edu
20160817
"""

import pandas as pd
import argparse
import sys

def main():
	################ Parse input parameters ################

	#set up command line argument parser
	parser = argparse.ArgumentParser(description='Script for easily reading a pickled file')
	group = parser.add_argument_group('required arguments')
	group.add_argument('-p', '--pickle_file', required=True,
	                    help='The pickle file that you want to read')
	if not len(sys.argv) > 1:
		parser.print_help()
		sys.exit()
	#parse command line arguments
	args = parser.parse_args()

	# Read data in
	df = pd.read_pickle(args.pickle_file)

	# Print data out
	df.to_csv(sys.stdout, sep="\t", na_rep='NA')



if __name__ == '__main__':
    main()