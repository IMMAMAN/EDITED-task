import uuid
from app.app import db
from datetime import datetime
from sqlalchemy.types import Enum
from .enums import CrawlSessionStatus


class ScreenshotSession(db.Model):
    __tablename__ = 'screenshot_sessions'
    id = db.Column(db.String(36), primary_key=True, nullable=False)
    start_url = db.Column(db.String(255), nullable=False)
    num_links = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(Enum(CrawlSessionStatus), nullable=False, default=CrawlSessionStatus.IN_PROGRESS)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)