#!/usr/bin/python

import sys, getopt, os, argparse

def combine_gene_sequences(filenames, dir_name):
	""" (list of str, str) -> list of str
		Combines the gene sequences from all the files in 
		a given directory into a single file based on gene type.
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
				gene_types = name_gene[1]
			else:
				gene_sequence += line.strip()

		formated_sequence = ">" + name + "\n" + gene_sequence + "\n"


		for gene_type in gene_types:
			gene_type = gene_type + ".fas"
			if gene_type not in gene_sequences.keys():
				gene_sequences[gene_type] = [formated_sequence]
			else:
				gene_sequences[gene_type].append(formated_sequence)

		input_file.close()


	write_genes(gene_sequences)



	return gene_sequences.keys()

def parse_header(header):
	""" (str) -> tuple
		Parses the header of a fasta file, retrieving the genus, 
		species name, and the gene type for a single gene sequence.
	"""
	header = header.split()
	header.pop(0)

	header = clean(header)

	name = get_name(header)

	genes = get_genes(header)

	return (name, genes)

def clean(header):
	""" (list of str) -> str
		Cleans each item in the header list of trailing puncuation,
		and brackets, and returns a new list. 
	"""

	clean_header = []

	for item in header:
		item = item.strip()
		if item[0] == "(":
			item = item[1:]
		if item[-1] == ")":
			item = item[:-1]
		if "," in item:
			item = item.replace(',', '')
		clean_header.append(item.strip())

	return clean_header

def get_name(header):
	""" (list of str) -> str
		Gets the genus name, species name, and sub-species name if it exists. 
	"""

	name = header[0] + "_" + header[1]

	if header[2] not in ["voucher", "isolate", "strain", "cytochrome", "clone", "interphotoreceptor", \
	"mitochondrial", "specimen-voucher", "IRBP"] and not any(char.isdigit() for char in header[2]):
		name += "_" + header[2]

	return name

def get_genes(header):
	""" (list of str) -> list of str
		Gets the gene type and equalizes based on known variables and conventions. 
	"""

	genes = []

	gene_indices = [i for i, item in enumerate(header) if item == "gene"]

	for gene_index in gene_indices:
		if "mitochondrial" != header[gene_index - 1]:
			gene = header[gene_index - 1]
			gene = gene.upper()
			if "X" in gene:
				gene = gene.replace("X", "")
			if "1" in gene:
				gene = gene.replace("1", "I")
			if "2" in gene:
				gene = gene.replace("2", "II")
			genes.append(gene)

	return genes

def write_genes(gene_sequences):
	""" (dictionary) -> NoneType
		Write each line of the species name and genes to an output file.
	"""

	for gene_type in gene_sequences.keys():

		output_file = open("unaligned_gene_files/" + gene_type, "w")

		for species in gene_sequences[gene_type]:
			output_file.write(species)

		output_file.close()

# if __name__ == '__main__':
# 	parser = argparse.ArgumentParser(description='Combines single gene files into a combined fasta file.')
# 	parser.add_argument('files', metavar='S', nargs='+',
#                    help='A directory containing files with a single gene sequence')
# 	args = parser.parse_args()
# 	input_file_list = os.listdir(sys.argv[1])


# 	# Check for '.DS_Store' on Macs
# 	if '.DS_Store' in input_file_list:
# 		input_file_list.remove('.DS_Store')

# 	gene_types = combine_gene_sequences(input_file_list, sys.argv[1])

