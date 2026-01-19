from fastapi import FastAPI, Depends, HTTPException, status
from fastapi import Query
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import User
from schemas import RegisterSchema, LoginSchema, EditProfileSchema
from auth import hash_password, verify_password, create_token
from recommender import recommend_jobs_from_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import Optional
from math import ceil

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Recommendation System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development only
    allow_credentials=True,
    allow_methods=["*"],  # IMPORTANT
    allow_headers=["*"],  # IMPORTANT
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "secret123"   # SAME as create_token
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Register
@app.post("/register")
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    user = User(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
        experience=data.experience,
        education=data.education,
        skills=",".join(data.skills)
    )
    db.add(user)
    db.commit()
    return {"message": "User registered successfully"}

# ✅ Login
@app.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"user_id": user.id})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "experience": user.experience,
            "education": user.education,
            "skills": user.skills.split(",") if user.skills else []
        }
    }


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise credentials_exception

    return user


# ✅ Dashboard (Recommended Jobs)
@app.get("/dashboard")
def dashboard(
    page: int = Query(1, ge=1),
    limit: int = Query(6, ge=1, le=50),
    min_salary: int | None = None,
    max_salary: int | None = None,
    experience: int | None = None,
    skills: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return recommend_jobs_from_db(
        current_user,
        db,
        page,
        limit,
        min_salary,
        max_salary,
        experience,
        skills
    )


# ✅ Edit Profile
@app.put("/edit-profile")
def edit_profile(
    data: EditProfileSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if data.experience is not None:
        current_user.experience = data.experience

    if data.education is not None:
        current_user.education = data.education

    if data.skills is not None:
        current_user.skills = ",".join(data.skills)

    db.add(current_user)        # 🔥 IMPORTANT
    db.commit()
    db.refresh(current_user)    # 🔥 IMPORTANT

    return {
        "message": "Profile updated",
        "user": {
            "experience": current_user.experience,
            "education": current_user.education,
            "skills": current_user.skills
        }
    }
