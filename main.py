#!/usr/bin/python3
#-*- coding: utf8 -*-

######################################################################

# fonction de création dico liste gène + espèce (clé : "geneSymbol,organism")

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
######################################################################

file = "GeneSymbols.txt"

from Ensembl import ensembl
from NCBI import ncbi

######################################################################

def table_Generator(filePath:str) :
    # création liste gène + espèce
    genesList = gene_list_generator(filePath)

    ##################################################################

    ### RESULTATS MODULE ENSEMBL
    print("### Fetching Ensembl data...")
    resEnsembl = ensembl(filePath)

    ### RESULTATS MODULE NCBI
    print("### Fetching NCBI data...")
    resNcbi = ncbi(filePath)

    ##################################################################

    ### OUTPUT
    print("### Building HTML output...")
    with open("Results.html", "w") as outputHtml :
        #partie commune
        outputHtml.write('''
            <style>
                table{border-collapse:collapse;}
                th {text-align: middle;}
                .scroll {white-space: nowrap ; max-height: 200px; overflow: scroll}
            </style>
            <table border="1px">
                <colgroup span="2"></colgroup>
                <colgroup span="4"></colgroup>
                <tr>
                    <th colspan="2" scope="colgroup">Query</th>
                    <th colspan="4" scope="colgroup">Ensembl</th>
                </tr>
                <tr>
                    <th scope="col">Gene symbol</th>
                    <th scope="col">Species</th>
                    <th scope="col">Gene ID</th>
                    <th scope="col">Genome Browser</th>
                    <th scope="col">Transcript IDs</th>
                    <th scope="col">Ortholog list</th>
                </tr>\n
            ''')

        # partie par gène
        for geneAndOrga in genesList.keys():
            geneSymbol = genesList[geneAndOrga][0]; organism = genesList[geneAndOrga][1]

            ### DONNEES GENERALES
            outputHtml.write(f"<tr>\n")
            outputHtml.write(f"<td>{geneSymbol}</td>\n")
            outputHtml.write(f"<td><i>{organism}</i></td>\n")

            ### DONNEES ENSEMBL
            outputHtml.write(f"<td>{resEnsembl[geneAndOrga]['ensGeneId']}</td>\n")
        
            if resEnsembl[geneAndOrga]['ensUrlBrowser'] == "Data not found" :
                outputHtml.write(f"<td>Data not found</td>\n")
            else:
                outputHtml.write(f"<td><a href={resEnsembl[geneAndOrga]['ensUrlBrowser']}>GenomeBrowser</a></td>\n")
            
            # Liste protéines
            outputHtml.write(f"""<td><div class="scroll">""")
            for transcrit in resEnsembl[geneAndOrga]['ensTranscriptId'] :
                outputHtml.write(f"{transcrit}<br>")
            outputHtml.write(f"</div></td>\n")

            # Liste orthos
            outputHtml.write(f"""<td><div class="scroll">""")
            for ortho in resEnsembl[geneAndOrga]['ensOrthoList']:
                outputHtml.write(f"{ortho}<br>")
            outputHtml.write(f"</div></td>\n")
            outputHtml.write(f"</tr>\n")

        # fin tableau
        outputHtml.write("</table>")

table_Generator(file)
