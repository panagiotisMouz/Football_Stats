from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case, desc
from ..database import get_db
from ..models import Match, Country
from .. import crud

router = APIRouter(
    prefix="/years",
    tags=["Years"]
)

@router.get("/{year}")
def get_yearly_stats(year: int, db: Session = Depends(get_db)):
    matches = crud.get_matches_by_year(db, year)
    match_list = []
    goal_counts = {}
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

    most_goals = max(goal_counts.values()) if goal_counts else 0
    top_teams_sorted = sorted(top_teams.items(), key=lambda x: -x[1])[:5]
    return {
        "year": year,
        "total_matches": len(matches),
        "top_teams": top_teams_sorted,
        "matches": match_list,
    }
