import sys, getopt, os, argparse, format, combine, gene_matrix
from subprocess import call

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Combines single gene files into a combined fasta file.')
	parser.add_argument('files', metavar='S', nargs='+',
                   help='A directory containing files with a single gene sequence')
	args = parser.parse_args()
	input_file_list = os.listdir(sys.argv[1])

	if not os.path.exists("gene_files"):
		os.makedirs("gene_files")
	if not os.path.exists("gene_files/unaligned_gene_files"):
		os.makedirs("gene_files/unaligned_gene_files")
	if not os.path.exists("gene_files/aligned_gene_files"):
		os.makedirs("gene_files/aligned_gene_files")
	if not os.path.exists("gene_files/formatted_aligned_gene_files"):
		os.makedirs("gene_files/formatted_aligned_gene_files")
	unaligned = "gene_files/unaligned_gene_files"

	aligned = "gene_files/aligned_gene_files"
	formatted = "gene_files/formatted_aligned_gene_files"

	# Check for '.DS_Store' on Macs
	if '.DS_Store' in input_file_list:
		input_file_list.remove('.DS_Store')

	sys.stdout.write("Combining single gene Sequences.\n")
	gene_types = combine.combine_gene_sequences(input_file_list, sys.argv[1])
	sys.stdout.write("Combination finished.\n")

	sys.stdout.write("Checking spelling.\n")
	gene_matrix.build_species_dict(gene_types, unaligned)
	sys.stdout.write("Spellcheck finished.\n")

	sys.stdout.write("Beginning sequence alignment...")
	for gene_type in gene_types:
		call(["./muscle", "-in", unaligned + '/' + gene_type,  "-out", aligned + '/' + gene_type])
		format.format(gene_type)
	sys.stdout.write("\nSequence alignment finished. \n")

	sys.stdout.write("Creating super matrix...")
	gene_matrix.concat_species_genes(gene_types, formatted, "fasta", "output")
	sys.stdout.write("\nSuper matrix finished. \n")