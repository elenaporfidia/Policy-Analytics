from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from models.Connection import Base


class CountryYearCriteriaModel(Base):
    __tablename__ = 'country_years_criteria'

    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('countries.id'))
    year_id = Column(Integer, ForeignKey('years.id'))
    criteria_id = Column(Integer, ForeignKey('criteria.id'))

    criteria = relationship('CriteriaModel', back_populates='country_years_criteria')
    year = relationship('YearModel', back_populates='criteria')
    country = relationship('CountryModel', back_populates='years')
    findings_recommendations = relationship('FindingRecommendationModel', back_populates='country_year_criteria')
