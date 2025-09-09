# F1 Dashboard Development Guide

## Project Overview
A Python FastAPI backend serving F1 data with a React frontend. Starting with Race Weekend Countdown, expanding to Driver Stats Dashboard.

## Backend Setup (Python/FastAPI)

### Prerequisites
- Python 3.8+
- pip or pipenv

### Installation
```bash
cd backend
pip install -r requirements.txt
```

### Requirements (requirements.txt)
```
fastapi==0.104.1
uvicorn==0.24.0
fastf1==3.3.7
python-dateutil==2.8.2
pytz==2023.3
```

### Running Backend
```bash
cd backend
uvicorn app:app --reload --port 8000
```

### API Endpoints (Phase 1 - Race Countdown)
- `GET /api/next-race` - Returns next race info with countdown data
- `GET /api/race-schedule` - Returns current season schedule

### Backend Structure
```
backend/
├── app.py                 # FastAPI app, routes
├── services/
│   └── f1_service.py      # FastF1 data fetching logic
├── models/
│   └── race_models.py     # Pydantic data models
└── requirements.txt
```

### Key FastF1 Usage
```python
import fastf1

# Get race schedule
schedule = fastf1.get_event_schedule(2024)
next_race = schedule[schedule['EventDate'] > datetime.now()].iloc[0]

# Get session times
session_schedule = next_race['Session1Date'], next_race['Session2Date']...
```

## Frontend Setup (React)

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation
```bash
cd frontend
npm install
```

### Key Dependencies
```bash
npm install axios date-fns
```

### Running Frontend
```bash
cd frontend
npm start
```
Runs on http://localhost:3000

### Frontend Structure
```
frontend/
├── src/
│   ├── components/
│   │   ├── RaceCountdown.jsx      # Phase 1
│   │   └── DriverStats.jsx        # Phase 2
│   ├── services/
│   │   └── api.js                 # API calls to backend
│   ├── App.jsx
│   └── index.js
├── package.json
└── public/
```

## Development Workflow

### Phase 1: Race Weekend Countdown
1. **Backend**: Create `/api/next-race` endpoint using FastF1
2. **Frontend**: Simple countdown component fetching from API
3. **Test**: Verify countdown updates every second

### Phase 2: Driver Stats Dashboard  
1. **Backend**: Add `/api/driver-standings` endpoint
2. **Frontend**: Table component for standings
3. **Enhancement**: Add basic charts

## API Response Examples

### Next Race Response
```json
{
  "race_name": "Abu Dhabi Grand Prix",
  "location": "Yas Marina Circuit",
  "country": "UAE", 
  "race_date": "2024-12-08T17:00:00Z",
  "sessions": [
    {"name": "Practice 1", "datetime": "2024-12-06T10:30:00Z"},
    {"name": "Practice 2", "datetime": "2024-12-06T14:00:00Z"},
    {"name": "Practice 3", "datetime": "2024-12-07T11:30:00Z"},
    {"name": "Qualifying", "datetime": "2024-12-07T15:00:00Z"},
    {"name": "Race", "datetime": "2024-12-08T17:00:00Z"}
  ]
}
```

## Deployment
- Both can be deployed to Vercel
- Backend as Python serverless functions
- Frontend as static React app
- CORS configured for cross-origin requests

## Tips
- FastF1 can be slow on first load (downloads data)
- Cache responses for better performance
- Handle timezone conversions properly
- React useState for countdown timers