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

    ### RESULTATS MODULE NCBI
    print("### Fetching NCBI data...")
    resNcbi = ncbi(filePath)

    ### RESULTATS MODULE ENSEMBL
    print("### Fetching Ensembl data...")
    resEnsembl = ensembl(filePath)

    ### RESULTATS MODULE UNIPROT
    print("### Fetching Uniprot data...")
    resUniprot = uniprot(filePath)

    ### RESULTATS MODULE PDB
    print("### Fetching PDB data...")
    resPDB = pdb(resUniprot)

    ### RESULTATS MODULE PFAM/InterPro
    print("### Fetching Pfam data...")
    resPfam = pfam(resUniprot)

    ### RESULTATS MODULE PROSITE
    print("### Fetching Prosite data...")
    resProSite = prosite(resUniprot)

    ##################################################################

    ### OUTPUT
    print("### Building HTML output...")
    with open("Results.html", "w") as outputHtml :
        # partie commune tableau
        with open("HeadResults.html", "r") as header :
            for line in header.readlines():
                outputHtml.write(line)

        # partie par gène
        for geneAndOrga in genesList.keys():
            geneSymbol = genesList[geneAndOrga][0]; organism = genesList[geneAndOrga][1]

            ### DONNEES GENERALES
            outputHtml.write(f"<tr>")
            outputHtml.write(f"<td>{geneSymbol}</td>")
            outputHtml.write(f"<td><i>{organism}</i></td>")


            ### DONNEES NCBI
            # Official full name
            outputHtml.write(f"<td>{resNcbi[geneAndOrga]['ncbiFullName']}</td>")

            # NCBI Gene ID
            outputHtml.write(f"""<td><div class="scroll">""")
            for ncbiid in resNcbi[geneAndOrga]['ncbiGeneId'] :
                outputHtml.write(f"{ncbiid}<br>")
            outputHtml.write(f"</div></td>")
            
            # RefSeq Transcript ID
            outputHtml.write(f"""<td><div class="scroll">""")
            for trans in resNcbi[geneAndOrga]['ncbiTranscriptAccess'] :
                outputHtml.write(f"{trans}<br>")
            outputHtml.write(f"</div></td>")

            # RefSeq prot ID
            outputHtml.write(f"""<td><div class="scroll">""")
            for prot in resNcbi[geneAndOrga]['ncbiProteinAccess'] :
                outputHtml.write(f"{prot}<br>")
            outputHtml.write(f"</div></td>")


            ### DONNEES ENSEMBL
            # Ensembl gene ID
            outputHtml.write(f"<td>{resEnsembl[geneAndOrga]['ensGeneId']}</td>")
        
            # Genome Browser
            if resEnsembl[geneAndOrga]['ensUrlBrowser'] == "Data not found" :
                outputHtml.write(f"<td>Data not found</td>")
            else:
                outputHtml.write(f"<td><a href={resEnsembl[geneAndOrga]['ensUrlBrowser']}>GenomeBrowser</a></td>")
            
            # Liste transcrits
            outputHtml.write(f"""<td><div class="scroll">""")
            for transcrit in resEnsembl[geneAndOrga]['ensTranscriptId'] :
                outputHtml.write(f"{transcrit}<br>")
            outputHtml.write(f"</div></td>")

            # Liste orthos
            outputHtml.write(f"""<td><div class="scroll">""")
            for ortho in resEnsembl[geneAndOrga]['ensOrthoList']:
                outputHtml.write(f"{ortho}<br>")
            outputHtml.write(f"</div></td>")


            ### DONNEES UniProt
            # Prot name
            outputHtml.write(f"<td>{resUniprot[geneAndOrga]['uniprotName']}</td>")

            # Prot ID
            outputHtml.write(f"<td>{resUniprot[geneAndOrga]['uniprotID']}</td>")


            ### DONNEES PDB
            # PDB IDs/names
            outputHtml.write(f"""<td><div class="scroll">""")
            if len(resPDB[geneAndOrga]['pdbID']) == 0 :
                outputHtml.write("Data Not Found")
            else :
                for i in range(len(resPDB[geneAndOrga]['pdbID'])):
                    outputHtml.write(f"<a href=https://www.rcsb.org/structure/{resPDB[geneAndOrga]['pdbID'][i][0]}>{resPDB[geneAndOrga]['pdbID'][i][0]}</a> : {resPDB[geneAndOrga]['pdbID'][i][1]}<br>")
            outputHtml.write(f"</div></td>")


            ### DONNEES PFAM/INTERPRO
            # Interpro IDs
            outputHtml.write(f"""<td><div class="scroll">""")
            outputHtml.write(f"<a href={resPfam[geneAndOrga]['pfamLink'][0]}>[Protein Link]</a><br>")
            for i in range(len(resPfam[geneAndOrga]['pfamID'])):
                outputHtml.write(f"<a href=https://www.ebi.ac.uk/interpro/entry/InterPro/{resPfam[geneAndOrga]['pfamID'][i]}/>{resPfam[geneAndOrga]['pfamID'][i]}</a><br>")
            outputHtml.write(f"</div></td>")
            

            ### DONNEES PROSITE
            # Prosite ID
            outputHtml.write(f"""<td><div class="scroll">""")
            outputHtml.write(f"<a href=https://prosite.expasy.org/cgi-bin/prosite/PSView.cgi?spac={resProSite[geneAndOrga]['prositeLink']}>[Protein Link]</a><br>")
            for i in range(len(resProSite[geneAndOrga]['prositeID'])):
                outputHtml.write(f"<a href=https://prosite.expasy.org/{resProSite[geneAndOrga]['prositeID'][i]}>{resProSite[geneAndOrga]['prositeID'][i]}</a><br>")
            outputHtml.write(f"</div></td>")


            ### DONNEES STRING
            # Interactions (lien)
            outputHtml.write(f"<td>PLACEHOLDER</td>")

            ### DONNEES KEGG
            # KEGG IDs
            outputHtml.write(f"<td>PLACEHOLDER</td>")

            # KEGG Pathways
            outputHtml.write(f"<td>PLACEHOLDER</td>")

            ### DONNEES GO
            # Cellular Component
            outputHtml.write(f"<td>PLACEHOLDER</td>")

            # Molecular Function
            outputHtml.write(f"<td>PLACEHOLDER</td>")

            # Biological Process
            outputHtml.write(f"<td>PLACEHOLDER</td>")

            # fin de ligne/gène
            outputHtml.write(f"</tr>")

        # fin tableau
        outputHtml.write("""
</tbody>

</table>

</body>

</html>
                    """)

table_generator(file)