from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id"), unique=True, nullable=False
    )
    passport_country = Column(String, nullable=True)
    monthly_income = Column(Float, nullable=True)
    income_type = Column(String, nullable=True)
    matches_json = Column(Text, nullable=True)
    checklist_json = Column(Text, nullable=True)

    user = relationship("User", back_populates="profile")
