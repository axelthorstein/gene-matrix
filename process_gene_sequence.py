import sys, getopt, os, argparse
from modules import format, combine, gene_matrix, spellcheck
from subprocess import call
from multiprocessing import Pool

def check_file_ending(out_file):
	if "." in out_file:
		return out_file[:out_file.index(".")]
	return out_file

def align(gene_type):
	in_file = "gene_files/unaligned_gene_files/" + gene_type
	out_file = "gene_files/aligned_gene_files/" + gene_type
	call(["./modules/muscle", "-in", in_file,  "-out", out_file])

if __name__ == '__main__':

	# Parse the commandline arguments.
	parser = argparse.ArgumentParser(description='Runs a process of step in combining, aligning, '+
		'and processing a directory of gene sequences.')
	parser.add_argument('files', metavar='S', nargs='+',
                   help="Specify the directory of files that you intended to ve processed. ")
	parser.add_argument('--startstep', choices=["combine", "spellcheck", "align", "format", "matrix"], 
		help='Select which step you would like the process to begin with, '
                   +'which assumes the directory that you are passing in is ready to be processed at that step. (default=combine)')
	parser.add_argument('--endstep', choices=["combine", "spellcheck", "align", "format", "matrix"], 
		help='Select which step you would like the process to end with. (default=matrix)')
	parser.add_argument('--type', choices=["fasta", "nexus", "phylip"], 
		help='Sepcify output file type [fasta, nexus, phylip]')
	parser.add_argument('--o', 
		help='Sepcify output file name (default=output.fas)')
	parser.add_argument('--pool', 
		help='Sepcify how many process pool workers to run the alignment (default=1)')
	args = parser.parse_args()
	filenames = os.listdir(sys.argv[1])

	# Set default parameters
	if args.startstep is None:
		args.startstep = "combine"
	if args.endstep is None:
		args.endstep = "matrix"
	if args.pool is None:
		args.pool = 1
	if args.o is None:
		args.o = 'output'
	if args.type is None:
		args.type = 'fasta'

	args.o = check_file_ending(args.o)

	# Create all the necessary directories.
	parent_dir = os.getcwd() + "/"
	if not os.path.exists("gene_files"):
		os.makedirs("gene_files")
	if not os.path.exists(parent_dir + "gene_files/unaligned_gene_files/"):
		os.makedirs(parent_dir + "gene_files/unaligned_gene_files/")
	if not os.path.exists(parent_dir + "gene_files/aligned_gene_files/"):
		os.makedirs(parent_dir + "gene_files/aligned_gene_files/")
	if not os.path.exists(parent_dir + "gene_files/formatted_aligned_gene_files/"):
		os.makedirs(parent_dir + "gene_files/formatted_aligned_gene_files/")
	unaligned = parent_dir + "gene_files/unaligned_gene_files/"
	aligned = parent_dir + "gene_files/aligned_gene_files/"
	formatted = parent_dir + "gene_files/formatted_aligned_gene_files/"

	# Check for '.DS_Store' on Macs
	if '.DS_Store' in filenames:
		filenames.remove('.DS_Store')

	if args.startstep == "combine":
		# Combine the single gene files. 
		sys.stdout.write("Combining single gene Sequences.\n")
		filenames = combine.combine_gene_sequences(filenames, parent_dir + sys.argv[1], unaligned)
		sys.stdout.write("Combination finished.\n")
		if args.endstep != "combine":
			args.startstep = "spellcheck"

	if args.startstep == "spellcheck":
		# Check the spelling of the collected species names.
		sys.stdout.write("Checking spelling.\n")
		spellcheck.misspelled_check(filenames, unaligned)
		sys.stdout.write("Spellcheck finished.\n")
		if args.endstep != "spellcheck":
			args.startstep = "align"

	if args.startstep == "align":
		# Align all of the sequences using the Muscle algorithm in a process pool. 
		sys.stdout.write("Beginning sequence alignment...")
		# Create a process pool.
		if (args.pool):
			pool = Pool(processes = int(args.pool))
		else:
			pool = Pool(processes = 1)
		pool.map(align, filenames)
		sys.stdout.write("\nSequence alignment finished. \n")
		if args.endstep != "align":
			args.startstep = "format"

	if args.startstep == "format":
		# Format all of the sequences. 
		sys.stdout.write("Formatting files.\n")
		format.format(filenames, aligned, formatted)
		sys.stdout.write("Formatting successful.\n")
		if args.endstep != "format":
			args.startstep = "matrix"

	# Add exta species. 

	if args.startstep == "matrix":
		# Create a super matrix based on the aligned genes. 
		sys.stdout.write("Creating super matrix...")
		gene_matrix.concat_species_genes(filenames, formatted, args.type, args.o)
		sys.stdout.write("\nSuper matrix finished. \n")
