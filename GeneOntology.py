#!/usr/bin/python3
# -*- coding: utf8 -*-
from mygene import MyGeneInfo
from GeneDictGenerator import gene_dict_generator
data = MyGeneInfo()


def info_gene_ontology(resUniprot):
    """
    MODULE POUR L'IMPORT DE DONNEES DEPUIS la base de Données gene ontology (utilise des IDs Uniprot)
    Données pour chaque ID Uniprot correspondent les trois go termes (Biological Process, Cellular Component, Molecular Function) :
    
    - bioProcess -> dictionnaire retourné associant à chaque couple gene et organisme sa liste de BP (format liste de listes [identifiant, nom])
    - molFunction -> dictionnaire retourné associant à chaque couple gene et organisme sa liste de CC (format liste de listes [identifiant, nom])
    - cellComponent -> dictionnaire retourné associant à chaque couple gene et organisme sa liste de MF (format liste de listes [identifiant, nom])
    
    Exemple d'accès aux GO de Biological Process pour un gène *A* dans organisme 1 *orga1* 
    (à partir d'un fichier situé en *filePath*) :
    resUniprot = uniprot("filePath")
    bioProcess, cellComponent, molFunction = info_gene_ontology(resUniprot)
    print(bioProcess["A,orga1"])
    """

    print("### Fetching GeneOntology data...")

    bioProcess = {}
    molFunction = {}
    cellComponent = {}
    for keys in resUniprot.keys():
        IdsUniprot = []
        for key in resUniprot[keys]["uniprotID"]:
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
                # Elimination des duplicats
                listBPnoDuplicate = []
                [listBPnoDuplicate.append(x) for x in listBP if x not in listBPnoDuplicate]

                bioProcess[keys] = listBPnoDuplicate
        #            print(bioProcess)

                #récupération des informations CC
                listCC = []
                for go_cc in go_ccs:
                    go_CCid = go_cc["id"]
                    #go_CCcategory = go_cc["gocategory"]
                    CC_term = go_cc["term"]
                    listCC.append([go_CCid, CC_term])
                # Elimination des duplicats
                listCCnoDuplicate = []
                [listCCnoDuplicate.append(x) for x in listCC if x not in listCCnoDuplicate]

                cellComponent[keys] = listCCnoDuplicate    
         #            print(cellComponent)

                #récupération des informations MF
                listMF = []
                for go_mf in go_mfs:
                    go_MFid = go_mf["id"]
                    #go_MFcategory = go_mf["category"]
                    MF_term = go_mf["term"]
                    listMF.append([go_MFid, MF_term])
                # Elimination des duplicats
                listMFnoDuplicate = []
                [listMFnoDuplicate.append(x) for x in listMF if x not in listMFnoDuplicate]

                molFunction[keys]= listMFnoDuplicate

#                   print(molFunction)

    return bioProcess, cellComponent, molFunction

#from Uniprot import uniprot
#resUniprot = uniprot("GeneSymbols.txt")
#bioProcess, cellComponent, molFunction = info_gene_ontology(resUniprot)
#print("BP:",bioProcess['RAD51,homo_sapiens'], "\n\nCC:", cellComponent['RAD51,homo_sapiens'],"\n\nMF:",  molFunction['RAD51,homo_sapiens'])
