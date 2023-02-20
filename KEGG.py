#!/usr/bin/python3
# -*- coding: utf8 -*-
import requests
import re

def kegg_data(IDsNBCI):
    """
    MODULE POUR L'IMPORT DE DONNEES DEPUIS la base de Données KEGG (utilise des IDs NCBI)
    Données pour chaque ID NCBI:
    - keggID -> ID kEGG correspondant à chaque ID NCBI
    - pathID -> ID de la voie métabolique associée à l'ID KEGG
    - pathLInk -> lien vers la pageweb KEGG correspondant à la voie métabolique
    - path -> nom de la voie métabolique associée à un ID KEGG
    - infoPath -> dictionnaire retourné associant lui-même un dictionnaire contenant les noms des voies et les liens de la page web comme valeur associée à l'ID de la voie correspondante utilisé comme clé
    """


    infoPath = {}  #dictionnaire final
    keggIDs = []  #liste recpérant les corresondances des ID NCBI dans KEGG
    for id_gene in IDsNBCI:
        
        convUrl = f"http://rest.kegg.jp/conv/genes/ncbi-geneid:{id_gene}"
        convResponse = requests.get(convUrl)
        try:
            convData = convResponse.text.split("\t")
            keggIDs.append(convData[1][:-1])
        except:
            continue 

    for keggID in keggIDs: 
    #    infoKegg = {}    
    #    linkInfoKegg = f"https://www.genome.jp/dbget-bin/www_bget?{keggID}"  #Exemple de lien vers KEGG à partir des IDs KEGG
        
        pathIDurl = f"http://rest.kegg.jp/link/pathway/{keggID}" #1 ère requête recupérant les informations sur IDs des pathways associés aux IDs kKEGG
        pathIDresponse = requests.get(pathIDurl)
        for line in pathIDresponse.text.split("\n"):
            pathIDs = [] #rstocke les IDs des pathways
            try:
                patternPathID = re.search("path:(.*)", line)
                if patternPathID:
                    pathIDs.append(patternPathID.group(1))
            except:
                continue

            for pathID in pathIDs:
                
                pathLink = f"https://www.genome.jp/dbget-bin/www_bget?{pathID}" #lien vers la page web KEGG contenant les onformations sur les pathways
                #print(pathLink)
                pathUrl = "http://rest.kegg.jp/get/{}".format(pathID)  
                pathNameResponse = requests.get(pathUrl) #2e requête récupérant les informations détaillées sur les pathways 
                try:
                    patternPathName = re.search("NAME\s+(.*?)\s-", pathNameResponse.text)  #on récupère le nom de la voie
                    if patternPathName:
                        path = patternPathName.group(1)
                except:
                    continue
                infoPath[pathID] = {"pathway": path, "link": pathLink}
                 
    return keggIDs, infoPath


# ncbi_ids =  ['7157','13405','414745','30590','100611736','809093','9481279','816394','852876','22242','102445482']
          
# essai = kegg_data(ncbi_ids)
# print(essai)

