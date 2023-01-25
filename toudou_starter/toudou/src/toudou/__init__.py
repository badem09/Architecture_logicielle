import click
import uuid
import pickle
import datetime

from dataclasses import dataclass


@dataclass
class Todo:
    id: int
    task: str
    complete : bool
    due : datetime.date

@click.group()
def cli():
    pass


@cli.command()
@click.option('--task', prompt='Task')
def display(task: str):
    todo = Todo(id=uuid.uuid4().int, task=task,complete=False, due=datetime.datetime.now())
    click.echo(todo)

@cli.command()
@click.option('--task', prompt='Task')
@click.option('--jour', prompt='Jour ')
@click.option('--mois', prompt='mois ')
@click.option('--annee', prompt='annee ')
def addTask(task: str,jour:str,mois:str,annee:str):
    
    date = datetime.date(int(jour),int(mois),int(annee))

    todo = Todo(id=uuid.uuid4().int, task=task,complete=False, due=date)
    click.echo(todo)
    click.echo("tache %s date %s ajoutée" % (task,date))

