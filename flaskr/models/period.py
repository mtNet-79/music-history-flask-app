from . import db
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy_utils import IntRangeType  # type: ignore
from typing import Optional, List
from .composer import Composer


class Period(db.Model):  # type: ignore
    __tablename__ = 'periods'
    id = Column(Integer, primary_key=True)  # type: ignore
    name = Column(String(120))  # type: ignore
    # years = Column(IntRangeType) # type: ignore
    dates = Column(String(25))
    composers = db.relationship(
        'Composer', backref=db.backref('periods', lazy=True))  # type: ignore

    def __init__(
        self,
        name: str,
        dates: str,
        composers: Optional[List["Composer"]] = None
    ):
        self.name = name
        self.dates = dates
        self.composers = composers or [] # type: ignore

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Period {self.name}>'
