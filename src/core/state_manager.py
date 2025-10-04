from typing import Dict, Any, Optional, List
import json
import asyncio
from datetime import datetime, timedelta
from models.schemas import UserInfo, ChatMessage

class StateManager:
    """Manages conversation state and student personalization context."""
    
    def __init__(self):
        # In-memory storage for demo purposes
        # In production, this would use Redis or a database
        self.user_sessions: Dict[str, Dict[str, Any]] = {}
        self.conversation_history: Dict[str, List[ChatMessage]] = {}
        self.user_preferences: Dict[str, Dict[str, Any]] = {}
        self.session_timeout = timedelta(hours=2)
    
    async def get_user_session(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve user session data."""
        
        session = self.user_sessions.get(user_id)
        
        if session:
            # Check if session is expired
            last_activity = datetime.fromisoformat(session.get("last_activity", ""))
            if datetime.now() - last_activity > self.session_timeout:
                # Session expired, clean up
                await self.clear_user_session(user_id)
                return None
        
        return session
    
    async def update_user_session(self, user_id: str, session_data: Dict[str, Any]) -> None:
        """Update user session with new data."""
        
        current_session = self.user_sessions.get(user_id, {})
        current_session.update(session_data)
        current_session["last_activity"] = datetime.now().isoformat()
        
        self.user_sessions[user_id] = current_session
    
    async def clear_user_session(self, user_id: str) -> None:
        """Clear user session data."""
        
        if user_id in self.user_sessions:
            del self.user_sessions[user_id]
        
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]
    
    async def add_conversation_message(self, user_id: str, message: ChatMessage) -> None:
        """Add a message to conversation history."""
        
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append(message)
        
        # Keep only last 20 messages to manage memory
        if len(self.conversation_history[user_id]) > 20:
            self.conversation_history[user_id] = self.conversation_history[user_id][-20:]
        
        # Update session activity
        await self.update_user_session(user_id, {})
    
    async def get_conversation_history(self, user_id: str, limit: int = 10) -> List[ChatMessage]:
        """Retrieve recent conversation history."""
        
        history = self.conversation_history.get(user_id, [])
        return history[-limit:] if limit > 0 else history
    
    async def update_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> None:
        """Update user learning preferences."""
        
        current_prefs = self.user_preferences.get(user_id, {})
        current_prefs.update(preferences)
        self.user_preferences[user_id] = current_prefs
        
        # Also update session
        await self.update_user_session(user_id, {"preferences": current_prefs})
    
    async def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Retrieve user learning preferences."""
        
        return self.user_preferences.get(user_id, {})
    
    async def track_tool_usage(self, user_id: str, tool_name: str, success: bool, 
                             parameters: Dict[str, Any]) -> None:
        """Track tool usage for analytics and personalization."""
        
        session = await self.get_user_session(user_id) or {}
        
        if "tool_usage" not in session:
            session["tool_usage"] = []
        
        usage_record = {
            "tool_name": tool_name,
            "success": success,
            "parameters": parameters,
            "timestamp": datetime.now().isoformat()
        }
        
        session["tool_usage"].append(usage_record)
        
        # Keep only last 50 usage records
        if len(session["tool_usage"]) > 50:
            session["tool_usage"] = session["tool_usage"][-50:]
        
        await self.update_user_session(user_id, session)
    
    async def get_learning_patterns(self, user_id: str) -> Dict[str, Any]:
        """Analyze user learning patterns from session data."""
        
        session = await self.get_user_session(user_id)
        if not session or "tool_usage" not in session:
            return {}
        
        tool_usage = session["tool_usage"]
        
        # Analyze patterns
        patterns = {
            "most_used_tools": self._get_most_used_tools(tool_usage),
            "success_rates": self._calculate_success_rates(tool_usage),
            "preferred_difficulty": self._infer_preferred_difficulty(tool_usage),
            "learning_frequency": self._calculate_learning_frequency(tool_usage),
            "topic_interests": self._extract_topic_interests(tool_usage)
        }
        
        return patterns
    
    def _get_most_used_tools(self, tool_usage: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get most frequently used tools."""
        
        tool_counts = {}
        for usage in tool_usage:
            tool_name = usage["tool_name"]
            tool_counts[tool_name] = tool_counts.get(tool_name, 0) + 1
        
        # Sort by usage count
        return dict(sorted(tool_counts.items(), key=lambda x: x[1], reverse=True))
    
    def _calculate_success_rates(self, tool_usage: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate success rates for each tool."""
        
        tool_stats = {}
        
        for usage in tool_usage:
            tool_name = usage["tool_name"]
            if tool_name not in tool_stats:
                tool_stats[tool_name] = {"total": 0, "successful": 0}
            
            tool_stats[tool_name]["total"] += 1
            if usage["success"]:
                tool_stats[tool_name]["successful"] += 1
        
        # Calculate success rates
        success_rates = {}
        for tool_name, stats in tool_stats.items():
            success_rates[tool_name] = stats["successful"] / stats["total"] if stats["total"] > 0 else 0
        
        return success_rates
    
    def _infer_preferred_difficulty(self, tool_usage: List[Dict[str, Any]]) -> str:
        """Infer user's preferred difficulty level."""
        
        difficulty_counts = {"easy": 0, "medium": 0, "hard": 0}
        
        for usage in tool_usage:
            params = usage.get("parameters", {})
            difficulty = params.get("difficulty")
            if difficulty in difficulty_counts:
                difficulty_counts[difficulty] += 1
        
        # Return most common difficulty
        if max(difficulty_counts.values()) == 0:
            return "medium"  # Default
        
        return max(difficulty_counts, key=difficulty_counts.get)
    
    def _calculate_learning_frequency(self, tool_usage: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate learning frequency patterns."""
        
        if not tool_usage:
            return {}
        
        # Group by day
        daily_usage = {}
        for usage in tool_usage:
            timestamp = datetime.fromisoformat(usage["timestamp"])
            date_key = timestamp.date().isoformat()
            daily_usage[date_key] = daily_usage.get(date_key, 0) + 1
        
        # Calculate average sessions per day
        if daily_usage:
            avg_sessions_per_day = sum(daily_usage.values()) / len(daily_usage)
        else:
            avg_sessions_per_day = 0
        
        return {
            "avg_sessions_per_day": avg_sessions_per_day,
            "total_learning_days": len(daily_usage),
            "most_active_day": max(daily_usage, key=daily_usage.get) if daily_usage else None
        }
    
    def _extract_topic_interests(self, tool_usage: List[Dict[str, Any]]) -> Dict[str, int]:
        """Extract topics the user is most interested in."""
        
        topic_counts = {}
        
        for usage in tool_usage:
            params = usage.get("parameters", {})
            topic = params.get("topic") or params.get("concept_to_explain")
            
            if topic:
                topic_lower = topic.lower()
                topic_counts[topic_lower] = topic_counts.get(topic_lower, 0) + 1
        
        # Return top topics
        return dict(sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:10])
    
    async def get_personalization_context(self, user_info: UserInfo) -> Dict[str, Any]:
        """Get comprehensive personalization context for a user."""
        
        user_id = user_info.user_id
        
        # Gather all personalization data
        session = await self.get_user_session(user_id) or {}
        preferences = await self.get_user_preferences(user_id)
        learning_patterns = await self.get_learning_patterns(user_id)
        recent_history = await self.get_conversation_history(user_id, limit=5)
        
        return {
            "user_info": {
                "user_id": user_info.user_id,
                "name": user_info.name,
                "grade_level": user_info.grade_level,
                "learning_style_summary": user_info.learning_style_summary,
                "emotional_state_summary": user_info.emotional_state_summary,
                "mastery_level_summary": user_info.mastery_level_summary
            },
            "session_data": session,
            "preferences": preferences,
            "learning_patterns": learning_patterns,
            "recent_conversations": [
                {"role": msg.role, "content": msg.content} for msg in recent_history
            ]
        }