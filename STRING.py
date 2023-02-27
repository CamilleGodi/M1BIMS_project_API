#!/usr/bin/python3
# -*- coding: utf8 -*-
import requests
import json

string_api_url = "https://version-11-5.string-db.org/api"
output_format = "tsv-no-header"
method = "get_string_ids"

def network_link_string(resUniprot):

    """
    MODULE POUR L'IMPORT DE DONNEES DEPUIS la base de Données STRING (utilise des IDs Uniprot)
    Données pour chaque ID Uniprot:
    - StringID   -> dictionnaire retourné par la fonction et qui contient les identifiants STRING

    """

    print("### Fetching STRING data...")

    infoString = {} #initialisation du dictionnaire
    
    for keys in resUniprot.keys():
        IdsUniprot = []
        for key in resUniprot[keys]["uniprotID"]:
            IdsUniprot.append(key)

        
    #création d'une fonction récupérant les ids des espèces dans Uniprot à partir d'une liste IDs Uniprot
        def species_uniprot_id(IdsUniprot):
            species = [] # identifiant des espèces dans la base de données Uniprot nécessaire pour les requêtes STRING
            for id in IdsUniprot:
                url = f"https://www.uniprot.org/uniprot/{id}.json"
                response = requests.get(url)
                data = json.loads(response.text)
                organism = data['organism']
                species.append(organism['taxonId'])
            return species
        species_uniprot = species_uniprot_id(IdsUniprot)  #récupération de la sortie de la fonction species_uniprot_id(IdsUniprot)
        
        #initialisation des listes links et network_zoom et du dictionnaire dictLink
    #    links = []
    #    network_zoom = [] 
        for species_id in species_uniprot:
                params = {
                    "identifiers" : "\r".join(IdsUniprot),
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
                        infoString[keys]= {"StringID": string_identifier}
                    except:
                        continue
                    # récupérations des liens vers le réseau d'interaction
                    #links = f"https://string-db.org/network/{string_identifier}"
                    #network_zoom = f"https://string-db.org/api/highres_image/network?identifiers={string_identifier}"
    print("STRING done")            
    return infoString

#from Uniprot import uniprot
#resUniprot =uniprot("GeneSymbols.txt")
#a = network_link_string(resUniprot)
#print(a)