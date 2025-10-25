from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_filename = db.Column(db.String(260), nullable=False)
    stored_filename = db.Column(db.String(260), nullable=False)
    filekey_enc = db.Column(db.String(512), nullable=False)  # hex of encrypted file key and wrap metadata
    nonce_hex = db.Column(db.String(48), nullable=False)
    tag_hex = db.Column(db.String(64), nullable=False)
    mimetype = db.Column(db.String(128))
    filesize = db.Column(db.Integer)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
