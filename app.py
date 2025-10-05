#!/usr/bin/env python3
"""
Main FastAPI application entry point for AI Tutor Orchestrator.
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
sys.path.append(str(Path(__file__).parent / "src"))

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from typing import Optional
import json
from datetime import datetime

from models.schemas import OrchestrationRequest, OrchestrationResponse
from core.orchestration_agent import OrchestrationAgent
from core.state_manager import StateManager
try:
    from database.database import init_database
    from database.user_service import UserService
    DATABASE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Database imports failed: {e}")
    print("🔄 Running without database support")
    DATABASE_AVAILABLE = False
    
    # Create mock functions for database operations
    async def init_database():
        print("📝 Database disabled - using demo mode")
        pass
    
    class UserService:
        @staticmethod
        async def create_user(*args, **kwargs):
            return None
        
        @staticmethod
        async def get_user_by_email(*args, **kwargs):
            return None
        
        @staticmethod
        async def update_last_login(*args, **kwargs):
            return True
        
        @staticmethod
        async def create_session(*args, **kwargs):
            return type('Session', (), {'session_token': 'demo_token', 'expires_at': datetime.now()})()
        
        @staticmethod
        async def clear_chat_history(*args, **kwargs):
            return True
        
        @staticmethod
        async def export_chat_history(*args, **kwargs):
            return []
        
        @staticmethod
        async def update_user_profile(*args, **kwargs):
            return True

# Load environment variables
load_dotenv()

# Global instances
orchestration_agent: OrchestrationAgent = None
state_manager: StateManager = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global orchestration_agent, state_manager
    
    # Initialize database
    try:
        if DATABASE_AVAILABLE:
            await init_database()
            print("✅ Database initialized")
        else:
            print("📝 Running in demo mode without database")
    except Exception as e:
        print(f"❌ Database initialization failed: {str(e)}")
        print("🔄 Continuing in demo mode")
        # Continue without database for demo mode
    
    # Initialize components with new LLM configuration
    try:
        orchestration_agent = OrchestrationAgent()
        state_manager = StateManager()
        
        # Test LLM connection
        from core.llm_config import test_llm_connection, get_model_info
        model_info = get_model_info()
        print(f"🚀 Initialized with {model_info['provider']} - {model_info['model']}")
        
    except Exception as e:
        print(f"❌ Failed to initialize orchestration agent: {str(e)}")
        raise
    
    yield
    
    # Cleanup if needed
    pass

# Create FastAPI app
app = FastAPI(
    title="AI Tutor Orchestrator",
    description="Intelligent middleware for autonomous AI tutoring systems with 3D web interface",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Also serve CSS and JS directly from root for compatibility
@app.get("/styles.css")
async def serve_styles():
    """Serve styles.css directly."""
    return FileResponse("static/styles.css", media_type="text/css")

@app.get("/script.js")
async def serve_script():
    """Serve script.js directly."""
    return FileResponse("static/script.js", media_type="application/javascript")

@app.get("/login.html")
async def serve_login():
    """Serve login page."""
    return FileResponse("static/login.html", media_type="text/html")

@app.get("/login-styles.css")
async def serve_login_styles():
    """Serve login styles."""
    return FileResponse("static/login-styles.css", media_type="text/css")

@app.get("/login-script.js")
async def serve_login_script():
    """Serve login script."""
    return FileResponse("static/login-script.js", media_type="application/javascript")

def get_orchestration_agent() -> OrchestrationAgent:
    """Dependency to get orchestration agent."""
    if orchestration_agent is None:
        raise HTTPException(status_code=500, detail="Orchestration agent not initialized")
    return orchestration_agent

def get_state_manager() -> StateManager:
    """Dependency to get state manager."""
    if state_manager is None:
        raise HTTPException(status_code=500, detail="State manager not initialized")
    return state_manager

@app.get("/")
async def serve_frontend():
    """Serve the main frontend application."""
    return FileResponse("static/index.html")

@app.get("/dashboard")
async def serve_dashboard():
    """Serve the main dashboard (alias for root)."""
    return FileResponse("static/index.html")

@app.get("/welcome")
async def serve_welcome():
    """Serve the welcome page."""
    return FileResponse("static/welcome.html")

@app.get("/settings")
async def serve_settings():
    """Serve the settings page."""
    return FileResponse("static/settings.html")

@app.get("/settings.html")
async def serve_settings_html():
    """Serve the settings page (alternative route)."""
    return FileResponse("static/settings.html")

@app.get("/settings-script.js")
async def serve_settings_script():
    """Serve settings script."""
    return FileResponse("static/settings-script.js", media_type="application/javascript")

@app.get("/signup.html")
async def serve_signup():
    """Serve the signup page."""
    return FileResponse("static/signup.html", media_type="text/html")

@app.get("/signup")
async def serve_signup_alt():
    """Serve the signup page (alternative route)."""
    return FileResponse("static/signup.html", media_type="text/html")

@app.get("/signup-script.js")
async def serve_signup_script():
    """Serve signup script."""
    return FileResponse("static/signup-script.js", media_type="application/javascript")

@app.post("/orchestrate", response_model=OrchestrationResponse)
async def orchestrate_tools(
    request: OrchestrationRequest,
    agent: OrchestrationAgent = Depends(get_orchestration_agent),
    state_mgr: StateManager = Depends(get_state_manager)
):
    """
    Main orchestration endpoint that processes conversational input and 
    autonomously executes appropriate educational tools.
    """
    try:
        print(f"🎯 Orchestrate request received: {request.current_message}")
        print(f"👤 User: {request.user_info.name} (Grade {request.user_info.grade_level})")
        print(f"🎓 Teaching style: {request.teaching_style}")
        
        # Add current message to conversation history
        from models.schemas import ChatMessage, MessageRole
        current_msg = ChatMessage(role=MessageRole.USER, content=request.current_message)
        await state_mgr.add_conversation_message(request.user_info.user_id, current_msg)
        
        # Execute orchestration
        print("🤖 Starting orchestration...")
        response = await agent.orchestrate(request)
        print(f"✅ Orchestration completed: {response.success}")
        print(f"🛠️ Selected tools: {response.selected_tools}")
        
        # Track tool usage for each executed tool
        for tool_response in response.tool_responses:
            tool_params = response.extracted_parameters.get(tool_response.tool_name, {})
            await state_mgr.track_tool_usage(
                user_id=request.user_info.user_id,
                tool_name=tool_response.tool_name,
                success=tool_response.success,
                parameters=tool_params
            )
        
        # Add assistant response to conversation history
        assistant_msg = ChatMessage(
            role=MessageRole.ASSISTANT, 
            content=f"Executed {len(response.tool_responses)} educational tools: {', '.join(response.selected_tools)}"
        )
        await state_mgr.add_conversation_message(request.user_info.user_id, assistant_msg)
        
        print(f"📤 Sending response with {len(response.tool_responses)} tool results")
        return response
        
    except Exception as e:
        print(f"❌ Orchestration error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Orchestration failed: {str(e)}")

@app.get("/health")
async def health_check(agent: OrchestrationAgent = Depends(get_orchestration_agent)):
    """Health check endpoint that also checks educational tool availability."""
    
    try:
        # Check tool health
        tool_health = await agent.tool_orchestrator.health_check()
        
        return {
            "status": "healthy",
            "orchestrator": "operational",
            "educational_tools": tool_health,
            "all_tools_healthy": all(tool_health.values())
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")

@app.get("/tools")
async def list_available_tools():
    """List all available educational tools and their capabilities."""
    
    return {
        "available_tools": [
            {
                "name": "note_maker",
                "description": "Generates structured notes on educational topics",
                "required_parameters": ["topic", "subject", "note_taking_style"],
                "optional_parameters": ["include_examples", "include_analogies"]
            },
            {
                "name": "flashcard_generator", 
                "description": "Creates flashcards for memorization and review",
                "required_parameters": ["topic", "count", "difficulty", "subject"],
                "optional_parameters": ["include_examples"]
            },
            {
                "name": "concept_explainer",
                "description": "Provides detailed explanations of educational concepts",
                "required_parameters": ["concept_to_explain", "current_topic", "desired_depth"],
                "optional_parameters": []
            }
        ],
        "supported_teaching_styles": ["direct", "socratic", "visual", "flipped_classroom"],
        "supported_emotional_states": ["focused", "anxious", "confused", "tired"]
    }

@app.get("/user/{user_id}/session")
async def get_user_session(
    user_id: str,
    state_mgr: StateManager = Depends(get_state_manager)
):
    """Get user session data and learning patterns."""
    
    try:
        session = await state_mgr.get_user_session(user_id)
        patterns = await state_mgr.get_learning_patterns(user_id)
        preferences = await state_mgr.get_user_preferences(user_id)
        
        return {
            "user_id": user_id,
            "session_active": session is not None,
            "session_data": session,
            "learning_patterns": patterns,
            "preferences": preferences
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve user session: {str(e)}")

@app.post("/user/{user_id}/preferences")
async def update_user_preferences(
    user_id: str,
    preferences: dict,
    state_mgr: StateManager = Depends(get_state_manager)
):
    """Update user learning preferences."""
    
    try:
        await state_mgr.update_user_preferences(user_id, preferences)
        return {"message": "Preferences updated successfully", "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update preferences: {str(e)}")

@app.post("/user/{user_id}/profile")
async def update_user_profile(user_id: str, profile_data: dict):
    """Update user profile information."""
    try:
        success = await UserService.update_user_profile(user_id, profile_data)
        if success:
            return {"success": True, "message": "Profile updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update profile: {str(e)}")

@app.get("/user/{user_id}/chat/history")
async def get_chat_history(user_id: str, limit: int = 50):
    """Get user's chat history."""
    try:
        messages = await UserService.get_chat_history(user_id, limit)
        return {
            "success": True,
            "messages": [
                {
                    "id": msg.id,
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat(),
                    "tools_used": msg.tools_used,
                    "tool_results": msg.tool_results
                }
                for msg in messages
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get chat history: {str(e)}")

@app.delete("/user/{user_id}/chat/history")
async def clear_chat_history(user_id: str):
    """Clear user's chat history."""
    try:
        success = await UserService.clear_chat_history(user_id)
        return {"success": success, "message": "Chat history cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear chat history: {str(e)}")

@app.get("/user/{user_id}/chat/export")
async def export_chat_history(user_id: str):
    """Export user's chat history."""
    try:
        chat_data = await UserService.export_chat_history(user_id)
        
        # Create export data
        export_data = {
            "user_id": user_id,
            "export_date": datetime.utcnow().isoformat(),
            "message_count": len(chat_data),
            "messages": chat_data
        }
        
        return JSONResponse(
            content=export_data,
            headers={
                "Content-Disposition": f"attachment; filename=mentoros_chat_export_{user_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export chat history: {str(e)}")

@app.delete("/user/{user_id}/session")
async def clear_user_session(
    user_id: str,
    state_mgr: StateManager = Depends(get_state_manager)
):
    """Clear user session data."""
    
    try:
        await state_mgr.clear_user_session(user_id)
        return {"message": "Session cleared successfully", "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear session: {str(e)}")

@app.get("/llm/test")
async def test_llm():
    """Test LLM connection and configuration."""
    
    try:
        from core.llm_config import test_llm_connection
        result = await test_llm_connection()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM test failed: {str(e)}")

@app.get("/llm/info")
async def get_llm_info():
    """Get current LLM configuration information."""
    
    try:
        from core.llm_config import get_model_info
        return get_model_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get LLM info: {str(e)}")

@app.post("/analyze")
async def analyze_context_only(
    request: OrchestrationRequest,
    agent: OrchestrationAgent = Depends(get_orchestration_agent)
):
    """Analyze context without executing tools (for testing parameter extraction)."""
    
    try:
        # Just do context analysis and parameter extraction
        intent_analysis = await agent.context_analyzer.analyze_intent(
            chat_history=request.chat_history,
            current_message=request.current_message,
            user_info=request.user_info
        )
        
        if intent_analysis.get("tools_needed"):
            extracted_params = await agent.context_analyzer.extract_parameters(
                tools_needed=intent_analysis["tools_needed"],
                chat_history=request.chat_history,
                current_message=request.current_message,
                user_info=request.user_info
            )
            
            # Apply teaching style adaptations
            adapted_params = agent._adapt_for_teaching_style(
                extracted_params,
                request.teaching_style,
                request.user_info
            )
        else:
            adapted_params = {}
        
        return {
            "success": True,
            "intent_analysis": intent_analysis,
            "extracted_parameters": adapted_params,
            "message": "Context analysis completed successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Context analysis failed: {str(e)}")

@app.post("/demo-tools")
async def demo_educational_tools(
    request: dict
):
    """Demo endpoint to show educational tool capabilities."""
    
    try:
        from core.mock_tools import mock_tools
        from models.schemas import UserInfo
        
        # Create demo user
        demo_user = UserInfo(
            user_id="demo_user",
            name="Demo Student",
            grade_level="10",
            learning_style_summary="Visual learner, prefers examples",
            emotional_state_summary="Focused and motivated",
            mastery_level_summary="Level 5: Developing competence"
        )
        
        tool_name = request.get("tool", "note_maker")
        params = request.get("params", {})
        
        if tool_name == "note_maker":
            result = await mock_tools.execute_note_maker(params, demo_user)
        elif tool_name == "flashcard_generator":
            result = await mock_tools.execute_flashcard_generator(params, demo_user)
        elif tool_name == "concept_explainer":
            result = await mock_tools.execute_concept_explainer(params, demo_user)
        else:
            raise HTTPException(status_code=400, detail="Unknown tool")
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Demo tool execution failed: {str(e)}")

@app.get("/favicon.ico")
async def favicon():
    """Serve favicon."""
    return FileResponse("static/favicon.png", media_type="image/png")

@app.get("/favicon.png")
async def favicon_png():
    """Serve favicon PNG."""
    return FileResponse("static/favicon.png", media_type="image/png")

@app.post("/auth/login")
async def login(request: Request):
    """Handle user login."""
    try:
        body = await request.json()
        email = body.get("email")
        password = body.get("password")
        provider = body.get("provider")
        
        if not email:
            raise HTTPException(status_code=400, detail="Email is required")
        
        # For demo purposes, accept any email/password
        # In production, you would verify credentials here
        
        # Get or create user
        user = await UserService.get_user_by_email(email)
        if not user:
            name = email.split("@")[0].title()
            user = await UserService.create_user(
                email=email,
                name=name,
                provider=provider
            )
        
        # Update last login
        await UserService.update_last_login(user.id)
        
        # Create session
        client_ip = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        session = await UserService.create_session(
            user_id=user.id,
            ip_address=client_ip,
            user_agent=user_agent
        )
        
        return {
            "success": True,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "grade_level": user.grade_level,
                "learning_style": user.learning_style,
                "emotional_state": user.emotional_state,
                "teaching_style": user.teaching_style
            },
            "session_token": session.session_token,
            "expires_at": session.expires_at.isoformat()
        }
        
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@app.post("/auth/signup")
async def signup(request: Request):
    """Handle user signup."""
    try:
        body = await request.json()
        name = body.get("name")
        email = body.get("email")
        password = body.get("password")
        provider = body.get("provider")
        grade_level = body.get("grade_level", "10")
        
        if not email or not name:
            raise HTTPException(status_code=400, detail="Name and email are required")
        
        # Check if user already exists
        existing_user = await UserService.get_user_by_email(email)
        if existing_user:
            raise HTTPException(status_code=400, detail="An account with this email already exists")
        
        # Create new user
        user = await UserService.create_user(
            email=email,
            name=name,
            provider=provider,
            grade_level=grade_level
        )
        
        # Create session
        client_ip = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")
        session = await UserService.create_session(
            user_id=user.id,
            ip_address=client_ip,
            user_agent=user_agent
        )
        
        return {
            "success": True,
            "message": "Account created successfully",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "grade_level": user.grade_level,
                "learning_style": user.learning_style,
                "emotional_state": user.emotional_state,
                "teaching_style": user.teaching_style
            },
            "session_token": session.session_token,
            "expires_at": session.expires_at.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Signup error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Signup failed: {str(e)}")

@app.post("/auth/logout")
async def logout(request: Request):
    """Handle user logout."""
    try:
        body = await request.json()
        session_token = body.get("session_token")
        
        if session_token:
            await UserService.invalidate_session(session_token)
        
        return {"success": True, "message": "Logged out successfully"}
        
    except Exception as e:
        print(f"❌ Logout error: {str(e)}")
        return {"success": True, "message": "Logged out"}  # Always succeed for logout

@app.get("/auth/verify")
async def verify_session(session_token: str):
    """Verify user session."""
    try:
        session = await UserService.get_session(session_token)
        if not session:
            raise HTTPException(status_code=401, detail="Invalid or expired session")
        
        user = await UserService.get_user_by_id(session.user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return {
            "valid": True,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "grade_level": user.grade_level,
                "learning_style": user.learning_style,
                "emotional_state": user.emotional_state,
                "teaching_style": user.teaching_style
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Session verification error: {str(e)}")
        raise HTTPException(status_code=500, detail="Session verification failed")

@app.get("/test")
async def test_endpoint():
    """Simple test endpoint to verify API connectivity."""
    print("🧪 Test endpoint called")
    return {"message": "Backend is working!", "timestamp": "2024-01-01T00:00:00Z"}

@app.post("/test-orchestrate")
async def test_orchestrate():
    """Test orchestration without dependencies."""
    return {
        "success": True,
        "selected_tools": ["test_tool"],
        "extracted_parameters": {"test_tool": {"param1": "value1"}},
        "tool_responses": [
            {
                "success": True,
                "tool_name": "test_tool",
                "data": {"message": "Test successful"},
                "error_message": None
            }
        ],
        "reasoning": "This is a test response",
        "error_message": None
    }

# For development
if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", "8000"))
    
    print(f"🚀 AI Tutor Orchestrator - 3D Web Interface")
    print(f"🌐 Starting server on http://{host}:{port}")
    print(f"🧠 Using DeepSeek AI via OpenRouter")
    print(f"📚 Ready to orchestrate educational tools autonomously!")
    print(f"✨ Features: Dark 3D theme, smooth animations, real-time chat")
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )