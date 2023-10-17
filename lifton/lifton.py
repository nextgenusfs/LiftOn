from lifton import extract_features, mapping, intervals, extra_copy
import argparse
from pyfaidx import Fasta, Faidx
from intervaltree import Interval, IntervalTree
import copy

from lifton import align, adjust_cds_boundaries, fix_trans_annotation, lifton_class, lifton_utils

def parse_args(arglist):
    print("arglist: ", arglist)
    parser = argparse.ArgumentParser(description='Lift features from one genome assembly to another')
    parser.add_argument('target', help='target fasta genome to lift genes to')

    outgrp = parser.add_argument_group('* Output')
    outgrp.add_argument(
        '-o', '--output', default='stdout', metavar='FILE',
        help='write output to FILE in same format as input; by default, output is written to terminal (stdout)'
    )

    outgrp.add_argument(
        '-d', '--dir', default='intermediate_files', metavar='DIR',
        help='name of directory to save intermediate fasta and SAM files; default is "intermediate_files"',
    )

    parser.add_argument('-V', '--version', help='show program version', action='version', version='v1.6.3')
    parser.add_argument(
        '-t', '--threads', default=1, type=int, metavar='P', help='use p parallel processes to accelerate alignment; by default p=1'
    )

    parser.add_argument('-f', '--features', metavar='TYPES', help='list of feature types to lift over')

    proteinrefrgrp = parser.add_argument_group('* Required input (Protein sequences)')
    proteinrefrgrp.add_argument(
        '-p', '--proteins', metavar='fasta', required=True,
        help='the reference protein sequences.'
    )

    liftoffrefrgrp = parser.add_argument_group('* Required input (Liftoff annotation)')

    liftoffgrp = liftoffrefrgrp.add_mutually_exclusive_group(required=True)
    liftoffgrp.add_argument(
        '-l', '--liftoff', metavar='gff',
        help='the annotation generated by Liftoff'
    )
    liftoffgrp.add_argument(
        '-ldb', '--liftoffdb', metavar='gff-DB',
        help='name of Liftoff gffutils database; if not specified, the -liftoff '
                                  'argument must be provided and a database will be built automatically'
    )

    miniprotrefrgrp = parser.add_argument_group('* Required input (miniprot annotation)')

    miniprotgrp = miniprotrefrgrp.add_mutually_exclusive_group(required=True)
    miniprotgrp.add_argument(
        '-m', '--miniprot', metavar='gff',
        help='the annotation generated by miniprot'
    )
    miniprotgrp.add_argument(
        '-mdb', '--miniprotdb', metavar='gff-DB',
        help='name of miniprot gffutils database; if not specified, the -miniprot '
                                  'argument must be provided and a database will be built automatically'
    )

    parser._positionals.title = '* Required input (sequences)'
    parser._optionals.title = '* Miscellaneous settings'

    parser._action_groups = [parser._positionals, proteinrefrgrp, liftoffrefrgrp, miniprotrefrgrp, outgrp, parser._optionals]
    args = parser.parse_args(arglist)
    return args


