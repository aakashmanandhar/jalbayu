# -*- coding: utf-8 -*-

import os
import sqlite3
# used to change the filename to secure format
from werkzeug.utils import secure_filename
# import Flask from module "flask"
from flask import Flask, render_template, request, g


BASEPATH = os.path.dirname(os.path.abspath(__file__))

print(BASEPATH)

# create a new web application object
application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = os.path.join(BASEPATH, 'static/uploads')


DATABASE = 'data/db.sqlite3'


def get_db():
    # g._database if g._database exists else None
    # getattribute
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@application.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# add a new route 
# http://localhost:5000/
@application.route('/')
def index():
    cur = get_db().cursor()
    cur.execute('SELECT id, name, dataset from dataset')
    print(cur.fetchall())
    return render_template('home.html')


@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # save this data to db or do something
        print("Posted data", request.form)
    return render_template('login.html')


@application.route('/data/add', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        # upload data file to server
        # save entry into db
        db = get_db()
        cur = db.cursor()
        # print what we need to save to db
        print(request.form['name'], request.files['datafile'].filename)
        
        file = request.files['datafile']
        filename = None
        if file:
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
        
        # save submitted details to db
        sql = 'INSERT INTO dataset(name, dataset) VALUES(?, ?)'
        cur.execute(sql, (request.form['name'], filename))
        db.commit()
        
    return render_template('data_add.html')


if __name__ == '__main__':
    
    application.run(debug=True)
