from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from models.Connection import Base


class FindingRecommendationModel(Base):
    __tablename__ = 'findings_recommendations'

    id = Column(Integer, primary_key=True)
    finding = Column(Text)
    recommendation = Column(Text)
    cyc_id = Column(Integer, ForeignKey('country_years_criteria.id'))

    country_year_criteria = relationship('CountryYearCriteriaModel', back_populates='findings_recommendations')
