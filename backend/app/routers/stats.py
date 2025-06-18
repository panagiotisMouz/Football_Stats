from datetime import date
from typing import Optional
from sqlalchemy.sql.expression import case

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, case, or_, desc

from .. import crud
from ..database import get_db
from ..models import Country, Match

router = APIRouter(
    prefix="/stats",
    tags=["Analytics"]
)



from sqlalchemy.sql.expression import case

from sqlalchemy.sql.expression import case
from sqlalchemy import and_

@router.get("/global")
def get_global_stats(db: Session = Depends(get_db)):
    try:

        wins_expr = case(
            *[
                (and_(Match.home_team_id == Country.id, Match.home_score > Match.away_score), 1),
                (and_(Match.away_team_id == Country.id, Match.away_score > Match.home_score), 1)
            ],
            else_=0
        )

        wins_by_team = db.query(
            Country.id,
            Country.name,
            func.sum(wins_expr).label("wins")
        ).join(Match, or_(
            Match.home_team_id == Country.id,
            Match.away_team_id == Country.id
        )).group_by(Country.id).all()

        top_wins = sorted(
            [{"country": name, "wins": int(w or 0)} for _, name, w in wins_by_team],
            key=lambda x: -x["wins"]
        )[:10]

        # GOALS
        goals_expr = case(
            *[
                (Match.home_team_id == Country.id, Match.home_score),
                (Match.away_team_id == Country.id, Match.away_score)
            ],
            else_=0
        )

        goal_counts = db.query(
            Country.name,
            func.sum(goals_expr).label("goals")
        ).join(Match, or_(
            Match.home_team_id == Country.id,
            Match.away_team_id == Country.id
        )).group_by(Country.id).order_by(desc("goals")).limit(10).all()

        top_goals = [{"country": name, "goals": int(g or 0)} for name, g in goal_counts]

        population_scatter = db.query(
            Country.name,
            func.sum(wins_expr).label("wins"),
            Country.population
        ).outerjoin(Match, or_(
            Match.home_team_id == Country.id,
            Match.away_team_id == Country.id
        )).group_by(Country.id).all()

        population_scatter = [
            {"country": name, "wins": int(w or 0), "population": pop}
            for name, w, pop in population_scatter if pop
        ]

        return {
            "top10_wins": top_wins,
            "top10_goals": top_goals,
            "population_scatter": population_scatter
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/{year}")
def get_yearly_stats(year: int, db: Session = Depends(get_db)):
    matches = crud.get_matches_by_year(db, year)
    match_list = []
    top_teams = {}

    for m in matches:
        match_list.append({
            "date": m.match_date,
            "home": m.home_team.name if m.home_team else None,
            "away": m.away_team.name if m.away_team else None,
            "score": f"{m.home_score}-{m.away_score}",
            "tournament": m.tournament
        })

        for tid, score in [(m.home_team_id, m.home_score), (m.away_team_id, m.away_score)]:
            top_teams[tid] = top_teams.get(tid, 0) + score

    top_teams_sorted = sorted(top_teams.items(), key=lambda x: -x[1])[:5]

    return {
        "year": year,
        "total_matches": len(matches),
        "top_teams": top_teams_sorted,
        "matches": match_list
    }



@router.get("/country/{country_id}/profile")
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
        or_(Match.home_team_id == country_id, Match.away_team_id == country_id)
    )

    if from_year:
        matches = matches.filter(Match.match_date >= date(from_year, 1, 1))
    if to_year:
        matches = matches.filter(Match.match_date <= date(to_year, 12, 31))

    matches = matches.all()
    total_matches = len(matches)
    wins, goals, points = 0, 0, 0

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

    return {
        "country": country.name,
        "region": country.region,
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
