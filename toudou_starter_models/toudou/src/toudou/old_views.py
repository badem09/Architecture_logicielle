import click
from datetime import datetime
import models
import services


@click.group()
def cli():
    pass


@cli.command()
def init_db():
    models.init_db()


@cli.command()
@click.option("-t", "--task", prompt="Your task", help="The task to remember.")
@click.option("-d", "--due", type=click.DateTime(), default=None, help="Due date of the task.")
def create(task: str, due: datetime):
    models.create_todo(task, due=due)


@cli.command()
@click.argument('id',  type=click.INT)
def get(id: int):
    click.echo(models.get_todo(id))


@cli.command()
@click.option("--as-csv", is_flag=True, help="Ouput a CSV string.")
def get_all(as_csv: bool):
    if as_csv:
        click.echo(services.export_to_csv())
    else:
        click.echo(models.get_todos())


@cli.command()
@click.argument('file')
def import_csv(file: str):
    tasks = services.import_from_csv(file)
    for t in tasks:
        models.write_to_bd(t)
    click.echo(str(len(tasks)) + " taches ont bien été enregistrés")


@cli.command()
def export_csv():
    services.export_to_csv()

@cli.command()
@click.option("--id", required=True, type=click.INT, help="Todo's id.")
@click.option("-c", "--complete", required=True, type=click.BOOL, help="Todo's id.")
@click.option("-t", "--task", prompt="Your task", help="The task to remember.")
@click.option("-d", "--due", type=click.DateTime(), default=None, help="Due date of the task.")
def update(id: int, complete: bool, task: str, due: datetime):
    models.update_todo(id, task, complete, due)


@cli.command()
@click.option("--id", required=True, type=click.INT, help="Todo's id.")
def delete(id: int):
    models.delete_todo(id)

@cli.command()
def delete_all():
    models.delete_all()

