#!/usr/bin/python

import collections, gene_matrix, sys, getopt, os, argparse

def format(filenames, input_dir, output_dir):
	""" (str) -> NoneType
		Formats a fasta file for that each gene is displayed 
		over only a single line. 
	"""

	for filename in filenames:

		gene_sequences = []

		input_file = open(input_dir + filename, 'r')

		output_file = open(output_dir + filename, "w")

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

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Formats a fasta file with multiple genes so that the genes display over only one line.')
	parser.add_argument('files', metavar='S', nargs='+',
                   help='A directory containing files with the same amount of gene sequences')
	args = parser.parse_args()
	input_dir = sys.argv[1]
	output_dir = sys.argv[2]
	filenames = os.listdir(input_dir)
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	if input_dir[-1] != "/":
		input_dir += "/"
	if output_dir[-1] != "/":
		output_dir += "/"

	# Check for '.DS_Store' on Macs
	if '.DS_Store' in filenames:
		filenames.remove('.DS_Store')

	sys.stdout.write("Formatting files.\n")
	format(filenames, input_dir, output_dir)
	sys.stdout.write("Formatting successful.\n")