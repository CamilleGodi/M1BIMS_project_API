#!/usr/bin/python3
#-*- coding: utf8 -*-

######################################################################

import requests

server = "https://rest.ensembl.org"

######################################################################

# focntion de création dico liste gène + espèce (clé : "geneSymbol,organism")

def gene_list_generator(filePath:str): 
    """
    GENERATEUR DE LISTE GENE + ESPECE ASSOCIEE DEPUIS FICHIER EXTERNE
    Sortie : genesList["geneAndOrga"] = ("geneSymbol","organism")
    """
    genesList = {} 
    with open(filePath,"r") as file :
        for line in file.readlines():
            name = line.rstrip()
            infos = line.rstrip().split(",") #rstrip enlève métacaractères, split sépare en une liste selon le séparateur donnée
            genesList[name] = (infos[0] , infos[1])
    return genesList

######################################################################

def ensembl(filePath:str):
    """
    MODULE POUR L'EXPORT DE DONNEES DEPUIS ENSEMBL
    Données pour chaque gène:
    - ensGeneId         -> ID Ensembl du gène
    - ensUrlBrowser     -> lien vers le gène dans le Ensembl Genome Browser
    - ensTranscriptId   -> IDs des transcrits du gène
    - ensProteinId      -> IDs des transcrits du gène
    - ensOrthoList      -> liste des orthologues du gène 
    - ensUrlPrefix      -> préfixe des URLs (dépend de la banque de donnée Ensembl où réside l'espèce)

    Exemple d'accès à l'ID Ensembl pour un gène *A* dans organisme 1 *orga1* 
    (à partir d'un fichier situé en *filePath*) :
    > res = ensembl("filePath") ; res["A,orga1"]["ensGeneId"]
    """

    # création liste gène + espèce
    genesList = gene_list_generator(filePath)

    # préfixe URL selon divisions
    divisionUrl = {
            "EnsemblVertebrates" : "www",
            "EnsemblBacteria" : "bacteria",
            "EnsemblMetazoa" : "metazoa",
            "EnsemblProtists" : "protists",
            "EnsemblFungi" : "fungi",
            "EnsemblPlants" : "plants"
            }

    # Data Ensembl pour chaque gène
    ensemblData = {}
    for geneAndOrga in genesList.keys():
        geneSymbol = genesList[geneAndOrga][0]; organism = genesList[geneAndOrga][1]
        # Initialisation dico associé au gène
        ensemblData[geneAndOrga] = {}

        # Vérifier que espèce dans Ensembl
        ext = f"/info/genomes/taxonomy/{organism}?"
        taxo = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
        if not taxo.ok:
            ensemblData[geneAndOrga] = { "ensGeneId" : "Data not found" ,
                                        "ensUrlBrowser" : "Data not found",
                                        "ensTranscriptId" : ["Data not found"],
                                        "ensProteinId" : ["Data not found"],
                                        "ensOrthoList" : ["Data not found"],
                                        "ensUrlPrefix" : "Data not found" }
        else:
            # Requête infos gène dans Ensembl
            ext = f"/lookup/symbol/{organism}/{geneSymbol}?expand=1"
            r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})

            if not r.ok:
                ensemblData[geneAndOrga] = {"ensGeneId" : "Data not found" ,
                                            "ensUrlBrowser" : "Data not found",
                                            "ensTranscriptId" : ["Data not found"],
                                            "ensProteinId" : ["Data not found"],
                                            "ensOrthoList" : ["Data not found"],
                                            "ensUrlPrefix" : "Data not found"}
            else:
                decoded = r.json()

                # Gene ID
                geneId = decoded["id"]

                # Transcript et protein IDs
                transIds = []; protIds = []
                for transcrit in decoded["Transcript"] :
                    transIds.append(transcrit["id"])
                    if "Translation" in transcrit.keys() :
                        protIds.append(transcrit["Translation"]["id"])

                # Lien genome browser + préfixe url (dbext)
                decodedTaxo = taxo.json()
                dbext = divisionUrl[decodedTaxo[0]["division"]]
                geneUrl = f"https://{dbext}.ensembl.org/{organism}/Gene/Summary?db=core;g={geneId}"

                # Liste orthologues
                ext = f"/homology/id/{geneId}?"
                r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})

                if not r.ok:
                    ensemblData[geneAndOrga] = {"ensGeneId" : geneId ,
                                            "ensUrlBrowser" : geneUrl,
                                            "ensTranscriptId" : transIds,
                                            "ensProteinId" : protIds,
                                            "ensOrthoList" : ["Data not found"], 
                                            "ensUrlPrefix" : dbext}
                else:
                    decoded = r.json()
                    orthos = []
                    for each in decoded["data"]:
                        for ort in each["homologies"]:
                            orthos.append(ort["target"]["id"])

                    ### Infos pour le gène
                    ensemblData[geneAndOrga] = {"ensGeneId" : geneId ,
                                            "ensUrlBrowser" : geneUrl,
                                            "ensTranscriptId" : transIds,
                                            "ensProteinId" : protIds,
                                            "ensOrthoList" : orthos,
                                            "ensUrlPrefix" : dbext}
    return ensemblData

######################################################################

#TEST fonction liste gènes et organismes associés:
#for k,v in gene_list_generator("GeneSymbols.txt").items():
#    print(k,v)

#TEST module individuel:
#for k,v in ensembl("GeneSymbols.txt").items():
#    print(k,v)