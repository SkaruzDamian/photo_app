from datetime import datetime
from . import db
from werkzeug.utils import secure_filename
import os

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    storage_path = db.Column(db.String(512), nullable=False)
    blob_url = db.Column(db.String(512), nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    approval_date = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, file, user_id):
        self.original_filename = file.filename
        self.filename = secure_filename(file.filename)
        self.mime_type = file.content_type
        self.user_id = user_id
        self.storage_path = self._generate_storage_path()

    def _generate_storage_path(self):
        """Generuje ścieżkę do przechowywania w Azure Blob Storage"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f'images/{self.user_id}/{timestamp}_{self.filename}'

    def approve(self):
        """Zatwierdza zdjęcie"""
        self.status = 'approved'
        self.approval_date = datetime.utcnow()
        db.session.commit()

    def reject(self):
        """Odrzuca zdjęcie"""
        self.status = 'rejected'
        db.session.commit()

    def get_url(self):
        """Zwraca URL do zdjęcia"""
        if self.blob_url:
            return self.blob_url
        return None

    @staticmethod
    def get_pending_images():
        """Pobiera wszystkie oczekujące zdjęcia"""
        return Image.query.filter_by(status='pending').order_by(Image.upload_date.desc()).all()

    @staticmethod
    def get_approved_images_for_user(user_id):
        """Pobiera zaakceptowane zdjęcia dla danego użytkownika"""
        return Image.query.filter_by(
            user_id=user_id, 
            status='approved'
        ).order_by(Image.approval_date.desc()).all()

    def __repr__(self):
        return f'<Image {self.filename} ({self.status})>'

    def to_dict(self):
        """Konwertuje obiekt na słownik do API"""
        return {
            'id': self.id,
            'filename': self.original_filename,
            'status': self.status,
            'upload_date': self.upload_date.isoformat(),
            'approval_date': self.approval_date.isoformat() if self.approval_date else None,
            'url': self.get_url(),
            'user_id': self.user_id
        }