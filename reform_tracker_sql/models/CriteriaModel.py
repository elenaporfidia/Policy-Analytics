from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from models.Connection import Base


class CriteriaModel(Base):
    __tablename__ = 'criteria'

    id = Column(Integer, primary_key=True)
    title = Column(Text)

    country_years_criteria = relationship("CountryYearCriteriaModel", back_populates="criteria")

