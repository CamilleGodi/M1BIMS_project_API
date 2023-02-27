#!/usr/bin/python3
#-*- coding: utf8 -*-

######################################################################

import requests

######################################################################

# NOTE : le site Pfam est décomissionné depuis janvier 2023. Interpro sera donc utilisé à la place.

def pfam(resUniprot):
    """
    MODULE POUR L'IMPORT DE DONNEES DEPUIS Pfam (Interpro)

    Données pour chaque gène (dico):
    - pfamID -> ID Interpro
    - pfamLink -> Lien graphique Interpro

    Exemple d'accès à l'ID Pfam pour un gène *A* dans organisme 1 *orga_1* 
    (à partir d'un fichier situé en *filePath*):
    > res = pfam(filePath) ; res["A,orga1"]['pfamID']
    """

    print("### Fetching Pfam data...")

    # Data NCBI pour chaque gène
    pfamData = {}

    for keys in resUniprot.keys():
        ids = []
        links= []
        for key in resUniprot[keys]["uniprotID"]:
            url = f"https://www.ebi.ac.uk/interpro/api/entry/interpro/protein/uniprot/{key}"

            try:
                r = requests.get(url)
                decoded = r.json()
                for id in decoded["results"]:
                    ids.append(id["metadata"]["accession"])
                    links.append(f"https://www.ebi.ac.uk/interpro/protein/reviewed/{id['proteins'][0]['accession']}/")

            except requests.exceptions.JSONDecodeError:
                pass
            
        #############################################################

        ### Infos pour le gène
        pfamData[keys] = {"pfamID": ids, "pfamLink": links}
    print("Pfam done")
    return(pfamData)

######################################################################
