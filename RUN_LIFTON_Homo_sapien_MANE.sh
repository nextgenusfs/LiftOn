python setup.py install

lifton -rg /ccb/salz2/kh.chao/PR_liftoff_protein_search/data/NCBI_Refseq_chr_fixed/GCF_000001405.40_GRCh38.p14_genomic.fna -db /ccb/salz3/kh.chao/PR_liftoff_protein_search/data/MANE_RefSeq/MANE.GRCh38.v1.2.refseq_genomic.cleaned.gff_db -tg /ccb/salz3/kh.chao/ref_genome/homo_sapiens/T2T-CHM13/chm13v2.0.fa -o results/CHM13_MANE/CHM13_MANE_lifton.gff3

#lifton chain --proteins /ccb/salz3/kh.chao/PR_liftoff_protein_search/data/MANE_RefSeq/MANE.GRCh38.v1.2.refseq_genomic.AA.cleaned.fa --liftoffdb /ccb/salz2/kh.chao/PR_liftoff_protein_search/results/liftoff/CHM13_MANE/CHM13_MANE_liftoff.sort.gff3_db --miniprotdb /ccb/salz2/kh.chao/PR_liftoff_protein_search/results/liftoff/CHM13_MANE/CHM13_MANE_miniprot.fix.sorted.gff_db -o results/CHM13_MANE/CHM13_MANE_lifton.gff3 -tg /ccb/salz3/kh.chao/ref_genome/homo_sapiens/T2T-CHM13/chm13v2.0.fa
#lifton --proteins /ccb/salz2/kh.chao/PR_liftoff_protein_search/data/protein.fasta --liftoffdb /ccb/salz2/kh.chao/PR_liftoff_protein_search/results/liftoff/CHM13_MANE/CHM13_MANE.sort.gff3_db --miniprotdb /ccb/salz2/kh.chao/PR_liftoff_protein_search/results/liftoff/CHM13_MANE/CHM13_MANE_miniprot.fix.sorted.gff_db -o results/CHM13_MANE/CHM13_MANE_lifton.gff3 /ccb/salz3/kh.chao/ref_genome/homo_sapiens/T2T-CHM13/chm13v2.0.fa

