#!/usr/bin/python

import sys, getopt, os, argparse

def combine_gene_sequences(filenames, dir_name, output_name):
	""" (list of str, str, str) -> NoneType
		
	"""

	for filename in filenames:

		input_file = open(dir_name + '/' + filename, 'r')
		lines = input_file.readlines()

		gene = ""

		for line in lines:
			if line[0] == ">":
				name = line
			else:
				gene += line.strip()
		print(name + gene)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Combines single gene files into a combined fasta file.')
	parser.add_argument('files', metavar='S', nargs='+',
                   help='A directory containing files with a single gene sequence')
	parser.add_argument('--o', 
		help='Sepcify output file name (default=output.fas)')
	args = parser.parse_args()
	input_file_list = os.listdir(sys.argv[1])

	if args.o is None:
		args.o = 'output'

	# Check for '.DS_Store' on Macs
	if '.DS_Store' in input_file_list:
		input_file_list.remove('.DS_Store')

	combine_gene_sequences(input_file_list, sys.argv[1], args.o)
