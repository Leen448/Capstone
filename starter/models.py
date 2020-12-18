from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime

app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate(app, db)


class Movies (db.Model):
    __tablename__ = 'Movies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime,
                         nullable=False,
                         default=datetime.datetime.today())
    pass


class Actors(db.Model):
    __tablename__ = 'Actors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)

    pass


class Play_roll(db.Model):
    __tablename__ = 'play_roll'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    actor_id = db.Column(
                        db.Integer,
                        db.ForeignKey('Actors.id'),
                        nullable=False)

    movie_id = db.Column(
                        db.Integer,
                        db.ForeignKey("Movies.id", ondelete="CASCADE")
                        )
    
    pass

