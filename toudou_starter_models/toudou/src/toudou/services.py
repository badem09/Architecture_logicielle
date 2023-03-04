import csv
import os
from datetime import datetime
import models


def export_to_csv(todos=[]) -> str:
    """
    Exporte les tâches dans un fichier csv 'todo.csv'.
    path : toudou/src/toudou
    Attention: écrase le fichier todos.csv s'il existe déja
    """
    if not todos:
        todos = models.get_todos()
    with open("todo.csv", "w", encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "task", "complete", "due"])
        for t in todos:
            writer.writerow([t.id, t.task, t.complete, t.due])
    return os.path.abspath(f.name)


def import_from_csv(file: str, tasks=None) -> list[models.Todo]:
    """
    Importe les tâches contenue dans le fichier [file].
    Retourne une liste d'objets Todo
    """
    if not tasks:
        tasks = []
    with open(file, 'r') as file:
        i = 0
        csvreader = csv.reader(file, delimiter=',')
        for ligne in csvreader:
            if i > 0:  # to avoid header
                date = [int(e) for e in ligne[3].split('-')]
                tasks.append(models.Todo(id=int(ligne[0]), task=ligne[1],
                                         complete=True if ligne[2] == 'True' else False,
                                         due=datetime(date[0], date[1], date[2])))
            i += 1
    return tasks
