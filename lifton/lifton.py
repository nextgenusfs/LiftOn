from lifton import extract_features, mapping, intervals, extra_copy
import argparse
from pyfaidx import Fasta, Faidx
from intervaltree import Interval, IntervalTree
import copy, os

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

    

    # referencegrp = parser.add_argument_group('* Required input (Reference sequences)')
    # referencegrp.add_argument(
    #     '-p', '--proteins', metavar='fasta', required=True,
    #     help='the reference protein sequences.'
    # )




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

    outdir = os.path.dirname(args.output)
    fw = open(args.output, "w")
    fw_truncated = open(args.output+".truncated", "w")
    fw_score = open(outdir+"/score.txt", "w")

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
    LIFTOFF_TOTAL_TRANS_COUNT = 0
    LIFTOFF_BAD_PROT_TRANS_COUNT = 0
    LIFTOFF_GOOD_PROT_TRANS_COUNT = 0
    LIFTOFF_NC_TRANS_COUNT = 0
    LIFTOFF_OTHER_TRANS_COUNT = 0

    
    LIFTON_BAD_PROT_TRANS_COUNT = 0
    LIFTON_GOOD_PROT_TRANS_COUNT = 0
    LIFTON_NC_TRANS_COUNT = 0
    LIFTON_OTHER_TRANS_COUNT = 0
    LIFTON_MINIPROT_FIXED_GENE_COUNT = 0

    ################################
    # Step 3: Iterating gene entries & fixing CDS lists
    ################################
    # For missing transcripts.
    gene_copy_num_dict["gene-LiftOn"] = 0
    features = lifton_utils.get_parent_features_to_lift(args.features)
    
    fw_other_trans = open(outdir+"/other_trans.txt", "w")
    fw_nc_trans = open(outdir+"/nc_trans.txt", "w")

    for feature in features:
        for gene in l_feature_db.features_of_type(feature):#, limit=("chr1", 0, 80478771)):
            LIFTOFF_TOTAL_GENE_COUNT += 1
            chromosome = gene.seqid
            gene_id = gene.attributes["ID"][0]
            gene_id_base = lifton_utils.get_ID_base(gene_id)

            ################################
            # Step 3.1: Creating gene copy number dictionary
            ################################
            lifton_utils.update_copy(gene_id_base, gene_copy_num_dict)

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
                LIFTOFF_TOTAL_TRANS_COUNT += 1

                lifton_status = lifton_class.Lifton_Status()
                lifton_gene.add_transcript(transcript)
                transcript_id = transcript["ID"][0]
                transcript_id_base = lifton_utils.get_ID_base(transcript_id)

                ################################
                # Step 3.3.1: Creating trans copy number dictionary
                ################################
                lifton_utils.update_copy(transcript_id_base, trans_copy_num_dict)

                print("\ttranscript_id      : ", transcript_id)                
                print("&& transcript_id_base : ", transcript_id_base)

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
                #############################################
                if (cds_num > 0) and (transcript_id_base in fai_protein.keys()):
                    l_lifton_aln = align.parasail_align("liftoff", l_feature_db, transcript, fai, fai_protein, transcript_id_base)

                    # SETTING Liftoff identity score
                    lifton_status.liftoff = l_lifton_aln.identity

                    if l_lifton_aln.identity < 1:
                        LIFTOFF_BAD_PROT_TRANS_COUNT += 1
                        #############################################
                        # Step 3.6.1: Liftoff annotation is not perfect
                        #############################################
                        lifton_status.annotation = "LiftOff_truncated"

                        # Writing out truncated LiftOff annotation
                        l_lifton_aln.write_alignment(outdir, "liftoff", transcript_id)
                    
                        m_lifton_aln, has_valid_miniprot = lifton_utils.LiftOn_check_miniprot_alignment(chromosome, transcript, lifton_status, m_id_dict, m_feature_db, tree_dict, fai, fai_protein, transcript_id_base)


                        #############################################
                        # Step 3.6.1.1: Running chaining algorithm if there are valid miniprot alignments
                        #############################################
                        if has_valid_miniprot:
                            LIFTON_MINIPROT_FIXED_GENE_COUNT += 1
                            cds_list = fix_trans_annotation.chaining_algorithm(l_lifton_aln, m_lifton_aln, fai, fw)
                            lifton_gene.update_cds_list(transcript_id, cds_list)
                            lifton_status.annotation = "LiftOff_miniprot_chaining_algorithm" 
                        else:
                            print("Has cds & protein & miniprot annotation; but no valid miniprot annotation!")
                            
                        #############################################
                        # Step 3.6.1.2: Check if there are mutations in the transcript
                        #############################################
                        on_lifton_aln, good_trans = lifton_gene.fix_truncated_protein(transcript_id, fai, fai_protein, lifton_status)
                        # SETTING LiftOn identity score
                        if on_lifton_aln.identity == 1:
                            LIFTON_GOOD_PROT_TRANS_COUNT += 1
                        elif on_lifton_aln.identity < 1:
                            # Writing out truncated LiftOn annotation
                            LIFTON_BAD_PROT_TRANS_COUNT += 1
                            on_lifton_aln.write_alignment(outdir, "lifton", transcript_id)                            

                    elif l_lifton_aln.identity == 1:
                        #############################################
                        # Step 3.6.2: Liftoff annotation is perfect
                        #############################################
                        LIFTOFF_GOOD_PROT_TRANS_COUNT += 1
                        LIFTON_GOOD_PROT_TRANS_COUNT += 1

                        m_lifton_aln, has_valid_miniprot = lifton_utils.LiftOn_check_miniprot_alignment(chromosome, transcript, lifton_status, m_id_dict, m_feature_db, tree_dict, fai, fai_protein, transcript_id_base)

                        # SETTING LiftOn identity score => Same as Liftoff
                        lifton_status.lifton = l_lifton_aln.identity
                        lifton_status.annotation = "LiftOff_identical"
                        lifton_status.status = "identical"

                    fw_score.write(f"{transcript_id}\t{lifton_status.liftoff}\t{lifton_status.miniprot}\t{lifton_status.lifton}\t{lifton_status.annotation}\t{lifton_status.status}\t{transcript.seqid}:{transcript.start}-{transcript.end}\n")
                
                else:
                    # Only liftoff annotation
                    print("No cds || no protein")
                    if (cds_num > 0):
                        LIFTOFF_OTHER_TRANS_COUNT += 1
                        LIFTON_OTHER_TRANS_COUNT += 1
                        lifton_status.annotation = "LiftOff_no_ref_protein"
                        lifton_status.status = "no_ref_protein"
                        fw_other_trans.write(transcript_id+"\n")

                    else:
                        LIFTOFF_NC_TRANS_COUNT += 1
                        LIFTON_NC_TRANS_COUNT += 1
                        lifton_status.annotation = "LiftOff_nc_transcript"
                        lifton_status.status = "nc_transcript"
                        fw_nc_trans.write(transcript_id+"\n")



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
    # EXTRA_COPY_MINIPROT_COUNT, NEW_LOCUS_MINIPROT_COUNT = extra_copy.find_extra_copy(m_feature_db, tree_dict, aa_id_2_m_id_dict, gene_info_dict, trans_info_dict, trans_2_gene_dict, gene_copy_num_dict, trans_copy_num_dict, fw)

    # LIFTOFF_TOTAL_GENE_COUNT = 0
    # LIFTOFF_BAD_PROT_TRANS_COUNT = 0
    # LIFTOFF_GOOD_PROT_TRANS_COUNT = 0
    # LIFTOFF_NC_TRANS_COUNT = 0
    # LIFTOFF_OTHER_TRANS_COUNT = 0

    
    # LIFTON_BAD_PROT_TRANS_COUNT = 0
    # LIFTON_GOOD_PROT_TRANS_COUNT = 0
    # LIFTON_NC_TRANS_COUNT = 0
    # LIFTON_OTHER_TRANS_COUNT = 0
    # LIFTON_MINIPROT_FIXED_GENE_COUNT = 0
    print("Liftoff total gene loci\t\t\t: ", LIFTOFF_TOTAL_GENE_COUNT)
    print("Liftoff total transcript\t\t\t: ", LIFTOFF_TOTAL_TRANS_COUNT)
    print("Liftoff bad protein trans count\t\t\t: ", LIFTOFF_BAD_PROT_TRANS_COUNT)
    print("Liftoff good protein trans count\t\t\t: ", LIFTOFF_GOOD_PROT_TRANS_COUNT)
    print("Liftoff non-coding trans count\t\t\t: ", LIFTOFF_NC_TRANS_COUNT)
    print("Liftoff OTHER trans count\t\t\t: ", LIFTOFF_OTHER_TRANS_COUNT)
    print("\n\n")

    print("LiftOn bad protein trans count\t\t\t: ", LIFTON_BAD_PROT_TRANS_COUNT)
    print("LiftOn good protein trans count\t\t\t: ", LIFTON_GOOD_PROT_TRANS_COUNT)
    print("LiftOn non-coding trans count\t\t\t: ", LIFTON_NC_TRANS_COUNT)
    print("LiftOn OTHER trans count\t\t\t: ", LIFTON_OTHER_TRANS_COUNT)
    print("LiftOn miniprot fixed trans count\t\t\t: ", LIFTON_MINIPROT_FIXED_GENE_COUNT)

    fw.close()
    fw_truncated.close()
    fw_other_trans.close()
    fw_nc_trans.close()

def main(arglist=None):
    args = parse_args(arglist)
    print("Run Lifton!!")
    print(args)
    run_all_liftoff_steps(args)