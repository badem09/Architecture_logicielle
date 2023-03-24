from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import sqlalchemy as db
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, Date

from toudou import config

TODO_FOLDER = "db"
metadata_obj = MetaData()
engine = create_engine(
config['DATABASE_URL'],
echo=config['DEBUG']
)
todo_table = Table(
    "todos",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("task", String(1000), nullable=False),
    Column("complete", Boolean, nullable=False),
    Column("due", Date, nullable=True)
)


@dataclass
class Todo:
    task: str
    complete: bool
    due: Optional[datetime]
    id: int

    def __init__(self,task,complete,due):
        self.id = id(self)
        self.due = due
        self.task = task
        self.complete = complete

    def __eq__(self, other):
        return self.due.strftime("%d-%m-%Y") == other.due.strftime("%d-%m-%Y") and self.task == other.task


def init_db() -> None:
    metadata_obj.create_all(engine)


def write_to_bd(todo: Todo) -> bool:
    """
    Enregistre une tâche [todo] à la base de données si son id n'y est pas.
    """
    if not get_todo(todo.id):
        requete = db.Insert(todo_table).values(task=todo.task, complete=todo.complete, due=todo.due)
        with engine.connect() as conn:
            conn.execute(requete)
            conn.commit()
        return True
    return False


def update_bd(todo: Todo) -> None:
    """
    Modifie une tâche dans la base de données avec son id
    """
    requete = db.Update(todo_table).values(id=todo.id, task=todo.task, complete=todo.complete, due=todo.due)
    requete = requete.where(db.sql.column('id') == todo.id)
    with engine.connect() as conn:
        conn.execute(requete)
        conn.commit()


def create_todo(task: str, complete: bool = False, due: Optional[datetime] = None) -> None:
    """
    Crée une tâche.
    """
    todo = Todo(task=task, complete=complete, due=due)
    write_to_bd(todo)


def get_todo(par_id: int) -> Todo | bool:
    """
    Retourne la tâche (objet Todo) correspondant à l'id (par_id).
    """
    col_id = db.sql.column('id')
    requete = todo_table.select()
    requete = requete.where(col_id == par_id)
    result = None
    with engine.connect() as conn:
        result = conn.execute(requete).fetchall()
        conn.commit()
    if result:
        return Todo(task=result[0][1], complete=result[0][2], due=result[0][3])
    return False


def get_todos() -> list:
    """
    Retourne une liste de tâches triées par date sous forme de tuple.
    Ex : [(id,task,complete,due),...]
    """
    requete = todo_table.select().order_by(db.sql.column("due"))
    with engine.connect() as conn:
        result = conn.execute(requete).fetchall()
        conn.commit()
    return result if result else []
    # Autre methode :
    # requete = select(todo_table)
    # result = engine.connect().execute(requete).fetchall()


def update_todo(id: int, task: str, complete: bool, due: Optional[datetime]) -> None:
    """
    Modifie une tâche (l'objet Todo) en fonction des paramêtres et l'enregistre dans la bd.
    """
    if get_todo(id):
        todo = get_todo(id)
        todo.task = task
        todo.complete = complete
        due = due.split("-")
        todo.due = datetime(int(due[0]), int(due[1]), int(due[2])) if due else todo.due  # pourrait être None
        update_bd(todo)


def delete_todo(id: int) -> bool:
    """
    Supprime une tâche de la bd en fonction de [id]
    Retourne True en cas de succès, False en cas d'échec
    """
    if get_todo(id):
        col_id = db.sql.column('id')
        requete = todo_table.delete()
        requete = requete.where(col_id == id)
        with engine.connect() as conn:
            conn.execute(requete)
            conn.commit()
        return True
    return False


def complete_todo(par_id: int) -> None:
    """
    Change le champs 'complete' d'un objet Todo en True.
    """
    tache = get_todo(par_id)
    tache.complete = True
    update_bd(tache)


def delete_all() -> None:
    """
    Supprime toutes les tâches contenues dans la bd.
    """
    requete = todo_table.delete()
    with engine.connect() as conn:
        conn.execute(requete)
        conn.commit()
