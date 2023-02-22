#!/usr/bin/python3
# -*- coding: utf8 -*-
from mygene import MyGeneInfo
from goatools import obo_parser
from GeneDictGenerator import gene_dict_generator
data = MyGeneInfo()


def info_gene_ontology(resUniprot):
    """
    MODULE POUR L'IMPORT DE DONNEES DEPUIS la base de Données gene ontology (utilise des IDs Uniprot)
    Données pour chaque ID Uniprot correspondent les trois go termes (bp,cc,mf) :
    
    - bioProcess -> dictionnaire retourné associant chaque ID BP et les termes correspondants à chaque couple gene et organisme
    - molFunction -> dictionnaire retourné associant chaque ID MF et les termes correspondants à chaque couple gene et organisme
    - cellComponent -> dictionnaire retourné associant chaque ID CC et les termes coresspondants à chaque couple gene et organisme
    """
    bioProcess = {}
    molFunction = {}
    cellComponent = {}
    for keys in resUniprot.keys():
        IdsUniprot = []
        for key in resUniprot[keys]["uniprotID"].split(" "):
            IdsUniprot.append(key)

        gene_info = data.querymany(IdsUniprot, scopes="uniprot", fields="go")
        
        for result in gene_info:
            if "go" in result:
                go_bps = result["go"]["BP"]
                go_ccs = result["go"]["CC"]
                go_mfs = result["go"]["MF"]

                #récupération des informations BP
                listBP = []
                for go_bp in go_bps:
                    go_BPid = go_bp["id"]
                    #go_BPcategory = go_bp["gocategory"]
                    BP_term = go_bp["term"]
                    listBP.append([go_BPid, BP_term])
                bioProcess[keys] = {"bioProcess": listBP}
        #            print(bioProcess)

                #récupération des informations CC
                listCC = []
                for go_cc in go_ccs:
                    go_CCid = go_cc["id"]
                    #go_CCcategory = go_cc["gocategory"]
                    CC_term = go_cc["term"]
                    listCC.append([go_CCid, CC_term])
                cellComponent[keys] = {"cellComponent": listCC}     
         #            print(cellComponent)

                #récupération des informations MF
                listMF = []
                for go_mf in go_mfs:
                    go_MFid = go_mf["id"]
                    #go_MFcategory = go_mf["category"]
                    MF_term = go_mf["term"]
                    listMF.append([go_MFid, MF_term])
                molFunction[keys]= {"molecularFunction": listMF}

#                   print(molFunction)
    return bioProcess, cellComponent, molFunction

#from Uniprot import uniprot
#resUniprot = uniprot("GeneSymbols.txt")
#bioProcess, cellComponent, molFunction = info_gene_ontology(resUniprot)
#print(bioProcess, cellComponent, molFunction)