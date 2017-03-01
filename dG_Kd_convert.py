#!/usr/bin/env python

"""
Convert between Kd and dG values
Assumes an R value of 0.0019858775 kcal/(mol*K)

Inputs:
   type of conversion, value to convert from, temperature

Outputs:
   converted value

Ben Ober-Reynolds
"""



import os
import sys
import argparse
import numpy as np

def main():
    ################ Parse input parameters ################

    #set up command line argument parser
    parser = argparse.ArgumentParser(description='script for converting between Kd and dG and vice versa')
    group = parser.add_argument_group('required arguments:')
    group.add_argument('-ct', '--conversion_type', required=True,
                        help='what type of conversion you want to do (type "dG" for dG_to_Kd, and type "Kd" for Kd_to_dG)')
    group.add_argument('-v', '--value', required=True,
                        help='value you want to convert. Provide Kd in nM and dG in kcal/mol')
    group.add_argument('-t', '--temp', required=True,
                        help='what temperature you want to use (in Celsius)')

    # print help if no arguments provided
    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit()
    
    #parse command line arguments
    args = parser.parse_args()
    args.value = float(args.value)
    K_temp = float(args.temp) + 273

    R_val = 0.0019858775 # in kcal / mol*K 

    if args.conversion_type == 'dG':
    	nM_val = 1/(dG_to_Kd(args.value, K_temp, R_val) / 10**9)
    	print "A dG of {} kcal/mol at {}C gives a Kd of {} nM".format(args.value, args.temp, nM_val)
    elif args.conversion_type == 'Kd':
    	mol_Val = 1/(args.value / 10**9)
    	print "A Kd of {} nM gives a dG of {} kcal/mol".format(args.value, args.temp, Kd_to_dG(mol_Val, K_temp, R_val))
    else:	
    	print "invalid conversion type given (type 'dG' for dG_to_Kd or 'Kd' for Kd_to_dG)"





    
def dG_to_Kd(dG, temp, R_val):
	return np.exp(-dG/(R_val*temp))

def Kd_to_dG(Kd, temp, R_val):
	return -R_val*temp*np.log(Kd)



if __name__ == '__main__':
    main()