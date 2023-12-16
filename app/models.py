from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

class ESP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    ip_address = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Esp {self.name}>'

class ProgramConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    esp_name = db.Column(db.String(100), nullable=False)
    configured_programs = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<ProgramConfig {self.configured_programs}>'