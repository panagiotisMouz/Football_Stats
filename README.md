# WhyBother: Football Statistics Explorer

A full-stack application for analyzing international football statistics.
Built with **FastAPI**, **MySQL**, and **Next.js (React)**.

---

##  Features

*  **Global Stats:** Top countries by wins, goals, points.
*  **Yearly Stats:** Select a year and view aggregated match data.
*  **Country Profiles:** Match history, wins per year, average goals.
*  **Top Scorers:** Individual player stats with goals per year.
*  **Interactive Charts:** Visualize trends and performance.
*  **Dynamic Filters:** Drill down by country or player.

---

##  Folder Structure

```
WhyBother/
├── backend/               # FastAPI application
│   ├── app/               # Main app code (models, routers, etc.)
│   ├── etl.py             # ETL script to load and clean CSV data
│   ├── schema.sql         # DDL: all tables and views
│   ├── views.sql          # SQL views for stats
│   └── requirements.txt   # Python dependencies
├── frontend/              # Next.js frontend
│   ├── components/        # Charts, layout, UI parts
│   ├── pages/             # Main routes
│   ├── services/          # Axios API services
│   └── ...
├── data/                  # CSV data files
│   ├── matches.csv
│   ├── players.csv
│   └── ...
├── .env.example           # Example environment variables
├── README.md              # This file
```

---

##  Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/WhyBother.git
cd WhyBother
```

### 2. Set up the backend

#### a) Create `.env` file

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=whybother
DB_USER=root
DB_PASS=root
```

#### b) Install Python dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### c) Create database and run SQL scripts

In MySQL:

```sql
CREATE DATABASE whybother;
USE whybother;
SOURCE schema.sql;
SOURCE views.sql;
```

#### d) Run the ETL loader

```bash
python etl.py
```

#### e) Start the FastAPI server

```bash
uvicorn app.main:app --reload
```

### 3. Set up the frontend

```bash
cd ../frontend
npm install
```

#### a) Create `.env.local`

```
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

#### b) Start the frontend

```bash
npm run dev
```

Go to `http://localhost:3000` to view the app.

---

##  SQL Views Summary

All key queries (wins, goals, points, top scorers, yearly stats) are implemented using SQL views defined in `views.sql`. This enables efficient in-DB aggregation and avoids unnecessary Python-side filtering.

---

##  Backup

To back up the full database:

```bash
mysqldump -u root -p --databases whybother > backup_whybother.sql
```

To restore:

```bash
mysql -u root -p < backup_whybother.sql
```

---

##  Authors

* \panagiotis mouzouris – Backend, ETL
* \panagiotis mouzouris – Frontend, Visualizations

---

## License

This project is for academic use at University of Ioannina – Course: E/E 053.
