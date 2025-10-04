from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class ChatMessage(BaseModel):
    role: MessageRole
    content: str

class UserInfo(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the student")
    name: str = Field(..., description="Student's full name")
    grade_level: str = Field(..., description="Student's current grade level")
    learning_style_summary: str = Field(..., description="Summary of student's preferred learning style")
    emotional_state_summary: str = Field(..., description="Current emotional state of the student")
    mastery_level_summary: str = Field(..., description="Current mastery level description")

class TeachingStyle(str, Enum):
    DIRECT = "direct"
    SOCRATIC = "socratic"
    VISUAL = "visual"
    FLIPPED_CLASSROOM = "flipped_classroom"

class EmotionalState(str, Enum):
    FOCUSED = "focused"
    ANXIOUS = "anxious"
    CONFUSED = "confused"
    TIRED = "tired"

class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class DepthLevel(str, Enum):
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    COMPREHENSIVE = "comprehensive"

class NoteStyle(str, Enum):
    OUTLINE = "outline"
    BULLET_POINTS = "bullet_points"
    NARRATIVE = "narrative"
    STRUCTURED = "structured"

# Request Models
class OrchestrationRequest(BaseModel):
    user_info: UserInfo
    chat_history: List[ChatMessage]
    current_message: str
    teaching_style: Optional[TeachingStyle] = TeachingStyle.DIRECT
    
class NoteRequest(BaseModel):
    user_info: UserInfo
    chat_history: List[ChatMessage]
    topic: str
    subject: str
    note_taking_style: NoteStyle
    include_examples: bool = True
    include_analogies: bool = False

class FlashcardRequest(BaseModel):
    user_info: UserInfo
    topic: str
    count: int = Field(..., ge=1, le=20)
    difficulty: DifficultyLevel
    subject: str
    include_examples: bool = True

class ConceptRequest(BaseModel):
    user_info: UserInfo
    chat_history: List[ChatMessage]
    concept_to_explain: str
    current_topic: str
    desired_depth: DepthLevel

# Response Models
class ToolResponse(BaseModel):
    success: bool
    tool_name: str
    data: Dict[str, Any]
    error_message: Optional[str] = None

class OrchestrationResponse(BaseModel):
    success: bool
    selected_tools: List[str]
    extracted_parameters: Dict[str, Any]
    tool_responses: List[ToolResponse]
    reasoning: str
    error_message: Optional[str] = None
    context_analysis: Optional[Dict[str, Any]] = None