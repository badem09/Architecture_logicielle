import click
import uuid
import pickle
import datetime
import glob
import os

from dataclasses import dataclass


@dataclass
class Todo:
    id: int
    task: str
    complete : bool
    due : datetime.date

    def __str__(self):
        return self.task + " (" + str(self.due) + ") " + "Done = " + str(self.complete)

@click.group()
def cli():
    pass


@cli.command()
def display():
    liste = os.listdir('tasks')
    for task in liste:
        click.echo(pickle.load(open('tasks/'+task,'rb')))

@cli.command()
@click.option('--task', prompt='Task')
@click.option('--jour', prompt='Jour ')
@click.option('--mois', prompt='mois ')
@click.option('--annee', prompt='annee ')
def addTask(task: str,jour:str,mois:str,annee:str):
    
    date = datetime.date(int(jour),int(mois),int(annee))
    todo = Todo(id=uuid.uuid4().int, task=task,complete=False, due=date)
    click.echo(todo)
    filee = open('tasks/toto' + str(todo.id) + '.pkl', 'wb')
    pickle.dump(todo, filee)
    filee.close()
    click.echo("tache %s date %s ajoutée" % (task,date))
    



