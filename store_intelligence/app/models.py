from sqlalchemy import Column, String, Integer, Float, Boolean, Text
from app.database import Base

class DBStoreEvent(Base):
    """
    Production tracking table architecture storing fused multi-camera cross-spatial frames.
    """
    __tablename__ = "store_tracking_events"
    
    event_id = Column(String, primary_key=True, index=True)
    store_id = Column(String, nullable=False, index=True)
    camera_id = Column(String, nullable=False)
    visitor_id = Column(String, nullable=False, index=True)
    event_type = Column(String, nullable=False)  # ENTRY, ZONE_ENTER, BILLING_QUEUE_JOIN
    timestamp = Column(String, nullable=False)
    zone_id = Column(String, nullable=True)
    dwell_ms = Column(Integer, default=0)
    is_staff = Column(Boolean, default=False)
    confidence = Column(Float, default=1.0)
    metadata_json = Column(Text, nullable=True)