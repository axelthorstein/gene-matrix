import sys, getopt, os, argparse, shutil, subprocess
from modules import combine, spellcheck, gene_matrix, format
from multiprocessing import Pool

def check_file_ending(out_file):
	if "." in out_file:
		return out_file[:out_file.index(".")]
	return out_file

def align(gene_type):
	in_file = "gene_files/unaligned_gene_files/" + gene_type
	out_file = "gene_files/aligned_gene_files/" + gene_type
	subprocess.call(["./modules/muscle", "-in", in_file,  "-out", out_file])

def input_args(message, options, default):
	if options:
		user_input = input(message + "\n[" + ', '.join(options) + "]\n")
	else:
		user_input = input(message + "\n")

	if user_input == "" and default != "":
		return default

	if options:
		while user_input not in options:
			if user_input == "quit":
				sys.exit()
			if user_input == "help":
				print(help_message)
			user_input = input("Please only input one of the options: " + "\n[" + ', '.join(options) + "]\n")

	return user_input

if __name__ == '__main__':
	# if len(sys.argv) > 1:

	# Parse the commandline arguments.
	parser = argparse.ArgumentParser(description='Runs a process of step in combining, aligning, '+
		'and processing a directory of gene sequences.')
	parser.add_argument('--input', 
                   help="Specify the directory of files that you intended to be processed. ")
	parser.add_argument('--startstep', choices=["combine", "spellcheck", "align", "format", "matrix"], 
		help='Select which step you would like the process to begin with, '
                   +'which assumes the directory that you are passing in is ready to be processed at that step. (default=combine)')
	parser.add_argument('--endstep', choices=["combine", "spellcheck", "align", "format", "matrix"], 
		help='Select which step you would like the process to end with. (default=matrix)')
	parser.add_argument('--type', choices=["fasta", "nexus", "phylip"], 
		help='Sepcify output file type [fasta, nexus, phylip]')
	parser.add_argument('--output', 
		help='Sepcify output file name (default=output.fas)')
	parser.add_argument('--pool', 
		help='Sepcify how many process pool workers to run the alignment (default=1)')
	args = parser.parse_args()
	filenames = os.listdir(args.input)

	input_file = args.input
	startstep = args.startstep
	endstep = args.endstep
	output = args.output
	type = args.type
	pool = args.pool
	if pool:
		pool = int(pool)

	# Welcome messages
	columns = shutil.get_terminal_size().columns
	print("".center(columns))
	print("The Super Genie Library".center(columns))
	print("-----------------------".center(columns))
	print("\n")
	print("Welcome to Axel and Ezra's gene concatenation tool set!\n".center(columns))
	print("These tools were developed for concatenating genetic data for species into a super matrix in order to increase efficiency for building phylogenies.\n".center(columns))
	print("Developed by Axel Thor Steingrimsson | Motivation by Dr. Ezra Z. Mendales\n".center(columns))
	print("MIT License".center(columns))
	print("Copyright (c) 2017 Axel Steingrimsson\n".center(columns))
	print("Enter quit to exit, and help for help.\n")
	
	
	# Get user input for program variables.
	gene_modules = ["combine", "spellcheck", "align", "format", "matrix"]
	if startstep == None:
		startstep = input_args("Please enter step you would like to start with: ", gene_modules, "combine")
	if startstep == "combine":
		species_parsing = input_args("Would you like the species names to be parse from the file header or file name? ", ["header", "filename"], "filename")
	if endstep == None:
		endstep = input_args("Please enter step you would like to end with: ", gene_modules, "matrix")
	if output == None and gene_modules.index(endstep) == 4:
		output = input_args("Please enter output file name: (default=output.fas)", [], "output.fas")
	if type == None:
		type = input_args("Please enter output file type: ", ["fasta", "nexus", "phylip"], "fasta")
	if type == "nexus":
		header_info = input_args("Please enter the datatype, missing character, gap character, and if it is interleaved, separated by spaces: (default= datatype=DNA missing=N gap=- interleave=yes)", [], "DNA N - yes")
	if input_file == None:
		input_file = input_args("Please enter the directory name that contains the gene files: ", [], "")
	if gene_modules.index(startstep) <= 2 <= gene_modules.index(endstep):
		if pool == None:
			pool = input_args("Would you like the alignment to run concurrently?: ", ["yes", "no"], "no")
		if pool == 'yes':
			pool = input_args("How many process would you like to run in the pool?: ", [], "1")
			pool = int(pool)
		else:
			pool = 1


	# Get filenames from input directory.
	filenames = os.listdir(input_file)


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
		filenames = combine.combine_gene_sequences(filenames, parent_dir + input_file, unaligned, species_parsing)
		sys.stdout.write("Combination finished.\n")
		if endstep != "combine":
			startstep = "align"

	if startstep == "align":
		# Align all of the sequences using the Muscle algorithm in a process pool. 
		sys.stdout.write("Beginning sequence alignment...")
		# Create a process pool.
		process_pool = Pool(processes = pool)
		process_pool.map(align, filenames)
		sys.stdout.write("\nSequence alignment finished. \n")
		if endstep != "align":
			startstep = "format"

	if startstep == "format":
		# Format all of the sequences. 
		sys.stdout.write("Formatting files.\n")
		format.format(filenames, aligned, formatted)
		sys.stdout.write("Formatting successful.\n")
		if endstep != "format":
			startstep = "spellcheck"

	if startstep == "spellcheck":
		# Check the spelling of the collected species names.
		sys.stdout.write("Checking spelling.\n")
		spellcheck.misspelled_check(filenames, formatted)
		sys.stdout.write("Spellcheck finished.\n")
		if endstep != "spellcheck":
			startstep = "matrix"

	# Add exta species. 

	if startstep == "matrix":
		# Create a super matrix based on the aligned genes. 
		sys.stdout.write("Creating super matrix...")
		gene_matrix.concat_species_genes(filenames, formatted, type, output, header_info)
		sys.stdout.write("\nSuper matrix finished. \n")
