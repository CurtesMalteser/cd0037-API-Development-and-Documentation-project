"""Models for the trivia app"""
from itertools import tee
import json
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

import os
database_name = os.environ['TRIVIA_DB_NAME']
database_path = os.environ['TRIVIA_DB_PATH']

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    """Binds a flask application and a SQLAlchemy service"""
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class Question(db.Model):
    """Question"""
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category = Column(String)
    difficulty = Column(Integer)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
            }

class Category(db.Model):
    """Category"""
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
            }
    

class QuestionDecoder(json.JSONDecoder):
    """QuestionDecoder"""

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        question = dct.get('question')

        if question is None or question == '':
            raise ValueError('question is required')

        answer = dct.get('answer')

        if answer is None or answer == '':
            raise ValueError('answer is required')

        category = -1

        try:
            category = int(dct.get('category'))
        except Exception as exc:
            raise ValueError('category is required') from exc
        
        if category == -1:
            raise ValueError('category is required')

        difficulty = -1

        try:
            difficulty = int(dct.get('difficulty'))
        except Exception as exc:
            raise ValueError('difficulty is required') from exc

        if difficulty < 1 or difficulty > 5:
            raise ValueError('difficulty is required')

        return Question(
            question= question,
            answer= answer,
            category= category,
            difficulty= difficulty
            )
  