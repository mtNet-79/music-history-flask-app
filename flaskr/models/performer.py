# flake8: noqa
from . import db
from sqlalchemy import Column, String, Integer, DateTime, Date
from . import composer_performer, performer_style, performer_title, performer_contemporaries, performer_nationalities
# from sqlalchemy_utils import IntRangeType
from datetime import datetime, date
# from typing import Optional, List


class Performer(db.Model):  # type: ignore
    """
    A class representing a music performer, which is a subclass of db.Model.

    Attributes:
        id (int): The primary key of the performer.
        name (str): The name of the performer.
        year_born (date): The birth year of the performer.
        year_deceased (date): The death year of the performer.
        bio (str): The biography of the performer.
        image (bytes): The image of the performer.
        composers (list): The list of composers associated with the performer.
        contemporaries (list): The list of contemporaries associated with the performer.
        nationalities (list): The list of nationalities associated with the performer.
        titles (list): The list of titles associated with the performer.
        styles (list): The list of styles associated with the performer.
        recordings (list): The list of recordings associated with the performer.
        rating (int): The rating of the performer.
        timestamp (datetime): The timestamp when the performer was last updated.
    """
    
    __tablename__ = 'performers'
    id = Column(Integer, primary_key=True)  # type: ignore
    name = Column(String(120))  # type: ignore
    year_born = Column(Date)  # type: ignore
    year_deceased = Column(Date)  # type: ignore
    bio = Column(String(1000))
    image = Column(db.LargeBinary) 
    composers = db.relationship(
        'Composer', secondary=composer_performer, back_populates='performers')  # type: ignore
    contemporaries = db.relationship(
        "Performer",
        secondary=performer_contemporaries,  # type: ignore
        primaryjoin=(id == performer_contemporaries.c.performer_id),  # type: ignore
        secondaryjoin=(id == performer_contemporaries.c.contemporary_id),  # type: ignore
        backref=db.backref('contemporaries_of', lazy='dynamic'),
        lazy='dynamic'
    )  # type: ignore
    nationalities = db.relationship('Nation', secondary=performer_nationalities, back_populates='performers')  # type: ignore
    titles = db.relationship( 
        "Title", secondary=performer_title, back_populates='performers')  # type: ignore
    styles = db.relationship(
        "Style", secondary=performer_style, back_populates='performers')  # type: ignore
    recordings = db.relationship(
        'Recording', backref=db.backref('performers', lazy=True))  # type: ignore
    rating = Column(Integer)  # type: ignore
    timestamp = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )  # type: ignore
    
    def insert(self) -> None:
        db.session.add(self)
        db.session.commit()

    def update(self) -> None:
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self) -> str:
        return f'<Performer {self.name}>'

    # def super().__init__(
    #     self,
    #     name: Column[str],
    #     year_born: Column[date],
    #     nationalities: Column[List[object]],
    #     year_deceased: Column[date] = None,  # type: ignore
    #     bio: Optional[str], # type: ignore,
    #     image: Optional[bytes]
    #     composers: Optional[Column[List[object]]] = None,  # type: ignore
    #     titles: Optional[Column[List[object]]] = None,  # type: ignore
    #     styles: Optional[Column[List[object]]] = None,  # type: ignore
    #     recordings: Optional[Column[Optional[List[object]]]] = None,  # type: ignore
    #     rating: Optional[Column[int]] = None  # type: ignore
    # ) -> None:
    #     self.name = name
    #     self.year_born = year_born
    #     self.year_deceased = year_deceased
    #     self.nationalities = nationalities
    #     self.bio = bio
    #     self.image = image
    #     self.composers = composers or []  # type: ignore
    #     self.styles = styles or []  # type: ignore
    #     self.titles = titles or []  # type: ignore
    #     self.recordings = recordings or []  # type: ignore
    #     self.rating = rating  # type: ignore

    

    # def format(self) -> dict:
    #     return {
    #         'id': self.id,
    #         'name': self.name,
    #         'years': [self.year_born, self.year_deceased],
    #         'composers': self.composers,
    #         'nationalities': self.nationalities,
    #         'styles': self.styles,
    #         'titles': [t.name for t in self.titles], # type: ignore
    #         'recordings': self.recordings,
    #         'contemporaries': [c.to_dict() for c in self.contemporaries.all()]
    #     }

    
