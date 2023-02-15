#!/usr/bin/python3
#-*- coding: utf8 -*-

######################################################################

file = "GeneSymbols.txt"

from GeneDictGenerator import gene_dict_generator

from Ensembl import ensembl
from NCBI import ncbi
from Uniprot import uniprot
from PDB import pdb
from Pfam import pfam
from Prosite import prosite

######################################################################

def table_generator(filePath:str) :
    # création liste gène + espèce
    genesList = gene_dict_generator(filePath)

    ##################################################################

    ### RESULTATS MODULE ENSEMBL
    print("### Fetching Ensembl data...")
    resEnsembl = ensembl(filePath)

    ### RESULTATS MODULE NCBI
    print("### Fetching NCBI data...")
    resNcbi = ncbi(filePath)

    ### RESULTATS MODULE UNIPROT
    print("### Fetching Uniprot data...")
    resUniprot = uniprot(filePath)

    ### RESULTATS MODULE PDB
    print("### Fetching PDB data...")
    resPDB = pdb(resUniprot)

    ### RESULTATS MODULE PFAM
    print("### Fetching Pfam data...")
    resPfam = pfam(resUniprot)

    ### RESULTATS MODULE PROSITE
    print("### Fetching Prosite data...")
    resProSite = prosite(resUniprot)

    ##################################################################

    ### OUTPUT
    print("### Building HTML output...")
    with open("Results.html", "w") as outputHtml :
        # partie commune
        with open("HeadResults.html", "r") as header :
            for line in header.readlines():
                print(line)
                outputHtml.write(line)

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
        outputHtml.write("""
</tbody>

</table>

</body>

</html>
                    """)

table_generator(file)