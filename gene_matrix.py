#!/usr/bin/python

import sys, getopt, os, argparse

def concat_species_genes(filenames, dir_name, flag, filename):
	""" (list of strings), str, str -> NoneType
			Precondition: Each line with a species name is prefaced with a '>' 
			character, and one gene is on the following line. 
		Take in a list of filenames and for each new species concatenate all 
		their genes. Then write each gene to the output file properly formatted. 
	"""

	# Build a dictionary of species names and genes
	names = build_species_dict(filenames, dir_name)
	header = ""

	# Format names
	if flag == 'nexus':
		header = create_nexus_header(names, filename)
		formatted_names = format_names_nexus(names, filename)
	elif flag == 'fasta':
		formatted_names = format_names_fasta(names)
	elif flag == 'phylip':
		header = create_phy_header(names, filename)
		formatted_names = format_names_fasta(names)
	
	formatted_names.sort()

	# Write each species and gene line to an ouput text file.
	write_genes(formatted_names, flag, filename, header)

def build_species_dict(filenames, dir_name):
	""" (list of strings, string) -> dictionary
		Builds a dictionary where the key is the name of the species and 
		the value is the concatentation of all the genes associated with 
		that species. 
	"""
	names = {}
	name = ''
	num_names = 0
	
	# Go through the file and concat all the genes associated to a species name
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

		# Raise an exception if all of the files don't have the same amount of species names, 
		# which may suggest that there may be a spelling error on one of the names.
		if filename == filenames[0]:
			num_names = len(names.keys())
		elif num_names != len(names.keys()):
			raise ValueError('One of the species names may be misspelled, or have a different number of species names in ' + filename)

		input_file.close()

	return names

def format_names_nexus(names, filename):
	""" (dictionary) -> list
		Format each species name and genes into a single line.
	"""
	
	formatted_names = []

	longest_name_len = longest_name(names.keys()) + 5 # Extra spacing

	for key, value in names.items():
		# Add the appropiate amount of spaces between the species name 
		# and gene so that all the genes line up. 
		num_spaces = longest_name_len - len(key)

		formatted_name = key.strip() + (num_spaces * ' ') + value.strip() + '\n'
		formatted_names.append(formatted_name)

	return formatted_names

def format_names_phy(names, filename):
	""" (dictionary) -> list
		Format each species name and genes into a single line.
	"""
	
	formatted_names = []

	for key, value in names.items():
		# Add the appropiate amount of spaces between the species name 
		# and gene so that all the genes line up. 
		num_spaces = longest_name_len - len(key)

		formatted_name = key.strip() + ' ' + value.strip() + '\n'
		formatted_names.append(formatted_name)

	return formatted_names

def create_nexus_header(names, filename):

	header_format = "#NEXUS\n[TITLE: {0} ]\n\nbegin data;\ndimensions ntax={1} nchar={2};\nformat datatype=DNA missing=N gap=- interleave=yes;\n\nMatrix\n"

	return header_format.format(filename, len(names.keys()), len(next(names.itervalues())))

def create_phy_header(names, filename):

	return " {0} {1}\n".format(len(names.keys()), len(next(names.itervalues())))

def format_names_fasta(names):
	""" (dictionary) -> list
		Format each species name and genes into fasta format.
	"""
	
	formatted_names = []

	for key, value in names.items():

		formatted_name = '>' + key.strip() + '\n' + value.strip() + '\n'
		formatted_names.append(formatted_name)

	return formatted_names

def longest_name(names):
	""" (list of strings) -> len
		Find the length of the longest_name in a list.
	"""

	longest_name = 0

	for name in names:
		if len(name) > longest_name:
			longest_name = len(name)

	return longest_name

def write_genes(names, flag, filename, header):
	""" (list of strings, string) -> NoneType
		Write each line of the species name and genes to an output_file.
	"""

	if flag == 'fasta':
		output_file = open(filename + ".fas", 'w') 
	elif flag == 'nexus':
		output_file = open(filename + ".nex", 'w') 
	elif flag == 'phylip':
		output_file = open(filename + ".phy", 'w') 

	output_file.write(header)

	for name in names:
		output_file.write(name)

	if flag == 'nexus':
		# For fasta file endings
		output_file.write(";")

	output_file.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Builds gene super matrix.')
	parser.add_argument('files', metavar='S', nargs='+',
                   help='A directory containing files with gene sequences')
	parser.add_argument('--type', help='Sepcify output file type [fasta, nexus, phylip]')
	parser.add_argument('--o', help='Sepcify output file name (default=output.fas')
	args = parser.parse_args()
	input_file_list = os.listdir(sys.argv[1])

	if args.o is None:
		args.o = 'output'
	if args.type is None:
		args.type = 'fasta'

	# Check for '.DS_Store'
	if '.DS_Store' in input_file_list:
		input_file_list.remove('.DS_Store')

	concat_species_genes(input_file_list, sys.argv[1], args.type, args.o)
