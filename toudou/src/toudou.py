import click
import os
import pickle
import uuid
import csv

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


TODO_FOLDER = "db"


@dataclass
class Todo:
    id: int
    task: str
    complete: bool
    due: Optional[datetime]


def init_folder() -> None:
    os.makedirs(TODO_FOLDER, exist_ok=True)


def read_from_file(filename: str) -> Todo:
    with open(os.path.join(TODO_FOLDER, filename), "rb") as f:
        return pickle.load(f)


def write_to_file(todo: Todo, filename: str) -> None:
    with open(os.path.join(TODO_FOLDER, filename), "wb") as f:
        pickle.dump(todo, f)



def create_todo(
    task: str,
    complete: bool = False,
    due: Optional[datetime] = None
) -> None:

    todo = Todo(uuid.uuid4().int, task=task, complete=complete, due=due)
    write_to_file(todo, str(todo.id))
    write_csv(todo, str(todo.id))

#update dans csv et dasn pickle / delete

def get_todo(id: int) -> Todo:
    return read_from_file(str(id))


def get_todos() -> list[Todo]:
    result = []
    for id in os.listdir(TODO_FOLDER):
        todo = get_todo(int(id))
        if todo:
            result.append(todo)
    return result

def write_csv(todo: Todo, filename: str):
    if not os.path.exists("taches.csv"):
        with open('taches.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Date", "Nom", "Status"])
    with open('taches.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([todo.id, todo.due, todo.task, todo.complete])

@click.group()
def cli():
    pass


@cli.command()
def init_db():
    init_folder()


@cli.command()
@click.option("-t", "--task", prompt="Your task", help="The task to remember.")
@click.option("-d", "--due", type=click.DateTime(), default=None, help="Due date of the task.")
def create(task: str, due: datetime):
    if not due:
        due = "Non renseignée !"
    create_todo(task, due=due)


@cli.command()
@click.option("--id", required=True, type=click.INT, help="Todo's id.")
def get(id: int):
    click.echo(get_todo(id))


@cli.command()
def get_all():
    click.echo(get_todos())

