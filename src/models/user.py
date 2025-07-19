from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }

class Reuniao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    data = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_termino = db.Column(db.Time, nullable=False)
    local = db.Column(db.String(200))
    participantes = db.Column(db.Text)
    descricao = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    criador = db.relationship('User', backref=db.backref('reunioes', lazy=True))

    def __repr__(self):
        return f'<Reuniao {self.titulo}>'

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'data': self.data.isoformat() if self.data else None,
            'hora_inicio': self.hora_inicio.strftime('%H:%M') if self.hora_inicio else None,
            'hora_termino': self.hora_termino.strftime('%H:%M') if self.hora_termino else None,
            'local': self.local,
            'participantes': self.participantes,
            'descricao': self.descricao,
            'created_by': self.created_by,
            'criador_nome': self.criador.username if self.criador else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    data = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False) # Nova coluna
    hora_termino = db.Column(db.Time, nullable=False) # Nova coluna
    local = db.Column(db.String(120), nullable=False)
    participantes = db.Column(db.String(500), nullable=False)
    descricao = db.Column(db.String(1000), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'data': self.data.isoformat(),
            'hora_inicio': self.hora_inicio.isoformat(), # Ajustado
            'hora_termino': self.hora_termino.isoformat(), # Ajustado
            'local': self.local,
            'participantes': self.participantes,
            'descricao': self.descricao,
            'created_by': self.created_by
        }