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
        complete = "Achevée" if self.complete else "Inachevée"
        return self.task + " (" + self.due.strftime('%d, %b %Y') + ") " + "Status = " + complete

@click.group()
def cli():
    pass


@cli.command()
def display():
    """
    Affiche les tâches qui ont été enregistrées.
    """
    liste = os.listdir('tasks')
    for task in liste:
        click.echo(pickle.load(open('tasks/'+task,'rb')))

@cli.command()
@click.argument('task')
@click.option('--jour', prompt='Jour ', default=1, help='Jour de la date de fin')
@click.option('--mois', prompt='mois ', default=1, help='Mois de la date de fin')
@click.option('--annee', prompt='annee', default=1, help='Année de la date de fin') #Option Importance?
def add(task: str,jour:str,mois:str,annee:str):
    """
    Ajoute une tâche à la todo liste
    """

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
        click.echo("tache '%s' date %s ajoutée" % (task,date))
    

@cli.command()
@click.argument('task')
def remove(task: str):
    """
    Supprime une tâche si elle existe.
    """
    liste = os.listdir('tasks')
    for file in liste:
        todo = pickle.load(open('tasks/'+file,'rb'))
        if todo.task == task:
            os.remove('tasks/'+file)
            click.echo('Tâche supprimée.')
            break
    else:
         click.echo("La tâche '" + task + "' n'éxiste pas ! ")
    
@cli.command()
@click.argument('task')
@click.option('-t','--true', help="Assigne le status 'Achevée'", is_flag=True, default=False, is_eager=True)
@click.option('-f','--false', help="Assigne le status 'Inachevée'", is_flag=True, default=False, is_eager=True)
def set(task: str,true: bool,false : bool):
    """
    Assigne à une tâche un status selon l'option .
    """
    liste = os.listdir('tasks')
    for nom_file in liste:
        file_r = open('tasks/'+nom_file,'rb')
        todo = pickle.load(file_r)
        if todo.task == task:
            todo.complete = True if true else False
            file_r .close()
            file_w = open('tasks/toto' + str(todo.id) + '.pkl', 'wb')
            pickle.dump(todo, file_w)
            file_w.close()
            click.echo('Tâche complétée.')
            break
    else:
         click.echo("La tâche '" + task + "' n'éxiste pas ! ")
    
