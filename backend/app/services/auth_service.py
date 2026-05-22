from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, auth

class AuthService:
    @staticmethod
    def register_user(db: Session, user: schemas.UserCreate) -> models.User:
        """Register a new user"""
        normalized_username = user.username.strip()
        normalized_email = user.email.strip().lower()

        # Check if user already exists
        existing_user = db.query(models.User).filter(
            (func.trim(models.User.username) == normalized_username) | (func.lower(func.trim(models.User.email)) == normalized_email)
        ).first()
        if existing_user:
            raise ValueError("Username or email already registered")

        # Hash password
        hashed_password = auth.get_password_hash(user.password)

        # Create user
        db_user = models.User(
            username=normalized_username,
            email=normalized_email,
            password_hash=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> models.User:
        """Authenticate a user"""
        normalized_username = username.strip()
        user = auth.authenticate_user(db, normalized_username, password)
        if not user:
            raise ValueError("Invalid username or password")
        return user

    @staticmethod
    def create_access_token(user: models.User) -> str:
        """Create JWT access token for user"""
        return auth.create_access_token(data={"sub": user.username})