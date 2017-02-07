import sys, getopt, os, argparse, format, combine
from subprocess import call

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Combines single gene files into a combined fasta file.')
	parser.add_argument('files', metavar='S', nargs='+',
                   help='A directory containing files with a single gene sequence')
	args = parser.parse_args()
	input_file_list = os.listdir(sys.argv[1])


	# Check for '.DS_Store' on Macs
	if '.DS_Store' in input_file_list:
		input_file_list.remove('.DS_Store')

	sys.stdout.write("Combining single gene Sequences.\n")
	gene_types = combine.combine_gene_sequences(input_file_list, sys.argv[1])
	sys.stdout.write("Combination finished.\n")

	sys.stdout.write("Beginning sequence alignment...")
	for gene_type in gene_types:
		call(["./muscle", "-in", gene_type + ".fasta",  "-out", gene_type + "_aligned.fasta"])
		format.format(gene_type + "_aligned.fasta")
	sys.stdout.write("\nSequence alignment finished. \n")


