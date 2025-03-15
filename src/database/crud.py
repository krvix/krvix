from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime

from src.models.supply_chain import (
    Product,
    Manufacturer,
    TrackingEvent,
    PredictionModel,
)
from src.utils.logger import blockchain_logger


def create_product(db: Session, product_data: Dict[str, Any]) -> Product:
    db_product = Product(
        name=product_data["name"],
        description=product_data.get("description", ""),
        manufacturer_id=product_data["manufacturer_id"],
        batch_number=product_data["batch_number"],
        manufacturing_date=datetime.utcnow(),
        status=product_data.get("status", "manufactured"),
        blockchain_hash=product_data.get("blockchain_hash"),
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
    return db.query(Product).offset(skip).limit(limit).all()


def update_product_status(
    db: Session, product_id: int, status: str, blockchain_hash: str
) -> Optional[Product]:
    db_product = get_product(db, product_id)
    if db_product:
        db_product.status = status
        db_product.blockchain_hash = blockchain_hash
        db.commit()
        db.refresh(db_product)
    return db_product


def create_manufacturer(db: Session, manufacturer_data: Dict[str, Any]) -> Manufacturer:
    db_manufacturer = Manufacturer(
        name=manufacturer_data["name"],
        location=manufacturer_data["location"],
        blockchain_address=manufacturer_data["blockchain_address"],
        certification=manufacturer_data.get("certification", ""),
    )
    db.add(db_manufacturer)
    db.commit()
    db.refresh(db_manufacturer)
    return db_manufacturer


def get_manufacturer(db: Session, manufacturer_id: int) -> Optional[Manufacturer]:
    return db.query(Manufacturer).filter(Manufacturer.id == manufacturer_id).first()


def create_tracking_event(db: Session, event_data: Dict[str, Any]) -> TrackingEvent:
    db_event = TrackingEvent(
        product_id=event_data["product_id"],
        timestamp=datetime.utcnow(),
        location=event_data["location"],
        event_type=event_data["event_type"],
        temperature=event_data.get("temperature"),
        humidity=event_data.get("humidity"),
        blockchain_hash=event_data.get("blockchain_hash"),
        additional_data=event_data.get("additional_data", {}),
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_product_history(db: Session, product_id: int) -> List[TrackingEvent]:
    return db.query(TrackingEvent).filter(TrackingEvent.product_id == product_id).all()


def save_prediction_model(db: Session, model_data: Dict[str, Any]) -> PredictionModel:
    db_model = PredictionModel(
        model_name=model_data["model_name"],
        model_type=model_data["model_type"],
        performance_metrics=model_data.get("performance_metrics", {}),
        parameters=model_data.get("parameters", {}),
        active=True,
    )
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model


def get_active_prediction_model(
    db: Session, model_type: str
) -> Optional[PredictionModel]:
    return (
        db.query(PredictionModel)
        .filter(
            PredictionModel.model_type == model_type, PredictionModel.active == True
        )
        .first()
    )


def deactivate_prediction_model(
    db: Session, model_id: int
) -> Optional[PredictionModel]:
    db_model = db.query(PredictionModel).filter(PredictionModel.id == model_id).first()
    if db_model:
        db_model.active = False
        db.commit()
        db.refresh(db_model)
    return db_model
