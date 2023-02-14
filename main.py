#!/usr/bin/python3
#-*- coding: utf8 -*-

######################################################################

file = "GeneSymbols.txt"

from GeneDictGenerator import gene_dict_generator

from Ensembl import ensembl
from NCBI import ncbi
from uniprot import uniprot
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
        #partie commune
        outputHtml.write('''
<!DOCTYPE html>
<html>

<head>
    <meta http-equiv="Content-type" content="text/html; charset=UTF-8" />

    <title>Results</title>
   
    <meta name="viewport" content="width=device-width,initial-scale=1">
	<link rel="stylesheet" type="text/css" href="/media/css/site-examples.css?_=6e5593ad4c5375eef5d919cfc10a0a54">
	<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.16/css/jquery.dataTables.min.css">
    <link rel="stylesheet" type="text/css" href="//cdn.datatables.net/1.10.16/css/jquery.dataTables.css">

	<script type="text/javascript" src="/media/js/site.js?_=a25d93b0b2ef7712783f57407f987734"></script>
	<script type="text/javascript" src="/media/js/dynamic.php?comments-page=examples%2Fdata_sources%2Fjs_array.html" async></script>
	<script type="text/javascript" language="javascript" src="https://code.jquery.com/jquery-1.12.4.js"></script>
	<script type="text/javascript" language="javascript" src="https://cdn.datatables.net/1.10.16/js/jquery.dataTables.min.js"></script>
	<script type="text/javascript" language="javascript" src="../resources/demo.js"></script>

    <script type="text/javascript" class="init">
        $(document).ready(function() {
            $("#table_genes").DataTable( {
                "scrollY": 700,
                "scrollX": true,
                "lengthMenu": [5, 10, 15, 20, "All" ],
                fixedColumns: {leftColumns: 2}
            } );
        } );
    </script>

    <style>
        table {border-collapse: collapse}
        th {text-align: middle}
        .scroll {white-space: nowrap ; max-height: 150px; overflow: scroll}
        table, th, td { border: 1px solid black; border-collapse: collapse}
    </style>
</head>

<body>
    
<h1 align="center"> Resultats </h1>

<br>

<table id="table_genes" class="display" width="100%"> 

    <thead>
    <tr>
        <th colspan="2">Query</th>
        <th colspan="4">Ensembl</th>
    </tr>
    <tr>
        <th>Gene symbol</th>
        <th>Species</th>
        <th>Gene ID</th>
        <th>Genome Browser</th>
        <th>Transcript IDs</th>
        <th>Ortholog list</th>
    </tr>
</thead>

<tbody>
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
        outputHtml.write("""
</tbody>

</table>

</body>

</html>
                    """)

table_generator(file)