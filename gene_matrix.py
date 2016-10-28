#!/usr/bin/python

import sys, getopt
import argparse

def concat_species_genes(filenames):
	""" (list of strings) -> NoneType
			Precondition: Each line with a species name is prefaced with a '>' 
			character, and one gene is on the following line. 
		Take in a list of filenames and for each new species concatenate all 
		their genes. Then write each gene to the output file properly formatted. 
	"""

	# Build a dictionary of species names and genes
	names = build_species_dict(filenames)

	# Format names
	formatted_names = format_names(names)
	formatted_names.sort()

	# Write each species and gene line to an ouput text file.
	write_genes(formatted_names)

def build_species_dict(filenames):
	""" (list of strings) -> dictionary
		Builds a dictionary where the key is the name of the species and 
		the value is the concatentation of all the genes associated with 
		that species. 
	"""
	names = {}
	name = ''
	
	# Go through the file and concat all the genes associated to a species name
	for filename in filenames:
		input_file = open(filename, 'r')
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


def format_names(names):
	""" (dictionary) -> list
		Format each species name and genes into a single line.
	"""
	
	formatted_names = []

	for key, value in names.items():
		# Add the appropiate amount of spaces between the species name 
		# and gene so that all the genes line up. 
		num_spaces = 37 - len(key)

		formatted_name = key.strip() + (num_spaces * ' ') + value.strip() + '\n'
		formatted_names.append(formatted_name)

	return formatted_names

def write_genes(names):
	""" (list of strings) -> NoneType
		Write each line of the species name and genes to an output_file.
	"""

	output_file = open("output.txt", 'w') 
	for name in names:
		output_file.write(name)

	output_file.close()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Builds gene super matrix.')
	parser.add_argument('files', metavar='S', nargs='+',
                   help='A file containing gene sequences')
	args = parser.parse_args()
	concat_species_genes(sys.argv[1:])