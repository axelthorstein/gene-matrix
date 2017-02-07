#!/usr/bin/python

import sys, getopt, os, argparse

def format(filename):
	""" (list of str, str, str) -> NoneType
		
	"""

	gene_sequences = []

	input_file = open(filename, 'r')

	output_filename = filename[0:-6] + "_formatted.fas"
	output_file = open(output_filename, "w")

	lines = input_file.readlines()

	gene_sequence = ""
	first = True

	for line in lines:
		if line[0] == ">":
			if first:
				gene_sequence += line
				first = False
			else:
				gene_sequence += "\n" + line
		else:
			gene_sequence += line.strip()

	output_file.write(gene_sequence + "\n")

	input_file.close()
	output_file.close()


# if __name__ == '__main__':
# 	parser = argparse.ArgumentParser(description='Combines single gene files into a combined fasta file.')
# 	parser.add_argument('files', metavar='S', nargs='+',
#                    help='A directory containing files with a single gene sequence')
# 	args = parser.parse_args()
# 	format(sys.argv[1])
