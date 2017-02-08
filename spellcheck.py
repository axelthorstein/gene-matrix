import collections

def misspelled_check(misspelled_species, filenames):
	""" (dict, list of str) -> NoneType
		Check if there are any species names misspelled and if so raise an error that 
		displays which species names are misspelled, and what files the mistakes occur. 
	"""

	misspelled_pairs = pair_misspelled_species(misspelled_species, len(filenames))

	misspelled_error(misspelled_pairs)

def remove_correctly_spelled_species(species_occurences, num_files):
	""" (dict, int) -> dict
		Check if the amount of occurences is equal to the number of files.
		If they are not equal this would imply there is a spelling mistake,
		so remove all the correctly spelled names. 
	"""

	misspelled_species = {}

	for species in species_occurences:
		# Indicating there are not spelling mistakes with this species.
		if species_occurences[species][0] != num_files:
			misspelled_species[species] = species_occurences[species]

	return misspelled_species

def pair_misspelled_species(misspelled_species, num_files):
	""" (dict, int) -> dict
		For each misspelled name compare the similarity to the other misspelled
		names, if they are similar enough then add the name with more occurences
		as the key, and the potentially misspelled word as the value, along with
		the file it was found in.  
	"""

	pairs = {}

	for species in misspelled_species:
		# Indicating correct spelling.
		if misspelled_species[species][0] >= num_files/2:
			pairs[species] = []
			for misspelled_name in misspelled_species:
				similarity = levenshtein(species, misspelled_name)

				if similarity <= len(species)/4 and similarity != 0:
					pairs[species].append((misspelled_name, misspelled_species[misspelled_name][1]))

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

def misspelled_error(misspelled_pairs):
	""" (dict) -> NoneType
		Raise an exception if all of the files don't have the same amount
		of species names, or if there may be a spelling 
		error on one of the names. Output all the possible misspellings.
	"""
	error_message = ''

	for species in misspelled_pairs:

		error = species + ' may be misspelled as: \n'

		for misspelling in misspelled_pairs[species]:

			error += "	" + misspelling[0] + " in the files " + ", ".join(misspelling[1]) + "\n"

		error_message += error + '\n'
	
	raise NameError("\n\nThe following species names may be misspelled, " +
		"or have a different number of species names:\n\n" + error_message)
