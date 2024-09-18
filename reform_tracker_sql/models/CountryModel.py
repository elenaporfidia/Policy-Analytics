from sqlalchemy import Integer, Column, Text
from sqlalchemy.orm import relationship

from models.Connection import Base

class CountryModel(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    name = Column(Text)

    years = relationship("CountryYearCriteriaModel", back_populates='country')
