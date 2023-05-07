import json
import traceback
from datetime import datetime

import flask
import logging
import toudou.models as models
import toudou.services as services
from flask_pydantic_spec import FlaskPydanticSpec
from toudou.forms import FormAjouter, FormModifier
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

todos = flask.Blueprint('todos', "__name__", url_prefix='/todos')
api = flask.Blueprint('api', __name__, url_prefix='/')

spec = FlaskPydanticSpec('flask', title='Todo API', version='1.0.0', openapi_version='3.0.2')
spec.register(api)

def create_app():
    app = flask.Flask(__name__)
    app.config.from_prefixed_env(prefix="TOUDOU_FLASK")
    app.register_blueprint(todos)
    app.register_blueprint(api)
    return app


auth = HTTPBasicAuth()
users = {
    'utilisateur': generate_password_hash('utilisateur'),
    'administrateur': generate_password_hash('administrateur')
}

role_user = {
    "utilisateur": "user",
    "administrateur": "admin"
}


@auth.get_user_roles
def get_user_roles(username):
    return role_user.get(username)


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s',
                    handlers=[logging.FileHandler('debug.log'), logging.StreamHandler()])


@todos.errorhandler(500)
def handle_internal_error(error):
    flask.flash('Erreur interne du serveur', 'error')
    logging.exception(error)
    return flask.redirect(flask.url_for('.index'))

@todos.errorhandler(501)
def handle_ajout_error(error):
    flask.flash("Un des champs n'a pas été remplit !", 'error')
    logging.exception(error)
    return flask.redirect(flask.url_for('.index'))


@todos.route('/')
def index() -> str:
    """
    Redirection vers la page 'index.html'
    """
    taches = models.get_todos()
    return flask.render_template('index.html', tasks=taches)


@auth.login_required(role='admin')
@todos.route('/<int:id>/completer')
def completer(id: int) -> str:
    """
    Modifie le status d'une tâches en "Complétée" (achevée) et redirige vers la page 'index.html'
    (Rafraichssement de la page)
    """
    models.complete_todo(id)
    return flask.render_template('index.html', tasks=models.get_todos())


@todos.route('/<int:id>/supprimer')
@auth.login_required(role='admin')
def supprimer(id: int) -> str:
    """
    Supprime une tâche et redirige vers la page 'index.html'
    (Rafraichssement de la page)
    """
    models.delete_todo(id)
    taches = models.get_todos()
    return flask.render_template('index.html', tasks=taches)


@todos.route('/<int:id>/modifier')
def redirect_modifier(id) -> str:
    """
    Redirection vers la page 'modifier.html'
    """
    task = models.get_todo(id)
    form = FormModifier()
    form.task.data = task.task
    form.status.data = "Complétée" if task.complete else "Incomplète"
    form.due.data = task.due
    form.id.data = task.id
    return flask.render_template('modifier.html', task=task, form=form)


@todos.route('/action_modifier', methods=['POST','GET'])
@auth.login_required(role='admin')
def action_modifier() -> str:
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


@todos.route('/ajouter')
def ajouter() -> str:
    """
    Redirection vers la page 'ajouter.html'
    """
    form = FormAjouter()
    return flask.render_template('ajouter.html', form=form)


@todos.route('/action_ajouter', methods=['POST'])
@auth.login_required(role='admin')
def action_ajouter() -> str:
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


@todos.route('/tous_supprimer')
@auth.login_required(role='admin')
def tous_supprimer():
    """
    Supprime toutes les tâches enregistrées et redirige vers la page 'index.html'
    """
    models.delete_all()
    return flask.render_template('index.html', tasks=[])


@todos.route('/import')
def redirect_import_csv():
    """
    Redirection vers la page 'import_csv.html'
    """
    return flask.render_template('import_csv.html', tasks=[], filename="")


@todos.route('/action_import_csv', methods=['POST'])
@auth.login_required(role='admin')
def action_import_taches_csv() -> str:
    """
    Importe les tâches contenue dans le fichier [filename] et renvoie les tâches
    """
    file = flask.request.files["file"]
    try:
        tasks = services.import_from_csv(file)
        tasks_json = json.dumps([t.to_dict() for t in tasks])
        return flask.render_template('import_csv.html', tasks=tasks, filename='"' + file.filename + '"', tasks_json=tasks_json)
    except Exception as e:
        traceback.print_exc()
        flask.flash("Problème de format du fichier csv. \n Pour plus "
                    "d informations, consultez le README", "error")
        return flask.render_template('import_csv.html', tasks=[], filename="")


@todos.route('/action_save_import_csv', methods=['POST'])
@auth.login_required(role='admin')
def action_save_taches_csv() -> str:
    """
    Enregistre les tâches dans la bd et redirige vers 'index.html'
    """
    tasks_dict = json.loads(flask.request.form['tasks_json'])
    tasks = [models.Todo(
        id=d['id'],
        task=d['task'],
        complete=d['complete'],
        due=datetime.strptime(d['due'], '%Y-%m-%d %H:%M:%S')
    ) for d in tasks_dict]

    for t in tasks:
        models.write_to_bd(t)
    return flask.render_template('index.html', tasks=models.get_todos())


@todos.route('/export')
def redirect_export_csv() -> str:
    """
    Redirige vers la page 'export_csv'.
    """
    return flask.render_template('export_csv.html', tasks=models.get_todos())


@todos.route('/action_export_csv', methods=['POST'])
@auth.login_required(role='admin')

def export_csv():
    """

    """
    if flask.request.method == 'POST':
        liste_id = flask.request.form.getlist("task")

        if len(liste_id) < 1:
            flask.flash("Aucune tâche n'a été séléctionnée", "error")
        else:
            tasks = [models.get_todo(int(id)) for id in liste_id]
            output = services.export_to_csv(tasks)
            response = flask.make_response(output)
            response.headers['Content-Disposition'] = 'attachment; filename=myfile.csv'
            response.headers['Content-Type'] = 'text/csv'
            return response

    return flask.render_template('export_csv.html', tasks=models.get_todos())
