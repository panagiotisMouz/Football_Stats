from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from httptools.parser.parser import Optional
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ..database import get_db
from .. import crud, models
from ..models import Country,Match
from sqlalchemy import or_

router = APIRouter(
    prefix="/countries",
    tags=["Countries"]
)

@router.get("/", response_model=List[dict])
def get_countries(db: Session = Depends(get_db)):
    countries = crud.get_countries(db)
    return [
        {
            "id": c.id,
            "name": c.name,
            "region": c.region,
            "population": c.population
        }
        for c in countries
    ]

@router.get("/{country_id}", response_model=dict)
def get_country(country_id: int, db: Session = Depends(get_db)):
    country = crud.get_country_by_id(db, country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return {
        "id": country.id,
        "name": country.name,
        "region": country.region,
        "iso_code": country.iso_code,
        "population": country.population,
        "continent": country.continent,
        "area_sq_km": country.area_sq_km
    }


@router.get("/{country_id}/profile")
def get_country_profile(
    country_id: int,
    from_year: Optional[int] = None,
    to_year: Optional[int] = None,
    db: Session = Depends(get_db)
):
    country = db.query(Country).filter(Country.id == country_id).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    matches = db.query(Match).filter(
        or_(
            Match.home_team_id == country_id,
            Match.away_team_id == country_id
        )
    )

    if from_year:
        matches = matches.filter(Match.match_date >= date(from_year, 1, 1))
    if to_year:
        matches = matches.filter(Match.match_date <= date(to_year, 12, 31))

    matches = matches.all()
    total_matches = len(matches)
    wins = 0
    goals = 0
    points = 0

    for match in matches:
        is_home = match.home_team_id == country_id
        scored = match.home_score if is_home else match.away_score
        conceded = match.away_score if is_home else match.home_score
        goals += scored
        if scored > conceded:
            wins += 1
            points += 3
        elif scored == conceded:
            points += 1

    avg_goals = goals / total_matches if total_matches else 0

    profile = {
        "country": country.name,
        "region": country.region,
        "continent": country.continent,  # ή άλλαξέ το σε 'continent' αν προτιμάς
        "population": country.population,
        "area": country.area_sq_km,
        "stats": {
            "matches": total_matches,
            "wins": wins,
            "goals": goals,
            "points": points,
            "avg_goals": round(avg_goals, 2)
        }


    }
    wins_by_year = {}
    match_list = []

    for match in matches:
        year = match.match_date.year
        is_home = match.home_team_id == country_id
        scored = match.home_score if is_home else match.away_score
        conceded = match.away_score if is_home else match.home_score

        match_list.append({
            "date": match.match_date.strftime("%Y-%m-%d"),
            "opponent": match.away_team.name if is_home else match.home_team.name,
            "venue": "Home" if is_home else "Away",
            "score": f"{scored}-{conceded}",
        })

        if scored > conceded:
            wins_by_year[year] = wins_by_year.get(year, 0) + 1

    # Convert dict to list of dicts for frontend
    wins_per_year = [{"year": y, "wins": w} for y, w in sorted(wins_by_year.items())]

    # Include in profile
    profile["wins_per_year"] = wins_per_year
    profile["matches"] = match_list

    return profile

@router.get("/{country_id}/matches", response_model=List[Dict[str, Any]])
def get_country_matches(country_id: int, db: Session = Depends(get_db)):

    country = db.query(models.Country).filter_by(id=country_id).first()
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")

    matches = crud.get_matches_for_country(db, country_id=country_id)
    result = []

    for match in matches:
        opponent_id = match.away_team_id if match.home_team_id == country_id else match.home_team_id
        opponent = db.query(models.Country).filter_by(id=opponent_id).first()
        result.append({
            "match_date": match.match_date,
            "opponent": opponent.name if opponent else "Unknown",
            "score": f"{match.home_score}-{match.away_score}",
            "home": match.home_team_id == country_id,
            "tournament": match.tournament,
            "city": match.city
        })

    return result
