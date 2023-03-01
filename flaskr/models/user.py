# flake8: noqa
from typing import List
from datetime import datetime
from . import db
from sqlalchemy import Column, String, Integer, DateTime
from . import performer_favorites, composer_favorites


class User(db.Model):  # type: ignore
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)  # type: ignore
    oauth_provider = Column(String(64), nullable=False)  # type: ignore
    oauth_id = Column(String(64), nullable=False, unique=True)  # type: ignore
    email = Column(String(120), nullable=False, unique=True)  # type: ignore
    first_name = Column(String(64))  # type: ignore
    last_name = Column(String(64))  # type: ignore
    avatar_url = Column(String(256))  # type: ignore
    created_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow)  # type: ignore
    favorite_composers = db.relationship('Composer', secondary=composer_favorites, lazy='subquery',
                                         backref=db.backref('users', lazy=True))
    favorite_performers = db.relationship('Performer', secondary=performer_favorites, lazy='subquery',
                                          backref=db.backref('users', lazy=True))

    def __init__(
        self,
        oauth_provider: Column[str],
        oauth_id: Column[str],
        email: Column[str],
        first_name: Column[str],
        last_name: Column[str],
        avatar_url: Column[str],
        created_at: Column[datetime],
        favorite_composers: List,  # type: ignore
        favorite_performers: List,  # type: ignore
    ) -> None:
        self.oauth_provider = oauth_provider
        self.oauth_id = oauth_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.avatar_url = avatar_url
        self.created_at = created_at
        self.favorite_composers = favorite_composers
        self.favorite_performers = favorite_performers

    def insert(self) -> None:
        print(f"Here is SELF {self}")
        db.session.add(self)
        db.session.commit()

    def update(self) -> None:
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def format(self) -> dict:
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'avatar_url': self.avatar_url,
            'favorite_performers': self.favorite_performers,
            'favorite_composers': self.favorite_composers
        }

    def __repr__(self) -> str:
        return '<User {}>'.format(self.email)
