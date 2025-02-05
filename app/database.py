from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

class Database:
    engine = create_engine("sqlite:///db.db", connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    @staticmethod
    def get_db():
        db = Database.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @staticmethod
    def add_user(username: str, user_id: str):
        from app.models import User

        db = Database.SessionLocal()
        try:
            new_user = User(name=username, id=user_id)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        
        except Exception as e:
            db.rollback()
            print(f"Ошибка при создании пользователя: {e}")
        finally:
            db.close()
