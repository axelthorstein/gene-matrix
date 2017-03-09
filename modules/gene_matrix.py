#!/usr/bin/python

import sys, getopt, os, argparse, collections
from modules import spellcheck

def concat_species_genes(filenames, dir_name, file_type, filename, header_info):
	""" (list of str, str, str, str) -> NoneType
		Take in a list of filenames and for each new species concatenate all 
		their genes. Then write each gene to the output file properly formatted. 
	"""

	# Build a dictionary of species names and genes
	names = build_species_dict(filenames, dir_name, append_species)

	# Check species name spelling. 
	spellcheck.misspelled_check(filenames, dir_name)

	# Create Headers
	header = create_headers(names, file_type, filename, header_info)

	# Format names
	formatted_names = format_names(names, file_type)
	formatted_names.sort()

	# Write each species and gene line to an ouput text file.
	write_genes(formatted_names, file_type, filename, header)

def build_species_dict(filenames, dir_name, species_func):
	""" (list of str, str) -> dictionary
		Builds a dictionary based on all of the species in 
		gene sequence fasta files. 
	"""

	species = {}

	# Concatenate all the genes associated to a species name. 
	for filename in filenames:

		input_file = open(dir_name + '/' + filename, 'r')
		lines = input_file.readlines()

		species = species_func(filename, lines, species)

		input_file.close()

	return species

def species_occurences(filename, lines, species_occurences):
	""" (str, list of str, dictionary) -> dictionary
		Builds a dictionary where the key is the name of the species and 
		the value is the number of occurences across all files and
		the filenames in which it is found. 
	"""

	for line in lines:

		if line[0] == ">":
			species = line[1:].strip()

		if species not in species_occurences:
			species_occurences[species] = [1, [filename]]
		elif line[0] == ">":
			species_occurences[species][0] += 1
			species_occurences[species][1].append(filename)

	return species_occurences

def append_species(filename, lines, names):
	""" (dictionary, str) -> NoneType
		Appends all of the species and genes from one file to a dictionary. 
		Returns a list that holds all the occurences of a species. 
	"""

	for line in lines:

		if line[0] == ">":
			name = line[1:].strip()

		if name not in names:
			names[name] = ""
		elif line[0] != ">":
			names[name] += line.strip()

	return names

def create_headers(names, file_type, filename, header_info):
	""" (dict, str, str) -> str
		Return the corresponding file header for the specified file type. 
	"""

	num_species = len(names.keys())
	gene_length = len(next(iter(names.values())))

	if file_type == 'nexus':
		if header_info:
			header_info = header_info.split(" ")
			header_format = "#NEXUS\n[TITLE: {0} ]\n\nbegin data;\ndimensions ntax={1} nchar={2};" + \
				"\nformat datatype={0} missing={1} gap={2} interleave={3};\n\nMatrix\n".format(
				header_info[0], header_info[1], header_info[2], header_info[3])
		else:
			header_format = "#NEXUS\n[TITLE: {0} ]\n\nbegin data;\ndimensions ntax={1} nchar={2};\
				\nformat datatype=DNA missing=N gap=- interleave=yes;\n\nMatrix\n"
		header = create_header(header_format, num_species, gene_length, filename)
	elif file_type == 'phylip':
		header = create_header(" {0} {1}\n", num_species, gene_length)
	else:
		header = ""

	return header

def create_header(header_format, num_species, gene_length, filename=None):
	""" (dict, str) -> str
		Return the file header. 
	"""

	if filename:
		header = header_format.format(filename, num_species, gene_length)
	else:
		header = header_format.format(num_species, gene_length)

	return header

def format_names(names, file_type):
	""" (dictionary) -> list
		Format each species name and genes.
	"""

	if file_type == 'fasta':
		front = '>'
		space = '\n'

	elif file_type == 'nexus':
		front = ''
		space = (len(max(names, key=len)) + 5) *  ' '

	elif file_type == 'phylip':
		front = ''
		space = ' '
		
	return create_names_list(names, file_type, front, space)

def create_names_list(names, file_type, front, space):
	""" (dictionary) -> list
		Combine the newly formatted name and gene string pairs into a list.
	"""
	nexus_space = space
	formatted_names = []

	for key, value in names.items():

		if file_type == 'nexus':
			space = nexus_space[len(key):]

		formatted_name = front + key + space + value + '\n'
		formatted_names.append(formatted_name)

	return formatted_names


def open_file(file_type, filename):
	""" (str, str) -> file
		Open a new file of the correct type. 
	"""

	if file_type == 'fasta':
		output_file = open(filename + ".fas", 'w') 
	elif file_type == 'nexus':
		output_file = open(filename + ".nex", 'w') 
	elif file_type == 'phylip':
		output_file = open(filename + ".phy", 'w') 

	return output_file

def write_genes(names, file_type, filename, header):
	""" (list of str, str, str, str) -> NoneType
		Write each line of the species name and genes to an output_file.
	"""

	output_file = open_file(file_type, filename)

	output_file.write(header)

	for name in names:
		output_file.write(name)

	if file_type == 'nexus':
		# For nexus file endings
		output_file.write(";")

	output_file.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Builds gene super matrix.')
	parser.add_argument('files', metavar='S', nargs='+',
                   help='A directory containing files with gene sequences')
	parser.add_argument('--type', choices=["fasta", "nexus", "phylip"], 
		help='Sepcify output file type [fasta, nexus, phylip]')
	parser.add_argument('--o', 
		help='Sepcify output file name (default=output.fas)')
	args = parser.parse_args()
	input_file_list = os.listdir(sys.argv[1])

	if args.o is None:
		args.o = 'output'
	if args.type is None:
		args.type = 'fasta'

	# Check for '.DS_Store' on Macs
	if '.DS_Store' in input_file_list:
		input_file_list.remove('.DS_Store')

	concat_species_genes(input_file_list, sys.argv[1], args.type, args.o)
