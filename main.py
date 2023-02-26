#!/usr/bin/python3
#-*- coding: utf8 -*-

######################################################################

### MODULES

from GeneDictGenerator import gene_dict_generator

from Ensembl import ensembl
from NCBI import ncbi
from Uniprot import uniprot
from PDB import pdb
from Pfam import pfam
from Prosite import prosite
from STRING import network_link_string
from KEGG import kegg_data
from GeneOntology import info_gene_ontology

######################################################################

### INTERFACE

from tkinter import filedialog as fd
filePath = fd.askopenfilename(title="Open your file (format : 'geneSymbol,Organism')", filetypes=[('txt files','.txt'), ('csv files','.csv')])

# Par défaut, si pas de fichier donné dans l'interface
if filePath == () :
    file = "GeneSymbols.txt" # fichier par défaut
    print("Default file used (GeneSymbols.txt)")
else :
    file = filePath
    print("file : ", file)


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

    ### RESULTATS MODULE STRING
    print("### Fetching STRING data...")
    resString = network_link_string(resUniprot)

    ### RESULTATS MODULE KEGG
    print("### Fetching KEGG data...")
    resKegg = kegg_data(resNcbi)

    ### RESULTATS MODULE GENEONTOLOGY
    print("### Fetching GeneOntology data...")
    bioProcess, cellComponent, molFunction = info_gene_ontology(resUniprot)

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
            outputHtml.write(f"<tr>\n")
            outputHtml.write(f"<td>{geneSymbol}</td>\n")
            outputHtml.write(f"<td><i>{organism}</i></td>\n")


            ### DONNEES NCBI
            # Official full name
            outputHtml.write(f"<td>{resNcbi[geneAndOrga]['ncbiFullName']}</td>\n")

            # NCBI Gene ID
            outputHtml.write(f"""<td><div class="scroll">""")
            for ncbiid in resNcbi[geneAndOrga]['ncbiGeneId'] :
                outputHtml.write(f"{ncbiid}<br>")
            outputHtml.write(f"</div></td>\n")
            
            # RefSeq Transcript ID
            outputHtml.write(f"""<td><div class="scroll">""")
            for trans in resNcbi[geneAndOrga]['ncbiTranscriptAccess'] :
                outputHtml.write(f"{trans}<br>")
            outputHtml.write(f"</div></td>\n")

            # RefSeq prot ID
            outputHtml.write(f"""<td><div class="scroll">""")
            for prot in resNcbi[geneAndOrga]['ncbiProteinAccess'] :
                outputHtml.write(f"{prot}<br>")
            outputHtml.write(f"</div></td>\n")


            ### DONNEES ENSEMBL
            # Ensembl gene ID
            outputHtml.write(f"<td>{resEnsembl[geneAndOrga]['ensGeneId']}</td>\n")
        
            # Genome Browser
            if resEnsembl[geneAndOrga]['ensUrlBrowser'] == "Data not found" :
                outputHtml.write(f"<td>Data not found</td>\n")
            else:
                outputHtml.write(f"<td><a href={resEnsembl[geneAndOrga]['ensUrlBrowser']}>GenomeBrowser</a></td>\n")
            
            # Liste transcrits
            outputHtml.write(f"""<td><div class="scroll">""")
            for transcrit in resEnsembl[geneAndOrga]['ensTranscriptId'] :
                outputHtml.write(f"{transcrit}<br>")
            outputHtml.write(f"</div></td>\n")

            # Liste orthos
            outputHtml.write(f"""<td><div class="scroll">""")
            for ortho in resEnsembl[geneAndOrga]['ensOrthoList']:
                outputHtml.write(f"{ortho}<br>")
            outputHtml.write(f"</div></td>\n")


            ### DONNEES UniProt
            # Prot name
            outputHtml.write(f"<td>{resUniprot[geneAndOrga]['uniprotName']}</td>\n")

            # Prot ID
            outputHtml.write(f"<td>{resUniprot[geneAndOrga]['uniprotID']}</td>\n")


            ### DONNEES PDB
            # PDB IDs/names
            outputHtml.write(f"""<td><div class="scroll">""")
            if len(resPDB[geneAndOrga]['pdbID']) == 0 :
                outputHtml.write(f"Data Not Found\n")
            else :
                for i in range(len(resPDB[geneAndOrga]['pdbID'])):
                    outputHtml.write(f"<a href=https://www.rcsb.org/structure/{resPDB[geneAndOrga]['pdbID'][i][0]}>{resPDB[geneAndOrga]['pdbID'][i][0]}</a> : {resPDB[geneAndOrga]['pdbID'][i][1]}<br>")
            outputHtml.write(f"</div></td>\n")


            ### DONNEES PFAM/INTERPRO
            # Interpro IDs
            outputHtml.write(f"""<td><div class="scroll">""")
            outputHtml.write(f"<a href={resPfam[geneAndOrga]['pfamLink'][0]}>[Protein Link]</a><br>")
            for i in range(len(resPfam[geneAndOrga]['pfamID'])):
                outputHtml.write(f"<a href=https://www.ebi.ac.uk/interpro/entry/InterPro/{resPfam[geneAndOrga]['pfamID'][i]}/>{resPfam[geneAndOrga]['pfamID'][i]}</a><br>")
            outputHtml.write(f"</div></td>\n")
            

            ### DONNEES PROSITE
            # Prosite ID
            outputHtml.write(f"""<td><div class="scroll">""")
            outputHtml.write(f"<a href=https://prosite.expasy.org/cgi-bin/prosite/PSView.cgi?spac={resProSite[geneAndOrga]['prositeLink']}>[Protein Link]</a><br>")
            for i in range(len(resProSite[geneAndOrga]['prositeID'])):
                outputHtml.write(f"<a href=https://prosite.expasy.org/{resProSite[geneAndOrga]['prositeID'][i]}>{resProSite[geneAndOrga]['prositeID'][i]}</a><br>")
            outputHtml.write(f"</div></td>\n")


            ### DONNEES STRING
            # Interactions (lien)
            if geneAndOrga in resString.keys() :
                outputHtml.write(f"<td>{resString[geneAndOrga]['StringID']}<br><a href=https://string-db.org/network/{resString[geneAndOrga]['StringID']}>Interactions (dynamic)</a><br><a href=https://string-db.org/api/highres_image/network?identifiers={resString[geneAndOrga]['StringID']}>Interactions (zoomed, still)</a></td>\n")
            else : 
                outputHtml.write(f"<td>Data Not Found<br></td>\n")

            
            ### DONNEES KEGG
            # KEGG IDs
            outputHtml.write(f"""<td><div class="scroll">""")
            if resKegg[geneAndOrga]['keggID'] == "Data Not Found" :
                outputHtml.write(f"Data Not Found")
            else:
                outputHtml.write(f"<a href=https://www.genome.jp/dbget-bin/www_bget?{resKegg[geneAndOrga]['keggID']}>{resKegg[geneAndOrga]['keggID']}</a><br>")
            outputHtml.write(f"</div></td>\n")

            # KEGG Pathways
            outputHtml.write(f"""<td><div class="scroll">""")
            if len(resKegg[geneAndOrga]['keggInfoPathways']) == 0 :
                outputHtml.write("Data Not Found")
            else :
                for i in range(len(resKegg[geneAndOrga]['keggInfoPathways'])):
                    outputHtml.write(f"<a href=https://www.genome.jp/dbget-bin/www_bget?{resKegg[geneAndOrga]['keggInfoPathways'][i]['pathID']}>{resKegg[geneAndOrga]['keggInfoPathways'][i]['pathID']}</a> : {resKegg[geneAndOrga]['keggInfoPathways'][i]['pathName']}<br>")
            outputHtml.write(f"</div></td>\n")

            ### DONNEES GO
            # Cellular Component
            outputHtml.write(f"""<td><div class="scroll">""")
            if geneAndOrga in cellComponent.keys() :
                for cc in cellComponent[geneAndOrga]:
                    outputHtml.write(f"<a href=http://amigo.geneontology.org/amigo/term/{cc[0]}>{cc[0]}</a> : {cc[1]}<br>")
            else:
                outputHtml.write(f"Data Not Found<br>")
            outputHtml.write(f"</div></td>\n")

            # Molecular Function
            outputHtml.write(f"""<td><div class="scroll">""")
            if geneAndOrga in molFunction.keys() :
                for mf in molFunction[geneAndOrga]:
                    outputHtml.write(f"<a href=http://amigo.geneontology.org/amigo/term/{mf[0]}>{mf[0]}</a> : {mf[1]}<br>")
            else:
                outputHtml.write(f"Data Not Found<br>")
            outputHtml.write(f"</div></td>\n")

            # Biological Process
            outputHtml.write(f"""<td><div class="scroll">""")
            if geneAndOrga in bioProcess.keys() :
                for bp in bioProcess[geneAndOrga]:
                    outputHtml.write(f"<a href=http://amigo.geneontology.org/amigo/term/{bp[0]}>{bp[0]}</a> : {bp[1]}<br>")
            else:
                outputHtml.write(f"Data Not Found<br>")
            outputHtml.write(f"</div></td>\n")


            # fin de ligne/gène
            outputHtml.write(f"</tr>\n\n")

        # fin tableau
        outputHtml.write("""
</tbody>

</table>

</body>

</html>
                    """)

table_generator(file)