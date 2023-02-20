#!/usr/bin/python3
# -*- coding: utf8 -*-
from mygene import MyGeneInfo
from goatools import obo_parser
data = MyGeneInfo()


def info_gene_ontology(IDsUniprot):
    """
    MODULE POUR L'IMPORT DE DONNEES DEPUIS la base de Données gene ontology (utilise des IDs Uniprot)
    Données pour chaque ID Uniprot correspondent les trois go termes (bp,cc,mf) :
    - gene_info  -> récupère les IDs correspondant à l'ensemble des IDs uniprot contenus dans la liste fournie en paramètre 
    - go_BPid -> identifiant du processus biologique
    - go_CCid -> identifiant du compartiment cellulaire
    - go_MFid -> identifiant de la fonction moléculaire
    - bioProcess -> dictionnaire retourné associant chaque ID BP au(x) terme(s) correspondants
    - cellFunction -> dictionnaire retourné associant chaque ID MF au(x) terme(s) correspondants
    - cellComponent -> dictionnaire retourné associant chaque ID CC au(x) terme(s) coresspondants
    """
    gene_info = data.querymany(IDsUniprot, scopes="uniprot", fields="go")
    go = obo_parser.GODag("go-basic.obo")
    bioProcess = {}
    cellFunction = {}
    cellComponent = {}
    
    for result in gene_info:
        if "go" in result:
            go_bps = result["go"]["BP"]
            go_ccs = result["go"]["CC"]
            go_mfs = result["go"]["MF"]
            for go_bp in go_bps:
                go_BPid = go_bp["id"]
                go_BPcategory = go_bp["gocategory"]
                BP_term = go_bp["term"]
                bioProcess[go_BPid] = {"biological_process": BP_term}
      #            print(bioProcess)
            for go_cc in go_ccs:
                go_CCid = go_cc["id"]
                go_CCcategory = go_cc["gocategory"]
                CC_term = go_cc["term"]
                cellComponent[go_CCid] = {"cell_component": CC_term}             
     #            print(cellComponent)
            for go_mf in go_mfs:
                go_MFid = go_mf["id"]
                go_MFcategory = go_mf["category"]
                MF_term = go_mf["term"]
                cellFunction[go_MFid] = {"function": MF_term}
#               print(cellFunction)
    return [bioProcess, cellComponent, cellFunction]

# listeIDuniprot = ["Q06609", "P11531", "P10288", "P79734", "A0A2J8QDL2", "P69551", "P14713", "P32771", "P35829", "A2RUV0"]
# essai = info_gene_ontology(listeIDuniprot)
# print(essai)