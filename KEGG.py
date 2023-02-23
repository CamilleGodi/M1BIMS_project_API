#!/usr/bin/python3
# -*- coding: utf8 -*-
import requests
import re
from NCBI import ncbi

def kegg_data(resNcbi):
    """
    MODULE POUR L'IMPORT DE DONNEES DEPUIS la base de Données KEGG (utilise des IDs NCBI)
    Données pour chaque ID NCBI:
    - infoPath -> dictionnaire retourné associant chaque clé (gène/organisme ) à son ou ses IDs kEGG et les IDs pathways et leurs noms correspondants
    
    """
    infoPath = {}  #dictionnaire des IDs KEGG et noms et IDs des pathways
    
    for keys in resNcbi.keys():
        listIdGene = resNcbi[keys]["ncbiGeneId"]
        keggIDs = []
        for id in listIdGene:
            convUrl = f"http://rest.kegg.jp/conv/genes/ncbi-geneid:{id}" #url pour convertir les IDs NCBI en IDs KEGG
            convResponse = requests.get(convUrl)
            if convResponse.ok:
                try:
                    convData = convResponse.text.split("\t")
                    keggID = convData[1][:-1]  #on recupère tout sauf le dernier élément qui est  "\n"
                except:
                    continue
                keggIDs.append(keggID)
        infoPath[keys] = {'infoPathways': []} #on utilise comme clé GeneAndOrga avec une autre clé pathway initialisée à vide à laquelle on ajoutera des valeurs plus tard
        for keggID in keggIDs: #on parcours la liste des IDs KEGG
            pathIDurl = f"http://rest.kegg.jp/link/pathway/{keggID}"
            pathIDresponse = requests.get(pathIDurl)
            if pathIDresponse.ok:
                pathIDs = [] #liste qui va récupérer les IDs des pathways coresspondant à l'ID KEGG
                for line in pathIDresponse.text.split("\n"):
                    try:
                        patternPathID = re.search("path:(.*)", line)
                        if patternPathID:
                            pathIDs.append(patternPathID.group(1))
                    except:
                        continue
                for pathID in pathIDs:
                    pathUrl = f"http://rest.kegg.jp/get/{pathID}" #requête pour récupérer les noms des pathways
                    pathNameResponse = requests.get(pathUrl)
                    if pathNameResponse.ok:
                        try:
                            patternPathName = re.search("NAME\s+(.*?)\s-", pathNameResponse.text)  #regex récupérant les noms
                            if patternPathName:
                                path = patternPathName.group(1)
                                infoPath[keys]['infoPathways'].append({'keggID': keggID, 'pathID': pathID, 'pathName': path})
                        except:
                            continue
    return infoPath



# resNcbi = ncbi("GeneSymbols.txt")
# a = kegg_data(resNcbi)
# print(a)

 