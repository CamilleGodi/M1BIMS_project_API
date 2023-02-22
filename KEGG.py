#!/usr/bin/python3
# -*- coding: utf8 -*-
import requests
import re
from NCBI import ncbi
def kegg_data(resNcbi):
    """
    MODULE POUR L'IMPORT DE DONNEES DEPUIS la base de Données KEGG (utilise des IDs NCBI)
    Données pour chaque ID NCBI:
    - infoIDs -> dictionnaire retourné assoiant chaque couple (gène/ogranisme ) à son ID KEGG
    - infoPath -> dictionnaire retourné associant chaque couple (gène/ogranisme ) à un ID pathway et le nom correspondant
    
    """
 
#    infoIDkegg = {}  #dictionnaire des IDs KEGG pathways
      #liste recupérant les correspondances des IDs NCBI dans KEGG
    keggIDs = []
    listIdGene = []
    for keys in resNcbi.keys():
        listIdGene.append(resNcbi[keys]["ncbiGeneId"][0])  
    for id in listIdGene:
        convUrl = f"http://rest.kegg.jp/conv/genes/ncbi-geneid:{id}"
        convResponse = requests.get(convUrl)
        try:
            convData = convResponse.text.split("\t") 
            keggIDs.append(convData[1][:-1])
        except:
            continue
    infoPath = {}  #dictionnaire des IDs et noms des pathways
    for keys in resNcbi.keys():
        for keggID in keggIDs: 
            
        #    linkInfoKegg = f"https://www.genome.jp/dbget-bin/www_bget?{keggID}"  #Exemple de lien vers KEGG à partir des IDs KEGG
            
            pathIDurl = f"http://rest.kegg.jp/link/pathway/{keggID}" #1 ère requête recupérant les informations sur IDs des pathways associés aux IDs kKEGG
            pathIDresponse = requests.get(pathIDurl)
            for line in pathIDresponse.text.split("\n"):
                pathIDs = [] #stocke les IDs des pathways
                try:
                    patternPathID = re.search("path:(.*)", line)
                    if patternPathID:
                        pathIDs.append(patternPathID.group(1))
                except:
                    continue
                listPath = []
                for pathID in pathIDs:
    #                    infoPath[pathID] = infoPath[keys]
    #                    pathLink = f"https://www.genome.jp/dbget-bin/www_bget?{pathID}" #lien vers la page web KEGG contenant les onformations sur les pathways
                    #print(pathLink)
                    pathUrl = f"http://rest.kegg.jp/get/{pathID}"     
                    pathNameResponse = requests.get(pathUrl) #2e requête récupérant les informations détaillées sur les pathways 
                    try:
                        patternPathName = re.search("NAME\s+(.*?)\s-", pathNameResponse.text)  #on récupère le nom de la voie
                        if patternPathName:
                            path = patternPathName.group(1)
                            listPath.append((pathID,path))
                    except:
                        continue
                    infoPath =  {keys: {'keggID': keggID, 'pathway': listPath}}

    return infoPath


resNcbi = ncbi("GeneSymbols.txt")
a = kegg_data(resNcbi)
print(a)

#'keggID': keggID,