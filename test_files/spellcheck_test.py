import unittest, sys, os, os.path
curfilePath = os.path.abspath(__file__)
curDir = os.path.abspath(os.path.join(curfilePath,os.pardir)) # this will return current directory in which python file resides.
parentDir = os.path.abspath(os.path.join(curDir,os.pardir)) # this will return parent directory.
sys.path.append(parentDir + '/modules/')
import spellcheck

class combine_test(unittest.TestCase):
    
    def test_parse_header(self):
    	# Regular case.
    	header = ">gi|158534356|gb|EU179516.1| Aotus azarae isolate PR01159 cytochrome oxidase subunit I (COI) gene, partial cds; mitochondrial"
        self.assertEqual(combine.parse_header(header), ("Aotus_azarae", ["COI"]))
        # No brackets.
        header = ">gi|112380346|gb|DQ679784.1| Alouatta guariba isolate SC12 cytochrome b cytb gene, partial cds; mitochondrial"
        self.assertEqual(combine.parse_header(header), ("Alouatta_guariba", ["CYTB"]))
        # Two genes.
        header = ">gi|239579420|gb|FJ529109.1| Cebus albifrons voucher CRB2678 cytochrome b cytb gene, complete cds; COI gene mitochondrial"
        self.assertEqual(combine.parse_header(header), ("Cebus_albifrons", ["CYTB", "COI"]))
        # Gene with variable.
        header = ">gi|239579420|gb|FJ529109.1| Cebus albifrons voucher CRB2678 cytochrome b COXI gene mitochondrial"
        self.assertEqual(combine.parse_header(header), ("Cebus_albifrons", ["COI"]))
        # Gene with numbers.
        header = ">gi|239579420|gb|FJ529109.1| Cebus albifrons voucher CRB2678 COX2 gene cytochrome b COX1 gene mitochondrial"
        self.assertEqual(combine.parse_header(header), ("Cebus_albifrons", ["COII", "COI"]))
        # Gene with comma.
        header = ">gi|239579420|gb|FJ529109.1| Cebus albifrons voucher CRB2678 COX2 gene, cytochrome b COX1 gene, mitochondrial"
        self.assertEqual(combine.parse_header(header), ("Cebus_albifrons", ["COII", "COI"]))
        # No intro codes.
        header = "Aotus azarae mitochondrial PR01159 cytochrome oxidase subunit I (COXI) gene, partial cds; mitochondrial"
        self.assertEqual(combine.parse_header(header), ("Aotus_azarae", ["COI"]))
        # No buffer word.
        header = "Aotus azarae PR01159 cytochrome oxidase subunit I (COXI) gene, partial cds; mitochondrial"
        self.assertEqual(combine.parse_header(header), ("Aotus_azarae", ["COI"]))

    def test_species_info(self):
        # Regular case.
        lines = [">gi|239579420|gb|FJ529109.1| Cebus albifrons voucher CRB2678 COX2 gene cytochrome b COX1 gene mitochondrial\n", "ATGACTTCNCCCCGCAAAACACACCCACTAGCAAAGATCATTAACGTTCATCGATCTCCCCACAC"]
        self.assertEqual(combine.get_species_info(lines), (['COII', 'COI'], '>Cebus_albifrons\nATGACTTCNCCCCGCAAAACACACCCACTAGCAAAGATCATTAACGTTCATCGATCTCCCCACAC\n'))

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)



if __name__ == '__main__':
    unittest.main()