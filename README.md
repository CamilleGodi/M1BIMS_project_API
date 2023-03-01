# Projet annotations de gènes via diverses APIs de BDD
### Camille Godi, Erwan Quignon, Dieu-Donné Toto  
### M1 BIMS & M2 CCB4, 2022-23

Script créant un tableau intéractif d'annotation de gènes depuis différentes bases de données en ligne (Ensembl, NCBI, UniProt...) via leurs APIs respectives.  

> Attention, nécessite la version du package python *requests* 2.27 ou supérieure, ainsi que les packages Bio (module Entrez) et mygene
.

---

## Pour lancer le script (dans le dossier des scripts source):
```python3 main.py```

## Format d'entrée:
Ce script prends un fichier .txt avec un gène par ligne, formatté comme suivant:
> SYMBOLE,genre_espèce  
> SYMBOLE2,genre_espèce2 

Par exemple: 
> RAD51,homo_sapiens  
> DMD,mus_musculus  
> RAD51,pan_troglodytes  

---

## En cas d'erreur "HTTP error 500 Internal Server Error":
Probablement été sorti de NCBI pour cause de serveur surchargé --> réessayer plus tard, hors des heures de pointe de NCBI

## En cas d'erreur "HTTP error 400 Bad Request":
Probablement NCBI qui considère que trop de requêtes on été formulées par l'utilisateur en peu de temps --> réessayer plus tard, attendre quelques minutes