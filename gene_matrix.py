#!/usr/bin/python

import sys, getopt, os, argparse

def concat_species_genes(filenames, dir_name, file_type, filename):
	""" (list of str, str, str, str) -> NoneType
		Take in a list of filenames and for each new species concatenate all 
		their genes. Then write each gene to the output file properly formatted. 
	"""

	header = ""

	# Build a dictionary of species names and genes
	names = build_species_dict(filenames, dir_name)

	num_species = len(names.keys())
	gene_length = len(next(names.itervalues()))

	# Format names
	if file_type == 'fasta':
		formatted_names = format_names("fasta", names)
	elif file_type == 'nexus':
		header = create_header("#NEXUS\n[TITLE: {0} ]\n\nbegin data;\
			\ndimensions ntax={1} nchar={2};\
			\nformat datatype=DNA missing=N gap=- interleave=yes;\
			\n\nMatrix\n", 
		num_species, 
		gene_length,
		filename)
		formatted_names = format_names("nexus", names)
	elif file_type == 'phylip':
		header = create_header(" {0} {1}\n", num_species, gene_length)
		formatted_names = format_names("phylip", names)
	
	formatted_names.sort()

	# Write each species and gene line to an ouput text file.
	write_genes(formatted_names, file_type, filename, header)

def build_species_dict(filenames, dir_name):
	""" (list of str, str) -> dictionary
		Builds a dictionary where the key is the name of the species and 
		the value is the concatentation of all the genes associated with 
		that species. 
	"""
	names = {}
	name = ''
	num_names = 0
	
	# Concatenate all the genes associated to a species name
	for filename in filenames:

		input_file = open(dir_name + '/' + filename, 'r')
		lines = input_file.readlines()

		for line in lines:

			if line[0] == '>': 
				name = line[1:]
				if name not in names:
					names[name] = ''
			else:
				names[name] += line.strip()

		num_names = check_species_amount(names, filenames, filename, num_names)

		input_file.close()

	return names

def check_species_amount(names, filenames, filename, num_names):
	""" (dict, list of str, str) -> int
		Raise an exception if all of the files don't have the same amount
		 of species names, which may suggest that there may be a spelling 
		 error on one of the names. Otherwise return the number of species.
	"""

	if filename == filenames[0]:
		num_names = len(names.keys())
	elif num_names != len(names.keys()):
		raise ValueError('One of the species names may be misspelled,\
		 or have a different number of species names in ' + filename)

	return num_names

def format_names(file_type, names):
	""" (dictionary) -> list
		Format each species name and genes.
	"""

	formatted_names = []

	if file_type == 'fasta':
		front = '>'
		space = '\n'

	elif file_type == 'nexus':
		front = ''
		longest_name_len = longest_name(names.keys()) + 5

	elif file_type == 'phylip':
		front = ''
		space = ' '
		
	for key, value in names.items():

		if file_type == 'nexus':
			space = (longest_name_len - len(key)) * ' '

		formatted_name = front + key.strip() + space + value.strip() + '\n'
		formatted_names.append(formatted_name)

	return formatted_names

def create_header(header_format, num_species, gene_length, filename=None):
	""" (dict, str) -> str
		Return the file header. 
	"""

	if filename:
		header = header_format.format(filename, num_species, gene_length)
	else:
		header = header_format.format(num_species, gene_length)

	return header

def longest_name(names):
	""" (list of str) -> int
		Find the length of the longest_name in a list.
	"""

	longest_name = 0

	for name in names:
		if len(name) > longest_name:
			longest_name = len(name)

	return longest_name

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
		# For fasta file endings
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
