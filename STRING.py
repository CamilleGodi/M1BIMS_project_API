#!/usr/bin/python3
# -*- coding: utf8 -*-
import requests
import json
string_api_url = "https://version-11-5.string-db.org/api"
output_format = "tsv-no-header"
method = "get_string_ids"

def network_link_string(IDsUniprot):

    """
    MODULE POUR L'IMPORT DE DONNEES DEPUIS la base de Données STRING (utilise des IDs Uniprot)
    Données pour chaque ID Uniprot:
    - species_id    -> identifiant des espèces dans la base de données Uniprot nécessaire pour les requêtes STRING
    - string_identifier  -> identifiant STRING 
    - links  ->  lien vers le réseau d'interaction 
    - network_zoom  -> haute résolution de l'image de l'interaction
    - dictLink   -> dictionnaire retourné par la fonction et qui récupère les Links et les network_zoom

    """
    #création d'une fonction récupérant les ids des espèces dans Uniprot à partir d'une liste IDs Uniprot
    def species_uniprot_id(listIDs):
        species = []
        for id in listIDs:
            url = f"https://www.uniprot.org/uniprot/{id}.json"
            response = requests.get(url)
            data = json.loads(response.text)
            organism = data['organism']
            species.append(organism['taxonId'])
        return species
    species_uniprot = species_uniprot_id(IDsUniprot)
     
    #initialisation des listes links et network_zoom et du dictionnaire dictLink
    links = []
    network_zoom = []
    dictLink = {}  
    for species_id in species_uniprot:
            params = {
                "identifiers" : "\r".join(IDsUniprot), # your protein list
                "species" : species_id,   
                "limit" : 1, 
                "echo_query" : 1,  
                }

            request_url = "/".join([string_api_url, output_format, method])

            results = requests.post(request_url, data=params)  #requête pour récupérer des informations dans la base de données STRING
            for line in results.text.strip().split("\n"):
                try:
                    l = line.split("\t")
                    string_identifier = l[2]  #On récupère les identifiants STRING
                except:
                    continue
                # récupérations des liens vers le réseau d'interaction
                links = f"https://string-db.org/network/{string_identifier}"
                network_zoom = f"https://string-db.org/api/highres_image/network?identifiers={string_identifier}"
                dictLink[species_id] = {"link": links, "zoom": network_zoom}
    return dictLink

# listeIDuniprot = ["Q06609", "P11531", "P10288", "P79734", "A0A2J8QDL2","A0A891GQG3", "K7GA16", "P69551", "P14713", "P32771", "P35829", "A2RUV0"]

# essai = network_link_string(listeIDuniprot)
# print(essai)