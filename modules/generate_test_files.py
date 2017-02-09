def generate_test_files(dirname):
	names = ['Callithrix aurita', 'Alouatta pigra', 'Plecturocebus hoffmannsi', 'Callithrix mauesi', 'Aotus nancymaae', 'Saguinus mystax mystax', 'Aotus vociferans', 'Ateles paniscus', 'Pithecia irrorata', 'Papio anubis', 'Ateles paniscus paniscus', 'Callithrix emiliae clones', 'Saguinus inustus', 'Saguinus midas midas', 'Alouatta seniculus seniculus', 'Leontopithecus chrysopygus', 'Callithrix penicillata', 'Cebus xanthosternos', 'Leontopithecus rosalia', 'Brachyteles hypoxanthus', 'Alouatta belzebul', 'Saguinus mystax', 'Ateles belzebuth hybridus', 'Cebus olivaceus', 'Lagothrix cana', 'Alouatta palliata', 'Macaca mulatta integrin', 'Pithecia monachus', 'Alouatta caraya', 'Plecturocebus cinerascens', 'Callimico goeldii', 'Sapajus nigritus robustus', 'Saimiri sciureus sciureus', 'Callithrix melanura', 'Alouatta palliata palliata', 'Aotus brumbacki', 'Ateles geoffroyi vellerosus', 'Aotus azarae boliviensis', 'Brachyteles arachnoides', 'Cebuella pygmaea', 'Plecturocebus moloch', 'Callicebus personatus personatus', 'Aotus azarae', 'Cebus apella nigritus', 'Callicebus lugens', 'Plecturocebus brunneus', 'Pithecia pithecia', 'Saguinus labiatus labiatus', 'Cacajao melanocephalus', 'Cacajao hosomi', 'Callithrix pygmaea', 'Callicebus torquatus', 'Saimiri oerstedii oerstedii', 'Plecturocebus caligatus', 'Ateles belzebuth chamek', 'Callithrix chrysoleuca', 'Pithecia pithecia pithecia', 'Cacajao calvus calvus', 'Lagothrix poeppigii', 'Callithrix geoffroyi', 'Ateles hybridus', 'Alouatta sara', 'Callicebus nigrifrons', 'Saguinus midas', 'Chiropotes albinasus', 'Cebus apella paraguayanus', 'Saguinus fuscicollis fuscicollis', 'Saimiri sciureus', 'Aotus griseimembra', 'Callicebus donacophilus haplotype', 'Alouatta seniculus', 'Callicebus personatus', 'Sapajus libidinosus', 'Cebus cay', 'Aotus infulatus', 'Aotus lemurinus', 'Callicebus cupreus', 'Macaca mulatta recombination', 'Aotus azarai infulatus', 'Aotus nigriceps', 'Leontopithecus chrysomelas', 'Callithrix saterei', 'Alouatta guariba clamitans', 'Callicebus coimbrai', 'Saguinus imperator', 'Aotus lemurinus griseimembra', 'Saimiri boliviensis', 'Callicebus caligatus', 'Saguinus bicolor bicolor', 'Lagothrix lugens', 'Callithrix argentata argentata', 'Callithrix jacchus', 'Cebus capucinus', 'Ateles geoffroyi', 'Ateles geoffroyi panamensis', 'Saguinus tripartitus', 'Cacajao rubicundus', 'Plecturocebus cupreus', 'Lagothrix lagotricha', 'Cheracebus lugens', 'Ateles belzebuth', 'Plecturocebus bernhardi', 'Cheracebus purinus', 'Saguinus nigricollis nigricollis', 'Callithrix humeralifera', 'Saimiri vanzolinii', 'Callicebus brunneus', 'Callithrix kuhlii', 'Saguinus fuscicollis', 'Saguinus imperator subgrisescens', 'Saimiri boliviensis boliviensis', 'Plecturocebus miltoni', 'Saguinus labiatus', 'Cacajao ayresi', 'Macaca mulatta', 'Aotus azarai', 'Callicebus hoffmannsi', 'Aotus azarai azarai', 'Callicebus moloch', 'Saguinus bicolor', 'Cebus apella', 'Callithrix emiliae', 'Cacajao calvus', 'Saguinus melanoleucus melanoleucus', 'Saguinus oedipus', 'Chiropotes chiropotes', 'Saimiri ustus', 'Alouatta guariba', 'Chiropotes utahicki', 'Aotus azarai boliviensis', 'Callithrix argentata', 'Ateles fusciceps', 'Alouatta stramineus', 'Colobus guereza', 'Sapajus flavius', 'Brachyteles arachnoides hypoxanthus', 'Cebus albifrons', 'Aotus azarae infulatus', 'Chiropotes israelita', 'Callicebus donacophilus', 'Cebus nigritus robustus', 'Aotus trivirgatus', 'Saguinus geoffroyi']
	gene_types = ['COI', 'COII', 'CYTB', 'FOPI', 'GHR', 'IRBP', 'ITGA4', 'RAGI', 'RAGII']
	header = ">gi|305690991|gb|HQ005493.1| {0} isolate 17956 cytochrome b ({1}) gene, complete cds; mitochondrial\n"
	genes = ["ATGACTTCCCCCCGCAAAACACACCCACTAGCAAAGATCATTAACGAATCATTCATCGATCTCCCCACAC", "ATGACCTCCCCCCGCAAAACACACCAGCAAAGATCATTAACGAATCATTCATCGATCTCCCCACAC", "ATGACTTCNCCCCGCAAAACACACCCACTAGCAAAGATCATTAACGTTCATCGATCTCCCCACAC", "CCCAAGATCTTGAGGATTACTTGAATGGCCCCTTCACTGTGGTTGTGAAGGAGTCTTGTGATGGAATGGGAGATGTGAGTGAGAAGCATGGGAGT"]
	i = 0
	for name in names:
		for gene in gene_types:
			file = open(dirname + name + gene + ".fas", "w")
			head = header.format(name, gene)
			file.write(head)
			file.write(genes[i])
			file.close()
			if i == 3:
				i = 0
			else:
				i += 1

if __name__ == '__main__':
	generate_test_files("gene_files/generated_gene_files/")


