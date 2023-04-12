from config.database import Base
from sqlalchemy import Column, Integer, String, Float

class Movie(Base):

    __tablename__ = "movies"

    id = Column(Integer, primary_key = True)
    title = Column(String)
    overview = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String)
    
    def update(self, values: dict):
        for key, value in values.items():
            setattr(self, key, value)