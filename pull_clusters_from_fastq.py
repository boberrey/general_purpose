#!/usr/bin/env python

"""
Pull specific clusters from fastq file

Inputs:
   file containing list of clusters to isolate
   directory of fastq files

Outputs:
   filtered fastq files

Ben Ober-Reynolds
"""



import os
import sys
import argparse
import numpy as np
from joblib import Parallel, delayed

def main():
    ################ Parse input parameters ################

    #set up command line argument parser
    parser = argparse.ArgumentParser(description='script for isolating specific clusters from fastq files')
    group = parser.add_argument_group('required arguments:')
    group.add_argument('-cl', '--cluster_list', required=True,
                        help='file containing list of clusters to select')
    group.add_argument('-fd', '--fastq_directory', required=True,
                        help='directory containing fastq files')
    group = parser.add_argument_group('optional arguments')
    group.add_argument('-od','--output_directory', default="",
                        help='output directory for filtered fastq files (default is original fastq_directory')
    group.add_argument('-op','--output_prefix', default="",
                        help='output prefix for filtered fastq files (default is cluster list filename')
    group.add_argument('-n','--num_cores', type=int, default=1,
                        help='number of cores to use (should be same as number of fastq files)')

    # print help if no arguments provided
    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit()

    #parse command line arguments
    args = parser.parse_args()

    fastq_dir = args.fastq_directory
    if not os.path.isdir(fastq_dir):
        print "Error: invalid fastq directory selection. Exiting..."
        sys.exit()
    # If no output directory given, use input directory
    output_dir = args.output_directory
    if output_dir == "":
        output_dir = fastq_dir
    if not os.path.isdir(output_dir):
        print "Error: invalid output directory selection. Exiting..."
        sys.exit()
    # If no prefix is given, use cluster list filename
    output_prefix = args.output_prefix
    if output_prefix == "":
        output_prefix = os.path.splitext(os.path.basename(args.cluster_list))[0]

    numCores = args.num_cores

    # Gather fastq files:
    fastq_list = find_files_in_directory(fastq_dir, extensionList=['.fastq'])

    # Make set of clusters to compare against:
    cluster_set = get_clusters_to_keep(args.cluster_list)

    # make dict of fastqs keyed by read information
    fastq_dict = make_fastq_dict(fastq_list)
    
    # loop thorugh fastq files in parallel or in sequence
    results = []
    if numCores > 1:
        results = (Parallel(n_jobs=numCores, verbose = 10)(delayed(filter_fastq)(cluster_set, 
            fastq_dict[key], key, output_prefix, output_dir) for key in fastq_dict.keys()))
    else:
        results = [filter_fastq(cluster_set, 
            fastq_dict[key], key, output_prefix, output_dir) for key in fastq_dict.keys()]

    # Report results of filtering:
    for result in results:
        print "file {} has {} clusters, filtered down from {}".format(result[0], result[1], result[2])



def find_files_in_directory(dirPath, extensionList=None, 
                            excludedExtensionList=None):
    """
    Locate files in a given directory path. Optionally, desired files are 
    identified as matching one of the extension types provided in 
    'extensionList'
    Input: directory path, list of approved extensions, (list of excluded extensions)
    Output: List of found files 
    """
    def extension_match(filename, extensionList=None):
        # from CPlibs
        if extensionList is not None:
            for currExt in extensionList:
                if filename.lower().endswith(currExt.lower()):
                    return True
        return False

    dirList = os.listdir(dirPath)
    fileList = []
    for currFilename in dirList:
        if (extension_match(currFilename, extensionList) 
            and not extension_match(currFilename, excludedExtensionList)):
            fileList.append(dirPath+currFilename)
    if len(dirList) == 0:
        print '\tNONE FOUND'
    else:
        for filename in fileList:
            print "found:\t\t{}".format(filename)
        return fileList


def get_clusters_to_keep(filename):
    """
    Generate a set of clusters extracted from a provided filename
    Input: filename
    Output: set of clusters
    """
    cluster_list = []
    with open(filename, 'r') as f:
        for line in f:
            cluster_list.append(line.strip())
    return set(cluster_list)

def make_fastq_dict(fastq_list):
    """
    Make a dictionary of fastq files keyed by read information
    """
    fastq_dict = {}
    for filename in fastq_list:
        identifier = '_'.join(os.path.splitext(filename)[0].split('_')[1:])
        fastq_dict[identifier] = filename
    return fastq_dict


def filter_fastq(filter_set, fastq_filename, identifier, output_prefix, output_dir):
    """
    filter a fastq file by clusters that exist in the cluster set, then
    save the filtered file as a new file
    Input: filter_set, fastq_filename, fastq_identifier, output_prefix
    Output: saved filtered file
    """
    # Example fastq format:
    # @M00653:218:000000000-AYC5G:1:1101:20964:1096 1:N:0:1
    # CNTATAATGATTCTTATTGACCAAAAAGCTGACAATTCACTTATTTTGCTTGACTATTTATTATACTTTCATCATA
    # +
    # C#8BCGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGFGGGGGGGGGGGG
    filtered_lines = []

    # get the total number of lines:
    total_lines = 0
    with open(fastq_filename, 'r') as f:
        for line in f:
            total_lines += 1
    num_clusters = total_lines/4
    cluster_count = 0
    # Loop through file in chunks of four lines:
    with open(fastq_filename, 'r') as f:
        for chunk in range(num_clusters):
            cluster = f.readline()
            seq = f.readline()
            spacer = f.readline()
            qual_score = f.readline()

            if cluster[1:].split()[0] in filter_set:
                cluster_count += 1
                filtered_lines.extend([cluster, seq, spacer, qual_score])
    new_filename = output_dir+output_prefix+'_'+identifier+'.fastq'
    with open(new_filename, 'w') as f:
        for line in filtered_lines:
            f.write(line)
    # return the new filename, the starting number of clusters,
    # and the number of clusters kept
    return [new_filename, cluster_count, num_clusters]






if __name__ == '__main__':
    main()