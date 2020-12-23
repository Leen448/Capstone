from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime
import os


database_path = (os.environ.get('DATABASE_URL'))

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] ="postgresql://postgres:Leen448@localhost:5432/CastingAgency"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Actors(db.Model):
    __tablename__ = 'Actors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete_object(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
       db.session.commit()

       
    pass

class Movies(db.Model):
    __tablename__ = 'Movies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime,
                         nullable=False,
                         default=datetime.datetime.today())

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


    pass


class Performance(db.Model):
    __tablename__ = 'performance'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    actor_id = db.Column(
                        db.Integer,
                        db.ForeignKey('Actors.id', ondelete="CASCADE"),
                        nullable=False)

    movie_id = db.Column(
                        db.Integer,
                        db.ForeignKey("Movies.id", ondelete="CASCADE"),
                        nullable=False)


    pass




