from . import db
from sqlalchemy import Column, String, Integer, DateTime, Date, ForeignKey
# from .performer import Performer


class Recording(db.Model): # type: ignore
    __tablename__ = 'recordings'
    id = Column(Integer, primary_key=True)
    name = Column(String(300))
    released_date = Column(Date)
    performer_id = Column(Integer, ForeignKey('performers.id'))
    style_id = Column(Integer, ForeignKey('styles.id'))
    image = Column(db.LargeBinary)
        
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def __repr__(self):
        return f'<Recording {self.name}>'
    
       # def __init__(
    #     self, 
    #     name: Column[str], 
    #     released_date: Column[int], 
    #     performer_id: Column[int],
    #     style_id: Column[int],
    #     image: Optional[bytes]
    # ):
    #     self.name = name
    #     self.released_date = released_date
    #     self.performer_id = performer_id
    #     self.style_id = style_id
    #     self.image = image