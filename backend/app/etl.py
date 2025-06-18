import os
import pandas as pd
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from app.database import SessionLocal, engine
from app.models import Country, FormerName, Match, Player, Goal, Shootout

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

TEAM_ALIASES = {
    "england": "United Kingdom",
    "wales": "United Kingdom",
    "china pr": "China",
    "dr congo": "Democratic Republic of the Congo",
    "republic of ireland": "Ireland",
    "german dr": "East Germany",
    "zaïre": "Democratic Republic of the Congo",
    "viet nam": "Vietnam",
    "ivory coast": "Cote d'Ivoire",
    "côte d’ivoire": "Cote d'Ivoire",
    "palestine": "Palestinian Territory",
    "north macedonia": "Macedonia",
    "iran": "Iran",
    "curacao": "Curacao",
    "czech republic": "Czechia",
    "reunion": "Réunion",
    "são tomé and príncipe": "Sao Tome and Principe",
    "timor-leste": "Timor Leste"
}

former_to_current = {}

def map_team_name(name):
    if not isinstance(name, str):
        return None
    key = name.strip().casefold()
    if key in TEAM_ALIASES:
        return TEAM_ALIASES[key]
    if key in former_to_current:
        return former_to_current[key]
    return name.strip()

def load_countries(path):
    session = SessionLocal()
    try:
        try:
            df = pd.read_csv(path, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(path, encoding="ISO-8859-1")

        required_columns = ['Display_Name', 'Region', 'Sub-Region', 'Status', 'Developed', 'Population', 'Area']
        for col in required_columns:
            if col not in df.columns:
                logging.error(f"Missing column '{col}' in countries.csv")
                return

        inserted, skipped = 0, 0
        for _, row in df.iterrows():
            name = str(row["Display_Name"]).strip()
            if not name:
                continue

            exists = session.query(Country).filter(Country.name == name).first()
            if exists:
                logging.info(f"Skipped duplicate no info: {name}")
                skipped += 1
                continue

            country = Country(
                name=name,
                region=row["Region"] if pd.notna(row["Region"]) else None,
                continent=row["Sub-Region"] if pd.notna(row["Sub-Region"]) else None,
                status=row["Status"] if pd.notna(row["Status"]) else None,
                developed=row["Developed"] if pd.notna(row["Developed"]) else None,
                population=int(row["Population"]) if pd.notna(row["Population"]) else None,
                area_sq_km=int(row["Area"]) if pd.notna(row["Area"]) else None,
            )

            session.add(country)
            inserted += 1

        session.commit()
        logging.info(f"Countries load complete. Insert: {inserted}, Skipped: {skipped}")
    except Exception as e:
        logging.error(f"Error loading countries: {e}")
    finally:
        session.close()

def load_former_names(path):
    session = SessionLocal()
    try:
        df = pd.read_csv(path)
        inserted = 0
        for _, row in df.iterrows():
            current_name = row["current"].strip()
            former = row["former"].strip()
            current_country = session.query(Country).filter_by(name=current_name).first()
            if not current_country:
                logging.warning(f"Skipped former name '{former}' → '{current_name}': current country not found")
                continue
            former_to_current[former.casefold()] = current_name
            fn = FormerName(
                current_name=current_name,
                former_name=former,
                start_date=row["start_date"],
                end_date=row["end_date"],
                country_id=current_country.id
            )
            session.add(fn)
            inserted += 1
        session.commit()
        logging.info(f" Former names loaded: {inserted} entries inserted.")
    except Exception as e:
        logging.error(f"Error loading former names: {e}")
    finally:
        session.close()

def load_matches(path):
    session = SessionLocal()
    df = pd.read_csv(path)
    skipped = 0
    for _, row in df.iterrows():
        home_name = map_team_name(row["home_team"])
        away_name = map_team_name(row["away_team"])
        home = session.query(Country).filter_by(name=home_name).first()
        away = session.query(Country).filter_by(name=away_name).first()
        host = session.query(Country).filter_by(name=row["country"]).first()
        if not home or not away:
            skipped += 1
            continue
        match = Match(
            match_date=pd.to_datetime(row["date"], errors="coerce"),
            home_team_id=home.id,
            away_team_id=away.id,
            home_score=row["home_score"],
            away_score=row["away_score"],
            tournament=row["tournament"],
            city=row["city"],
            country_id=host.id if host else None,
            neutral=row["neutral"]
        )
        session.add(match)
    session.commit()
    session.close()
    logging.info(f"Matches loaded with {skipped} skipped due to unknown names")

def load_goalscorers(path):
    session = SessionLocal()
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)
    inserted, skipped = 0, 0
    for _, row in df.iterrows():
        if pd.isna(row["date"]):
            skipped += 1
            continue
        home = map_team_name(row["home_team"])
        away = map_team_name(row["away_team"])
        team = map_team_name(row["team"])
        home_team = session.query(Country).filter_by(name=home).first()
        away_team = session.query(Country).filter_by(name=away).first()
        team_country = session.query(Country).filter_by(name=team).first()
        if not home_team or not away_team or not team_country:
            skipped += 1
            continue
        match = session.query(Match).filter(
            Match.match_date == row["date"],
            Match.home_team_id == home_team.id,
            Match.away_team_id == away_team.id
        ).first()
        if not match:
            skipped += 1
            continue
        scorer = str(row["scorer"]).strip()
        if not scorer:
            skipped += 1
            continue
        player = session.query(Player).filter_by(name=scorer, country_id=team_country.id).first()
        if not player:
            player = Player(name=scorer, country_id=team_country.id)
            session.add(player)
            session.flush()
        goal = Goal(
            match_id=match.id,
            player_id=player.id,
            team_id=team_country.id,
            own_goal=row["own_goal"],
            penalty=row["penalty"]
        )
        session.add(goal)
        inserted += 1
    try:
        session.commit()
    except Exception as e:
        logging.error(f" Error committing goalscorers: {e}")
    session.close()
    logging.info(f"Goalscorers loaded successfully. Insert: {inserted}, Skipped: {skipped}")

