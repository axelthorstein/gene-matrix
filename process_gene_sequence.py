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

def input_args(message, options):
	user_input = input(message + "\n" + str(options) + "\n")
	if (options):
		while user_input not in options:
			user_input = input("Please only input one of the options: " + "\n" + str(options) + "\n")

	return user_input

if __name__ == '__main__':


	startstep = input_args("Please enter step you would like to start with: ", ["combine", "spellcheck", "align", "format", "matrix"])
	endstep = input_args("Please enter step you would like to start with: ", ["combine", "spellcheck", "align", "format", "matrix"])
	output = input_args("Please ener output file name: (default=output.fas)", [])
	type = input_args("Please enter output file type: ", ["fasta", "nexus", "phylip"])
	filenames = input_args("Please enter the directory name that contains the gene files: \n", [])
	pool = input_args("Would you like the sequencing to run concurrently?: \n[y, n]\n")
	if pool == 'y':
		pool = input_args("How many process would you like to run in the pool?: \n")
	else:
		pool = 1

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

	startstep = args.startstep
	endstep = args.endstep
	output = args.o
	type = args.type
	filenames = args.filesnames
	pool = int(args.pool)


	# Set default parameters
	if startstep is None:
		startstep = "combine"
	if endstep is None:
		endstep = "matrix"
	if pool is None:
		pool = 1
	if output is None:
		output = 'output'
	if type is None:
		type = 'fasta'

	output = check_file_ending(output)

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

	if startstep == "combine":
		# Combine the single gene files. 
		sys.stdout.write("Combining single gene Sequences.\n")
		filenames = combine.combine_gene_sequences(filenames, parent_dir + sys.argv[1], unaligned)
		sys.stdout.write("Combination finished.\n")
		if endstep != "combine":
			startstep = "spellcheck"

	if startstep == "spellcheck":
		# Check the spelling of the collected species names.
		sys.stdout.write("Checking spelling.\n")
		spellcheck.misspelled_check(filenames, unaligned)
		sys.stdout.write("Spellcheck finished.\n")
		if endstep != "spellcheck":
			startstep = "align"

	if startstep == "align":
		# Align all of the sequences using the Muscle algorithm in a process pool. 
		sys.stdout.write("Beginning sequence alignment...")
		# Create a process pool.
		Pool(processes = 1)
		pool.map(align, filenames)
		sys.stdout.write("\nSequence alignment finished. \n")
		if endstep != "align":
			startstep = "format"

	if startstep == "format":
		# Format all of the sequences. 
		sys.stdout.write("Formatting files.\n")
		format.format(filenames, aligned, formatted)
		sys.stdout.write("Formatting successful.\n")
		if endstep != "format":
			startstep = "matrix"

	# Add exta species. 

	if startstep == "matrix":
		# Create a super matrix based on the aligned genes. 
		sys.stdout.write("Creating super matrix...")
		gene_matrix.concat_species_genes(filenames, formatted, type, output)
		sys.stdout.write("\nSuper matrix finished. \n")
