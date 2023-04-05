#!/usr/bin/python3

import argparse
import os
import sys

import pandas as pd


def process_arguments(args):
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('csv_file', type=str,
                        help="The path to the CSV file (ID, path)")

    parser.add_argument('output_directory', type=str,
                        help="output directory")

    parser.add_argument('rowsize', type=int,
                        help="number of rows in each csv file")

    return parser.parse_args(args)


params = process_arguments(sys.argv[1:])

#csv file name to be read in 
in_csv = params.csv_file

if not os.path.exists(params.output_directory):
  os.makedirs(params.output_directory)

#get the number of lines of the csv file to be read
number_lines = sum(1 for row in (open(in_csv)))

#size of rows of data to write to the csv, 
#you can change the row size according to your need
rowsize = params.rowsize

#start looping through data writing it to a new file for each set
for i in range(1,number_lines,rowsize):
    df = pd.read_csv(in_csv,
          header=None,
          nrows = rowsize,#number of rows to read at each loop
          skiprows = i)#skip rows that have been read
    #csv to write data to a new file with indexed name. input_1.csv etc.
    out_csv = params.output_directory + os.sep + 'input' + str(i) + '.csv'
    df.to_csv(out_csv,
          index=False,
          header=False,
          mode='a',#append data to csv file
          chunksize=rowsize)#size of data to append for each loop