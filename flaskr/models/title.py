# flake8: noqa
from . import db, Composer, Performer
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from typing import Optional, List


class Title(db.Model): # type: ignore
    __tablename__ = 'titles'
    id = Column(Integer, primary_key=True) # type: ignore
    name = Column(String(250)) # type: ignore
    composers = db.relationship(
        'Composer', secondary='composer_title', back_populates='titles') # type: ignore
    performers = db.relationship(
        'Performer', secondary='performer_title', back_populates='titles') # type: ignore
    
    def __init__(
        self, 
        name: Column[str], 
        composers: Column[Optional[List["Composer"]]] = None, # type: ignore
        performers: Column[Optional[List["Performer"]]] = None # type: ignore
    ) -> None:
        self.name = name
        self.composers = composers or [] # type: ignore
        self.performers = performers or [] # type: ignore
        
    def insert(self) -> None:
        db.session.add(self)
        db.session.commit()

    def update(self) -> None:
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()
        
    def __repr__(self) -> str:
        return f'<Title {self.name}>'