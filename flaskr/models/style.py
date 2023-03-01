from . import db, Composer, Performer
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from typing import Optional, List

class Style(db.Model):  # type: ignore
    __tablename__ = 'styles'
    id = Column(Integer, primary_key=True)  # type: ignore
    name = Column(String(250))  # type: ignore
    composers = db.relationship(
        'Composer', secondary='composer_style', back_populates='styles')  # type: ignore
    performers = db.relationship(
        'Performer', secondary='performer_style', back_populates='styles')  # type: ignore
    
    def __init__(
        self, 
        name: Column[str], # type: ignore
        composers: Column[Optional[List["Composer"]]] = None,   # type: ignore
        performers: Column[Optional[List["Performer"]]] = None  # type: ignore
    ) -> None:
        self.name = name, # type: ignore
        self.composers = composers or []  # type: ignore
        self.performers = performers or []  # type: ignore
        
    def insert(self) -> None:
        db.session.add(self)
        db.session.commit()

    def update(self) -> None:
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()
        
    def __repr__(self) -> str:
        return f'<Style {self.name}>'