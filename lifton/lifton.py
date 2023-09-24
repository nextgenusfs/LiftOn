from lifton import extract_features
import argparse
from pyfaidx import Fasta, Faidx

from lifton import align, adjust_cds_boundaries, fix_trans_annotation, lifton_class, lifton_utils

def parse_args(arglist):
    print("arglist: ", arglist)
    parser = argparse.ArgumentParser(description='Lift features from one genome assembly to another')
    parser.add_argument('target', help='target fasta genome to lift genes to')

    # refrgrp = parser.add_argument_group('Required input (annotation)')
    # mxgrp = refrgrp.add_mutually_exclusive_group(required=True)
    # mxgrp.add_argument(
    #     '-g', metavar='GFF', help='annotation file to lift over in GFF or GTF format'
    # )
    # mxgrp.add_argument(
    #     '-db', metavar='DB', help='name of feature database; if not specified, the -g '
    #                               'argument must be provided and a database will be built automatically'
    # )

    outgrp = parser.add_argument_group('Output')
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

    parser.add_argument(
        '-p', '--proteins', metavar='fasta', required=True,
        help='the reference protein sequences.'
    )

    liftoffrefrgrp = parser.add_argument_group('Required input (Liftoff annotation)')

    liftoffgrp = liftoffrefrgrp.add_mutually_exclusive_group(required=True)
    liftoffgrp.add_argument(
        '-l', '--liftoff', metavar='gff',
        help='the annotation generated by Liftoff'
    )
    liftoffgrp.add_argument(
        '-ldb', '--liftoffdb', metavar='gff-DB',
        help='name of Liftoff database; if not specified, the -liftoff '
                                  'argument must be provided and a database will be built automatically'
    )

    miniprotrefrgrp = parser.add_argument_group('Required input (miniprot annotation)')

    miniprotgrp = miniprotrefrgrp.add_mutually_exclusive_group(required=True)
    miniprotgrp.add_argument(
        '-m', '--miniprot', metavar='gff',
        help='the annotation generated by miniprot'
    )
    miniprotgrp.add_argument(
        '-mdb', '--miniprotdb', metavar='gff-DB',
        help='name of miniprot database; if not specified, the -miniprot '
                                  'argument must be provided and a database will be built automatically'
    )

    parser._positionals.title = 'Required input (sequences)'
    parser._optionals.title = 'Miscellaneous settings'

    parser._action_groups = [parser._positionals, liftoffrefrgrp, miniprotrefrgrp, outgrp, parser._optionals]
    args = parser.parse_args(arglist)
    return args



# def extract_features_to_lift(ref_chroms, liftover_type, parents_to_lift, args):
#     print("extracting features")
#     if os.path.exists(args.dir) is False:
#         os.mkdir(args.dir)
#     feature_db = create_feature_db_connections(args)
#     feature_hierarchy, parent_order = seperate_parents_and_children(feature_db, parents_to_lift)
#     get_gene_sequences(feature_hierarchy.parents, ref_chroms, args, liftover_type)
#     return feature_hierarchy, feature_db, parent_order


# def lift_original_annotation(ref_chroms, target_chroms, lifted_features_list, args, unmapped_features, parents_to_lift):
#     liftover_type = "chrm_by_chrm"
#     if target_chroms[0] == args.target and args.exclude_partial == False:
#         min_cov, min_seqid = 0.05, 0.05
#     else:
#         min_cov, min_seqid = args.a, args.s

#     feature_hierarchy, feature_db, ref_parent_order = extract_features.extract_features_to_lift(ref_chroms,
#                                                                                                 liftover_type,
#                                                                                                 parents_to_lift, args)

