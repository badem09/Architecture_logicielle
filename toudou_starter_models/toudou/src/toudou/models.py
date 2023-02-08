import os
import pickle
import uuid

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


def init_db() -> None:
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
    due: Optional[datetime] = None,
) -> None:
    todo = Todo(uuid.uuid4().int, task=task, complete=complete, due=due)
    write_to_file(todo, str(todo.id))


def get_todo(id: int) -> Todo:
    return read_from_file(str(id))


def get_todos() -> list[Todo]:
    result = []
    for id in os.listdir(TODO_FOLDER):
        todo = get_todo(int(id))
        if todo:
            result.append(todo)
    return result


def update_todo(
    id: int,
    task: str,
    complete: bool,
    due: Optional[datetime]
) -> None:
    if get_todo(id):
        todo = Todo(id, task=task, complete=complete, due=due)
        write_to_file(todo, str(todo.id))


def delete_todo(id: int) -> None:
    os.remove(os.path.join(TODO_FOLDER, str(id)))
