# Scrape d'un site  

## Ce dépôt sert au projet 2 de la formation  Développeur d'application Python d'Openclassrooms.  

### Présentation  

Les scripts notés scraper 1-3 ont été créés pour récuperer les informations suivantes :  
-l'url du produit  
-l'UPC (universal product code)  
-le titre du livre  
-son prix taxes incluses  
-son prix hors taxes, 
le nombre d'unités disponibles  
-la description du produit  
-sa catégorie, le nombre d'étoiles (sur 5)  
-l'url de l'image de la première de couverture 
Il télécharge également l'image du livre.  
Les informations sont écrites dans un fichier csv enregistré sur le bureau avec ce chemin : 'C:\\users\\%username%\\Desktop\\bookdata\\categorie\\categorie.csv'  
Les images sont téléchargés dans un dossier avec ce chemin : 'C:\\users\\%username%\\Desktop\\bookdata\\categorie\\images\titredulivre.jpg'

### Requirement  
[Git](https://git-scm.com)  
[Python](www.python.org)  
[Liste des paquets python](https://github.com/elvisOC/P1/blob/master/requirement.txt)  
Pour installer les paquets, lancer python et écrire la commande pip install *nom du paquet*  
```
pip install beautifulsoup
```


### Comment l'utiliser  

#### Télécharger le script
Avec git executer la commande git clone *lien du dépôt* dans un nouveau dossier (il faut l'indiquer dans la commande) 
```
git clone github.com/ElvisOC/P1.git C:\users\%username%\Desktop\Nouveau
```
 

#### Executer le script
Dans le dossier contenant le script :  

```
python main.py
```


