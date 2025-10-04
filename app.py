#!/usr/bin/env python3
"""
Main FastAPI application entry point for AI Tutor Orchestrator.
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
sys.path.append(str(Path(__file__).parent / "src"))

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from models.schemas import OrchestrationRequest, OrchestrationResponse
from core.orchestration_agent import OrchestrationAgent
from core.state_manager import StateManager

# Load environment variables
load_dotenv()

# Global instances
orchestration_agent: OrchestrationAgent = None
state_manager: StateManager = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global orchestration_agent, state_manager
    
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
    return FileResponse("static/favicon.ico", status_code=404)

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