#!/usr/bin/python3
# -*- coding: utf8 -*-
import requests
import re
from NCBI import ncbi

def kegg_data(resNcbi):
    """
    MODULE POUR L'IMPORT DE DONNEES DEPUIS la base de Données KEGG (utilise des IDs NCBI)
    Données pour chaque ID NCBI:
    - keggID -> ID KEGG du gène
    - keggInfoPathways -> dictionnaire retourné associant chaque clé (gène/organisme ) les IDs pathways et leurs noms correspondants
    
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
        infoPath[keys] = {'keggID' : keggID, 'keggInfoPathways': []} #on utilise comme clé GeneAndOrga avec une autre clé pathway initialisée à vide à laquelle on ajoutera des valeurs plus tard
        
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
                            infoPath[keys]['keggInfoPathways'].append({'pathID': pathID, 'pathName': path})
                    except:
                        continue
    return infoPath



#resNcbi = ncbi("GeneSymbols.txt")
#a = kegg_data(resNcbi)
#print(a)

# tests d'accès aux ifnos
#res = {'RAD51,homo_sapiens': {'keggID': 'hsa:5888', 'keggInfoPathways': [{'pathID': 'hsa03440', 'pathName': 'Homologous recombination'}, {'pathID': 'hsa03460', 'pathName': 'Fanconi anemia pathway'}, {'pathID': 'hsa05200', 'pathName': 'Pathways in cancer'}, {'pathID': 'hsa05212', 'pathName': 'Pancreatic cancer'}]}, 'DMD,mus_musculus': {'keggID': 'mmu:13405', 'keggInfoPathways': [{'pathID': 'mmu05410', 'pathName': 'Hypertrophic cardiomyopathy'}, {'pathID': 'mmu05412', 'pathName': 'Arrhythmogenic right ventricular cardiomyopathy'}, {'pathID': 'mmu05414', 'pathName': 'Dilated cardiomyopathy'}, {'pathID': 'mmu05416', 'pathName': 'Viral myocarditis'}]}, 'CDH2,gallus_gallus': {'keggID': 'gga:414745', 'keggInfoPathways': [{'pathID': 'gga04514', 'pathName': 'Cell adhesion molecules'}]}, 'TP53,danio_rerio': {'keggID': 'dre:30590', 'keggInfoPathways': [{'pathID': 'dre04010', 'pathName': 'MAPK signaling pathway'}, {'pathID': 'dre04110', 'pathName': 'Cell cycle'}, {'pathID': 'dre04115', 'pathName': 'p53 signaling pathway'}, {'pathID': 'dre04137', 'pathName': 'Mitophagy'}, {'pathID': 'dre04210', 'pathName': 'Apoptosis'}, {'pathID': 'dre04216', 'pathName': 'Ferroptosis'}, {'pathID': 'dre04218', 'pathName': 'Cellular senescence'}, {'pathID': 'dre04310', 'pathName': 'Wnt signaling pathway'}, {'pathID': 'dre05168', 'pathName': 'Herpes simplex virus 1 infection'}]}, 'RAD51,pan_troglodytes': {'keggID': 'ptr:453339', 'keggInfoPathways': [{'pathID': 'ptr03440', 'pathName': 'Homologous recombination'}, {'pathID': 'ptr03460', 'pathName': 'Fanconi anemia pathway'}, {'pathID': 'ptr05200', 'pathName': 'Pathways in cancer'}, {'pathID': 'ptr05212', 'pathName': 'Pancreatic cancer'}]}, 'PSBA,pinus_thunbergii': {'keggID': 'ptr:453339', 'keggInfoPathways': [{'pathID': 'ptr03440', 'pathName': 'Homologous recombination'}, {'pathID': 'ptr03460', 'pathName': 'Fanconi anemia pathway'}, {'pathID': 'ptr05200', 'pathName': 'Pathways in cancer'}, {'pathID': 'ptr05212', 'pathName': 'Pancreatic cancer'}]}, 'RPL33,pteridium_aquilinum': {'keggID': 'ptr:453339', 'keggInfoPathways': [{'pathID': 'ptr03440', 'pathName': 'Homologous recombination'}, {'pathID': 'ptr03460', 'pathName': 'Fanconi anemia pathway'}, {'pathID': 'ptr05200', 'pathName': 'Pathways in cancer'}, {'pathID': 'ptr05212', 'pathName': 'Pancreatic cancer'}]}, 'PHYB,arabidopsis_thaliana': {'keggID': 'ath:AT2G18790', 'keggInfoPathways': [{'pathID': 'ath04712', 'pathName': 'Circadian rhythm'}]}, 'SFA1,saccharomyces_cerevisiae': {'keggID': 'sce:YDL168W', 'keggInfoPathways': [{'pathID': 'sce00010', 'pathName': 'Glycolysis / Gluconeogenesis'}, {'pathID': 'sce00071', 'pathName': 'Fatty acid degradation'}, {'pathID': 'sce00350', 'pathName': 'Tyrosine metabolism'}, {'pathID': 'sce00620', 'pathName': 'Pyruvate metabolism'}, {'pathID': 'sce00680', 'pathName': 'Methane metabolism'}, {'pathID': 'sce01100', 'pathName': 'Metabolic pathways'}, {'pathID': 'sce01110', 'pathName': 'Biosynthesis of secondary metabolites'}, {'pathID': 'sce01200', 'pathName': 'Carbon metabolism'}]}, 'SLPA,lactobacillus_acidophilus': {'keggID': 'sce:YDL168W', 'keggInfoPathways': [{'pathID': 'sce00010', 'pathName': 'Glycolysis / Gluconeogenesis'}, {'pathID': 'sce00071', 'pathName': 'Fatty acid degradation'}, {'pathID': 'sce00350', 'pathName': 'Tyrosine metabolism'}, {'pathID': 'sce00620', 'pathName': 'Pyruvate metabolism'}, {'pathID': 'sce00680', 'pathName': 'Methane metabolism'}, {'pathID': 'sce01100', 'pathName': 'Metabolic pathways'}, {'pathID': 'sce01110', 'pathName': 'Biosynthesis of secondary metabolites'}, {'pathID': 'sce01200', 'pathName': 'Carbon metabolism'}]}, 'DRGX,pelodiscus_sinensis': {'keggID': 'pss:102445482', 'keggInfoPathways': []}, 'NOTCH1,xenopus_tropicalis': {'keggID': 'xtr:100037842', 'keggInfoPathways': [{'pathID': 'xtr04330', 'pathName': 'Notch signaling pathway'}]}}
#print(res['RAD51,homo_sapiens']['keggID'])
#print(res['RAD51,homo_sapiens']['keggInfoPathways'][0])
#print(res['RAD51,homo_sapiens']['keggInfoPathways'][1])