from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Enum,
    JSON,
    Boolean,
)
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .base import Base


class ProductStatus(enum.Enum):
    MANUFACTURED = "manufactured"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    RECALLED = "recalled"


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id"))
    batch_number = Column(String, index=True)
    manufacturing_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(ProductStatus))
    blockchain_hash = Column(String, unique=True)

    manufacturer = relationship("Manufacturer", back_populates="products")
    tracking_events = relationship("TrackingEvent", back_populates="product")


class Manufacturer(Base):
    __tablename__ = "manufacturers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    blockchain_address = Column(String, unique=True)
    certification = Column(String)

    products = relationship("Product", back_populates="manufacturer")


class TrackingEvent(Base):
    __tablename__ = "tracking_events"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    location = Column(String)
    event_type = Column(String)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    blockchain_hash = Column(String, unique=True)
    additional_data = Column(JSON)

    product = relationship("Product", back_populates="tracking_events")


class PredictionModel(Base):
    __tablename__ = "prediction_models"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, unique=True)
    model_type = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow)
    performance_metrics = Column(JSON)
    parameters = Column(JSON)
    active = Column(Boolean, default=True)
