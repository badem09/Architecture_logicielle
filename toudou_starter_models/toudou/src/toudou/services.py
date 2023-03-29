import csv
import os
from datetime import datetime
import toudou.models as models
#import models

def export_to_csv(todos=[]) -> str:
    """
    Exporte les tâches dans un fichier csv 'todo.csv'.
    path : toudou/src/toudou
    """
    n = len(os.listdir("csv"))
    if not todos:
        todos = models.get_todos()
    with open("csv/todo"+str(n)+".csv", "w", encoding='UTF8', newline='') as f:
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
    with open("csv/"+file, 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        next(csvreader)  # to avoid header
        for ligne in csvreader:
            date = [int(e) for e in ligne[3].split('-')]
            tasks.append(models.create_todo(task=ligne[1],
                                     complete=True if ligne[2] == 'True' else False,
                                     due=datetime(date[0], date[1], date[2])))
    return tasks
