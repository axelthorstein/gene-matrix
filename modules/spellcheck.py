import collections, gene_matrix, sys, getopt, os, argparse

def misspelled_check(filenames, dirname):
	""" (dict, list of str) -> NoneType
		Check if there are any species names misspelled and if so raise an error that 
		displays which species names are misspelled, and what files the mistakes occur. 
	"""

	# Gather all species occurrences
	gene_matrix.species_occurences
	species = gene_matrix.build_species_dict(filenames, dirname, gene_matrix.species_occurences)

	misspelled_species = remove_correctly_spelled_species(species, len(filenames))

	if misspelled_species:
		misspelled_pairs = pair_misspelled_species(misspelled_species, len(filenames))
		raise_misspelled_error(misspelled_pairs, filenames)

def remove_correctly_spelled_species(species_occurrences, num_files):
	""" (dict, int) -> dict
		Check if the amount of occurrences is equal to the number of files.
		If they are not equal this would imply there is a spelling mistake,
		so remove all the correctly spelled names. 
	"""

	misspelled_species = {}

	for species in species_occurrences:
		# Indicating there are not spelling mistakes with this species.
		if species_occurrences[species][0] != num_files:
			misspelled_species[species] = species_occurrences[species]

	return misspelled_species

def pair_misspelled_species(misspelled_species, num_files):
	""" (dict, int) -> dict
		For each misspelled name compare the similarity to the other misspelled
		names, if they are similar enough then add the name with more occurrences
		as the key, and the potentially misspelled word as the value, along with
		the file it was found in.  
	"""
	pairs = {}

	for species in misspelled_species:
		print species
		# Indicating correct spelling.
		if misspelled_species[species][0] != num_files:
			pairs[species] = []
		for misspelled_name in misspelled_species:
			similarity = levenshtein(species, misspelled_name)
			if similarity <= len(species)/5 and similarity != 0:
				pairs[species].append((misspelled_name, misspelled_species[misspelled_name][1]))

	# Find missing names.
	for pair in pairs:
		# Indicating it isn't misspelled.
		if pairs[pair] == []:
			pairs[pair] += ("", misspelled_species[pair][1])

	return pairs

def levenshtein(name1, name2):
	""" (str, str) -> int
		The Levenshtein distance is a string metric for measuring the difference 
		between two sequences. It was developed by Vladimir Levenshtein in 1965, 
		used here to find the similarity between species names. 
	"""	

	if len(name1) < len(name2):
		return levenshtein(name2, name1)

	# len(name1) >= len(name2)
	if len(name2) == 0:
	    return len(name1)

	previous_row = range(len(name2) + 1)
	for i, c1 in enumerate(name1):
	    current_row = [i + 1]
	    for j, c2 in enumerate(name2):
	        insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
	        deletions = current_row[j] + 1       # than name2
	        substitutions = previous_row[j] + (c1 != c2)
	        current_row.append(min(insertions, deletions, substitutions))
	    previous_row = current_row

	return previous_row[-1]

def raise_misspelled_error(misspelled_pairs, filenames):
	""" (dict) -> NoneType
		Raise an exception if all of the files don't have the same amount
		of species names, or if there may be a spelling 
		error on one of the names. Output all the possible misspellings.
	"""
	error_message = ''
	misspelled_error_format = '{0} may be misspelled as: \n'
	missing_error_format = "The species {0} may be missing from the following file(s): \n"
	duplicate_error_format = "The species {0} may be duplicated in the following file(s): \n"

	for species in misspelled_pairs:
		error = ""

		if len(misspelled_pairs[species]) > 1:
			if len(misspelled_pairs[species][1]) >= len(filenames):
				# Take all duplicate files.  
				files = [file for i, file in enumerate(misspelled_pairs[species][1]) if file in misspelled_pairs[species][1][:i]]
				duplicate_files = ""
				for file in files:
					duplicate_files += "	" + file + "\n"
				error = duplicate_error_format.format(species) + duplicate_files

			elif misspelled_pairs[species][0] == "":
				# Take the files it exists in minus all of the files. 
				files = set(misspelled_pairs[species][1]) ^ set(filenames)
				files_missing_in = ""
				for file in files:
					files_missing_in += "	" + file + "\n"
				error = missing_error_format.format(species) + files_missing_in
			
		else:
			error = misspelled_error_format.format(species)

			for misspelling in misspelled_pairs[species]:
				error += "	" + misspelling[0] + " in the file(s) " + ", ".join(misspelling[1]) + "\n"

		error_message += error + '\n'
	
	raise NameError("\n\nThe following species names may be misspelled, " +
		"or have a different number of species names:\n\n" + error_message)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Checks the spelling between multiple gene files.')
	parser.add_argument('files', metavar='S', nargs='+',
                   help='A directory containing files with the same amount of gene sequences')
	args = parser.parse_args()
	dirname = sys.argv[1]
	filenames = os.listdir(dirname)

	if dirname[-1] != "/":
		dirname += "/"

	# Check for '.DS_Store' on Macs
	if '.DS_Store' in filenames:
		filenames.remove('.DS_Store')

	# Check the spelling of the collected species names.
	sys.stdout.write("Checking spelling.\n")
	misspelled_check(filenames, dirname)
	sys.stdout.write("Spellcheck successful.\n")
