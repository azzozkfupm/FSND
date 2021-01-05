import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask
from flask_migrate import Migrate
from flask_moment import Moment


# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

db = SQLAlchemy()


def setup_db(app):
    app.config.from_object('config')
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)


# defining many to many relationship for actors and movies


class Movie(db.Model):

    # __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Movie {self.id}, {self.title}"

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return{
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }


class Actor(db.Model):

    # __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Actor {self.id}, {self.name}"

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return{
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }


def db_drop_create_all():
    db.drop_all()
    db.create_all()
