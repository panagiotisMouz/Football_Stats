from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..models import Player, Country
from .. import crud
from pydantic import BaseModel

router = APIRouter(
    prefix="/players",
    tags=["Players"]
)


class PlayerOut(BaseModel):
    id: int
    name: str
    country_id: Optional[int]
    country_name: Optional[str]

    class Config:
        orm_mode = True

@router.get("/", response_model=List[PlayerOut])
def list_players(country_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    if country_id:
        players = db.query(Player).filter(Player.country_id == country_id).all()
    else:
        players = crud.get_players(db)


    return [
        PlayerOut(
            id=p.id,
            name=p.name,
            country_id=p.country_id,
            country_name=p.country.name if p.country else None
        )
        for p in players
    ]



@router.get("/{player_id}", response_model=PlayerOut)
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = crud.get_player_by_id(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    return PlayerOut(
        id=player.id,
        name=player.name,
        country_id=player.country_id,
        country_name=player.country.name if player.country else None
    )

scorer_router = APIRouter(prefix="/scorers", tags=["Scorers"])

@scorer_router.get("/", response_model=List[dict])
def get_top_scorers(limit: int = 10, db: Session = Depends(get_db)):
    top_scorers = crud.get_top_scorers(db, limit=limit)
    return [
        {
            "player_id": pid,
            "players": name,
            "country": country_name,
            "total_goals": int(total_goals or 0)
        }
        for pid, name, country_name, total_goals in top_scorers
    ]

@scorer_router.get("/{player_id}", response_model=dict)
def get_scorer_profile(player_id: int, db: Session = Depends(get_db)):
    player = crud.get_player_by_id(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    goals = crud.get_goals_by_player(db, player_id)
    total_goals = len(goals)
    # Max goals by players in a single match
    goals_by_match = {}
    for g in goals:
        goals_by_match.setdefault(g.match_id, 0)
        goals_by_match[g.match_id] += 1
    max_goals_in_match = max(goals_by_match.values()) if goals_by_match else 0
    # Determine active years (first and last year with a goal)
    years = [g.match.match_date.year for g in goals]
    active_from = min(years) if years else None
    active_to = max(years) if years else None
    # Team goals per match overall (across active years)
    country_id = player.country_id
    team_matches = 0
    team_goals = 0
    if active_from and active_to:
        for year in range(active_from, active_to + 1):
            matches_year = crud.get_matches_by_year(db, year)
            for match in matches_year:
                if match.home_team_id == country_id or match.away_team_id == country_id:
                    team_matches += 1
                    team_goals += (match.home_score if match.home_team_id == country_id else match.away_score)
    team_gpm_overall = (team_goals / team_matches) if team_matches else None
    # Yearly performance stats for players and team
    yearly_stats = []
    if active_from and active_to:
        for year in range(active_from, active_to + 1):
            # Player goals in that year
            goals_in_year = sum(1 for g in goals if g.match.match_date.year == year)
            # Team average goals per match in that year
            matches_year = crud.get_matches_by_year(db, year)
            team_matches_year = 0
            team_goals_year = 0
            for match in matches_year:
                if match.home_team_id == country_id or match.away_team_id == country_id:
                    team_matches_year += 1
                    team_goals_year += (match.home_score if match.home_team_id == country_id else match.away_score)
            team_gpm_year = (team_goals_year / team_matches_year) if team_matches_year else None
            yearly_stats.append({
                "year": year,
                "player_goals": goals_in_year,
                "team_goals_per_match": round(team_gpm_year, 2) if team_gpm_year is not None else None
            })
    return {
        "players": player.name,
        "country": player.country.name if player.country else None,
        "active_years": {"from": active_from, "to": active_to} if active_from and active_to else None,
        "total_goals": total_goals,
        "max_goals_in_a_match": max_goals_in_match,
        "team_goals_per_match_overall": round(team_gpm_overall, 2) if team_gpm_overall is not None else None,
        "yearly_stats": yearly_stats
    }
