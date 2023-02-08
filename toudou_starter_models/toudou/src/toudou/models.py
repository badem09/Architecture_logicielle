import os
import pickle
import uuid

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, DateTime

TODO_FOLDER = "db"
metadata_obj = MetaData()
engine = create_engine("sqlite:///todos.db", echo=True)
todo_table = Table(
    "todos",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("task", String(1000), nullable=False),
    Column("complete", Boolean, nullable=False),
    Column("due", DateTime, nullable=True)
)


@dataclass
class Todo:
    id: int
    task: str
    complete: bool
    due: Optional[datetime]


def init_db() -> None:
    metadata_obj.create_all(engine)
    # n'écrase pas si ya deja une bd.


def write_to_bd(todo: Todo, filename: str) -> None:
    requete = sqlalchemy.Insert(todo_table).values(
        task = todo.task,
        complete = todo.complete,
        due = todo.due
    )
    with engine.connect() as conn:
        result = conn.execute(requete)
        conn.commit()


def create_todo(
    task: str,
    complete: bool = False,
    due: Optional[datetime] = None,
) -> None:
    todo = Todo(uuid.uuid4().int, task=task, complete=complete, due=due)
    write_to_bd(todo, str(todo.id))


def get_todo(id: int) -> Todo:
    id = sqlalchemy.sql.column('id')
    s = sqlalchemy.sql.select(['*']).where(id == 1)


def get_todos() -> list[Todo]:
    requete = todo_table.select()
    with engine.connect() as conn:
        result = conn.execute(requete).fetchall()
        conn.commit()
    return result


def update_todo(
    id: int,
    task: str,
    complete: bool,
    due: Optional[datetime]
) -> None:
    if get_todo(id):
        todo = Todo(id, task=task, complete=complete, due=due)
        write_to_bd(todo, str(todo.id))


def delete_todo(id: int) -> None:
    os.remove(os.path.join(TODO_FOLDER, str(id)))