def run_all_liftoff_steps(args):
    ref_chroms = []

    ################################
    # Step 0: Getting the arguments (required / optional)
    ################################
    fai = Fasta(args.target)
    fai_protein = Fasta(args.proteins)
    l_feature_db, m_feature_db = extract_features.extract_features_to_fix(ref_chroms, args)

    print("args.features: ", args.features)
    print("args.threads: ", args.threads)
    print("args.proteins: ", args.proteins)

    fw = open(args.output, "w")
    ################################
    # Step 1: Creating miniprot 2 Liftoff ID mapping
    ################################
    m_id_dict, aa_id_2_m_id_dict = mapping.id_mapping(m_feature_db)

    ################################
    # Step 2: Initializing intervaltree
    ################################
    tree_dict = intervals.initialize_interval_tree(l_feature_db)

    # Dictionary for extra copy
    gene_copy_num_dict = {}
    trans_copy_num_dict = {}
    gene_info_dict = {}
    trans_info_dict = {}
    trans_2_gene_dict = {}

    LIFTOFF_TOTAL_GENE_COUNT = 0
    LIFTOFF_ONLY_GENE_COUNT = 0
    LIFTOFF_INVALID_TRANS_COUNT = 0
    LIFTOFF_MINIPROT_FIXED_GENE_COUNT = 0

    ################################
    # Step 3: Iterating gene entries & fixing CDS lists
    ################################
    # For missing transcripts.
    gene_copy_num_dict["gene-LiftOn"] = 0
    features = lifton_utils.get_parent_features_to_lift(args.features)
    for feature in features:
        for gene in l_feature_db.features_of_type(feature):#, limit=("chr1", 0, 259055730)):
            LIFTOFF_TOTAL_GENE_COUNT += 1
            chromosome = gene.seqid
            gene_id = gene.attributes["ID"][0]
            gene_id_base = lifton_utils.get_ID_base(gene_id)

            ################################
            # Step 3.1: Creating gene copy number dictionary
            ################################
            if gene_id_base in gene_copy_num_dict.keys():
                gene_copy_num_dict[gene_id_base] += 1
            else:
                gene_copy_num_dict[gene_id_base] = 0

            ################################
            # Step 3.2: Creating LiftOn gene & gene_info
            ################################
            lifton_gene = lifton_class.Lifton_GENE(gene)
            gene_info = copy.deepcopy(gene)
            lifton_gene_info = lifton_class.Lifton_GENE_info(gene_info.attributes, gene_id_base)
            gene_info_dict[gene_id_base] = lifton_gene_info
            
            ################################
            # Step 3.3: Adding LiftOn transcripts
            ################################
            # Assumption that all 1st level are transcripts
            transcripts = l_feature_db.children(gene, level=1)
            for transcript in list(transcripts):
                lifton_gene.add_transcript(transcript)
                transcript_id = transcript["ID"][0]
                transcript_id_base = lifton_utils.get_trans_ID_base(transcript_id)

                ################################
                # Step 3.3.1: Creating trans copy number dictionary
                ################################
                if transcript_id_base in trans_copy_num_dict.keys():
                    trans_copy_num_dict[transcript_id_base] += 1
                else:
                    trans_copy_num_dict[transcript_id_base] = 0

                print("\ttranscript_id      : ", transcript_id)
                # print("&& transcript_id_base : ", transcript_id_base)

                transcript_info = copy.deepcopy(transcript)
                lifton_trans_info = lifton_class.Lifton_TRANS_info(transcript_info.attributes, transcript_id_base, gene_id_base)

                trans_2_gene_dict[transcript_id_base] = gene_id_base
                trans_info_dict[transcript_id_base] = lifton_trans_info

                ###########################
                # Step 3.4: Adding exons
                ###########################
                exons = l_feature_db.children(transcript, featuretype='exon')  # Replace 'exon' with the desired child feature type
                for exon in list(exons):
                    lifton_gene.add_exon(transcript_id, exon)
                
                ###########################
                # Step 3.5: Adding CDS
                ###########################
                cdss = l_feature_db.children(transcript, featuretype='CDS')  # Replace 'exon' with the desired child feature type
                cds_num = 0
                for cds in list(cdss):
                    cds_num += 1
                    lifton_gene.add_cds(transcript_id, cds)

                #############################################
                # Step 3.6: Processing transcript
                #   1. There are CDS features
                #   2. transcript ID is in both miniprot & Liftoff & protein FASTA file
                #############################################
                if (cds_num > 0) and (transcript_id in m_id_dict.keys()) and (transcript_id in fai_protein.keys()):
                    ################################
                    # Step 3.6.1: liftoff transcript alignment
                    ################################
                    l_lifton_aln = align.parasail_align("liftoff", l_feature_db, transcript, fai, fai_protein, transcript_id)

                    if l_lifton_aln.identity < 1:
                        m_ids = m_id_dict[transcript_id]
                        for m_id in m_ids:
                            m_entry = m_feature_db[m_id]
                            overlap = lifton_utils.segments_overlap((m_entry.start, m_entry.end), (transcript.start, transcript.end))

                            if not overlap or m_entry.seqid != transcript.seqid:
                                continue
                            
                            ################################
                            # Step 3.6.2: Protein sequences are in both Liftoff and miniprot & overlap
                            #   Fix & update CDS list
                            ################################
                            ################################
                            # Step 3.6.3: miniprot transcript alignment
                            ################################
                            m_lifton_aln = align.parasail_align("miniprot", m_feature_db, m_entry, fai, fai_protein, transcript_id)

                            # Check reference overlapping status
                            # 1. Check it the transcript overlapping with the next gene
                            # Check the miniprot protein overlapping status
                            # The case I should not process the transcript 
                            # 1. The Liftoff does not overlap with other gene
                            # 2. The miniprot protein overlap the other gene
                            ovps_liftoff = tree_dict[chromosome].overlap(transcript.start, transcript.end)
                            ovps_miniprot = tree_dict[chromosome].overlap(m_entry.start, m_entry.end)


                            # if len(ovps_liftoff) == 1 and len(ovps_miniprot) > 1:
                            miniprot_cross_gene_loci = False
                            liftoff_set = set()
                            for ovp_liftoff in ovps_liftoff:
                                liftoff_set.add(ovp_liftoff[2])
                                # print("\tovp_liftoff: ", ovp_liftoff)
                            # print("liftoff_set : ", liftoff_set)
                            
                            for ovp_miniprot in ovps_miniprot:
                                if ovp_miniprot[2] not in liftoff_set:
                                    # Miniprot overlap to more genes
                                    miniprot_cross_gene_loci = True
                                    break

                            if miniprot_cross_gene_loci:
                                continue                            

                            # LIFTOFF_MINIPROT_FIXED_GENE_COUNT += 1
                            cds_list = fix_trans_annotation.fix_transcript_annotation(l_lifton_aln, m_lifton_aln, fai, fw)
                            lifton_gene.update_cds_list(transcript_id, cds_list)

                            # Check if there are mutations in the transcript
                            good_trans = lifton_gene.fix_truncated_protein(transcript_id, fai, fai_protein)
                            if not good_trans:
                                LIFTOFF_INVALID_TRANS_COUNT += 1
                
                else:
                    LIFTOFF_ONLY_GENE_COUNT += 1

            ###########################
            # Step 4.7: Writing out LiftOn entries
            ###########################
            lifton_gene.write_entry(fw)
            # print("Final!!")
            # lifton_gene.print_gene()

            ###########################
            # Step 4.8: Adding LiftOn intervals
            ###########################
            gene_interval = Interval(lifton_gene.entry.start, lifton_gene.entry.end, gene_id)
            tree_dict[chromosome].add(gene_interval)


    ################################
    # Step 5: Finding extra copies
    ################################
    EXTRA_COPY_MINIPROT_COUNT = 0 
    NEW_LOCUS_MINIPROT_COUNT = 0
    EXTRA_COPY_MINIPROT_COUNT, NEW_LOCUS_MINIPROT_COUNT = extra_copy.find_extra_copy(m_feature_db, tree_dict, aa_id_2_m_id_dict, gene_info_dict, trans_info_dict, trans_2_gene_dict, gene_copy_num_dict, trans_copy_num_dict, fw)

    print("Liftoff truncated trans loci\t\t\t: ", LIFTOFF_INVALID_TRANS_COUNT)
    print("Liftoff total gene loci\t\t\t: ", LIFTOFF_TOTAL_GENE_COUNT)
    print("Liftoff only gene loci\t\t\t: ", LIFTOFF_ONLY_GENE_COUNT)
    print("Liftoff & miniprot matched gene loci\t: ", LIFTOFF_MINIPROT_FIXED_GENE_COUNT)

    print("miniprot found extra copy gene loci\t: ", EXTRA_COPY_MINIPROT_COUNT)
    print("miniprot found new loci\t\t\t: ", NEW_LOCUS_MINIPROT_COUNT)


def main(arglist=None):
    args = parse_args(arglist)
    print("Run Lifton!!")
    print(args)
    run_all_liftoff_steps(args)