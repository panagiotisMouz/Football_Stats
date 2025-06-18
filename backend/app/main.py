from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import authenticate_user, create_token
from app.routers import countries, stats, players, years, matches
from app.crud import get_country_profile
import logging

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="WhyBother API", version="1.0", debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the WhyBother API"}

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not authenticate_user(form_data.username, form_data.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_token(form_data.username)
    return {"access_token": token, "token_type": "bearer"}


app.include_router(countries.router)
app.include_router(stats.router)
app.include_router(players.router)
app.include_router(players.scorer_router)
app.include_router(years.router)
app.include_router(matches.router)


@app.get("/debug/country/{id}")
def debug_country_profile(id: int, db: Session = Depends(get_db)):
    try:
        profile = get_country_profile(db, id)
        if not profile:
            raise HTTPException(status_code=404, detail="Country not found or empty profile")
        logging.info(f"✅ Country {id} profile: {profile}")
        return profile
    except Exception as e:
        logging.error(f" Error fetching country profile: {e}")
        raise HTTPException(status_code=500, detail="Server error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
