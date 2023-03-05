# Module Architechture logicielle 
# Projet Toudou

BA Demba INFI2B

## Installation


Dans le dossier du projet, rendez vous dans le dossier toudou et executez la commande suivante:
```bash
$ pdm install 
```

## Lancement

Pour lancer le projet, vous pouvez exécuter le fichier toudou/src/toudou/views.py

```bash
$ python src/toudou/views.py
```
Vous devrez ensuite vous rendre dans un navigateur et taper l'adresse suivante : http://127.0.0.1:5000 


## Structure du code

L'application web est structurée en 3 parties : views.py (la vue / le controlleur), 
models.py (le modèle) et services.py (les services).

views.py possède des fonctions de redirections (commençant pas 'redirect') et des fonctions de traitements.

models.py renferme les fonctions relatives à la base de données et aux objets Todo

services.py permet d'importer et d'exporter des tâches au format csv.

Les fonctionnalités présentes sont :
- la création de tâches et leur sauvegarde
- la modification de tâches
- la suppression de tâches
- l'importation de tâches d'un fichier csv (voir format ci-dessous)
- l'exportation des tâches dans un fichier csv (1 exportation = 1 nouveau fichier)


### Importation csv

Pour que l'application web puisse reconnaitre les tâches de votre fichier .csv, 
il faut qu'il suive le format suivant:

```
id,task,complete,due
1(int), Nom de la tâche, True/False, date au format YYYY-MM-DD
```

Exemple:

```
id,task,complete,due
3,truc,True,2022-02-02
1,SCsfc,False,2023-03-04
2,taches 1,False,2023-03-04
4,kkk,False,2023-03-16
```

## Limites / Pistes d'améiliorations

En faisant mon auto-critique, je remarques que mon projet possèdes certaines limites telles que :


- L'application peut être vulnérable aux injections sql (sécurité des formulaires).
- Dans la fonction import_csv de views.py, l'importation est réalisé 2 fois.
Cela est du à la preview. Pour ne lire le fichier csv qu'une seule fois, il est
possible que je crée un converter (type de donnés transmit avec les balises < a >)
personalisé.
- Id des tâches: La fonction getnext_id() génere un nouvel id en ajoutant 1
à l'id maximum dans la base de données. Cela à ses limites dans le cas où
l'application est utilisée pendant une longue période ou s'il y a beaucoup 
tâches.
- La répetition: le template html pour l'ajout de tâches et celui pour
les modifier est très similaire ce qui entraine de la répétition. Cependant,
Celles-ci étant 2 fonctionnalités bien différentes et pour respecter le SOC
je n'ai pas fusionné ces 2 templates (ajouter.html et modifier.html).
- Lors de l'ajout de tâches ou de leurs importation, les tâches déja présentes 
(même intitulé et même date) ne sont pas enregistrées.