def run_all_liftoff_steps(args):
    print(">> run_all_lifton_steps")
    lifted_feature_list = {}
    unmapped_features = []

    liftover_type = "chrm_by_chrm"
    ref_chroms = []
    
    fai = Fasta(args.target)
    print("fai: ", fai.keys())
    print(args.output)
    print(args.dir)

    fai_protein = Fasta(args.proteins)

    l_feature_db, m_feature_db = extract_features.extract_features_to_fix(ref_chroms, liftover_type, args)
    print("l_feature_db: ", l_feature_db)

    fw = open(args.output, "w")
    # fw_protein = open("lifton_protein.gff3", "w")

    m_id_dict = {}
    for feature in m_feature_db.features_of_type("mRNA"):
        # Print all attributes and their values for the feature
        miniprot_id = feature["ID"][0]

        aa_trans_id = str(feature.attributes["Target"][0]).split(" ")[0]
        # print("aa_trans_id: ", aa_trans_id)
        if aa_trans_id in m_id_dict.keys():
            m_id_dict[aa_trans_id].append(miniprot_id)
        else:
            m_id_dict[aa_trans_id] = [miniprot_id]

    # for key, vals in m_id_dict.items():
    #     print("key : ", key)
    #     print("vals: ", vals)

    # gene_of_interest_id = "gene-RINT1"
    # gene_of_interest = l_feature_db[gene_of_interest_id]


    ################################
    # Iterating Liftoff transcript
    ################################
    # # Iterate through the features in the database and collect unique feature types
    # print("l_feature_db.features_of_type('mRNA')", l_feature_db.all_features())
    # for feature in l_feature_db.all_features(strand="+"):
    # # for feature in l_feature_db.features_of_type("mRNA"):
    #     print("feature ", feature)


    # print(" m_feature_db.features_of_type('mRNA'):",  m_feature_db.all_features())
    # for feature in m_feature_db.features_of_type("mRNA"):
    #     print("feature ", feature)



    for gene in l_feature_db.features_of_type('gene'):#, limit=("chr1", 0, 250000000)):
    # for gene in l_feature_db.features_of_type('gene', limit=("NC_000069.7", 142270709, 142273588)):
        lifton_gene = lifton_class.Lifton_GENE(gene)
        
        # transcripts = l_feature_db.children(gene, featuretype='mRNA')  # Replace 'exon' with the desired child feature type
        transcripts = l_feature_db.children(gene, level=1)  # Replace 'exon' with the desired 

        # lifton_gene.write_entry(fw)
        # lifton_gene.write_entry(fw_protein)

        for transcript in list(transcripts):
            # print("transcript: ", transcript)
            lifton_gene.add_transcript(transcript)
            transcript_id = transcript["ID"][0]
    
            exons = l_feature_db.children(transcript, featuretype='exon')  # Replace 'exon' with the desired child feature type
            for exon in list(exons):
                lifton_gene.add_exon(transcript_id, exon)
                # print(exon)

            cdss = l_feature_db.children(transcript, featuretype='CDS')  # Replace 'exon' with the desired child feature type
            # print(">> ### >> cdss: list(cdss): ", len(list(cdss)))
            # print("list(cdss): ", len(list(cdss)))

            cds_num = 0
            for cds in list(cdss):
                lifton_gene.add_cds(transcript_id, cds)
                cds_num += 1
            # print("cds: ", cds_num)

            if (cds_num == 0) or (transcript_id not in fai_protein.keys()) or (transcript_id not in m_id_dict.keys()) or transcript_id == "rna-NM_003240.5":
                # or transcript_id == "rna-NM_001394862.1" or transcript_id == "rna-NM_001039127.6": # => MANE
                # 
                ################################
                # Write out those that 
                #   (1) do not have proper protein sequences.
                #   (2) transcript_id not in proteins
                #   (3) transcript ID not in miniprot 
                ################################
                # lifton_gene.transcripts[transcript_id].write_entry(fw)
                # print("Write out 1")
                pass

            else:
                ################################
                # Protein sequences are in both Liftoff and miniprot
                #   Fix the protein sequences
                ################################
                
                ################################
                # liftoff transcript alignment
                ################################
                l_lifton_aln = align.parasail_align("liftoff", l_feature_db, transcript, fai, fai_protein, transcript_id)

                # print("After liftoff alignment")

                ################################
                # miniprot transcript alignment
                ################################
# try:
                # print("Inside miniprot alignment")
                print("transcript_id: ", transcript_id)
                print(gene)
                
                m_ids = m_id_dict[transcript_id]
                liftoff_miniprot_overlapping = False

                ################################
                # Case 1: at least 1 miniprot and Liftoff transcripts overlapping
                ################################
                for m_id in m_ids:
                    # print("\tm_id: ", m_id)
                    m_entry = m_feature_db[m_id]
                    m_lifton_aln = align.parasail_align("miniprot", m_feature_db, m_entry, fai, fai_protein, transcript_id)
                    # print("\tm_lifton_aln: ", m_lifton_aln)
                    overlap = lifton_utils.segments_overlap((m_entry.start, m_entry.end), (transcript.start, transcript.end))

                    # print((m_entry.start, m_entry.end), (transcript.start, transcript.end))
                    # print("overlap: ", overlap, ";  share transcript seqid: ", m_entry.seqid == transcript.seqid)

                    if overlap and m_entry.seqid == transcript.seqid:
                        liftoff_miniprot_overlapping = True

                        # liftoff_transcript
                        cds_list = fix_trans_annotation.fix_transcript_annotation(m_lifton_aln, l_lifton_aln, fai, fw)

                        # print("Write out 4. Fixing!")
                        # print("\tcds_list: ", len(lifton_gene.transcripts[transcript_id].exons))
                        lifton_gene.update_cds_list(transcript_id, cds_list)
                        # print("\tnew cds_list: ", len(lifton_gene.transcripts[transcript_id].exons))

                        # lifton_gene.transcripts[transcript_id].write_entry(fw)
                        # print("Write out 2")

                        # print(transcript_id)
                        # print(m_entry)
                        # print(l_entry)
                        # print("miniprot_identity: ", miniprot_identity, "; number of children: ", len(m_lifton_aln.cds_children))
                        # print("liftoff_identity: ", liftoff_identity, "; number of children: ", len(l_lifton_aln.cds_children))
                        # print("\n\n")

                # except:
                #     # print("An exception occurred")
                #     print("Exception write")
                #     liftoff_transcript.write_entry(fw)

                ################################
                # Case 2: no miniprot and Liftoff transcripts overlap
                ################################
                # if not liftoff_miniprot_overlapping:
                #     print("Write out 3")
                    # lifton_gene.transcripts[transcript_id].write_entry(fw)

        lifton_gene.write_entry(fw)
        # print("Next gene!!!\n\n")

def main(arglist=None):
    args = parse_args(arglist)
    print("Run Lifton!!")
    print(args)
    run_all_liftoff_steps(args)