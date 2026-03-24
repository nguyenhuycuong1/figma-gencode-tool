import uuid

from sqlalchemy import Column, ForeignKey, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.core.db import Base
from datetime import datetime

class ConversationJob(Base):
    __tablename__ = "conversation_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    figma_file_key = Column(String, nullable=False)
    figma_file_id = Column(String, nullable=True)
    status = Column(String, nullable=False, default='pending')
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)