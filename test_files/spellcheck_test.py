import unittest, sys, os, os.path
curfilePath = os.path.abspath(__file__)
curDir = os.path.abspath(os.path.join(curfilePath,os.pardir)) # this will return current directory in which python file resides.
parentDir = os.path.abspath(os.path.join(curDir,os.pardir)) # this will return parent directory.
sys.path.append(parentDir + '/modules/')
import spellcheck

class combine_test(unittest.TestCase):

    def test_parse_header(self):
    	species_occurences = {'Aotus_azarae_boliviensis': [3, ['COI.fas', 'COII.fas', 'CYTB.fas']], 'Callithrix_aurita': [3, ['COI.fas', 'COII.fas', 'CYTB.fas']]}
    	num_files = 9
    	# Regular case.
        self.assertEqual(spellcheck.remove_correctly_spelled_species(species_occurences, num_files), {})

        # One missing.
        species_occurences['Callithrix_aurita'][0] -= 1
        species_occurences['Callithrix_aurita'][1].pop(0)
        self.assertEqual(spellcheck.remove_correctly_spelled_species(species_occurences, num_files), {'Callithrix_aurita': [2, ['COII.fas', 'CYTB.fas']]})

if __name__ == '__main__':
    unittest.main()