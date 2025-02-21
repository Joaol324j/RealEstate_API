from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import create_property, get_all_properties, get_property_by_id, update_property, delete_property
from app.schemas import PropertyCreate, PropertyUpdate, PropertyResponse
from app.dependencies import verify_admin

router = APIRouter(prefix="/properties", tags=["Properties"])

@router.post("/", response_model=PropertyResponse, dependencies=[Depends(verify_admin)])
def create_new_property(property_data: PropertyCreate, db: Session = Depends(get_db)):
    return create_property(db, property_data)

@router.get("/", response_model=list[PropertyResponse])
def read_all_properties(db: Session = Depends(get_db)):
    properties = get_all_properties(db)
    if not properties:
        raise HTTPException(status_code=404, detail="Nenhum imóvel encontrado.")
    return properties

@router.get("/{property_id}", response_model=PropertyResponse)
def read_property(property_id: int, db: Session = Depends(get_db)):
    if property_id <= 0:
        raise HTTPException(status_code=400, detail="ID do imóvel inválido.")
    
    property_item = get_property_by_id(db, property_id)
    if not property_item:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado.")
    return property_item

@router.put("/{property_id}", response_model=PropertyResponse, dependencies=[Depends(verify_admin)])
def update_existing_property(property_id: int, property_data: PropertyUpdate, db: Session = Depends(get_db)):
    if property_id <= 0:
        raise HTTPException(status_code=400, detail="ID do imóvel inválido.")
    
    updated_property = update_property(db, property_id, property_data)
    if not updated_property:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado.")
    return updated_property

@router.delete("/{property_id}", dependencies=[Depends(verify_admin)])
def delete_existing_property(property_id: int, db: Session = Depends(get_db)):
    if property_id <= 0:
        raise HTTPException(status_code=400, detail="ID do imóvel inválido.")
    
    deleted_property = delete_property(db, property_id)
    if not deleted_property:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado.")
    return {"message": "Imóvel deletado com sucesso"}
