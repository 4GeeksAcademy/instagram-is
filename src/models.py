from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    full_name = Column(String(100))
    bio = Column(Text)
    profile_picture = Column(String(300))
    created_at = Column(DateTime, default=datetime.utcnow)

    posts = relationship('Post', back_populates='usuario', cascade='all, delete-orphan')
    comentarios = relationship('Comentario', back_populates='usuario', cascade='all, delete-orphan')
    likes = relationship('Like', back_populates='usuario', cascade='all, delete-orphan')

class Post(db.Model):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    image_url = Column(String(300), nullable=False)
    caption = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    usuario = relationship('Usuario', back_populates='posts')
    comentarios = relationship('Comentario', back_populates='post', cascade='all, delete-orphan')
    likes = relationship('Like', back_populates='post', cascade='all, delete-orphan')

class Comentario(db.Model):
    __tablename__ = 'comentario'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    post = relationship('Post', back_populates='comentarios')
    usuario = relationship('Usuario', back_populates='comentarios')

class Like(db.Model):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    post = relationship('Post', back_populates='likes')
    usuario = relationship('Usuario', back_populates='likes')


if __name__ == "__main__":
   
    from flask import Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instagram.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.drop_all()  
        db.create_all()
        print("Base de datos creada con éxito")

        try:
            from eralchemy import render_er
            render_er('sqlite:///instagram.db', 'diagram.png')
            print("Diagrama ER generado en diagram.png")
        except ImportError:
            print("No tienes instalada la librería 'eralchemy'. Instálala con: pip install eralchemy")
