# Projet annotations de gènes via diverses APIs de BDD
### Camille Godi, Erwan Quignon, Dieu-Donné Toto  
### M1 BIMS & M2 CCB4, 2022-23

Script créant un tableau intéractif d'annotation de gènes depuis différentes bases de données en ligne (Ensembl, NCBI, UniProt...) via leurs APIs respectives.  

> Attention, nécessite la version du package python *requests* 2.27 ou supérieure, ainsi que les packages Bio (module Entrez) et mygene
.

---

## Pour lancer le script:
```python3 main.py```

## Format d'entrée:
Ce script prends un fichier (par défaut  'GeneSymbols.txt' disponible dans le dossier) avec un gène par ligne, formatté comme suivant:
> SYMBOLE,genre_espèce  
> SYMBOLE2,genre_espèce2 

Par exemple: 
> RAD51,homo_sapiens  
> DMD,mus_musculus  
> RAD51,pan_troglodytes  
