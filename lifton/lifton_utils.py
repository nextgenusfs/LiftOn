import re
from Bio.Seq import Seq
from lifton import align, lifton_class

def segments_overlap(segment1, segment2):
    # Check if the segments have valid endpoints
    # print("Checking two segments overlapping.!")

    # print(segment1, segment2)

    if len(segment1) != 2 or len(segment2) != 2:
        raise ValueError("Segments must have exactly 2 endpoints")
    
    # Sort the segments by their left endpoints
    segment1, segment2 = sorted([segment1, segment2], key=lambda x: x[0])


    # Check if the right endpoint of the first segment is greater than or equal to the left endpoint of the second segment
    # print(segment1[1] >= segment2[0])

    return segment1[1] >= segment2[0]


def custom_bisect_insert(sorted_list, element_to_insert):
    low = 0
    high = len(sorted_list)

    while low < high:
        mid = (low + high) // 2
        if sorted_list[mid].entry.end < element_to_insert.entry.end:
            low = mid + 1
        else:
            high = mid

    sorted_list.insert(low, element_to_insert)

def get_ID_base(id):

    id_base = id.split("_")[0]
    return id_base

def get_trans_ID_base(id):

    # Regular expression pattern to match the desired substrings
    pattern = r'[A-Za-z0-9_]+-([A-Za-z0-9_]+_\d+\.\d+)'

    match = re.search(pattern, id)
    id_base = ""
    if match:
        id_base = match.group(0)  # Full match

    return id_base

def get_parent_features_to_lift(feature_types_file):
    feature_types = ["gene"]
    if feature_types_file is not None:
        f = open(feature_types_file)
        for line in f.readlines():
            feature_types.append(line.rstrip())
    return feature_types


def update_copy(id_base, copy_num_dict):
    if id_base in copy_num_dict.keys():
        copy_num_dict[id_base] += 1
    else:
        copy_num_dict[id_base] = 0


def LiftOn_no_miniprot(lifton_gene, transcript_id, fai, fai_protein, lifton_status, outdir, LIFTON_BAD_PROT_TRANS_COUNT):
    on_lifton_aln, good_trans = lifton_gene.fix_truncated_protein(transcript_id, fai, fai_protein, lifton_status)
    # SETTING LiftOn score

    if on_lifton_aln.identity < 1:
        # Writing out truncated miniprot annotation
        on_lifton_aln.write_alignment(outdir, "lifton", transcript_id)
    if not good_trans:
        LIFTON_BAD_PROT_TRANS_COUNT += 1

    return LIFTON_BAD_PROT_TRANS_COUNT
    

def LiftOn_check_miniprot_alignment(chromosome, transcript, lifton_status, m_id_dict, m_feature_db, tree_dict, fai, fai_protein, transcript_id):
    m_lifton_aln = None
    has_valid_miniprot = False
    if (transcript_id in m_id_dict.keys()):
        #############################################
        # Step 3.6.1.1: Liftoff annotation is not perfect & miniprot annotation exists => Fix by protein information
        #############################################
        m_ids = m_id_dict[transcript_id]

        for m_id in m_ids:

            ##################################################
            # Check 1: Check if the miniprot transcript is overlapping the current gene locus
            ##################################################
            m_entry = m_feature_db[m_id]
            overlap = segments_overlap((m_entry.start, m_entry.end), (transcript.start, transcript.end))
            if not overlap or m_entry.seqid != transcript.seqid:
                print("Not overlapping")
                continue

            ##################################################
            # Check 2: reference overlapping status
            #   1. Check it the transcript overlapping with the next gene
            # Check the miniprot protein overlapping status
            # The case I should not process the transcript 
            #   1. The Liftoff does not overlap with other gene
            #   2. The miniprot protein overlap the other gene
            ##################################################
            ovps_liftoff = tree_dict[chromosome].overlap(transcript.start, transcript.end)
            ovps_miniprot = tree_dict[chromosome].overlap(m_entry.start, m_entry.end)

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

            ################################
            # Step 3.6.2: Protein sequences are in both Liftoff and miniprot & overlap
            #   Fix & update CDS list
            ################################
            ################################
            # Step 3.6.3: miniprot transcript alignment
            ################################
            has_valid_miniprot = True

            if m_lifton_aln == None or m_lifton_aln.identity > lifton_status.miniprot:
                # # Writing out truncated miniprot annotation
                # m_lifton_aln.write_alignment(outdir, "miniprot", m_id)
                # SETTING miniprot identity score
                
                m_lifton_aln = align.parasail_align("miniprot", m_feature_db, m_entry, fai, fai_protein, transcript_id)
                lifton_status.miniprot = m_lifton_aln.identity
        
    return m_lifton_aln, has_valid_miniprot
            