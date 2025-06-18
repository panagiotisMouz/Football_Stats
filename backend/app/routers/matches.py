from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud
from ..database import get_db

router = APIRouter(
    prefix="/matches",
    tags=["Matches"]
)

@router.get("/", response_model=List[dict])
def list_matches(db: Session = Depends(get_db)):
    matches = crud.get_matches(db)
    return [
        {
            "id": m.id,
            "match_date": m.match_date,
            "home_team": m.home_team.name if m.home_team else None,
            "away_team": m.away_team.name if m.away_team else None,
            "home_score": m.home_score,
            "away_score": m.away_score,
            "tournament": m.tournament,
            "city": m.city,
            "host_country": m.host_country.name if m.host_country else None,
            "neutral": m.neutral
        }
        for m in matches
    ]


@router.get("/{match_id}", response_model=dict)
def get_match_by_id(match_id: int, db: Session = Depends(get_db)):

    match = crud.get_match_by_id(db, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    goals = crud.get_goals_by_match(db, match.id)
    goal_events = [
        {
            "scorer": g.player.name,
            "team": g.team.name,
            "minute": g.minute,
            "own_goal": g.own_goal,
            "penalty": g.penalty
        }
        for g in goals
    ]

    shootout = crud.get_shootout_by_match(db, match.id)
    shootout_info = (
        {
            "winner": shootout.winner.name if shootout.winner else None,
            "first_shooter": shootout.first_shooter.name if shootout.first_shooter else None
        }
        if shootout else None
    )

    return {
        "id": match.id,
        "date": match.match_date,
        "home_team": match.home_team.name if match.home_team else None,
        "away_team": match.away_team.name if match.away_team else None,
        "home_score": match.home_score,
        "away_score": match.away_score,
        "tournament": match.tournament,
        "city": match.city,
        "host_country": match.host_country.name if match.host_country else None,
        "neutral": match.neutral,
        "goals": goal_events,
        "shootout": shootout_info
    }
