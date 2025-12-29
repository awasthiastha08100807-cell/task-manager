from fastapi import FastAPI, Depends, HTTPException, Header, Body
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from passlib.hash import bcrypt
import jwt, datetime

import models
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

# -----------------------
# CORS Middleware
# -----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# JWT Config
# -----------------------
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def create_token(data: dict, expires_minutes: int = 60):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def verify_password(plain_password, hashed):
    return bcrypt.verify(plain_password, hashed)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------
# Auth Dependency
# -----------------------
def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization.replace("Bearer ", "")
    payload = decode_token(token)
    return payload["user_id"]

# -----------------------
# Pydantic Models
# -----------------------
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

# -----------------------
# Auth APIs
# -----------------------
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter_by(email=user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    password = user.password[:72]  # bcrypt limit
    hashed_password = bcrypt.hash(password)

    db_user = models.User(name=user.name, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"msg": "User registered"}

@app.get("/users")
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter_by(email=user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"user_id": db_user.id})
    return {"token": token}

# -----------------------
# Task APIs
# -----------------------
@app.get("/tasks")
def list_tasks(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Task).filter_by(user_id=user_id).all()

@app.post("/tasks")
def create_task(task: TaskCreate, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    db_task = models.Task(title=task.title, description=task.description, status="pending", user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updates: dict = Body(...), user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(models.Task).filter_by(id=task_id, user_id=user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if "title" in updates:
        task.title = updates["title"]
    if "description" in updates:
        task.description = updates["description"]
    if "status" in updates and updates["status"] in ["pending", "in_progress", "done"]:
        task.status = updates["status"]
    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(models.Task).filter_by(id=task_id, user_id=user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"msg": "Task deleted"}
