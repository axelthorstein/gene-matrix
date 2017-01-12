#!/usr/bin/python

import sys, getopt, os, argparse

def concat_species_genes(filenames, dir_name, flag):
	""" (list of strings), str, str -> NoneType
			Precondition: Each line with a species name is prefaced with a '>' 
			character, and one gene is on the following line. 
		Take in a list of filenames and for each new species concatenate all 
		their genes. Then write each gene to the output file properly formatted. 
	"""

	# Build a dictionary of species names and genes
	names = build_species_dict(filenames, dir_name)

	# Format names
	if flag == '-t':
		formatted_names = format_names_txt(names)
	elif flag == '-f':
		formatted_names = format_names_fasta(names)
	
	formatted_names.sort()

	# Write each species and gene line to an ouput text file.
	write_genes(formatted_names, flag)

def build_species_dict(filenames, dir_name):
	""" (list of strings) -> dictionary
		Builds a dictionary where the key is the name of the species and 
		the value is the concatentation of all the genes associated with 
		that species. 
	"""
	names = {}
	name = ''
	
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

		input_file.close()

	return names

def format_names_txt(names):
	""" (dictionary) -> list
		Format each species name and genes into a single line.
	"""
	
	formatted_names = []

	longest_name_len = longest_name(names.keys()) + 10 # Extra spacing

	for key, value in names.items():
		# Add the appropiate amount of spaces between the species name 
		# and gene so that all the genes line up. 
		num_spaces = longest_name_len - len(key)

		formatted_name = key.strip() + (num_spaces * ' ') + value.strip() + '\n'
		formatted_names.append(formatted_name)

	return formatted_names

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

def write_genes(names, flag):
	""" (list of strings), string -> NoneType
		Write each line of the species name and genes to an output_file.
	"""

	if flag == '-f':
		output_file = open("output.fas", 'w') 
	elif flag == '-t':
		output_file = open("output.txt", 'w') 
	for name in names:
		output_file.write(name)

	output_file.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Builds gene super matrix.')
	parser.add_argument('files', metavar='S', nargs='+',
                   help='A file containing gene sequences')
	parser.add_argument('--f', help='Sepcify output file type fasta', action="store_true")
	parser.add_argument('--t', help='Sepcify output file type txt (default)', action="store_true")
	args = parser.parse_args()
	input_file_list = os.listdir(sys.argv[1])

	flag = '-t'

	if args.f:
		flag = '-f'

	# Check for '.DS_Store'
	if '.DS_Store' in input_file_list:
		input_file_list.remove('.DS_Store')

	concat_species_genes(input_file_list, sys.argv[1], flag)
