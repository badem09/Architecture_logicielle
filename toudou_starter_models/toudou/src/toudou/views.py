import flask
from datetime import datetime
import os

app = flask.Flask(__name__)
app.secret_key = "secret key"

import toudou.models as models
import toudou.services as services
#import models
#import services

models.init_db()

categories = flask.Blueprint(
'categories',
__name__,
url_prefix='/categories'
)
@categories.route('/')
def test():
    return "<h1> Le Blueprint catégories marche bien </h1>"

app.register_blueprint(categories)

@app.route('/')
def redirect_index() -> str:
    """
    Redirection vers la page 'index.html'
    """
    taches = models.get_todos()
    return flask.render_template('index.html', tasks=taches)


@app.route('/completer/<int:id>')
def completer(id: int) -> str:
    """
    Modifie le status d'une tâches en "Complétée" (achevée) et redirige vers la page 'index.html'
    (Rafraichssement de la page)
    """
    models.complete_todo(id)
    return flask.render_template('index.html', tasks=models.get_todos())


@app.route('/supprimer/<int:id>')
def supprimer(id: int) -> str:
    """
    Supprime une tâche et redirige vers la page 'index.html'
    (Rafraichssement de la page)
    """
    models.delete_todo(id)
    taches = models.get_todos()
    return flask.render_template('index.html', tasks=taches)


@app.route('/redirect_modifier/<int:id>')
def redirect_modifier(id) -> str:
    """
    Redirection vers la page 'modifier.html'
    """
    return flask.render_template('modifier.html', task=models.get_todo(id))


@app.route('/modifier', methods=['POST'])
def modifier() -> str:
    """
    Modifie une tâche à partir des entrées du formulaire de la page 'modifier.html'
    et renvoie vers la page 'index.html'
    """
    if flask.request.method == 'POST':
        tab = flask.request.form
        id = tab.get("id")

        for e in tab.values():  # Vérifie que tous les champs sont remplis
            if e == "":
                flask.flash("Tous les champs ne sont pas remplit !", "error")
                return flask.render_template('modifier.html', task=models.get_todo(id))

        intitule = tab.get("intitule")
        status = True if tab.get("status") == 'Complétée' else False
        date = tab.get("date")
        models.update_todo(id, intitule, status, date)

    taches = models.get_todos()
    return flask.render_template('index.html', tasks=taches)


@app.route('/redirect_ajouter')
def redirect_ajouter() -> str:
    """
    Redirection vers la page 'ajouter.html'
    """
    return flask.render_template('ajouter.html')


@app.route('/ajout', methods=['POST'])
def ajout() -> str:
    """
    Ajoute une tâche à partir des entrées du formulaire de la page 'ajout.html'
    et refdirige vers la page 'index.html'
    """
    if flask.request.method == 'POST':
        tab = flask.request.form
        for e in tab.values():  # Vérifie que tous les champs sont remplis
            if e == "":
                flask.flash("Tous les champs ne sont pas remplit !", "error")
                return flask.render_template('ajouter.html')
        else:
            intitule = tab.get("intitule")
            liste_date = tab.get("date").split("-")
            date = datetime(int(liste_date[0]), int(liste_date[1]), int(liste_date[2]))
            models.create_todo(task=intitule, complete=False, due=date)
            taches = models.get_todos()
            return flask.render_template('index.html', tasks=taches)


@app.route('/tous_supprimer')
def tous_supprimer():
    """
    Supprime toutes les tâches enregistrées et redirige vers la page 'index.html'
    """
    models.delete_all()
    return flask.render_template('index.html', tasks=[])


@app.route('/redirect_import_csv')
def redirect_import_csv():
    """
    Redirection vers la page 'import_csv.html'
    """
    return flask.render_template('import_csv.html', tasks=[], filename="")


@app.route('/import_csv', methods=['POST'])
@app.route('/import_csv/<filename>')
def import_csv(filename="") -> str:
    """
    Importe les tâches contenue dans le fichier [filename] et selon l'appel de fonction,
    affiche les tâches (appel avec le Formulaire) ou
    enregistre les tâches et redirige vers 'index.html'(appel avec le boutton "Enregistrer'
    de la page 'import_csv.html')
    """
    if flask.request.method == 'POST':  # Affiche les tâches dans le scrollBox
        tab = flask.request.files
        f = tab["file"]
        try: # En cas d'erreur de format
            tasks = services.import_from_csv(f.filename)
            return flask.render_template('import_csv.html', tasks=tasks, filename=f.filename)
        except:
            flask.flash("Problème de format du fichier csv. \n Pour plus "
                        "d informations, consultez le README", "error")
            return flask.render_template('import_csv.html', tasks=[], filename="")


    else:  # Enregistre les tâches et redirige vers 'index.html'
        tasks = services.import_from_csv(filename)
        for t in tasks:
            models.write_to_bd(t)
        return flask.render_template('index.html', tasks=models.get_todos())


@app.route('/redirect_export_csv')
def redirect_export_csv() -> str:
    """
    Redirige vers la page 'export_csv'.
    """
    return flask.render_template('export_csv.html', tasks=models.get_todos())


@app.route('/export_csv', methods=['POST'])
def export_csv():
    """
    Récupere les tâches à exporter et les exportes via 'services".
    Attention: écrase le fichier todos.csv s'il existe déja
    """
    if flask.request.method == 'POST':
        liste_id = flask.request.form.getlist("task")

        if len(liste_id) < 1:
            flask.flash("Aucune tâche n'a été séléctionnée", "error")
        else:
            tasks = [models.get_todo(int(id)) for id in liste_id]
            path = services.export_to_csv(tasks)
            flask.flash("Les tàches séléctionnées ont bien été exportées ici : \n" + path)

    return flask.render_template('export_csv.html', tasks=models.get_todos())


if __name__ == '__main__':
    app.run(debug=True)
