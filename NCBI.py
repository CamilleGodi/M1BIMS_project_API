#!/usr/bin/python3
#-*- coding: utf8 -*-

######################################################################

import re
from Bio import Entrez

from GeneDictGenerator import gene_dict_generator

Entrez.email = "camille.godi@univ-rouen.fr"

######################################################################

def ncbi(filePath:str):
    """
    MODULE POUR L'IMPORT DE DONNEES DEPUIS NCBI

    Données pour chaque gène (dico):
    - ncbiFullName           -> Nom commun complet du gène
    - ncbiGeneId             -> ID NCBI du gène
    - ncbiTranscriptAccess   -> Access number des transcrits du gène (via RefSeq)
    - ncbiProteinAccess      -> Access number des transcrits du gène (via RefSeq)

    Exemple d'accès au NCBI Gene ID pour un gène *A* dans organisme 1 *orga_1* 
    (à partir d'un fichier situé en *filePath*):
    > res = ncbi(filePath) ; res["A,orga1"]['ncbiGeneId']
    """

    # création liste gène + espèce
    genesList = gene_dict_generator(filePath)

    # Data NCBI pour chaque gène
    ncbiData = {}

    for geneAndOrga in genesList.keys():
        geneSymbol = genesList[geneAndOrga][0]; organism = genesList[geneAndOrga][1]
        # Initialisation dico associé au gène
        ncbiData[geneAndOrga] = {}

        # Chercher les séquences correspondant à nos critères
        handle = Entrez.esearch(db = "Gene", 
                                term = f"({geneSymbol}[Gene Name]) AND {organism}[Organism]")

        # Enregistrer IDs
        records = Entrez.read(handle)
        geneId = records["IdList"]

        # Chercher nom complet
        handle = Entrez.efetch(db = "Gene",
                                id = geneId,
                                rettype = "gb",
                                retmode = "text")
        text = handle.read()

        if re.search("Name: [\w\s\-\,]*", text) :
            fullName = re.sub("Name: ", "", re.search("Name: [\w\s\-\,]*", text).group())
        else :
            if re.search("[\w\s\-\,]*", text.splitlines()[2]):
                fullName = re.search("[\w\s\-\,]*", text.splitlines()[2]).group()

        #############################################################

        ### Refseq
        # Transcrits liés (liste ids)
        handle = Entrez.elink(dbfrom="Gene", id = geneId, linkname = "gene_nuccore_refseqrna")
        recordT = Entrez.read(handle)
        handle.close()
        if len(recordT[0]['LinkSetDb']) > 0:
            linkedTrans = [link["Id"] for link in recordT[0]["LinkSetDb"][0]["Link"]]
            
            # Transcrits liés (liste access numbers)
            handle = Entrez.efetch(db = "nuccore",
                                    id = linkedTrans,
                                    rettype = "gb",
                                    retmode = "text")
            listTranscriptAccess = []
            for line in handle.readlines():
                if re.match("LOCUS", line) :
                    access = re.search("LOCUS[\s]*[\w\_\.]*", line).group()
                    access = re.sub("LOCUS[\s]*", "", access)
                    listTranscriptAccess.append(access)
            if len(listTranscriptAccess) == 0:
                listTranscriptAccess = ["Data not found"]
        else:
            listTranscriptAccess = ["Data not found"]


        # Proteines liées (liste ids)
        handle = Entrez.elink(dbfrom="Gene", id = geneId, linkname = "gene_protein_refseq")
        recordP = Entrez.read(handle)
        handle.close()
        if len(recordP[0]['LinkSetDb']) > 0 :
            linkedProt = [link["Id"] for link in recordP[0]["LinkSetDb"][0]["Link"]]
            # Protéines liés (liste access numbers)
            handle = Entrez.efetch(db = "protein",
                                    id = linkedProt,
                                    rettype = "gb",
                                    retmode = "text")
            ncbiProteinAccess = []
            for line in handle.readlines():
                if re.match("LOCUS", line) :
                    access = re.search("LOCUS[\s]*[\w\_\.]*", line).group()
                    access = re.sub("LOCUS[\s]*", "", access)
                    ncbiProteinAccess.append(access)
            if len(ncbiProteinAccess) == 0:
                ncbiProteinAccess = ["Data not found"]
        else:
            ncbiProteinAccess = ["Data not found"]

        #############################################################

        ### Infos pour le gène
        ncbiData[geneAndOrga] = {"ncbiFullName" : fullName,
                                "ncbiGeneId" : geneId,
                                "ncbiTranscriptAccess" : listTranscriptAccess,
                                "ncbiProteinAccess" : ncbiProteinAccess }
    return(ncbiData)

######################################################################

#TEST module individuel:
#for k,v in ncbi("GeneSymbols.txt").items():
#    print(k,v)