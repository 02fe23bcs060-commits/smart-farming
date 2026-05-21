from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Farmer
from app.schemas import FarmerCreate, FarmerResponse

router = APIRouter(prefix="/api/farmers", tags=["farmers"])


@router.post("", response_model=FarmerResponse)
def create_farmer(payload: FarmerCreate, db: Session = Depends(get_db)):
    farmer = Farmer(**payload.model_dump())
    db.add(farmer)
    db.commit()
    db.refresh(farmer)
    return farmer


@router.get("", response_model=list[FarmerResponse])
def list_farmers(db: Session = Depends(get_db)):
    return db.query(Farmer).order_by(Farmer.created_at.desc()).limit(50).all()


@router.get("/{farmer_id}", response_model=FarmerResponse)
def get_farmer(farmer_id: int, db: Session = Depends(get_db)):
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    return farmer
