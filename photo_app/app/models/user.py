from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    images = db.relationship('Image', backref='user', lazy=True, cascade='all, delete-orphan')

    def __init__(self, username, password=None, is_admin=False):
        self.username = username
        if password:
            self.set_password(password)
        self.is_admin = is_admin

    def set_password(self, password):
        """Ustawia zahaszowane hasło"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Sprawdza czy hasło jest poprawne"""
        return check_password_hash(self.password_hash, password)

    def get_pending_images(self):
        """Pobiera oczekujące zdjęcia użytkownika"""
        return Image.query.filter_by(user_id=self.id, status='pending').all()

    def get_approved_images(self):
        """Pobiera zaakceptowane zdjęcia użytkownika"""
        return Image.query.filter_by(user_id=self.id, status='approved').all()

    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        """Ładuje użytkownika na podstawie ID dla Flask-Login"""
        return User.query.get(int(user_id))

    def __repr__(self):
        return f'<User {self.username}>'