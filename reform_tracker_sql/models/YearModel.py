from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from models.Connection import Base


class YearModel(Base):
    __tablename__ = "years"

    id = Column(Integer, primary_key=True)
    name = Column(Text)

    criteria = relationship("CountryYearCriteriaModel", back_populates='year')
