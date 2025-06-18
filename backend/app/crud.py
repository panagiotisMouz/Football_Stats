from sqlalchemy.orm import Session
from sqlalchemy import func, or_, desc, case
from app.models import Country, Match, Player, Goal, Shootout, FormerName

# === Countries ===
def get_countries(db: Session):
    return db.query(Country).all()

def get_country_by_id(db: Session, country_id: int):
    return db.query(Country).filter(Country.id == country_id).first()

def get_country_by_name(db: Session, name: str):
    return db.query(Country).filter(Country.name == name).first()

def add_country(db: Session, data: dict):
    country = Country(**data)
    db.add(country)
    db.commit()
    db.refresh(country)
    return country

def get_country_profile(db: Session, country_id: int):
    country = get_country_by_id(db, country_id)
    if not country:
        return None

    stats = db.query(
        func.count(Match.id).label("matches_played"),
        func.sum(case([
            ((Match.home_team_id == country_id) & (Match.home_score > Match.away_score), 1),
            ((Match.away_team_id == country_id) & (Match.away_score > Match.home_score), 1)
        ], else_=0)).label("wins"),
        func.sum(case([
            ((Match.home_team_id == country_id) & (Match.home_score < Match.away_score), 1),
            ((Match.away_team_id == country_id) & (Match.away_score < Match.home_score), 1)
        ], else_=0)).label("losses"),
        func.sum(case([(Match.home_score == Match.away_score, 1)], else_=0)).label("draws")
    ).filter(
        or_(Match.home_team_id == country_id, Match.away_team_id == country_id)
    ).first()

    first_year = db.query(func.min(Match.match_date)).filter(
        or_(Match.home_team_id == country_id, Match.away_team_id == country_id)
    ).scalar()

    last_year = db.query(func.max(Match.match_date)).filter(
        or_(Match.home_team_id == country_id, Match.away_team_id == country_id)
    ).scalar()

    yearly = db.query(
        func.year(Match.match_date).label("year"),
        func.sum(case([
            ((Match.home_team_id == country_id) & (Match.home_score > Match.away_score), 1),
            ((Match.away_team_id == country_id) & (Match.away_score > Match.home_score), 1)
        ], else_=0)).label("wins"),
        func.sum(case([
            ((Match.home_team_id == country_id) & (Match.home_score < Match.away_score), 1),
            ((Match.away_team_id == country_id) & (Match.away_score < Match.home_score), 1)
        ], else_=0)).label("losses"),
        func.sum(case([(Match.home_score == Match.away_score, 1)], else_=0)).label("draws"),
        func.count(Match.id).label("matches")
    ).filter(
        or_(Match.home_team_id == country_id, Match.away_team_id == country_id)
    ).group_by(func.year(Match.match_date)).order_by(func.year(Match.match_date)).all()

    yearly_stats = [
        dict(year=int(row.year), wins=int(row.wins), losses=int(row.losses), draws=int(row.draws), matches=int(row.matches))
        for row in yearly
    ]

    return {
        "country": {
            "id": country.id,
            "name": country.name,
            "region": country.region,
            "population": country.population
        },
        "summary": {
            "matches_played": int(stats.matches_played),
            "wins": int(stats.wins),
            "losses": int(stats.losses),
            "draws": int(stats.draws)
        },
        "active_years": {
            "from": first_year.year if first_year else None,
            "to": last_year.year if last_year else None
        },
        "yearly_stats": yearly_stats
    }


# === Former Names ===
def get_former_names(db: Session):
    return db.query(FormerName).all()

def get_former_names_for_country(db: Session, country_id: int):
    return db.query(FormerName).filter(FormerName.country_id == country_id).all()

# === Matches ===
def get_matches(db: Session):
    return db.query(Match).all()

def get_match_by_id(db: Session, match_id: int):
    return db.query(Match).filter(Match.id == match_id).first()

def get_matches_for_country(db: Session, country_id: int):
    return db.query(Match).filter(
        (Match.home_team_id == country_id) | (Match.away_team_id == country_id)
    ).all()

def get_matches_by_year(db: Session, year: int):
    return db.query(Match).filter(func.year(Match.match_date) == year).all()

def add_match(db: Session, data: dict):
    match = Match(**data)
    db.add(match)
    db.commit()
    db.refresh(match)
    return match

# === Players ===
def get_players(db: Session):
    return db.query(Player).all()

def get_player_by_id(db: Session, player_id: int):
    return db.query(Player).filter(Player.id == player_id).first()

def get_players_by_country(db: Session, country_id: int):
    return db.query(Player).filter(Player.country_id == country_id).all()

def add_player(db: Session, data: dict):
    player = Player(**data)
    db.add(player)
    db.commit()
    db.refresh(player)
    return player

# === Goals ===
def get_goals(db: Session):
    return db.query(Goal).all()

def get_goals_by_match(db: Session, match_id: int):
    return db.query(Goal).filter(Goal.match_id == match_id).all()

def get_goals_by_player(db: Session, player_id: int):
    return db.query(Goal).filter(Goal.player_id == player_id).all()

def add_goal(db: Session, data: dict):
    goal = Goal(**data)
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal

# === Shootouts ===
def get_shootout_by_match(db: Session, match_id: int):
    return db.query(Shootout).filter(Shootout.match_id == match_id).first()

def add_shootout(db: Session, data: dict):
    shootout = Shootout(**data)
    db.add(shootout)
    db.commit()
    db.refresh(shootout)
    return shootout

# === Scoring Analytics ===
def get_top_scorers(db: Session, limit: int = 10):
    return db.query(
        Player.id,
        Player.name,
        Country.name.label("country_name"),
        func.count(Goal.id).label("total_goals")
    ).join(Goal, Goal.player_id == Player.id)\
     .join(Country, Player.country_id == Country.id)\
     .group_by(Player.id)\
     .order_by(desc("total_goals"))\
     .limit(limit).all()

