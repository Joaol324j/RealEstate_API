from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import create_property, get_all_properties, get_property_by_id, update_property, delete_property

from app.schemas import PropertyCreate, PropertyUpdate, PropertyResponse

router = APIRouter()

@router.post("/", response_model=PropertyResponse)
def create_new_property(property_data: PropertyCreate, db: Session = Depends(get_db)):
    return create_property(db, property_data)

@router.get("/", response_model=list[PropertyResponse])
def read_all_properties(db: Session = Depends(get_db)):
    return get_all_properties(db)

@router.get("/{property_id}", response_model=PropertyResponse)
def read_property(property_id: int, db: Session = Depends(get_db)):
    property_item = get_property_by_id(db, property_id)
    if not property_item:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado")
    return property_item

@router.put("/{property_id}", response_model=PropertyResponse)
def update_existing_property(property_id: int, property_data: PropertyUpdate, db: Session = Depends(get_db)):
    updated_property = update_property(db, property_id, property_data)
    if not updated_property:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado")
    return updated_property

@router.delete("/{property_id}")
def delete_existing_property(property_id: int, db: Session = Depends(get_db)):
    deleted_property = delete_property(db, property_id)
    if not deleted_property:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado")
    return {"message": "Imóvel deletado com successo"}
