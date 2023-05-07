import csv
import io
import os
from datetime import datetime
import toudou.models as models
#import models

def export_to_csv(todos=[]) -> str:
    """
    """
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "task", "complete", "due"])
    for todo in todos:
        writer.writerow([todo.id, todo.task, todo.complete, todo.due])
    return output.getvalue()


def import_from_csv(file, tasks=None) -> list[models.Todo]:
    """
    Importe les tâches contenue dans le fichier [file].
    Retourne une liste d'objets Todo
    """
    if not tasks:
        tasks = []
    csv_reader = csv.reader(file.stream.read().decode("utf-8").splitlines())
    next(csv_reader)
    for ligne in csv_reader:
        date = [int(e) for e in ligne[3].split('-')]
        tasks.append(models.create_todo(task=ligne[1],
                                        complete=True if ligne[2] == 'True' else False,
                                        due=datetime(date[0], date[1], date[2])))
    return tasks