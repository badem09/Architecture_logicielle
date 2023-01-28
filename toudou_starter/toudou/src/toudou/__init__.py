import click
import uuid
import pickle
import datetime
import glob
import os

from dataclasses import dataclass

#verifier si on est bien dans archilog/toudou_starter/toudou avec try catch

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
@click.option('--annee', prompt='annee ') #Option Importance?
def addTask(task: str,jour:str,mois:str,annee:str):

    date = datetime.date(int(jour),int(mois),int(annee))
    liste = os.listdir('tasks')
    for file in liste:
        todo = pickle.load(open('tasks/'+file,'rb'))
        if todo.task == task and todo.due == date:
            click.echo("Une tâche à la même date et au même nom existe déja.")
            break
    else:
        date = datetime.date(int(jour),int(mois),int(annee))
        todo = Todo(id=uuid.uuid4().int, task=task,complete=False, due=date)
        click.echo(todo)
        filee = open('tasks/toto' + str(todo.id) + '.pkl', 'wb')
        pickle.dump(todo, filee)
        filee.close()
        click.echo("tache %s date %s ajoutée" % (task,date))
    

@cli.command()
@click.option('--task', prompt='Task')
def removeTask(task: str):
    liste = os.listdir('tasks')
    for file in liste:
        todo = pickle.load(open('tasks/'+file,'rb'))
        if todo.task == task:
            os.remove('tasks/'+file)
            click.echo('Tâche supprimée.')
            break
    else:
         click.echo("La tâche '" + task + "' n'éxiste pas ! ")
    
