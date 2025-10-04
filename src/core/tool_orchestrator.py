from typing import Dict, Any, List, Optional
import httpx
import asyncio
from models.schemas import (
    UserInfo, ChatMessage, NoteRequest, FlashcardRequest, 
    ConceptRequest, ToolResponse, NoteStyle, DifficultyLevel, DepthLevel
)
import os
from dotenv import load_dotenv
from .mock_tools import mock_tools

load_dotenv()

class ToolOrchestrator:
    """Orchestrates API calls to educational tools with proper schema validation."""
    
    def __init__(self):
        self.tool_endpoints = {
            "note_maker": os.getenv("NOTE_MAKER_API_URL", "http://localhost:8001/api/note-maker"),
            "flashcard_generator": os.getenv("FLASHCARD_API_URL", "http://localhost:8002/api/flashcard-generator"),
            "concept_explainer": os.getenv("CONCEPT_EXPLAINER_API_URL", "http://localhost:8003/api/concept-explainer")
        }
        self.timeout = httpx.Timeout(30.0)
    
    async def execute_tools(self, tool_parameters: Dict[str, Dict[str, Any]], 
                          user_info: UserInfo, chat_history: List[ChatMessage]) -> List[ToolResponse]:
        """Execute multiple tools concurrently with proper parameter validation."""
        
        tasks = []
        for tool_name, params in tool_parameters.items():
            if tool_name in self.tool_endpoints:
                task = self._execute_single_tool(tool_name, params, user_info, chat_history)
                tasks.append(task)
        
        if not tasks:
            return []
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Convert exceptions to error responses
        tool_responses = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                tool_name = list(tool_parameters.keys())[i]
                tool_responses.append(ToolResponse(
                    success=False,
                    tool_name=tool_name,
                    data={},
                    error_message=str(result)
                ))
            else:
                tool_responses.append(result)
        
        return tool_responses
    
    async def _execute_single_tool(self, tool_name: str, params: Dict[str, Any], 
                                 user_info: UserInfo, chat_history: List[ChatMessage]) -> ToolResponse:
        """Execute a single educational tool with proper request formatting."""
        
        try:
            # First try to use mock tools for demonstration
            if tool_name == "note_maker":
                return await mock_tools.execute_note_maker(params, user_info)
            elif tool_name == "flashcard_generator":
                return await mock_tools.execute_flashcard_generator(params, user_info)
            elif tool_name == "concept_explainer":
                return await mock_tools.execute_concept_explainer(params, user_info)
            
            # If mock tools don't handle it, try real API
            # Validate and format request based on tool type
            if tool_name == "note_maker":
                request_data = self._format_note_request(params, user_info, chat_history)
            elif tool_name == "flashcard_generator":
                request_data = self._format_flashcard_request(params, user_info)
            elif tool_name == "concept_explainer":
                request_data = self._format_concept_request(params, user_info, chat_history)
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
            
            # Make API call
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.tool_endpoints[tool_name],
                    json=request_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    return ToolResponse(
                        success=True,
                        tool_name=tool_name,
                        data=response.json()
                    )
                else:
                    # Fall back to mock if real API fails
                    print(f"Real API failed for {tool_name}, using mock response")
                    if tool_name == "note_maker":
                        return await mock_tools.execute_note_maker(params, user_info)
                    elif tool_name == "flashcard_generator":
                        return await mock_tools.execute_flashcard_generator(params, user_info)
                    elif tool_name == "concept_explainer":
                        return await mock_tools.execute_concept_explainer(params, user_info)
        
        except Exception as e:
            # Fall back to mock tools on any error
            print(f"Error with {tool_name}, using mock response: {str(e)}")
            try:
                if tool_name == "note_maker":
                    return await mock_tools.execute_note_maker(params, user_info)
                elif tool_name == "flashcard_generator":
                    return await mock_tools.execute_flashcard_generator(params, user_info)
                elif tool_name == "concept_explainer":
                    return await mock_tools.execute_concept_explainer(params, user_info)
            except Exception as mock_error:
                return ToolResponse(
                    success=False,
                    tool_name=tool_name,
                    data={},
                    error_message=f"Both real API and mock failed: {str(mock_error)}"
                )
    
    def _format_note_request(self, params: Dict[str, Any], user_info: UserInfo, 
                           chat_history: List[ChatMessage]) -> Dict[str, Any]:
        """Format parameters for Note Maker tool."""
        
        # Validate and set defaults
        note_style = params.get("note_taking_style", "outline")
        if note_style not in ["outline", "bullet_points", "narrative", "structured"]:
            note_style = "outline"
        
        return {
            "user_info": {
                "user_id": user_info.user_id,
                "name": user_info.name,
                "grade_level": user_info.grade_level,
                "learning_style_summary": user_info.learning_style_summary,
                "emotional_state_summary": user_info.emotional_state_summary,
                "mastery_level_summary": user_info.mastery_level_summary
            },
            "chat_history": [{"role": msg.role, "content": msg.content} for msg in chat_history],
            "topic": params.get("topic", "General Study"),
            "subject": params.get("subject", "General"),
            "note_taking_style": note_style,
            "include_examples": params.get("include_examples", True),
            "include_analogies": params.get("include_analogies", False)
        }
    
    def _format_flashcard_request(self, params: Dict[str, Any], user_info: UserInfo) -> Dict[str, Any]:
        """Format parameters for Flashcard Generator tool."""
        
        # Validate count
        count = params.get("count", 5)
        count = max(1, min(20, count))  # Ensure within valid range
        
        # Validate difficulty
        difficulty = params.get("difficulty", "medium")
        if difficulty not in ["easy", "medium", "hard"]:
            difficulty = "medium"
        
        return {
            "user_info": {
                "user_id": user_info.user_id,
                "name": user_info.name,
                "grade_level": user_info.grade_level,
                "learning_style_summary": user_info.learning_style_summary,
                "emotional_state_summary": user_info.emotional_state_summary,
                "mastery_level_summary": user_info.mastery_level_summary
            },
            "topic": params.get("topic", "General Study"),
            "count": count,
            "difficulty": difficulty,
            "subject": params.get("subject", "General"),
            "include_examples": params.get("include_examples", True)
        }
    
    def _format_concept_request(self, params: Dict[str, Any], user_info: UserInfo, 
                              chat_history: List[ChatMessage]) -> Dict[str, Any]:
        """Format parameters for Concept Explainer tool."""
        
        # Validate depth
        depth = params.get("desired_depth", "intermediate")
        if depth not in ["basic", "intermediate", "advanced", "comprehensive"]:
            depth = "intermediate"
        
        return {
            "user_info": {
                "user_id": user_info.user_id,
                "name": user_info.name,
                "grade_level": user_info.grade_level,
                "learning_style_summary": user_info.learning_style_summary,
                "emotional_state_summary": user_info.emotional_state_summary,
                "mastery_level_summary": user_info.mastery_level_summary
            },
            "chat_history": [{"role": msg.role, "content": msg.content} for msg in chat_history],
            "concept_to_explain": params.get("concept_to_explain", "basic concepts"),
            "current_topic": params.get("current_topic", "General"),
            "desired_depth": depth
        }
    
    def validate_parameters(self, tool_name: str, params: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate parameters for a specific tool."""
        
        try:
            if tool_name == "note_maker":
                required_fields = ["topic", "subject", "note_taking_style"]
                for field in required_fields:
                    if field not in params:
                        return False, f"Missing required field: {field}"
                
                if params["note_taking_style"] not in ["outline", "bullet_points", "narrative", "structured"]:
                    return False, "Invalid note_taking_style"
            
            elif tool_name == "flashcard_generator":
                required_fields = ["topic", "count", "difficulty", "subject"]
                for field in required_fields:
                    if field not in params:
                        return False, f"Missing required field: {field}"
                
                if not (1 <= params["count"] <= 20):
                    return False, "Count must be between 1 and 20"
                
                if params["difficulty"] not in ["easy", "medium", "hard"]:
                    return False, "Invalid difficulty level"
            
            elif tool_name == "concept_explainer":
                required_fields = ["concept_to_explain", "current_topic", "desired_depth"]
                for field in required_fields:
                    if field not in params:
                        return False, f"Missing required field: {field}"
                
                if params["desired_depth"] not in ["basic", "intermediate", "advanced", "comprehensive"]:
                    return False, "Invalid desired_depth"
            
            return True, None
            
        except Exception as e:
            return False, str(e)
    
    async def health_check(self) -> Dict[str, bool]:
        """Check health status of all educational tools."""
        
        health_status = {}
        
        async def check_tool_health(tool_name: str, endpoint: str) -> tuple[str, bool]:
            try:
                async with httpx.AsyncClient(timeout=httpx.Timeout(5.0)) as client:
                    response = await client.get(f"{endpoint}/health")
                    return tool_name, response.status_code == 200
            except:
                return tool_name, False
        
        tasks = [check_tool_health(name, endpoint) for name, endpoint in self.tool_endpoints.items()]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, tuple):
                tool_name, is_healthy = result
                health_status[tool_name] = is_healthy
            else:
                # Handle exception case
                health_status["unknown"] = False
        
        return health_status