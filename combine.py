#!/usr/bin/python

import sys, getopt, os, argparse, format
from subprocess import call

def combine_gene_sequences(filenames, dir_name):
	""" (list of str, str, str) -> list of str
		
	"""

	gene_sequences = {}

	for filename in filenames:
		


		input_file = open(dir_name + '/' + filename, 'r')
		lines = input_file.readlines()

		gene_sequence = ""

		for line in lines:
			if line[0] == ">":
				name_gene = parse_header(line)
				name = name_gene[0]
				gene_type = name_gene[1]
			else:
				gene_sequence += line.strip()

		formated_sequence = ">" + name + "\n" + gene_sequence + "\n"


		if gene_type not in gene_sequences.keys():
			gene_sequences[gene_type] = [formated_sequence]
		else:
			gene_sequences[gene_type].append(formated_sequence)

		input_file.close()


	write_genes(gene_sequences)

	return gene_sequences.keys()

def parse_header(header):
	""" (str) -> list of str
		
	"""
	header = header.split()
	header.pop(0)

	header = clean(header)

	name = get_name(header)

	gene = get_gene(header)

	return (name, gene)

def clean(header):

	clean_header = []

	for item in header:
		item = item.strip()
		if item[0] == "(" and item[-1] == ")":
			item = item[1:-1]
		clean_header.append(item.strip())

	return clean_header

def get_name(header):

	name = header[0] + " " + header[1]

	if header[2] != "voucher" and header[2] != "isolate" and not any(char.isdigit() for char in header[2]):
		name += " " + header[2]

	return name

def get_gene(header):

	gene_index = header.index("gene,")

	gene = header[gene_index - 1]

	# remove the variable
	if "X" in gene:
		gene = gene.replace("X", "")
	if "1" in gene:
		gene = gene.replace("1", "I")

	return gene

def write_genes(gene_sequences):
	""" (dictionary) -> NoneType
		Write each line of the species name and genes to an output_file.
	"""

	for gene_type in gene_sequences.keys():

		output_file = open(gene_type + ".fasta", "w")

		for species in gene_sequences[gene_type]:
			output_file.write(species)

		output_file.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Combines single gene files into a combined fasta file.')
	parser.add_argument('files', metavar='S', nargs='+',
                   help='A directory containing files with a single gene sequence')
	args = parser.parse_args()
	input_file_list = os.listdir(sys.argv[1])


	# Check for '.DS_Store' on Macs
	if '.DS_Store' in input_file_list:
		input_file_list.remove('.DS_Store')

	gene_types = combine_gene_sequences(input_file_list, sys.argv[1])

	for gene_type in gene_types:
		call(["./muscle", "-in", gene_type + ".fasta",  "-out", gene_type + "_aligned.fasta"])
		format.format(gene_type + "_aligned.fasta")

