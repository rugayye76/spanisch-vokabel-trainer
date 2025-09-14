models.py
from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    theme_preference = db.Column(db.String(16), default='light', nullable=False)  # 'light' or 'dark'

    # Relationships
    progress_entries = db.relationship('UserProgress', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationships
    vocabularies = db.relationship('Vocabulary', backref='chapter', lazy=True)

    def __repr__(self):
        return f'<Chapter {self.name}>'


class Vocabulary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    deutsch = db.Column(db.String(256), nullable=False)
    spanisch = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Vocabulary {self.deutsch} -> {self.spanisch}>'


class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vocabulary_id = db.Column(db.Integer, db.ForeignKey('vocabulary.id'), nullable=False)
    status = db.Column(db.String(16), nullable=False)  # 'known', 'review', 'new'
    last_reviewed = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationships
    vocabulary = db.relationship('Vocabulary', backref='progress_entries')

    def __repr__(self):
        return f'<UserProgress {self.user_id}: {self.vocabulary_id} - {self.status}>'