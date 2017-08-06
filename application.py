# -*- coding: utf-8 -*-

import os
# import pandas as pd
import sqlite3
# used to change the filename to secure format
from werkzeug.utils import secure_filename

## import application modules
import click
from flask import Flask, render_template, request, g, redirect, flash
# from flask_login import LoginManager, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
# from deprecation import deprecated


BASEPATH = os.path.dirname(os.path.abspath(__file__))

print(BASEPATH)

# create a new web application object
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(BASEPATH, 'static/uploads')
app.config['SECRET_KEY'] = 'kaskdjh9213nkwej923fnkwvjnc92kejrvnkv93vkejv93'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASEPATH, 'data/db.sqlite3')

ALLOWED_EXTENSIONS = {'.csv',}

db = SQLAlchemy(app)

# login_manager = LoginManager()
# login_manager.init_app(application)


# deprecated
DATABASE = 'data/db.sqlite3'


# deprecated
def get_db():
    """
    connect to database if not already connected and
    return connection object
    """
    # g._database if g._database exists else None
    # getattribute
    db = getattr(g, '_database', None)
    if db is None:
        # g._database = sqlite3.connect(DATABASE)
        # db = g._database
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

"""
ORM (Object Relational Mapper)
------------------------------

maps your database table to your python class, so you can use a table and its rows,
as class and its instances.

"""

class User(db.Model):
    """
    Model == Model from MVC ( Model View Controller )
    """
    # db attributes
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(60))
    status = db.Column(db.Boolean, default=True)

# #    users = ({
# #        'username': 'test@example.net',
# #        'password': 'pass1'          
# #    },)
# #    authenticated = False
# #    user = {}
    
#     def is_authenticated(self):
# #        return self.authenticated
#         return self.id and True
    
#     def is_active(self):
# #        return True
#         return self.status
    
#     def is_anonymous(self):
#         return False
    
#     def get_id(self):
#         return self.id
# #        if self.is_authenticated():
# ##            return self.user['username']
# #            return self.user['id']
# #        return None
    
# #    @staticmethod
# #    def user_exists(email, password):
# ##        user_dct = [dct for dct in User.users if dct['username'] == email 
# ##                    and dct['password'] == password]
# #        cur = get_db().cursor()
# #        user_sql = "SELECT id, username FROM users WHERE username=? AND password=?"
# #        cur.execute(user_sql, (email, password))
# #        user_record = cur.fetchone()
# #        print("record found", user_record)
# ##        print("found user", user_dct)
# ##        if user_dct:
# #        if user_record:
# #            user = User()
# ##            user.user = user_dct[0]
# #            user.user = {
# #                'id': user_record[0],
# #                'username': user_record[1]
# #            }
# #            user.authenticated = True
# #            return user
# #        return None


class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    dataset = db.Column(db.String(250))
    
    def __repr__(self):
        return "{}, {}".format(self.name, self.dataset)


# @login_manager.user_loader
# def load_user(user_id):
#     """
#     this is used by login manager object to load user object from user_id
#     user_id is obtained from session on consecutive requests
#     """
# #    cur = get_db().cursor()
# #    user_sql = "SELECT id, username FROM users WHERE id=?"
# #    cur.execute(user_sql, (user_id,))
# #    user_record = cur.fetchone()
# ##    user_dct = [dct for dct in User.users if dct['username'] == user_id]
# #    user = User()
# ##    user.user = user_dct[0]
# #    user.user = {
# #        'id': user_record[0],
# #        'username': user_record[1]
# #    }
# #    user.authenticated = True
#     user = User.query.get(user_id)
#     return user


def allowed_file(filename):
    """
    Check if given extension for the file is allowed
    """
    return os.path.splitext(filename)[1] in ALLOWED_EXTENSIONS


# add a new route 
# http://localhost:5000/
@app.route('/')
def index():
    """
    this route will be run when a user visits main page of our application.
    """
    # using hardcoded records
    # records = [{'name': 'Hello', 'dataset': 'hello.csv'}]

    # get records from database using sql query
    # cur = get_db().cursor()
    # cur.execute('SELECT id, name, dataset from dataset')
    # records = cur.fetchall()


    records = Dataset.query.all()
    print(records)
    return render_template('home.html', records=records)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # save this data to db or do something
        print("Posted data", request.form)
        # check if requested user is in our database
#        user = User.user_exists(request.form['email'], request.form['password'])
        # user = User.query.filter_by(username=request.form['email'],
        #                             password=request.form['password']).first()
        # if user:
        #     # login_user(user)
        #     print("logged in")
        # else:
        #     print("Unable to login")
    return render_template('login.html')


@app.route('/logout')
def logout():
    # logout_user()
    return redirect('/')


# @application.route('/data/add', methods=['GET', 'POST'])
# @login_required
# def add_data():
#     if request.method == 'POST':
#         # upload data file to server
#         # save entry into db
# #        db = get_db()
# #        cur = db.cursor()
#         # print what we need to save to db
#         print(request.form['name'], request.files['datafile'].filename)
#         dataset_name = request.form['name']
        
