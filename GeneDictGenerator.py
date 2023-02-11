#!/usr/bin/python3
#-*- coding: utf8 -*-

# fonction de création dico liste gène + espèce (clé : "geneSymbol,organism")

def gene_dict_generator(filePath:str): 
    """
    GENERATEUR DE LISTE GENE + ESPECE ASSOCIEE DEPUIS FICHIER EXTERNE
    Sortie : genesList["gene,Orga"] = ("geneSymbol","organism")
    """
    genesDict = {} 
    with open(filePath,"r") as file :
        for line in file.readlines():
            name = line.rstrip()
            infos = line.rstrip().split(",") #rstrip enlève métacaractères, split sépare en une liste selon le séparateur donnée
            genesDict[name] = (infos[0] , infos[1])
    return genesDict

#TEST fonction liste gènes et organismes associés (gene_list_generator):
#for k,v in gene_dict_generator("GeneSymbols.txt").items():
#    print(k,v)

######################################################################