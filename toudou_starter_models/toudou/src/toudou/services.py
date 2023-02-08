import csv
import dataclasses
import io

from datetime import datetime

from toudou.models import create_todo, get_todos, Todo


def export_to_csv() -> str:
    output = io.StringIO()
    csv_writer = csv.DictWriter(
        output,
        fieldnames=[f.name for f in dataclasses.fields(Todo)]
    )
    for todo in get_todos():
        csv_writer.writerow(dataclasses.asdict(todo))
    return output.getvalue()


def import_from_csv(data: str) -> None:
    with io.StringIO(data) as csvfile:
        csv_reader = csv.DictReader(
            csvfile,
            fieldnames=[f.name for f in dataclasses.fields(Todo)]
        )
        for row in csv_reader:
            create_todo(
                task=row["task"],
                due=datetime.fromisoformat(row["due"]) if row["due"] else None,
                complete=bool(row["complete"])
            )