#         file = request.files['datafile']
#         filename = None
#         if file:
#             filename = secure_filename(file.filename)
#             print(filename)
#             if not allowed_file(filename):
#                 flash('File is not allowed, Use either of {}'.format(', '.join(ALLOWED_EXTENSIONS)), 
#                       'danger')
#                 return redirect('data/add')
#             fullpath = os.path.join(application.config['UPLOAD_FOLDER'], filename)
#             file.save(fullpath)
            
#             # we work with csv file, generate a png image and save it to database
#             dframe = pd.read_csv(fullpath)
#             dframe = dframe.set_index(["Edition"])
#             print(dframe)
            
#             # returns a axes object
#             # plt = dframe[["Edition", "Grand Total"]].plot()
#             plt = dframe["Grand Total"].plot(color='red', linewidth=2.5)
            
#             # '_'.join(request.form['name'].split(' '))
#             fig_name = '_'.join(dataset_name.split(' ')) + '.png'
            
#             # plt.savefig(fig_name) # if this was a matplotlib plot object
#             fig = plt.get_figure()
#             fig.savefig(os.path.join(application.config['UPLOAD_FOLDER'], fig_name))
        
#         # save submitted details to db
# #        sql = 'INSERT INTO dataset(name, dataset) VALUES(?, ?)'
# #        cur.execute(sql, (request.form['name'], filename))
# #        db.commit()
#         dataset = Dataset(name=dataset_name,
#                           dataset=fig_name)
#         db.session.add(dataset)
#         db.session.commit()
#         flash("Record added successfully", 'success')
#         return redirect('/data/list')
        
#     return render_template('data_add.html')


# @application.route('/data/edit/<int:did>', methods=['GET', 'POST'])
# @login_required
# def edit_data(did):
#     # fetch data
#     dataset = Dataset.query.get(did)
#     if not dataset:
#         flash('Requested record was not found.', 'warning')
#         return redirect('/data/add')
#     if request.method == 'POST':
#         file = request.files['datafile']

#         # update name from inputted value
#         dataset.name = request.form['name']

#         filename = None
#         if file:
#             filename = secure_filename(file.filename)
#             if not allowed_file(filename):
#                 flash('File is not allowed, Use either of {}'.format(', '.join(ALLOWED_EXTENSIONS)), 
#                       'danger')
#                 return redirect('data/edit/' + str(dataset.id))
#             file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            
#             # update dataset only if file is uploaded
#             dataset.dataset = filename
        
#         db.session.add(dataset)
#         db.session.commit()
#         flash("Record updated successfully", 'success')
#     return render_template('data_edit.html', dataset=dataset)


# @application.route('/data/list')
# @login_required
# def list_data():
#     records = Dataset.query.all()
#     return render_template('data_list.html', records=records)


# @application.route('/data/delete/<int:did>')
# @login_required
# def delete_data(did):
#     data = Dataset.query.get(did)
#     db.session.delete(data)
#     db.session.commit()
#     flash("Record removed successfully", 'success')
#     return redirect('/data/list')


@app.cli.command()
def initdb():
    """
    this is used to initialize database using command line
    """
    click.echo("Creating new tables...")
    # db = get_db()
    # db.execute("CREATE TABLE user(id INTEGER, username TEXT, password TEXT, status INTEGER)")
    # db.execute("CREATE TABLE dataset(id INTEGER, name TEXT, dataset TEXT)")
    # db.commit()

    # using sqlalchemy
    db.create_all()
    click.echo("...done")


@app.cli.command()
def populate():
    """
    this is used to populate all the database tables using dummy data
    """
    click.echo("Loading data...")
    # db = get_db()
    # cur = db.cursor()
    # cur.execute("INSERT INTO user(id, username, password, status) VALUES(?, ?, ?, ?)",
    #             (1, 'admin', 'admin123', 1))
    # cur.executemany("INSERT INTO dataset(id, name, dataset) VALUES(?, ?, ?)",
    #                 [(1, 'type1', 'type1.csv'), (2, 'type2', 'type2.csv'),
    #                  (3, 'type3', 'type3.csv'), (4, 'type4', 'type4.csv'),
    #                  (5, 'type5', 'type5.csv'), (6, 'type6', 'type6.csv'),
    #                  (7, 'type7', 'type7.csv'), (8, 'type8', 'type8.csv'),
    #                  (9, 'type9', 'type9.csv'), (10, 'type10', 'type10.csv')])
    # db.commit()
    user = User(username='admin', password='admin123', status=1)
    db.session.add(user)
    dataset = [(1, 'type1', 'type1.csv'), (2, 'type2', 'type2.csv'),
                     (3, 'type3', 'type3.csv'), (4, 'type4', 'type4.csv'),
                     (5, 'type5', 'type5.csv'), (6, 'type6', 'type6.csv'),
                     (7, 'type7', 'type7.csv'), (8, 'type8', 'type8.csv'),
                     (9, 'type9', 'type9.csv'), (10, 'type10', 'type10.csv')]
    for d in dataset:
        db.session.add(Dataset(name=d[1], dataset=d[2]))
    db.session.commit()
    click.echo("...done")

