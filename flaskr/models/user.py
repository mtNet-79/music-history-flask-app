# flake8: noqa
from typing import List, Optional
from datetime import datetime
from . import db
from sqlalchemy import Column, String, Integer, DateTime
from . import performer_favorites, composer_favorites, Composer, Performer


class User(db.Model):  # type: ignore
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)  # type: ignore
    oauth_provider = Column(String(64), nullable=False)  # type: ignore
    oauth_id = Column(String(64), nullable=False, unique=True)  # type: ignore
    email = Column(String(120), nullable=False, unique=True)  # type: ignore
    first_name = Column(String(64))  # type: ignore
    last_name = Column(String(64))  # type: ignore
    user_name = Column(String(120)) # type: ignore
    avatar_url = Column(String(256))  # type: ignore
    role = Column(String(64))
    created_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow)  # type: ignore
    favorite_composers = db.relationship('Composer', secondary=composer_favorites, lazy='subquery',
                                         backref=db.backref('users', lazy=True))
    favorite_performers = db.relationship('Performer', secondary=performer_favorites, lazy='subquery',
                                          backref=db.backref('users', lazy=True))

    def __init__(
        self,
        oauth_provider: str,
        oauth_id: str,
        email: str,
        first_name: str,
        last_name: str,
        user_name: str,
        avatar_url: Optional[str] = None,
        role: Optional[str] = None,
        created_at: Optional[datetime] = None,
        favorite_composers: Optional[List[Composer]] = None,
        favorite_performers: Optional[List[Performer]] = None,
    ) -> None:
        self.oauth_provider = oauth_provider
        self.oauth_id = oauth_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.avatar_url = avatar_url
        self.role = role
        self.created_at = created_at if created_at is not None else datetime.utcnow()
        self.favorite_composers = favorite_composers if favorite_composers is not None else []
        self.favorite_performers = favorite_performers if favorite_performers is not None else []
        
        
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
            'oauth_provider': self.oauth_provider,
            'oauth_id': self.oauth_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'user name': self.user_name,
            'email': self.email,
            'avatar_url': self.avatar_url,
            'created_at': self.created_at,
            'role': self.role,
            'favorite_performers': self.favorite_performers,
            'favorite_composers': self.favorite_composers
        }

    def __repr__(self) -> str:
        return '<User {}>'.format(self.email)
