# Sportomic Metrics Backend

A minimal, production-ready Python backend that models venues, members, bookings, and transactions, computes dashboard metrics, and exposes APIs with a lightweight UI dashboard.

## Tech Stack
- FastAPI for APIs and docs
- SQLAlchemy for ORM and schema
- SQLite for local dev (PostgreSQL ready for prod)
- Jinja2 + Chart.js for a simple dashboard at `/dashboard`

## Project Structure
```
.
├─ app.py                 # FastAPI app and routes
├─ db.py                  # Database engine and session
├─ models.py              # ORM models and relations
├─ queries.py             # Metrics and list queries
├─ seed_data.py           # Sample data loader
├─ requirements.txt       # Python dependencies
├─ api/index.py           # Vercel function entry (ASGI app)
├─ templates/dashboard.html  # Minimal dashboard UI
└─ .gitignore
```

## Core Flow (Who does what)
- `db.py`: reads `DATABASE_URL` and creates `engine` and `SessionLocal`.
- `models.py`: defines tables `Venue`, `Member`, `Booking`, `Transaction` with relations.
- `seed_data.py`: creates tables and inserts assignment data.
- `queries.py`: business logic to compute metrics and revenue time-series; also lists venues and sports.
- `app.py`: wires endpoints and serves the dashboard UI.
- `api/index.py`: exposes `app` for serverless/edge platforms like Vercel.

## Metrics Definitions
- Active/Inactive Members: `Member.status` counts.
- Bookings: count of bookings where status is `Confirmed` or `Completed`.
- Booking Revenue: sum of `Transaction.amount` where `type='Booking'` and `status='Success'`.
- Coaching Revenue: sum of `Transaction.amount` where `type='Coaching'` and `status='Success'`.
- Total Revenue: sum of all `Success` transactions.
- Repeat Booking %: members with >1 confirmed bookings ÷ members with ≥1 confirmed booking.
- Slots Utilization %: confirmed bookings ÷ total bookings in range.
- Coupon Redemption: count of confirmed bookings with a non-empty `coupon_code`.
- Trial Conversion Rate %: `converted_from_trial` true ÷ `is_trial_user` true.
- Refunds & Disputes: amount and count of transactions with status `Refunded` or `Dispute`.

## API Endpoints
- `GET /` → service info
- `GET /health` → health check
- `GET /venues` → list venues
- `GET /sports` → distinct sport ids from bookings
- `GET /metrics/general` → dashboard metrics
  - Query params: `start_date`, `end_date`, `venue_id`, `sport_id`
- `GET /metrics/revenue_timeseries` → [{ date, revenue }] time-series
  - Query params: `start_date`, `end_date`, `venue_id`, `sport_id`
- `GET /dashboard` → minimal HTML dashboard

## Setup (Local Dev)
```powershell
cd C:\Users\KASHISH\Downloads\sportomic_backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
set DATABASE_URL=sqlite:///sportomic.db
python seed_data.py
uvicorn app:app --reload --port 8000
```

Open:
- `http://127.0.0.1:8000/dashboard`
- `http://127.0.0.1:8000/docs`


## GitHub Push
```powershell
cd C:\Users\KASHISH\Downloads\sportomic_backend
git init
git config --global user.name "YOUR_NAME"
git config --global user.email "YOUR_EMAIL"
# create .gitignore with: venv/, __pycache__/, *.pyc, sportomic.db, .env, .vercel/
git add -A
git commit -m "Initial commit: Sportomic Metrics API + dashboard"
git branch -M main
git remote add origin https://github.com/<your-username>/sportomic_backend.git
git push -u origin main
```
Use a GitHub Personal Access Token for the password when prompted.

## Sample Requests
```powershell
# venues
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8000/venues

# metrics for a period
Invoke-WebRequest -UseBasicParsing "http://127.0.0.1:8000/metrics/general?start_date=2025-12-10&end_date=2025-12-15"

# revenue time-series
Invoke-WebRequest -UseBasicParsing "http://127.0.0.1:8000/metrics/revenue_timeseries?start_date=2025-12-10&end_date=2025-12-15"
```

## Notes
- Status normalization: `Confirmed` and `Completed` considered successful bookings.
- The dashboard UI is intentionally minimal and uses your backend APIs.
- Never commit secrets (`.env`, tokens). Keep `sportomic.db` out of Git history.
