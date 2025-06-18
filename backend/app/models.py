from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    iso_code = Column(String(3))
    continent = Column(String(50))
    region = Column(String(50))
    status = Column(String(50))
    developed = Column(String(15))
    population = Column(Integer)
    area_sq_km = Column(Integer)

    home_matches = relationship("Match", foreign_keys="Match.home_team_id", back_populates="home_team")
    away_matches = relationship("Match", foreign_keys="Match.away_team_id", back_populates="away_team")
    players = relationship("Player", back_populates="country")
    former_names = relationship("FormerName", back_populates="country")  # NEW


class FormerName(Base):
    __tablename__ = "former_names"

    id = Column(Integer, primary_key=True, index=True)
    current_name = Column(String(100), nullable=False)
    former_name = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    country_id = Column(Integer, ForeignKey("countries.id"))  # NEW
    country = relationship("Country", back_populates="former_names")  # NEW


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    match_date = Column(Date, nullable=False)

    home_team_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    away_team_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    home_score = Column(Integer)
    away_score = Column(Integer)

    tournament = Column(String(100))
    city = Column(String(100))
    country_id = Column(Integer, ForeignKey("countries.id"))
    neutral = Column(Boolean, default=False)

    home_team = relationship("Country", foreign_keys=[home_team_id], back_populates="home_matches")
    away_team = relationship("Country", foreign_keys=[away_team_id], back_populates="away_matches")
    host_country = relationship("Country", foreign_keys=[country_id])

    goals = relationship("Goal", back_populates="match")
    shootout = relationship("Shootout", back_populates="match", uselist=False)  # NEW


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)

    country = relationship("Country", back_populates="players")
    goals = relationship("Goal", back_populates="player")  # ✅ fixed from "players"


class Goal(Base):
    __tablename__ = "goalscorers"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    minute = Column(Integer, nullable=True)
    own_goal = Column(Boolean, default=False)
    penalty = Column(Boolean, default=False)

    match = relationship("Match", back_populates="goals")
    player = relationship("Player", back_populates="goals")  # ✅ fixed from "players"
    team = relationship("Country")


class Shootout(Base):
    __tablename__ = "shootouts"

    id = Column(Integer, primary_key=True, index=True)
    match_date = Column(Date, nullable=False)

    home_team_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    away_team_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    winner_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    first_shooter_id = Column(Integer, ForeignKey("countries.id"), nullable=True)

    match_id = Column(Integer, ForeignKey("matches.id"))  # NEW
    match = relationship("Match", back_populates="shootout")  # NEW

    home_team = relationship("Country", foreign_keys=[home_team_id])
    away_team = relationship("Country", foreign_keys=[away_team_id])
    winner = relationship("Country", foreign_keys=[winner_id])
    first_shooter = relationship("Country", foreign_keys=[first_shooter_id])
