import csv
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import sqlalchemy as db
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, DateTime

TODO_FOLDER = "db"
metadata_obj = MetaData()
engine = create_engine("sqlite:///todos.db", echo=True)
todo_table = Table(
    "todos",
    metadata_obj,
    Column("id", Integer, primary_key=True),
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

def write_to_bd(todo: Todo) -> None:
    if not get_todo(todo.id):
        requete = db.Insert(todo_table).values(
            id=todo.id,
            task=todo.task,
            complete=todo.complete,
            due=todo.due
        )
        with engine.connect() as conn:
            conn.execute(requete)
            conn.commit()
        return True
    return False


def update_bd(todo: Todo) -> None:
    requete = db.Update(todo_table).values(
        id=todo.id,
        task=todo.task,
        complete=todo.complete,
        due=todo.due
    )
    col_id = db.sql.column('id')
    requete = requete.where(col_id == todo.id)
    with engine.connect() as conn:
        conn.execute(requete)
        conn.commit()


def get_next_id():
    # devieng obsoloete si 10000000 de taches
    with engine.connect() as conn:
        result = conn.execute(db.text("""SELECT MAX(id) FROM todos""")).fetchone()
        conn.commit()
    if result[0]:
        return int(result[0]) + 1
    return 1


def create_todo(task: str, complete: bool = False, due: Optional[datetime] = None) -> None:
    id = get_next_id()
    todo = Todo(id=id, task=task, complete=complete, due=due)
    write_to_bd(todo)


def get_todo(par_id: int) -> Todo | bool:
    col_id = db.sql.column('id')
    requete = todo_table.select()
    requete = requete.where(col_id == par_id)
    result = None
    with engine.connect() as conn:
        result = conn.execute(requete).fetchall()
        conn.commit()
    if result:
        return Todo(result[0][0], result[0][1], result[0][2], result[0][3])
    return False


def get_todos() -> list:
    requete = todo_table.select()
    with engine.connect() as conn:
        result = conn.execute(requete).fetchall()
        conn.commit()
    return sorted(result,key=lambda x : x[3])

    # Autre methode :
    # requete = select(todo_table)
    # result = engine.connect().execute(requete).fetchall()


def update_todo(
        id: int,
        task: str,
        complete: bool,
        due: Optional[datetime]
) -> None:
    if get_todo(id):
        todo = get_todo(id)
        todo.task = task
        todo.complete = complete
        due = due.split("-")
        todo.due = datetime(int(due[0]), int(due[1]), int(due[2])) if due else todo.due  # coz can be none
        update_bd(todo)


def delete_todo(id: int) -> None:
    col_id = db.sql.column('id')
    requete = todo_table.delete()
    requete = requete.where(col_id == id)
    with engine.connect() as conn:
        result = conn.execute(requete)
        conn.commit()


def complete_todo(par_id: int) -> None:
    tache = get_todo(par_id)
    tache.complete = True
    update_bd(tache)


def delete_all() -> None:
    requete = todo_table.delete()
    with engine.connect() as conn:
        result = conn.execute(requete)
        conn.commit()


def import_from_csv(file: str) -> list:
    i = 0
    tasks = []
    with open(file, 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        for r in csvreader:
            if i > 0:
                date = [int(e) for e in r[3].split(' ')[0].split('-')]
                tasks.append(Todo(int(r[0]), r[1], True if r[2] == 'True' else False,
                                  datetime(date[0], date[1], date[2])))
            i += 1
        return tasks
