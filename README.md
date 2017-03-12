## Gene Matrix Builder

A python program to efficiently build a super matrix from single gene sequence files.

## To-do

+ After alignment, before matrix: add missing species with "N"

+ Auto generate nexus and phylip if they are going to run partition finder

+ Add error states for website. 

+ Bring all new functionality to website.

+ Create all test cases for header parsing.

+ Check if there are duplicates in the single gene files, and whether this will cause a mistake. 

+ Add option for auto correct spelling. 

+ Testing similarity between genus/species names.

+ If they use a process pool then redirect the output to a pipe.

+ Do checks on species vs sub species gene sequences. 

+ Look into retrieving gene files from database based on search. 

+ Change misspell varible names to include missing names. 

+ Website uploads files in wrong order

## Synopsis

This program is designed to make phylogeny building more efficient by building a genetic super matrix automatically. The user can input several different fasta files each representing a single aligned gene for any number of species. The output is a single file that concatenates all the different genes into one file. If the different files do not have the same labels, the program will return an output file describing where the mis-label is occurring. The order of the genes in the concatenated file is the order that the separate files of aligned genes is uploaded to the program. The labels in each file do not have to be in the same order. The output can be defined into fasta, nexus, or phylip format depending on your step in your phylogenetic tree building. This can allow users to get to steps like PartitionFinder and MrBayes quicker to get to when building a phylogenetic tree using several genes.

## Code Example

The code below is an example of usage where the fasta files are located in a directory called gene_files, the desired name of the output file is 'Platyrrhine Phylogeny', and the desired output format is nexus. 

```shell
python3 modules/combine.py --input gene_files/generated_gene_files

python3 modules/spellcheck.py --input gene_files/aligned_gene_files

python3 gene_matrix.py --input gene_files --output "Platyrrhine Phylogeny" --type nexus

python3 process_gene_sequence.py --input gene_files/generated_gene_files --output final.txt --type nexus --pool 4

python3 process_gene_sequence.py --input gene_files/unaligned_gene_files --output final.txt --type nexus --pool 4 --startstep align --endstep format
```

## Installation

Simply download the gene_matrix.py file and give it a directory that only contains fasta files. 

## Contributors

Axel Steingrimsson: development

Ezra Mendales: Motivation

## License

MIT License

Copyright (c) 2017 Axel Steingrimsson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
