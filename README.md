# Module Architechture logicielle 
# Projet Toudou

BA Demba INFI2B

## Installation


Dans le dossier du projet, rendez-vous dans le dossier \Architecture_logicielle\toudou\ et executez la commande suivante:

```bash
$ pdm install 
```

## Lancement

Pour lancer le projet, executez la commande suivante (toujours dans le dossier \Architecture_logicielle\toudou\)

```bash
$ pdm run start
```
Vous devrez ensuite vous rendre dans un navigateur et taper l'adresse suivante : http://127.0.0.1:5000/todos/


## Structure du code

L'application web est structurée en 3 parties : app.py (la vue / le controlleur), 
models.py (le modèle) et services.py (les services).

app.py gère les redirections entre les pages web, l'authentification, les erreurs
et l'interface en ligne de commande.

models.py renferme les fonctions relatives à la base de données et aux objets Todo.

services.py permet d'importer et d'exporter des tâches au format csv.

Les fonctionnalités présentes sont :
- la création de tâches et leur sauvegarde
- la modification de tâches
- la suppression de tâches
- l'importation de tâches d'un fichier csv (voir format ci-dessous)
- l'exportation des tâches dans un fichier csv (1 exportation = 1 nouveau fichier)
- l'authentification (logins: utilisateur/utilisateur et administrateur/administrateur )


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

## Points d'améliorations

Par rapport au premier rendu, je pense que mon application web s'est renforcée sur
les points suivants :

-La sécurité des données : les formulaires sont maintenant gérés par WTForms, 
des logging ont été mit en place et les erreurs sont gérées par des handlers.

-L'industrialisation : Des BluePrint ont été implémentés pour améliorer la modularité 
de l'applicatio webb. Cela permet aussi d'uniformiser les routes (url) et ainsi respecter
les contraintes REST.

-Les import : Dans la version précédente, les imports étaient fait deux fois. 
Une première fois pour la preview et une seconde pour l'enregistrement. Désormait, 
les tâches ne sont importés qu'une seule fois. La solution a été de les serialiser en JSON
pour pouvoir les transferer du clients au serveur.

-Les export : Dans la version précédente, chaque export était stocké localement dans 
le projet même, ce qui pourrait poser des problème si trop d'export sont faits. Désormais,
un export génére un fichier .csv qui pourrait être télécharger par le client sur sa machine.


