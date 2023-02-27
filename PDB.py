#!/usr/bin/python3
#-*- coding: utf8 -*-

######################################################################

import requests

######################################################################

def pdb(resUniprot):
    """
    MODULE POUR L'IMPORT DE DONNEES DEPUIS PDB

    Données pour chaque gène (dico):
    - pdbID -> Liste avec ID PDB du gène et le domaine associé (liste de listes)

    Exemple d'accès aux données pour un gène *A* dans organisme 1 *orga_1* 
    (à partir d'un fichier situé en *filePath*):
    > res = pdb(filePath) ; res["A,orga1"]['pdbID']
    """

    print("### Fetching PDB data...")

    # Data NCBI pour chaque gène
    pdbData = {}

    for keys in resUniprot.keys():
        ids = []
        for key in resUniprot[keys]["uniprotID"]:
            url = 'https://search.rcsb.org/rcsbsearch/v2/query?json={"query": {"type": "terminal", "service": "full_text", "parameters": {"value": "' + str(key) + '"} }, "return_type": "entry"}'

            try:
                r = requests.get(url)
                decoded = r.json()

                for id in decoded["result_set"]:
                    url = f"https://data.rcsb.org/rest/v1/core/entry/{id['identifier']}"
                    r = requests.get(url)
                    deco = r.json()
                    ids.append([id["identifier"], deco["struct"]["title"]])
            except requests.exceptions.JSONDecodeError:
                pass
            
        #############################################################

        ### Infos pour le gène
        pdbData[keys] = {"pdbID" : ids}

    return(pdbData)

######################################################################