def load_shootouts(path):
    session = SessionLocal()
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"], errors="coerce", format="%Y-%m-%d")
    inserted, skipped = 0, 0
    for _, row in df.iterrows():
        home = map_team_name(row["home_team"])
        away = map_team_name(row["away_team"])
        winner = map_team_name(row["winner"])
        first = map_team_name(row["first_shooter"])
        home_team = session.query(Country).filter_by(name=home).first()
        away_team = session.query(Country).filter_by(name=away).first()
        winner_team = session.query(Country).filter_by(name=winner).first()
        first_team = session.query(Country).filter_by(name=first).first()

        if not home_team or not away_team or not winner_team:
            skipped += 1
            continue

        match = session.query(Match).filter(
            Match.match_date == row["date"],
            Match.home_team_id == home_team.id,
            Match.away_team_id == away_team.id
        ).first()

        if not match:
            skipped += 1
            continue

        shootout = Shootout(
            match_date=row["date"],
            home_team_id=home_team.id,
            away_team_id=away_team.id,
            winner_id=winner_team.id,
            first_shooter_id=first_team.id if first_team else None,
            match_id=match.id
        )
        session.add(shootout)
        inserted += 1

    session.commit()
    session.close()
    logging.info(f"✅ Shootouts loaded successfully. Inserted: {inserted}, Skipped: {skipped}")

import os
base_path = os.path.join(os.path.dirname(__file__), "..", "datas")
base_path = os.path.abspath(base_path)

load_countries(f"{base_path}/countries.csv")
load_former_names(f"{base_path}/former_names.csv")
load_matches(f"{base_path}/results.csv")
load_goalscorers(f"{base_path}/goalscorers.csv")
load_shootouts(f"{base_path}/shootouts.csv")
