"""
Database models for MentorOS user management and session storage.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    """User model for storing login and profile information."""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=True)  # For future password auth
    provider = Column(String, nullable=True)  # google, github, etc.
    provider_id = Column(String, nullable=True)
    
    # Profile information
    grade_level = Column(String, default="10")
    learning_style = Column(String, default="visual")
    emotional_state = Column(String, default="focused")
    teaching_style = Column(String, default="direct")
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    preferences = Column(JSON, default=dict)
    
    # Relationships
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")

class UserSession(Base):
    """User session tracking."""
    __tablename__ = "user_sessions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    session_token = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Session data
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="sessions")

class ChatMessage(Base):
    """Chat message history."""
    __tablename__ = "chat_messages"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    role = Column(String, nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Tool execution data
    tools_used = Column(JSON, nullable=True)
    tool_results = Column(JSON, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="chat_messages")

class ToolUsage(Base):
    """Track tool usage for analytics."""
    __tablename__ = "tool_usage"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    tool_name = Column(String, nullable=False)
    parameters = Column(JSON, nullable=True)
    success = Column(Boolean, nullable=False)
    execution_time = Column(DateTime, default=datetime.utcnow)
    response_data = Column(JSON, nullable=True)
    error_message = Column(String, nullable=True)

class UserPreferences(Base):
    """User preferences and settings."""
    __tablename__ = "user_preferences"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, unique=True)
    
    # UI Preferences
    theme = Column(String, default="dark")
    language = Column(String, default="en")
    notifications_enabled = Column(Boolean, default=True)
    
    # Learning Preferences
    preferred_difficulty = Column(String, default="medium")
    study_reminders = Column(Boolean, default=True)
    progress_tracking = Column(Boolean, default=True)
    
    # Privacy Settings
    data_sharing = Column(Boolean, default=False)
    analytics_tracking = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)