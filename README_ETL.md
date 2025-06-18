# WhyBother Project - ETL Documentation (Phase I)

This document describes the steps followed to extract, transform, and load (ETL) the football statistics data into a clean, normalized, and queryable MySQL database schema. It corresponds to **Phase I** of the WhyBother project.

---

## 1. File Structure

```
whybother-backend/
├── app/
│   ├── main.py                # FastAPI app entry point
│   ├── models.py              # SQLAlchemy ORM models
│   ├── crud.py                # Query logic
│   ├── routers/               # Routers: countries, players, matches, etc.
│   └── database.py            # SQLAlchemy DB session/engine
├── etl.py                     # ETL script to load and normalize data
├── schema.sql                 # MySQL schema with PK/FK constraints
├── requirements.txt           # All dependencies
├── backup.sql                 # Full MySQL dump after data load ✅
└── .env                       # DB credentials
```

---

##  2. Technologies Used

* **MySQL** with InnoDB engine
* **FastAPI** with SQLAlchemy ORM
* **Docker Compose** for isolated development
* **Pandas** for CSV cleaning
* **Python dotenv** to load DB credentials

---

##  3. Database Schema (schema.sql)

* `countries`: Reference table for all country/team identifiers 
* `former_names`: Links historical names to current countries 
* `players`, `goalscorers`, `shootouts`, `matches`: Cleaned relational tables with PK/FK 
* All tables use surrogate integer keys for indexing and relationships

---

## . ETL Flow (etl.py)

### Step 1: Load Countries from Kaggle File

* Normalize name casing
* Remove duplicates
* Use ISO codes for FK consistency

### Step 2: Load Former Names

* Match former names to canonical countries
* Store with `start_date`/`end_date` for historical tracking

### Step 3: Load Matches

* Normalize home/away team names
* Drop matches where countries are not found (with log warning)
* Ensure date parsing is safe

### Step 4: Load Goalscorers

* Parse `minute`, `penalty`, `own_goal`
* Ensure scorer player exists or insert
* Map team name using normalized country\_id
* Drop orphan goals with missing match/player/team

### Step 5: Load Shootouts

* Join on valid match ID only
* Drop entries with unmatched matches (export to quarantine folder)

---

## 5. Data Validations

* Logs show inserted vs. skipped entries
* Invalid or unmapped country names are logged and ignored
* Orphan rows are redirected to quarantine CSVs (e.g., `orphan_shootouts.csv`)
* NaN and nulls are sanitized to SQL-safe defaults (empty string or NULL)

---

## 6. Backup and Recovery

*Full MySQL export after successful load:

bash
mysqldump -u root -p whybother > backup.sql

Can be restored using:

bash
mysql -u root -p whybother < backup.sql

---

## Summary

✔ Schema is normalized and uses PK/FK constraints
✔ Countries have a single reference source of truth
✔ Data is loaded via safe, clean ETL with Pandas + SQLAlchemy
✔ Orphan data is identified and logged
✔ Ready for Phase II: SQL view-based query answering

---

## Next Step

Move to `views.sql` to define queries using SQL views for analytics and visualization endpoints.
