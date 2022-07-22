from flask import Flask, render_template, redirect, url_for, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://nicco:5dAwmuwXNXhkVHvl@cluster0.6jcpz.mongodb.net/cluster0?retryWrites=true&w=majority'
mongo = PyMongo(app)

# Collegamento a MongoDB
todo_list = mongo.db.todo


# Pagina iniziale > Rendering index.html
@app.route('/')
def index():
    available_todo = todo_list.find().sort('date', -1)
    return render_template('index.html', todo_list=available_todo)


# Aggiunta nota
@app.route('/add', methods=['POST'])
def add_note():
    note_title = request.form.get('title')
    if note_title == '':
        note_title = 'Nuova nota'

    note_body = request.form.get('body')
    now = datetime.today()
    todo_list.insert_one({
        'title': note_title,
        'body': note_body,
        'date': now.strftime("%d/%m/%Y | %H:%M:%S"),
        'expired': False
    })
    return redirect(url_for('index'))


# Visualizza dettagli nota
@app.route('/details/<oid>')
def show_details(oid):
    todo_item = todo_list.find_one({'_id': ObjectId(oid)})
    return render_template('details.html', item=todo_item)


# Imposta come completato
@app.route('/completed/<oid>')
def mark_as_completed(oid):
    todo_item = {'_id': ObjectId(oid)}
    updated_item = {'$set': {'expired': True}}
    todo_list.update_one(todo_item, updated_item)
    return redirect(url_for('index'))


# Imposta come da completare
@app.route('/todo/<oid>')
def mark_as_todo(oid):
    todo_item = {'_id': ObjectId(oid)}
    updated_item = {'$set': {'expired': False}}
    todo_list.update_one(todo_item, updated_item)
    return redirect(url_for('index'))

# Elimina specifico
@app.route('/delete/<oid>')
def delete_specific(oid):
    todo_list.delete_one({'_id': ObjectId(oid)})
    return redirect(url_for('index'))


# Elimina completate
@app.route('/delete_completed')
def delete_completed():
    todo_list.delete_many({'expired': True})
    return redirect(url_for('index'))


# Elimina tutte
@app.route('/delete_all')
def delete_all():
    todo_list.delete_many({})
    return redirect(url_for('index'))
