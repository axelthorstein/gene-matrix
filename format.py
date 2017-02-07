#!/usr/bin/python

def format(filename):
	""" (str) -> NoneType
		Formats a fasta file for that each gene is displayed 
		over only a single line. 
	"""

	gene_sequences = []

	input_file = open("unaligned_gene_files/" + filename, 'r')

	output_filename = filename[0:-6] + "_formatted.fas"
	output_file = open(output_filename, "w")

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
