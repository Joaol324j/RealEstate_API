from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Property, PropertyImage, PropertyType, ListingType
from app.schemas import PropertyCreate, PropertyUpdate, PropertyResponse
from app.crud import create_property, update_property, get_property_by_id, delete_property
from app.dependencies import verify_admin
from app.utils.images_utils import save_image, delete_image  

router = APIRouter(prefix="/properties", tags=["Properties"])

@router.get("/", response_model=list[PropertyResponse])
def read_all_properties(
    db: Session = Depends(get_db),
    listing_type: ListingType = Query(None, description="Tipo de negociação: rent ou sale"),
    min_price: float = Query(None, description="Preço mínimo"),
    max_price: float = Query(None, description="Preço máximo")
):
    query = db.query(Property)

    if listing_type:
        query = query.filter(Property.listing_type == listing_type)
    
    if min_price is not None:
        query = query.filter(Property.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Property.price <= max_price)
    
    properties = query.all()
    
    if not properties:
        raise HTTPException(status_code=404, detail="Nenhum imóvel encontrado com os critérios fornecidos.")

    return properties

@router.get("/{property_id}", response_model=PropertyResponse)
def read_property(property_id: int, db: Session = Depends(get_db)):
    if property_id <= 0:
        raise HTTPException(status_code=400, detail="ID do imóvel inválido.")
    
    property_item = get_property_by_id(db, property_id)
    if not property_item:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado.")
    
    return property_item

@router.post("/", response_model=PropertyResponse, dependencies=[Depends(verify_admin)])
def create_new_property(
    title: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    location: str = Form(...),
    property_type: PropertyType = Form(...),
    listing_type: ListingType = Form(...),
    images: list[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    property_data = PropertyCreate(
        title=title,
        description=description,
        price=price,
        location=location,
        property_type=property_type,
        listing_type=listing_type
    )
    new_property = create_property(db, property_data)

    if images:
        for file in images:
            file_path = save_image(file)
            image = PropertyImage(property_id=new_property.id, image_url=file_path)
            db.add(image)
    
    db.commit()
    return new_property

@router.put("/{property_id}", response_model=PropertyResponse, dependencies=[Depends(verify_admin)])
def update_existing_property(
    property_id: int,
    title: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    location: str = Form(...),
    property_type: PropertyType = Form(...),
    listing_type: ListingType = Form(...),
    images: list[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    updated_property = update_property(
        db, property_id, PropertyUpdate(
            title=title,
            description=description,
            price=price,
            location=location,
            property_type=property_type,
            listing_type=listing_type
        )
    )
    if not updated_property:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado.")

    if images:
        old_images = db.query(PropertyImage).filter(PropertyImage.property_id == property_id).all()
        for old_image in old_images:
            delete_image(old_image.image_url)
            db.delete(old_image)

        for file in images:
            file_path = save_image(file)
            image = PropertyImage(property_id=property_id, image_url=file_path)
            db.add(image)
        
        db.commit()
    
    return updated_property

@router.delete("/{property_id}", dependencies=[Depends(verify_admin)])
def delete_existing_property(property_id: int, db: Session = Depends(get_db)):
    if property_id <= 0:
        raise HTTPException(status_code=400, detail="ID do imóvel inválido.")
    
    images = db.query(PropertyImage).filter(PropertyImage.property_id == property_id).all()
    for image in images:
        delete_image(image.image_url)
        db.delete(image)
    
    deleted_property = delete_property(db, property_id)
    if not deleted_property:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado.")
    
    db.commit()
    return {"message": "Imóvel deletado com sucesso"}
