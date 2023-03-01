# flake8 : noqa
from __future__ import annotations
from . import db
from sqlalchemy import Column, String, Integer, Date, ForeignKey
from .composer import Composer
from .style import Style
from typing import Optional



class Composition(db.Model):  # type: ignore
    __tablename__ = 'compositions'
    id = Column(Integer, primary_key=True)
    name = Column(String(300))
    image = Column(db.LargeBinary)
    release_date = Column(Date)
    composer_id = Column(Integer, ForeignKey('composers.id'))
    style_id = Column(Integer, ForeignKey('styles.id'))

    def __init__(
        self,
        name: Column[str],
        release_date: Date,
        composer_id: int,
        style_id: Optional[int],
        image: Optional[bytes]

    ) -> None:
        self.name = name
        self.release_date = release_date
        self.composer_id = composer_id
        self.style_id = style_id
        self.image = image

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
            'release_Date': self.release_Date,
            'composer': Composer.query.get(self.composer_id).one_or_none(),
            'style': Style.query.get(self.style_id).one_or_none(),
            'image': self.image
        }

    def __repr__(self) -> str:
        return f'<Composition {self.name}>'
