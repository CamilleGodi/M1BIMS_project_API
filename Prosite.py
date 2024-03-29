#!/usr/bin/python3
#-*- coding: utf8 -*-

######################################################################

import requests

######################################################################

def prosite(resUniprot):
    """
    MODULE POUR L'IMPORT DE DONNEES DEPUIS Prosite

    Données pour chaque gène (dico):
    - prositeID -> ID Prosite
    - prositeLink -> Lien graphique Prosite

    Exemple d'accès à l'ID Prosite pour un gène *A* dans organisme 1 *orga_1* 
    (à partir d'un fichier situé en *filePath*):
    > res = prosite(filePath) ; res["A,orga1"]['prositeID']
    """

    print("### Fetching Prosite data...")

    # Data prosite pour chaque gène
    prositeData = {}

    for keys in resUniprot.keys():
        ids = []
        links= []
        for key in resUniprot[keys]["uniprotID"]:
            url = f"https://prosite.expasy.org/cgi-bin/prosite/PSScan.cgi?seq={key}&output=json"

            try:
                r = requests.get(url)
                decoded = r.json()
                for id in decoded["matchset"]:
                    ids.append(id["signature_ac"])
                links.append(f"https://prosite.expasy.org/cgi-bin/prosite/PSView.cgi?spac={key}")

            except requests.exceptions.JSONDecodeError:
                pass

            # Elimination des duplicats
            prositeIDsNoDupli = []
            [prositeIDsNoDupli.append(x) for x in ids if x not in prositeIDsNoDupli]

        #############################################################

        ### Infos pour le gène
        prositeData[keys] = {"prositeID": prositeIDsNoDupli, "prositeLink": links}

    return(prositeData)

######################################################################
