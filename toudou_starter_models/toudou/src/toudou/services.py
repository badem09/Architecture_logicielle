import csv
import dataclasses
import io
import os

from datetime import datetime

import models


def export_to_csv(todos=[]) -> str:
    if not todos:
        todos = models.get_todos()
    with open("todo.csv", "w", encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "task", "complete", "due"])
        for t in todos:
            writer.writerow([t.id, t.task, t.complete, t.due])
    return os.path.abspath(f.name)

def import_from_csv(file:str,tasks=[]) -> None:

    with open(file, 'r') as file:
        i = 0
        csvreader = csv.reader(file, delimiter=',')
        for r in csvreader:
            if i > 0:
                date = [int(e) for e in r[3].split(' ')[0].split('-')]
                tasks.append(models.Todo(int(r[0]), r[1], True if r[2] == 'True' else False,
                                            datetime(date[0], date[1], date[2])))
            i += 1
    return tasks
