# flake8: noqa
from typing import Optional, List
from datetime import datetime, date
from . import db
from sqlalchemy import Column, String, Integer, DateTime, Date
from . import (performer_nationalities, composer_nationalities)

class Nation(db.Model):  # type: ignore
    __tablename__ = 'nations'
    id = Column(Integer, primary_key=True)  # type: ignore
    name = Column(String(125), nullable=False)  # type: ignore
    composers = db.relationship('Composer', secondary=composer_nationalities, back_populates='nations')
    performers = db.relationship('Performer', secondary=performer_nationalities, back_populates='nations')

    def __init__(
        self,
        name: Column[str],
        composers: Optional[List["Composer"]] = [],  # type: ignore
        performers: Optional[List["Performer"]] = [],  # type: ignore
    ) -> None:
        self.name = name
        self.composers = composers
        self.performers = performers

    def insert(self) -> None:
        db.session.add(self)
        db.session.commit()

    def update(self) -> None:
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()
   

    def __repr__(self):
        return f'<Nation(id={self.id}, name="{self.name}")>'