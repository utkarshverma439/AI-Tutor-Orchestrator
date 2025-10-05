"""
User service for handling authentication and user management.
"""

import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User, UserSession, ChatMessage, ToolUsage, UserPreferences
from .database import get_db_session

class UserService:
    """Service for user management operations."""
    
    @staticmethod
    async def create_user(
        email: str,
        name: str,
        provider: Optional[str] = None,
        provider_id: Optional[str] = None,
        **profile_data
    ) -> User:
        """Create a new user."""
        async with get_db_session() as session:
            # Check if user already exists
            existing_user = await UserService.get_user_by_email(email)
            if existing_user:
                return existing_user
            
            user = User(
                email=email,
                name=name,
                provider=provider,
                provider_id=provider_id,
                grade_level=profile_data.get('grade_level', '10'),
                learning_style=profile_data.get('learning_style', 'visual'),
                emotional_state=profile_data.get('emotional_state', 'focused'),
                teaching_style=profile_data.get('teaching_style', 'direct'),
                preferences=profile_data.get('preferences', {})
            )
            
            session.add(user)
            await session.commit()
            await session.refresh(user)
            
            # Create default preferences
            await UserService.create_user_preferences(user.id)
            
            return user
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        """Get user by email."""
        async with get_db_session() as session:
            result = await session.execute(
                select(User).where(User.email == email)
            )
            return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[User]:
        """Get user by ID."""
        async with get_db_session() as session:
            result = await session.execute(
                select(User).where(User.id == user_id)
            )
            return result.scalar_one_or_none()
    
    @staticmethod
    async def update_user_profile(user_id: str, profile_data: Dict[str, Any]) -> bool:
        """Update user profile information."""
        async with get_db_session() as session:
            result = await session.execute(
                update(User)
                .where(User.id == user_id)
                .values(**profile_data)
            )
            await session.commit()
            return result.rowcount > 0
    
    @staticmethod
    async def update_last_login(user_id: str) -> bool:
        """Update user's last login timestamp."""
        async with get_db_session() as session:
            result = await session.execute(
                update(User)
                .where(User.id == user_id)
                .values(last_login=datetime.utcnow())
            )
            await session.commit()
            return result.rowcount > 0
    
    @staticmethod
    async def create_session(
        user_id: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        expires_in_hours: int = 24
    ) -> UserSession:
        """Create a new user session."""
        async with get_db_session() as session:
            session_token = secrets.token_urlsafe(32)
            expires_at = datetime.utcnow() + timedelta(hours=expires_in_hours)
            
            user_session = UserSession(
                user_id=user_id,
                session_token=session_token,
                expires_at=expires_at,
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            session.add(user_session)
            await session.commit()
            await session.refresh(user_session)
            
            return user_session
    
    @staticmethod
    async def get_session(session_token: str) -> Optional[UserSession]:
        """Get session by token."""
        async with get_db_session() as session:
            result = await session.execute(
                select(UserSession)
                .where(UserSession.session_token == session_token)
                .where(UserSession.is_active == True)
                .where(UserSession.expires_at > datetime.utcnow())
            )
            return result.scalar_one_or_none()
    
    @staticmethod
    async def invalidate_session(session_token: str) -> bool:
        """Invalidate a user session."""
        async with get_db_session() as session:
            result = await session.execute(
                update(UserSession)
                .where(UserSession.session_token == session_token)
                .values(is_active=False)
            )
            await session.commit()
            return result.rowcount > 0
    
    @staticmethod
    async def save_chat_message(
        user_id: str,
        role: str,
        content: str,
        tools_used: Optional[List[str]] = None,
        tool_results: Optional[Dict] = None
    ) -> ChatMessage:
        """Save a chat message."""
        async with get_db_session() as session:
            message = ChatMessage(
                user_id=user_id,
                role=role,
                content=content,
                tools_used=tools_used,
                tool_results=tool_results
            )
            
            session.add(message)
            await session.commit()
            await session.refresh(message)
            
            return message
    
    @staticmethod
    async def get_chat_history(user_id: str, limit: int = 50) -> List[ChatMessage]:
        """Get user's chat history."""
        async with get_db_session() as session:
            result = await session.execute(
                select(ChatMessage)
                .where(ChatMessage.user_id == user_id)
                .order_by(ChatMessage.timestamp.desc())
                .limit(limit)
            )
            messages = result.scalars().all()
            return list(reversed(messages))  # Return in chronological order
    
    @staticmethod
    async def clear_chat_history(user_id: str) -> bool:
        """Clear user's chat history."""
        async with get_db_session() as session:
            result = await session.execute(
                delete(ChatMessage).where(ChatMessage.user_id == user_id)
            )
            await session.commit()
            return result.rowcount > 0
    
    @staticmethod
    async def export_chat_history(user_id: str) -> List[Dict]:
        """Export user's chat history as JSON."""
        messages = await UserService.get_chat_history(user_id, limit=1000)
        return [
            {
                "timestamp": msg.timestamp.isoformat(),
                "role": msg.role,
                "content": msg.content,
                "tools_used": msg.tools_used,
                "tool_results": msg.tool_results
            }
            for msg in messages
        ]
    
    @staticmethod
    async def log_tool_usage(
        user_id: str,
        tool_name: str,
        parameters: Dict,
        success: bool,
        response_data: Optional[Dict] = None,
        error_message: Optional[str] = None
    ) -> ToolUsage:
        """Log tool usage for analytics."""
        async with get_db_session() as session:
            usage = ToolUsage(
                user_id=user_id,
                tool_name=tool_name,
                parameters=parameters,
                success=success,
                response_data=response_data,
                error_message=error_message
            )
            
            session.add(usage)
            await session.commit()
            await session.refresh(usage)
            
            return usage
    
    @staticmethod
    async def create_user_preferences(user_id: str) -> UserPreferences:
        """Create default user preferences."""
        async with get_db_session() as session:
            preferences = UserPreferences(user_id=user_id)
            session.add(preferences)
            await session.commit()
            await session.refresh(preferences)
            return preferences
    
    @staticmethod
    async def get_user_preferences(user_id: str) -> Optional[UserPreferences]:
        """Get user preferences."""
        async with get_db_session() as session:
            result = await session.execute(
                select(UserPreferences).where(UserPreferences.user_id == user_id)
            )
            return result.scalar_one_or_none()
    
    @staticmethod
    async def update_user_preferences(user_id: str, preferences_data: Dict[str, Any]) -> bool:
        """Update user preferences."""
        async with get_db_session() as session:
            result = await session.execute(
                update(UserPreferences)
                .where(UserPreferences.user_id == user_id)
                .values(**preferences_data, updated_at=datetime.utcnow())
            )
            await session.commit()
            return result.rowcount > 0