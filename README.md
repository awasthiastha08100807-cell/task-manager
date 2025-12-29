## Setup

### Backend
pip install -r requirements.txt
uvicorn main:app --reload

### Frontend
npm install
npm start

## API Endpoints
POST /register
POST /login
GET /tasks
POST /tasks
PUT /tasks/{id}
DELETE /tasks/{id}

## Assumptions
- JWT auth
- SQLite for simplicity
