
import uuid
import sqlite3
from collections import namedtuple
from flask import Flask, render_template, request, redirect, url_for

Mode = namedtuple('Mode', ['LINK', 'FILE', 'MEMO'])
modes = Mode(LINK=1, FILE=2, MEMO=3)


def new_id():

    return uuid.uuid4().hex[:12]


app = Flask(__name__)


# Route to show the form and existing data
@app.route('/')
def index():
    with sqlite3.connect('constellations.sqlite3') as conn:
        c = conn.cursor()
        #c.execute('SELECT * FROM Items')
    #data = c.fetchall()

    return render_template('index.html')


@app.route('/links')
def links():
    with sqlite3.connect('constellations.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT Body,Tags FROM Items WHERE Mode=1;')
    data = cursor.fetchall()

    modified_data = []
    for row in data:
        
        row_dict = dict(row)
        row_dict['tags_list'] = row_dict['Tags'].split('#')
        modified_data.append((row_dict['Body'],row_dict['tags_list']))


    return render_template('links.html', items=modified_data)


@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['tag']
    mode = request.form['mode']

    with sqlite3.connect('constellations.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT Body,Tags FROM Items WHERE Mode=? and Tags like ?;', (mode, '%{}%'.format(keyword)))
    data = cursor.fetchall()

    modified_data = []
    for row in data:
        
        row_dict = dict(row)
        row_dict['tags_list'] = row_dict['Tags'].split('#')
        modified_data.append((row_dict['Body'],row_dict['tags_list']))

    return render_template('links.html', items=modified_data)


@app.route('/add', methods=['POST'])
def add_user():
    body = request.form['body']
    mode = request.form['mode']

    with sqlite3.connect('constellations.sqlite3') as conn:
        cursor = conn.cursor()
        query = 'INSERT INTO Items (ID, Mode, Tags, Body) VALUES(?,?,?,?);'
        cursor.execute(query, (new_id(), mode, '', body))

    return redirect(url_for('index'))


if __name__ == '__main__':
    
    app.run(debug=True)
