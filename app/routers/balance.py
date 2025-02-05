from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas, database
from app.database import Database


router = APIRouter(prefix="/balance", tags=["balance"])

@router.get("/get", response_model=schemas.Balance)
def get_balance(balance_request: schemas.BalanceRequest, db: Session = Depends(Database.get_db)):
    return crud.get_balance(db, balance_request.user_id)
