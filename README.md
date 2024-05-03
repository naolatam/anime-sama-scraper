# anime-sama-scraper
Un scraper du site anime-sama. (anime only)

⚠️ Je ne continuerai pas ce programme sur github. Aucune version ne sera publié après celle-ci.

## Ce programme n'est qu'une exploatation des données qu'on indexé [Anime-Sama](https://anime-sama.fr). Je ne serait nullement tenu responsable de vos actes avec ce programme. 


# A propos du programme

Programme écrit et imaginé par: [MATA Loan](https://github.com/naolatam)


# Caractéristiques
- Possibilités d'utiliser des threads (déconseillé, cause des erreurs avec le réseau en fonction de votre machine. Et flemme de développé une solution pour l'utiliter du code) (code pour utiliser les thread en commentaire)
- Supportes les hébergeurs : sibnet.ru, (VK.com peut être)
- Télécharge la VF, et la VOSTFR, si disponible
- Ajout des épisodes, saisons, animes, dans une base de données mysql
- Upload des épisodes sur filemoon.sx (permet de les héberger, 40to gratuit de stockage de vidéos avec filemoon.sx, je ne suis pas affilié à leur plateforme)

<br/>
<br/>

# Prérequis:

- Python 3 (utilisé sur la 3.11)
- mysql-connector-python, selenium, requests

<br/><br/>

# Installation et utilisation du programme

#### Installations des dépendances 

Dans le dossier où se situe les fichiers ".py", ouvrez un terminal et entrer :
##### Sur window : 
```
$ python -m pip install -r requirements.txt
```
##### Sur linux : 
```
$ apt install python3 (optionnel)
$ python3 -m pip install -r requirements.txt
```

#### Configuration 

Ouvrir le fichier main.py,
modifier la variable "FILEMOON_API_KEY" à la ligne 13, par les identifiants de connexion à votre base de données
Enregistrer puis fermer.

Ouvrir le fichier fileTransferor.py,
modifier la variable "DbCredit" à la ligne 7, par la valeur de votre clé d'API filemoon.sx.
Enregistrer puis fermer.


<br/><br/>

#### executer le programme

Pour executer le programme, ouvrez un terminal dans le dossier qui contient tout les fichiers ".py", et entrez:
##### Sur window : 
```
$ python main.py
```
##### Sur linux : 
```
$ python3 main.py
```



# Erreurs
- Si vous utilisez les threads, il se peut que le code rencontre des erreurs. Dans quel cas les épisodes ne seront pas upload sur filemoon.sx

<br/><br/>
