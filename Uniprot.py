#!/usr/bin/python3
#-*- coding: utf8 -*-

######################################################################

import requests

from Bio import Entrez
from GeneDictGenerator import gene_dict_generator

Entrez.email = "erwan.quignon@univ-rouen.fr"

######################################################################

def uniprot(filePath:str):
    """
    MODULE POUR L'IMPORT DE DONNEES DEPUIS UNIPROT

    Données pour chaque gène (dico):
    - uniprotID             -> ID Uniprot du gène
    - uniprotName           -> Nom du gène dans Uniprot

    Exemple d'accès au Uniprot Gene ID pour un gène *A* dans organisme 1 *orga_1* 
    (à partir d'un fichier situé en *filePath*):
    > res = uniprot(filePath) ; res["A,orga1"]['uniprotID']
    """

    print("### Fetching Uniprot data...")

    # Création liste gène + espèce
    genesList = gene_dict_generator(filePath)

    # Data UNIPROT pour chaque gène
    uniprotData = {}

    for geneAndOrga in genesList.keys():
        geneSymbol, organism = genesList[geneAndOrga][0], genesList[geneAndOrga][1]
        # Initialisation dico associé au gène
        uniprotData[geneAndOrga] = {}
        ids = []
        names = []

        # Création de l'URL

        url = f"https://rest.uniprot.org/uniprotkb/search?query={'organism_name:' + organism}+{'gene_exact:' + geneSymbol}&format=json"

        # Lecture de la réponse serveur

        r = requests.get(url)
        decoded = r.json()

        # Récupération des valeurs

        for id in decoded["results"]:
            ids.append(id["primaryAccession"])
            try:
                names.append(id["proteinDescription"]["recommendedName"]["fullName"]["value"])
            except KeyError:
                names.append(id["proteinDescription"]["submissionNames"][0]["fullName"]["value"])

        # Elimination des duplicats
        uniNamesnoDuplicate = []
        [uniNamesnoDuplicate.append(x) for x in names if x not in uniNamesnoDuplicate]

        #############################################################

        ### Infos pour le gène

        uniprotData[geneAndOrga] = {"uniprotID" : ids,
                                "uniprotName" : uniNamesnoDuplicate
                                }

        #############################################################

    return(uniprotData)

######################################################################
