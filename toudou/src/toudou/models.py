from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import sqlalchemy as db
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, Date

TODO_FOLDER = "db"
metadata_obj = MetaData()
engine = create_engine("sqlite:///todos.db", echo=True)
todo_table = Table(
    "todos",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("task", String(1000), nullable=False),
    Column("complete", Boolean, nullable=False),
    Column("due", Date, nullable=True)
)


@dataclass
class Todo:
    id: int
    task: str
    complete: bool
    due: Optional[datetime]

    def __eq__(self, other):
        """
        Assigne la manière de comparer deux objets Todo.
        Ici compare la date et l'intitulé.
        """
        return self.due.strftime("%d-%m-%Y") == other.due.strftime("%d-%m-%Y") and self.task == other.task


def init_db() -> None:
    metadata_obj.create_all(engine)


def exist(todo: Todo) -> bool:
    """
    Vérfie si un objet Todo similaire est déja enregistré dans la bd.
    Retourne True si oui, False sinon.
    """
    todos = get_todos()
    for t in todos:
        if todo == t:
            return True
    return False


def write_to_bd(todo: Todo) -> bool:
    """
    Enregistre une tâche [todo] à la base de données si son id n'y est pas.
    """
    if not exist(todo):
        todo.id = get_next_id() if get_todo(todo.id) else todo.id
        requete = db.Insert(todo_table).values(id=todo.id, task=todo.task, complete=todo.complete, due=todo.due)
        with engine.connect() as conn:
            conn.execute(requete)
            conn.commit()
        return True
    return False


def get_next_id() -> int:
    """
    Génere un nouvel id selon ceux des tâches deja enregistrés (max des id +1).
    Limite: Si le nombre de tâches devient trop grand.
    """
    with engine.connect() as conn:
        result = conn.execute(db.text("""SELECT MAX(id) FROM todos""")).fetchone()
        conn.commit()
    if result[0]:
        return int(result[0]) + 1
    return 1


def create_todo(task: str, complete: bool = False, due: Optional[datetime] = None) -> None:
    """
    Crée une tâche.
    """
    id = get_next_id()
    todo = Todo(id=id, task=task, complete=complete, due=due)
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
        return Todo(result[0][0], result[0][1], result[0][2], result[0][3])
    return False


def get_todos() -> list:
    """
    Retourne une liste de tâches triées par date sous forme de tuple.
    Ex : [(id,task,complete,due),...]
    """
    requete = todo_table.select()
    with engine.connect() as conn:
        result = conn.execute(requete).fetchall()
        conn.commit()
    if result:
        return sorted(result, key=lambda x: x[3])
    return []


def update_bd(todo: Todo) -> None:
    """
    Modifie une tâche dans la base de données avec son id
    """
    requete = db.Update(todo_table).values(id=todo.id, task=todo.task, complete=todo.complete, due=todo.due)
    requete = requete.where(db.sql.column('id') == todo.id)
    with engine.connect() as conn:
        conn.execute(requete)
        conn.commit()


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


def complete_todo(par_id: int) -> None:
    """
    Change le champs 'complete' d'un objet Todo en True.
    """
    tache = get_todo(par_id)
    tache.complete = True
    update_bd(tache)


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


def delete_all() -> None:
    """
    Supprime toutes les tâches contenues dans la bd.
    """
    requete = todo_table.delete()
    with engine.connect() as conn:
        conn.execute(requete)
        conn.commit()
