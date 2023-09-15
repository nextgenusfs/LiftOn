from lifton import extract_features
import argparse
from pyfaidx import Fasta, Faidx

from lifton import align, adjust_cds_boundaries, fix_trans_annotation, lifton_class

def segments_overlap(segment1, segment2):
    # Check if the segments have valid endpoints
    # print("Checking two segments overlapping.!")
    if len(segment1) != 2 or len(segment2) != 2:
        raise ValueError("Segments must have exactly 2 endpoints")
    
    # Sort the segments by their left endpoints
    segment1, segment2 = sorted([segment1, segment2], key=lambda x: x[0])

    # Check if the right endpoint of the first segment is greater than or equal to the left endpoint of the second segment
    return segment1[1] >= segment2[0]


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
        '-o', default='stdout', metavar='FILE',
        help='write output to FILE in same format as input; by default, output is written to terminal (stdout)'
    )

    outgrp.add_argument(
        '-dir', default='intermediate_files', metavar='DIR',
        help='name of directory to save intermediate fasta and SAM files; default is "intermediate_files"',
    )

    parser.add_argument('-V', '--version', help='show program version', action='version', version='v1.6.3')
    parser.add_argument(
        '-p', default=1, type=int, metavar='P', help='use p parallel processes to accelerate alignment; by default p=1'
    )

    parser.add_argument(
        '-proteins', metavar='fasta', required=True,
        help='the reference protein sequences.'
    )

    liftoffrefrgrp = parser.add_argument_group('Required input (Liftoff annotation)')

    liftoffgrp = liftoffrefrgrp.add_mutually_exclusive_group(required=True)
    liftoffgrp.add_argument(
        '-liftoff', metavar='gff',
        help='the annotation generated by Liftoff'
    )
    liftoffgrp.add_argument(
        '-liftoffdb', metavar='gff-DB',
        help='name of Liftoff database; if not specified, the -liftoff '
                                  'argument must be provided and a database will be built automatically'
    )

    miniprotrefrgrp = parser.add_argument_group('Required input (miniprot annotation)')

    miniprotgrp = miniprotrefrgrp.add_mutually_exclusive_group(required=True)
    miniprotgrp.add_argument(
        '-miniprot', metavar='gff',
        help='the annotation generated by miniprot'
    )
    miniprotgrp.add_argument(
        '-miniprotdb', metavar='gff-DB',
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

    fai_protein = Fasta(args.proteins)
    # print("fai: ", fai_protein["rna-NM_001370185.1-2"])

    l_feature_db, m_feature_db = extract_features.extract_features_to_fix(ref_chroms, liftover_type, args)
    print("l_feature_db: ", l_feature_db)
    
    fw = open("lifton.gff3", "w")


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


    for gene in l_feature_db.features_of_type('gene'):

        lifton_gene = lifton_class.Lifton_GENE(gene)

        transcripts = l_feature_db.children(gene, featuretype='mRNA')  # Replace 'exon' with the desired child feature type

        for transcript in list(transcripts):
            lifton_gene.add_transcript(transcript)
            
            print(transcript)
            exons = l_feature_db.children(transcript, featuretype='exon')  # Replace 'exon' with the desired child feature type
            for exon in list(exons):
                print(exon)
        print("\n\n")
        # lifton_gene = lifton_class.Lifton_gene(feature)

    #     overlaps = l_feature_db.region(region=("chr1", 110000, 120000), featuretype="exon")
    #     for overlap_feature in overlaps:
    #         print(overlap_feature)
    #         # print(f"Gene {feature.id} overlaps with exon {overlap_feature.id}")

    #     # # Check for overlap
    #     # if gene_of_interest.overlaps(feature):
    #     #     print(f'Gene {gene_of_interest_id} overlaps with gene {feature.id}')
    #     #     # You can perform any specific action here if there's an overlap

        # lifton_gene.update_boundaries()
        # lifton_gene.write_entry(1)
        # lifton_gene.print()


    # for aa_trans_id in fai_protein.keys():
    #     l_entry = None
    #     m_entry = None
    #     try:
    #         l_entry = l_feature_db[aa_trans_id]
    #         l_lifton_aln = align.parasail_align("liftoff", l_feature_db, l_entry, fai, fai_protein, aa_trans_id)
    #         print("l_lifton_aln: ", l_lifton_aln)
    #     except:
    #         # print("An exception occurred")
    #         pass


    #     try:
    #         m_ids = m_id_dict[aa_trans_id]
    #         print("aa_trans_id: ", aa_trans_id)
    #         for m_id in m_ids:
    #             print("\tm_id: ", m_id)
    #             m_entry = m_feature_db[m_id]
    #             m_lifton_aln = align.parasail_align("miniprot", m_feature_db, m_entry, fai, fai_protein, aa_trans_id)
    #             print("\tm_lifton_aln: ", m_lifton_aln)
    #     except:
    #         # print("An exception occurred")
    #         pass

    #     if l_entry is not None and m_entry is not None:   
    #         print("Entry exist in both Liftoff & miniprot")
    #     elif l_entry is None and m_entry is not None:   
    #         print("Only miniprot exists")
    #     elif l_entry is not None and m_entry is None:   
    #         print("Only Liftoff exists")








    # # Iterating miniprot
    # for feature in m_feature_db.features_of_type("mRNA"):
    #     # Print all attributes and their values for the feature
    #     # print(feature)

    #     aa_trans_id = str(feature.attributes["Target"][0]).split(" ")[0]
    #     # miniprot_identity = float(feature.attributes["Identity"][0])

    #     miniprot_trans_id = feature.attributes["ID"][0]
    #     m_entry = m_feature_db[miniprot_trans_id]

    #     # print(m_entry)
    #     miniprot_identity = 0.0
    #     # miniprot_identity, m_children, m_aln_query, m_aln_comp, m_aln_ref, m_cdss_aln_boundary, m_protein, ref_protein         
    #     m_lifton_aln = align.parasail_align("miniprot", m_feature_db, m_entry, fai, fai_protein, aa_trans_id)
    #     miniprot_identity = m_lifton_aln.identity
        
    #     # for attr_name, attr_value in feature.attributes.items():
    #     #     print(f"{attr_name}: {attr_value}")

    #     liftoff_identity = 0.0
    #     try:
    #         l_entry = l_feature_db[aa_trans_id]
    #         # liftoff_identity, l_children, l_aln_query, l_aln_comp, l_aln_ref, l_cdss_aln_boundary, l_protein, ref_protein = 
    #         l_lifton_aln = align.parasail_align("liftoff", l_feature_db, l_entry, fai, fai_protein, aa_trans_id)
    #         liftoff_identity = l_lifton_aln.identity

    #     except:
    #         print("An exception occurred")

    #     # if miniprot_identity > liftoff_identity and liftoff_identity > 0:

    #     if liftoff_identity >= 0:
    #         overlap = segments_overlap((m_entry.start, m_entry.end), (l_entry.start, l_entry.end))
    #         if (overlap and m_entry.seqid == l_entry.seqid):
    #             print("aa_trans_id: ", aa_trans_id)

    #             fix_trans_annotation.fix_transcript_annotation(m_lifton_aln, l_lifton_aln, fai, fw)


    #             print(aa_trans_id)
    #             print(m_entry)
    #             print(l_entry)
    #             print("miniprot_identity: ", miniprot_identity, "; number of children: ", len(m_lifton_aln.cds_children))
    #             print("liftoff_identity: ", liftoff_identity, "; number of children: ", len(l_lifton_aln.cds_children))
    #             print("\n\n")
    #     elif liftoff_identity == 0:
    #         pass

    fw.close()






    #     try:
    #         m_entry = m_feature_db[aa_trans_id]
    #         miniprot_identity = parasail_align(m_feature_db, m_entry, fai, fai_protein, aa_trans_id)
    #     except:
    #         print("An exception occurred")


        # if aa_trans_id in l_feature_db:
        #     print(aa_trans_id)
        # else:
        #     print(f"Feature not found for {aa_trans_id}")

        # if aa_trans_id in l_feature_db:
        #     print(aa_trans_id) 
            # Example 1: Extract sequence by feature ID
            # l_entry = l_feature_db[aa_trans_id]
            # print(l_entry)

    # chrom_seq = reference_fasta_idx[current_chrom][:].seq

    # if liftover_type == "unplaced":
    #     open(args.dir + "/unplaced_genes.fa", 'w')
    # for chrom in ref_chroms:
    #     fasta_out = get_fasta_out(chrom, args.reference, liftover_type, args.dir)
    #     sorted_parents = sorted(list(parent_dict.values()), key=lambda x: x.seqid)

    #     if len(sorted_parents) == 0:
    #         sys.exit(
    #             "GFF does not contain any gene features. Use -f to provide a list of other feature types to lift over.")
    #     write_gene_sequences_to_file(chrom, args.reference, fai, sorted_parents, fasta_out, args)
    #     fasta_out.close()


    # l_feature_hierarchy, l_feature_db, l_ref_parent_order, m_feature_hierarchy, m_feature_db, m_ref_parent_order = extract_features.extract_features_to_fix(ref_chroms, liftover_type, args)

        # self.parents = parents
        # self.intermediates = intermediates
        # self.children = children

    
    

    # m_entry = m_feature_db["MP000005"]
    # print(m_entry)


    # # print("l_feature_hierarchy: ", l_feature_hierarchy.parents)
    # # print("l_feature_hierarchy: ", l_feature_hierarchy.intermediates)
    
    # # print("l_feature_hierarchy: ", l_feature_hierarchy)
    # print("l_feature_db: ", l_feature_db)
    # # print("l_ref_parent_order: ", len(l_ref_parent_order))
    # # print("m_feature_hierarchy: ", m_feature_hierarchy)
    # print("m_feature_db: ", m_feature_db)
    # # print("m_ref_parent_order: ", len(m_ref_parent_order))



def main(arglist=None):
    args = parse_args(arglist)
    print("Run Lifton!!")
    print(args)
    run_all_liftoff_steps(args)