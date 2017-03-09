#!/usr/bin/python

import sys, getopt, os, argparse

def combine_gene_sequences(filenames, input_dir, output_dir, species_parsing):
	""" (list of str, str) -> list of str
		Combines the gene sequences from all the files in 
		a given directory into a single file based on gene type.
	"""

	gene_sequences = {}

	for filename in filenames:

		# Open File
		input_file = open(input_dir + '/' + filename, 'r')
		lines = input_file.readlines()

		# Gather one species information. 
		if species_parsing == "filename":
			species = get_species_info(lines, filename)
		elif species_parsing == "header":
			species = get_species_info(lines, species_parsing)

		# Add the formatted sequence to the dictionary.
		catalogue_sequence(gene_sequences, species[0], species[1])
		input_file.close()

	write_genes(gene_sequences, output_dir)

	return gene_sequences.keys()

def get_species_info(lines, species_parsing):
	""" (list of str) -> tuple
		Get the species name and gene sequence from a single file. 
	"""

	gene_sequence = ""

	for line in lines:
		if line[0] == ">":
			species_info = parse_header(line, species_parsing)
		else:
			gene_sequence += line.strip()

	formated_sequence = ">" + species_info[0] + "\n" + gene_sequence + "\n"

	return (species_info[1], formated_sequence)

def catalogue_sequence(gene_sequences, gene_types, formated_sequence):
	""" (dict, list of str, str) -> NoneType
		For each gene that a species has add the formated sequence to the gene
		sequence dictionary. 
	"""
	# In case one species sequence applies to multiple genes.
	for gene_type in gene_types:
		gene_type = gene_type + ".fas"
		if gene_type not in gene_sequences.keys():
			gene_sequences[gene_type] = [formated_sequence]
		else:
			gene_sequences[gene_type].append(formated_sequence)

def parse_header(header, species_parsing):
	""" (str) -> tuple
		Parses the header of a fasta file, retrieving the genus, 
		species name, and the gene type for a single gene sequence.
	"""
	header = header.split()
	if (any(char.isdigit() for char in header[0])):
		header.pop(0)

	header = clean(header)

	name = get_name(header, species_parsing)

	genes = get_genes(header)

	return (name, genes)

def clean(header):
	""" (list of str) -> str
		Cleans each item in the header list of non-alphanumeric characters. 
	"""

	clean_header = []

	for item in header:
		item = item.replace(',', '')
		item = item.replace(')', '')
		item = item.replace('(', '')
		item = item.replace('|', '')
		item = item.replace(';', '')
		item = item.replace("2", "II")
		item = item.replace("1", "I")
		item = item.replace("X", "")
		clean_header.append(item.strip())

	return clean_header

def get_name(header, species_parsing):
	""" (list of str) -> str
		Gets the genus name, species name, and sub-species name if it exists. 
	"""

	if species_parsing == "header":
		name = header[0] + "_" + header[1]

		if header[2] not in ["voucher", "isolate", "strain", "cytochrome", "clone", "interphotoreceptor", \
		"mitochondrial", "specimen-voucher", "IRBP"] and not any(char.isdigit() for char in header[2]):
			name += "_" + header[2]
	else:
		name = os.path.splitext(os.path.basename(species_parsing))[0].split()
		name = "_".join(name)

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
			genes.append(gene)

	return genes

def write_genes(gene_sequences, output_dir):
	""" (dictionary) -> NoneType
		Write each line of the species name and genes to an output file.
	"""

	for gene_type in gene_sequences.keys():

		output_file = open(output_dir + gene_type, "w")

		for species in gene_sequences[gene_type]:
			output_file.write(species)

		output_file.close()

if __name__ == '__main__':
	print(get_name("header", "Hello world.fasta"))
	# parser = argparse.ArgumentParser(description='Combines single gene files into a combined fasta file.')
	# parser.add_argument('files', metavar='S', nargs='+',
 #                   help='A directory containing files with a single gene sequence')
	# parser.add_argument('--in', 
	# 	help='Sepcify input file name')
	# parser.add_argument('--out', 
	# 	help='Sepcify output file name (default=output.fas)')
	# args = parser.parse_args()

	# input_dir = sys.argv[1]
	# output_dir = sys.argv[2]

	# if input_dir[-1] != "/":
	# 	input_dir += "/"
	# if output_dir[-1] != "/":
	# 	output_dir += "/"

	# filenames = os.listdir(input_dir)
	# if not os.path.exists(output_dir):
	# 	os.makedirs(output_dir)

	# # Check for '.DS_Store' on Macs
	# if '.DS_Store' in filenames:
	# 	filenames.remove('.DS_Store')

	# # Combine the single gene files. 
	# sys.stdout.write("Combining single gene Sequences.\n")
	# gene_types = combine_gene_sequences(filenames, input_dir, output_dir)
	# sys.stdout.write("Combination finished.\n")

