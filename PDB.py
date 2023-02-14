#!/usr/bin/python3
#-*- coding: utf8 -*-

######################################################################

import re
from Bio import Entrez

from GeneDictGenerator import gene_dict_generator

Entrez.email = "erwan.quignon@univ-rouen.fr"

######################################################################

def pdb(filePath:str):
    """
    MODULE POUR L'IMPORT DE DONNEES DEPUIS PDB

    Données pour chaque gène (dico):
    - pdbId             -> ID PDB du gène
    - proteinDomains    -> Domaines protéiques

    Exemple d'accès au PDB ID pour un gène *A* dans organisme 1 *orga_1* 
    (à partir d'un fichier situé en *filePath*):
    > res = ncbi(filePath) ; res["A,orga1"]['pdbId']
    """

    # Récupération de la liste d'ID Uniprot (temporaire)
    UniprotID = {'RAD51,homo_sapiens': {'uniprotID': 'Q06609', 'uniprotName': 'DNA repair protein RAD51 homolog 1'}, 'DMD,mus_musculus': {'uniprotID': 'P11531', 'uniprotName': 'Dystrophin'}, 'CDH2,gallus_gallus': {'uniprotID': 'P10288', 'uniprotName': 'Cadherin-2'}, 'TP53,danio_rerio': {'uniprotID': 'P79734', 'uniprotName': 'Cellular tumor antigen p53'}, 'RAD51,pan_troglodytes': {'uniprotID': 'A0A2J8QDL2', 'uniprotName': 'DNA repair protein RAD51 homolog'}, 'PSBA,pinus_thunbergii': {'uniprotID': 'P69551', 'uniprotName': 'Photosystem II protein D1'}, 'RPL33,pteridium_aquilinum': {'uniprotID': 'E2IH32', 'uniprotName': '50S ribosomal protein L33, chloroplastic'}, 'PHYB,arabidopsis_thaliana': {'uniprotID': 'P14713', 'uniprotName': 'Phytochrome B'}, 'SFA1,saccharomyces_cerevisiae': {'uniprotID': 'P32771', 'uniprotName': 'S-(hydroxymethyl)glutathione dehydrogenase'}, 'SLPA,lactobacillus_acidophilus': {'uniprotID': 'P35829', 'uniprotName': 'S-layer protein'}, 'DRGX,pelodiscus_sinensis': {'uniprotID': 'K7GA16', 'uniprotName': 'No data'}, 'NOTCH1,xenopus_tropicalis': {'uniprotID': 'A2RUV0', 'uniprotName': 'Neurogenic locus notch homolog protein 1'}}

    # Data NCBI pour chaque gène
    pdbData = {}

    for id in UniprotID:
        
        # Insérer code

        #############################################################

        # Insérer code

        #############################################################

        ### Infos pour le gène
        pdbData[id] = {"ncbiFullName" : fullName,
                                "ncbiGeneId" : geneId,
                                "ncbiTranscriptAccess" : listTranscriptAccess,
                                "ncbiProteinAccess" : ncbiProteinAccess }
    return(ncbiData)

######################################################################