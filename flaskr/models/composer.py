from __future__ import annotations
from . import db
from sqlalchemy import Column, String, Integer, DateTime, Date, ForeignKey
from datetime import datetime, date
from typing import Optional, List, Any
from . import (composer_contemporaries, composer_performer,
               composer_style, composer_title, composer_nationalities)




class Composer(db.Model):  # type: ignore
    """
    A class representing a music composer, which is a subclass of db.Model.

    Attributes:
        id (int): The primary key of the composer.
        name (str): The name of the composer.
        bio (str): The biography of the composer.
        image (bytes): The image of the composer.
        performers (list): The list of performers associated with the composer.
        titles (list): The list of titles associated with the composer.
        styles (list): The list of styles associated with the composer.
        recordings (list): The list of recordings associated with the composer.
        rating (int): The rating of the composer.
        timestamp (datetime): The timestamp when the composer was last updated.
    """ 
    __tablename__ = 'composers'

    id = Column(Integer, primary_key=True)  # type: ignore
    name = Column(String(120))  # type: ignore
    year_born = Column(Date)  # type: ignore
    year_deceased = Column(Date)  # type: ignore
    bio = Column(String(1000))
    image = Column(db.LargeBinary) 
    performers = db.relationship(
        'Performer', secondary=composer_performer, back_populates='composers')  # type: ignore
    titles = db.relationship(
        "Title", secondary=composer_title, back_populates='composers')  # type: ignore
    styles = db.relationship(
        'Style', secondary=composer_style, back_populates='composers')  # type: ignore
     # Define a many-to-many relationship with the Nation model
    nationalities = db.relationship('Nation', secondary=composer_nationalities, 
                                    back_populates='composers') # type: ignore
    period_id = Column(Integer, ForeignKey('periods.id'))  # type: ignore
    compostitions = db.relationship(
        'Composition', backref=db.backref('composer_compositions', lazy=True))  # type: ignore
    contemporaries = db.relationship(
        'Composer',
        secondary=composer_contemporaries,
        primaryjoin=(id == composer_contemporaries.c.composer_id),
        secondaryjoin=(id == composer_contemporaries.c.contemporary_id),
        backref=db.backref('contemporaries_of', lazy='dynamic'),
        lazy='dynamic'
    )  # type: ignore
    timestamp = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )  # type: ignore

    def __init__(
        self,
        name: Column[str],
        year_born: Column[date],
        nationalities: Column[List[Any]],
        year_deceased: Column[date],
        bio: Optional[str],
        image: Optional[bytes],
        period_id: Column[Optional[int]] = None,  # type: ignore
        performers: Column[Optional[List[int]]] = None,  # type: ignore
        titles: Column[Optional[list[Any]]] = None,  # type: ignore
        styles: Column[Optional[list[Any]]] = None,  # type: ignore
        compostitions: Column[Optional[list[Any]]] = None,  # type: ignore
        contemporaries: Column[Optional[List[Any]]] = None  # type: ignore
    ) -> None:
        self.name = name
        self.year_born = year_born
        self.year_deceased = year_deceased
        self.bio = bio
        self.image = image
        self.nationalities = nationalities
        self.period_id = period_id
        self.performers = performers or [] # type: ignore
        self.styles = styles or [] # type: ignore
        self.titles = titles or [] # type: ignore
        self.compostitions = compostitions or [] # type: ignore
        self.contemporaries = contemporaries or [] # type: ignore

    def insert(self) -> None:
        db.session.add(self)
        db.session.commit()

    def update(self) -> None:
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    # period = Period.query.get(period_id)

    def format(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'years': [self.year_born, self.year_deceased],
            'bio': self.bio,
            'image': self.image,
            'period_id': self.period_id,
            'performers': self.performers,
            'nationalities': self.nationalities,
            'styles': self.styles,
            'titles': self.titles,
            'compostitions': self.compostitions,
            'contemporaries': [c.to_dict() for c in self.contemporaries.all()]
        }

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"{self.name!r}, {self.year_born!r} - {self.year_deceased!r}"
            f")"
        )
# def get_composers():
#     composers = Composer.query.all()
#     all_composers: List["Composer"] = []
#     for composer in composers:
#         all_composers.append((str(composer.id), composer.name))

#     all_composers.sort(key=lambda x: x[1], reverse=True)
#     return all_composers
