import click
import uuid

from dataclasses import dataclass


@dataclass
class Todo:
    id: int
    task: str


@click.group()
def cli():
    pass


@cli.command()
@click.option('--task', prompt='Task')
def display(task: str):
    todo = Todo(id=uuid.uuid4().int, task=task)
    click.echo(todo)
