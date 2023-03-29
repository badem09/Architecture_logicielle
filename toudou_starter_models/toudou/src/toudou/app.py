import flask
import os
import toudou.models as models
import toudou.services as services
from toudou.forms import FormAjouter, FormModifier
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

models.init_db()

categories = flask.Blueprint('categories', "__name__", url_prefix='/categories')
old_app = flask.Blueprint("old_app", "__name__", url_prefix='')


def create_app():
    app = flask.Flask(__name__)
    app.config.from_prefixed_env(prefix="TOUDOU_FLASK")
    app.register_blueprint(categories)
    app.register_blueprint(old_app)
    return app


@categories.route('/')
def test():
    return "<h1> Le Blueprint catégories marche bien </h1>"


@old_app.route('/')
def redirect_index() -> str:
    """
    Redirection vers la page 'index.html'
    """
    taches = models.get_todos()
    return flask.render_template('index.html', tasks=taches)


@old_app.route('/completer/<int:id>')
def completer(id: int) -> str:
    """
    Modifie le status d'une tâches en "Complétée" (achevée) et redirige vers la page 'index.html'
    (Rafraichssement de la page)
    """
    models.complete_todo(id)
    return flask.render_template('index.html', tasks=models.get_todos())


@old_app.route('/supprimer/<int:id>')
def supprimer(id: int) -> str:
    """
    Supprime une tâche et redirige vers la page 'index.html'
    (Rafraichssement de la page)
    """
    models.delete_todo(id)
    taches = models.get_todos()
    return flask.render_template('index.html', tasks=taches)


@old_app.route('/redirect_modifier/<int:id>')
def redirect_modifier(id) -> str:
    """
    Redirection vers la page 'modifier.html'
    """
    task = models.get_todo(id)
    form = FormModifier()
    form.task.data = task.task
    form.status.data = "Complétée" if task.complete else "Incomplète"
    print(form.status.data)
    form.due.data = task.due
    form.id.data = task.id
    return flask.render_template('modifier.html', task=task, form=form)


@old_app.route('/modifier', methods=['POST'])
def modifier() -> str:
    """
    Modifie une tâche à partir des entrées du formulaire de la page 'modifier.html'
    et renvoie vers la page 'index.html'
    """
    form = FormModifier()
    if form.validate_on_submit():
        id = form.id.data
        intitule = form.task.data
        status = True if form.status.data == 'Complétée' else False
        date = form.due.data
        models.update_todo(id, intitule, status, date)
        taches = models.get_todos()
        return flask.render_template('index.html', tasks=taches)

    return flask.render_template('modifier.html', task=models.get_todo(id))


@old_app.route('/redirect_ajouter')
def redirect_ajouter() -> str:
    """
    Redirection vers la page 'ajouter.html'
    """
    form = FormAjouter()
    return flask.render_template('ajouter.html', form=form)


@old_app.route('/ajout', methods=['POST'])
def ajout() -> str:
    """
    Ajoute une tâche à partir des entrées du formulaire de la page 'ajout.html'
    et refdirige vers la page 'index.html'
    """
    form = FormAjouter()
    if form.validate_on_submit():
        intitule = form.task.data
        date = form.due.data
        models.create_todo(task=intitule, complete=False, due=date)
        taches = models.get_todos()
        return flask.render_template('index.html', tasks=taches)
    return flask.render_template('ajouter.html')


@old_app.route('/tous_supprimer')
def tous_supprimer():
    """
    Supprime toutes les tâches enregistrées et redirige vers la page 'index.html'
    """
    models.delete_all()
    return flask.render_template('index.html', tasks=[])


@old_app.route('/redirect_import_csv')
def redirect_import_csv():
    """
    Redirection vers la page 'import_csv.html'
    """
    return flask.render_template('import_csv.html', tasks=[], filename="")


@old_app.route('/import_csv', methods=['POST'])
@old_app.route('/import_csv/<filename>')
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
        try:  # En cas d'erreur de format
            tasks = services.import_from_csv(f.filename)
            return flask.render_template('import_csv.html', tasks=tasks, filename=f.filename)
        except Exception as e:
            print(e)
            flask.flash("Problème de format du fichier csv. \n Pour plus "
                        "d informations, consultez le README", "error")
            return flask.render_template('import_csv.html', tasks=[], filename="")


    else:  # Enregistre les tâches et redirige vers 'index.html'
        tasks = services.import_from_csv(filename)
        for t in tasks:
            models.write_to_bd(t)
        return flask.render_template('index.html', tasks=models.get_todos())


@old_app.route('/redirect_export_csv')
def redirect_export_csv() -> str:
    """
    Redirige vers la page 'export_csv'.
    """
    return flask.render_template('export_csv.html', tasks=models.get_todos())


@old_app.route('/export_csv', methods=['POST'])
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
