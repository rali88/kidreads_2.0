from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    topic = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    bullet_points = db.Column(db.Text, nullable=False)
    characters = db.Column(db.JSON, default={})
    pages = db.relationship('Page', backref='story', lazy=True)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    illustration = db.Column(db.Text, nullable=False)
    page_number = db.Column(db.Integer, nullable=False)
