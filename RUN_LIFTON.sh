#lifton -proteins /ccb/salz2/kh.chao/PR_liftoff_protein_search/data/protein.fasta -liftoff /ccb/salz2/kh.chao/PR_liftoff_protein_search/results/liftoff/CHM13_MANE/CHM13_MANE.sort.gff3 -miniprot /ccb/salz2/kh.chao/PR_liftoff_protein_search/results/liftoff/CHM13_MANE/CHM13_MANE_miniprot.fix.gff /ccb/salz3/kh.chao/ref_genome/homo_sapiens/T2T-CHM13/chm13v2.0.fa

python setup.py install

lifton -proteins /ccb/salz2/kh.chao/PR_liftoff_protein_search/data/protein.fasta -liftoffdb /ccb/salz2/kh.chao/PR_liftoff_protein_search/results/liftoff/CHM13_MANE/CHM13_MANE.sort.gff3_db -miniprotdb /ccb/salz2/kh.chao/PR_liftoff_protein_search/results/liftoff/CHM13_MANE/CHM13_MANE_miniprot.fix.gff_db /ccb/salz3/kh.chao/ref_genome/homo_sapiens/T2T-CHM13/chm13v2.0.fa
