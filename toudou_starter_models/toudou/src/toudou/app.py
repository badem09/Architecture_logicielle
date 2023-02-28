import csv

from flask import Flask
import flask
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret key"

import models
import services

@app.route('/')
def redirect_index():
    taches = models.get_todos()
    return flask.render_template('index.html', tasks=taches)

@app.route('/completer/<int:id>')
def completer(id):
    models.complete_todo(id)
    return flask.render_template('index.html', tasks=models.get_todos())

@app.route('/redirect_modifier/<int:id>')
def redirect_modifier(id):
    return flask.render_template('modifier.html', task=models.get_todo(id))

@app.route('/supprimer/<int:id>')
def supprimer(id):
    models.delete_todo(id)
    taches = models.get_todos()
    return flask.render_template('index.html', tasks=taches)

@app.route('/redirect_ajouter')
def redirect_ajouter():
    return flask.render_template('ajouter.html')

@app.route('/modifier', methods=['POST'])
def modifier():
    if flask.request.method == 'POST':
        tab = flask.request.form
        id = flask.request.form.get("id")
        for e in tab.values():
            if e == "":
                flask.flash("Un des champs n'est pas remplit !", "error")
                return flask.render_template('modifier.html', task=models.get_todo(id))

        task = models.get_todo(id)
        intitule = tab.get("intitule")
        status = True if tab.get("status")=='Complétée' else False
        date = tab.get("date")

        models.update_todo(id,intitule,status,date)

    taches = models.get_todos()
    return flask.render_template('index.html', tasks=taches)

@app.route('/ajout', methods=['POST'])
def ajout():
    if flask.request.method == 'POST':
        tab = flask.request.form
        intitule = tab.get("intitule")
        liste_date = tab.get("date").split("-")
        date = datetime(int(liste_date[0]), int(liste_date[1]), int(liste_date[2]))
        models.create_todo(intitule,False,date)
    taches = models.get_todos()
    return flask.render_template('index.html', tasks=taches)

@app.route('/tous_supprimer')
def tous_supprimer():
    models.delete_all()
    return flask.render_template('index.html', tasks=[])

@app.route('/redirect_import_csv')
def redirect_import_csv():
    return flask.render_template('import_csv.html', tasks=[], filename="")


@app.route('/import_csv', methods=['POST'])
@app.route('/import_csv/<filename>')
def import_csv(filename=""):
    # creer custom conveter : https://exploreflask.com/en/latest/views.html#url-converters

    if flask.request.method == 'POST':
        tab = flask.request.files
        print(tab['file'])
        f = tab["file"]
        tasks = models.import_from_csv(f.filename)
        filename = f.filename
        return flask.render_template('import_csv.html', tasks=tasks, filename=filename)
    else:
        tasks = models.import_from_csv(filename)
        for t in tasks:
            models.write_to_bd(t)
        tasks = models.get_todos()
        return flask.render_template('index.html', tasks=tasks)


@app.route('/redirect_export_csv')
def redirect_export_csv():
    #tick box pour slectionne quelles tahces exporter
    return flask.render_template('export_csv.html', tasks=models.get_todos())

@app.route('/export_csv', methods=['POST'])
def export_csv():
    tasks=[]
    # Attention : ecrase
    if flask.request.method == 'POST':
        tab = flask.request.form
        for t in tab.values():
            tasks.append(models.get_todo(t))
        path = services.export_to_csv(tasks)
        print(list(tab.items()))

        flask.flash("Les tàches séléctionnées ont bien été exportées ici : \n" + path)

    return flask.render_template('export_csv.html', tasks=models.get_todos())


if __name__ == '__main__':
    app.run(debug=True)

