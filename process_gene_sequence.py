import sys, getopt, os, argparse, format, combine, gene_matrix
from subprocess import call
from multiprocessing import Pool

def align(gene_type):
	call(["./muscle", "-in", "gene_files/unaligned_gene_files" + '/' + gene_type,  "-out", "gene_files/aligned_gene_files" + '/' + gene_type])

if __name__ == '__main__':

	# Parse the commandline arguments.
	parser = argparse.ArgumentParser(description='Combines single gene files into a combined fasta file.')
	parser.add_argument('files', metavar='S', nargs='+',
                   help='A directory containing files with a single gene sequence')
	args = parser.parse_args()
	input_file_list = os.listdir(sys.argv[1])

	# Create all the necessary directories.
	if not os.path.exists("gene_files"):
		os.makedirs("gene_files")
	if not os.path.exists("gene_files/unaligned_gene_files/"):
		os.makedirs("gene_files/unaligned_gene_files/")
	if not os.path.exists("gene_files/aligned_gene_files/"):
		os.makedirs("gene_files/aligned_gene_files/")
	if not os.path.exists("gene_files/formatted_aligned_gene_files/"):
		os.makedirs("gene_files/formatted_aligned_gene_files/")
	unaligned = "gene_files/unaligned_gene_files/"
	aligned = "gene_files/aligned_gene_files/"
	formatted = "gene_files/formatted_aligned_gene_files/"

	# Check for '.DS_Store' on Macs
	if '.DS_Store' in input_file_list:
		input_file_list.remove('.DS_Store')

	# Combine the single gene files. 
	sys.stdout.write("Combining single gene Sequences.\n")
	gene_types = combine.combine_gene_sequences(input_file_list, sys.argv[1], unaligned)
	sys.stdout.write("Combination finished.\n")

	# Check the spelling of the collected species names.
	sys.stdout.write("Checking spelling.\n")
	gene_matrix.build_species_dict(gene_types, unaligned)
	sys.stdout.write("Spellcheck finished.\n")

	# Align all of the sequences using the Muscle algorithm in a process pool. 
	sys.stdout.write("Beginning sequence alignment...")
	pool = Pool(processes = (len(gene_types)/4) + 1)
	pool.map(align, gene_types)
	sys.stdout.write("\nSequence alignment finished. \n")

	# Format all of the sequences. 
	sys.stdout.write("Formatting files.\n")
	format.format(gene_types, aligned, formatted)
	sys.stdout.write("Formatting successful.\n")

	# Create a super matrix based on the aligned genes. 
	sys.stdout.write("Creating super matrix...")
	gene_matrix.concat_species_genes(gene_types, formatted, "fasta", "output")
	sys.stdout.write("\nSuper matrix finished. \n")