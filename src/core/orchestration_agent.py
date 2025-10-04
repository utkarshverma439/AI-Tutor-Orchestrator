from typing import Dict, Any, List, Optional, TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from models.schemas import (
    OrchestrationRequest, OrchestrationResponse, UserInfo, 
    ChatMessage, ToolResponse, TeachingStyle
)
from core.context_analyzer import ContextAnalyzer
from core.tool_orchestrator import ToolOrchestrator
from core.state_manager import StateManager
from core.llm_config import create_llm
import json

class OrchestrationState(TypedDict):
    """State object for the orchestration workflow."""
    request: Optional[OrchestrationRequest]
    intent_analysis: Dict[str, Any]
    extracted_parameters: Dict[str, Dict[str, Any]]
    validation_results: Dict[str, tuple]
    tool_responses: List[ToolResponse]
    reasoning: str
    error_message: Optional[str]
    success: bool

class OrchestrationAgent:
    """Main orchestration agent using LangGraph workflow."""
    
    def __init__(self, api_key: Optional[str] = None):
        # Use the new LLM configuration system
        self.llm = create_llm()
        self.context_analyzer = ContextAnalyzer(self.llm)
        self.tool_orchestrator = ToolOrchestrator()
        self.state_manager = StateManager()
        
        # Build the workflow graph
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow for orchestration."""
        
        workflow = StateGraph(OrchestrationState)
        
        # Add nodes
        workflow.add_node("analyze_context", self._analyze_context_node)
        workflow.add_node("extract_parameters", self._extract_parameters_node)
        workflow.add_node("validate_parameters", self._validate_parameters_node)
        workflow.add_node("execute_tools", self._execute_tools_node)
        workflow.add_node("generate_response", self._generate_response_node)
        workflow.add_node("handle_error", self._handle_error_node)
        
        # Define the flow
        workflow.set_entry_point("analyze_context")
        
        workflow.add_edge("analyze_context", "extract_parameters")
        workflow.add_edge("extract_parameters", "validate_parameters")
        
        # Conditional edge based on validation
        workflow.add_conditional_edges(
            "validate_parameters",
            self._should_execute_tools,
            {
                "execute": "execute_tools",
                "error": "handle_error"
            }
        )
        
        workflow.add_edge("execute_tools", "generate_response")
        workflow.add_edge("generate_response", END)
        workflow.add_edge("handle_error", END)
        
        return workflow.compile()
    
    async def orchestrate(self, request: OrchestrationRequest) -> OrchestrationResponse:
        """Main orchestration method."""
        
        # Initialize state
        state: OrchestrationState = {
            "request": request,
            "intent_analysis": {},
            "extracted_parameters": {},
            "validation_results": {},
            "tool_responses": [],
            "reasoning": "",
            "error_message": None,
            "success": False
        }
        
        try:
            # Execute the workflow
            final_state = await self.workflow.ainvoke(state)
            
            # Build response
            return OrchestrationResponse(
                success=final_state["success"],
                selected_tools=list(final_state["extracted_parameters"].keys()),
                extracted_parameters=final_state["extracted_parameters"],
                tool_responses=final_state["tool_responses"],
                reasoning=final_state["reasoning"],
                error_message=final_state["error_message"],
                context_analysis=final_state.get("intent_analysis")
            )
            
        except Exception as e:
            return OrchestrationResponse(
                success=False,
                selected_tools=[],
                extracted_parameters={},
                tool_responses=[],
                reasoning="Workflow execution failed",
                error_message=str(e)
            )
    
    async def _analyze_context_node(self, state: OrchestrationState) -> OrchestrationState:
        """Analyze conversation context and determine required tools."""
        
        try:
            # Context analyzer returns dict with analysis results
            intent_analysis = await self.context_analyzer.analyze_intent(
                chat_history=state["request"].chat_history,
                current_message=state["request"].current_message,
                user_info=state["request"].user_info
            )
            
            state["intent_analysis"] = intent_analysis
            tools_needed = intent_analysis.get("tools_needed", [])
            state["reasoning"] += f"Intent Analysis: Identified {len(tools_needed)} tools needed. "
            
        except Exception as e:
            state["error_message"] = f"Context analysis failed: {str(e)}"
        
        return state
    
    async def _extract_parameters_node(self, state: OrchestrationState) -> OrchestrationState:
        """Extract parameters for each required tool."""
        
        try:
            tools_needed = state["intent_analysis"].get("tools_needed", [])
            
            if not tools_needed:
                state["error_message"] = "No tools identified from context analysis"
                return state
            
            extracted_params = await self.context_analyzer.extract_parameters(
                tools_needed=tools_needed,
                chat_history=state["request"].chat_history,
                current_message=state["request"].current_message,
                user_info=state["request"].user_info
            )
            
            # Apply teaching style adaptations
            adapted_params = self._adapt_for_teaching_style(
                extracted_params, 
                state["request"].teaching_style,
                state["request"].user_info
            )
            
            state["extracted_parameters"] = adapted_params
            state["reasoning"] += f"Parameter Extraction: Extracted parameters for {len(adapted_params)} tools. "
            
        except Exception as e:
            state["error_message"] = f"Parameter extraction failed: {str(e)}"
        
        return state
    
    async def _validate_parameters_node(self, state: OrchestrationState) -> OrchestrationState:
        """Validate extracted parameters against tool schemas."""
        
        validation_results = {}
        
        for tool_name, params in state["extracted_parameters"].items():
            is_valid, error_msg = self.tool_orchestrator.validate_parameters(tool_name, params)
            validation_results[tool_name] = (is_valid, error_msg)
        
        state["validation_results"] = validation_results
        
        # Check if any validations failed
        failed_validations = [tool for tool, (valid, _) in validation_results.items() if not valid]
        
        if failed_validations:
            error_details = []
            for tool in failed_validations:
                _, error_msg = validation_results[tool]
                error_details.append(f"{tool}: {error_msg}")
            
            state["error_message"] = f"Parameter validation failed for: {', '.join(error_details)}"
        else:
            state["reasoning"] += "Parameter Validation: All parameters validated successfully. "
        
        return state
    
    async def _execute_tools_node(self, state: OrchestrationState) -> OrchestrationState:
        """Execute the educational tools with validated parameters."""
        
        try:
            # Filter out tools with validation errors
            valid_params = {
                tool: params for tool, params in state["extracted_parameters"].items()
                if state["validation_results"].get(tool, (False, ""))[0]
            }
            
            if not valid_params:
                state["error_message"] = "No valid parameters for tool execution"
                return state
            
            tool_responses = await self.tool_orchestrator.execute_tools(
                tool_parameters=valid_params,
                user_info=state["request"].user_info,
                chat_history=state["request"].chat_history
            )
            
            state["tool_responses"] = tool_responses
            
            # Check if any tools succeeded
            successful_tools = [resp for resp in tool_responses if resp.success]
            
            if successful_tools:
                state["success"] = True
                state["reasoning"] += f"Tool Execution: Successfully executed {len(successful_tools)} tools. "
            else:
                state["error_message"] = "All tool executions failed"
            
        except Exception as e:
            state["error_message"] = f"Tool execution failed: {str(e)}"
        
        return state
    
    async def _generate_response_node(self, state: OrchestrationState) -> OrchestrationState:
        """Generate final response with reasoning."""
        
        if state["success"]:
            successful_tools = [resp.tool_name for resp in state["tool_responses"] if resp.success]
            state["reasoning"] += f"Orchestration completed successfully with tools: {', '.join(successful_tools)}."
        
        return state
    
    async def _handle_error_node(self, state: OrchestrationState) -> OrchestrationState:
        """Handle errors in the workflow."""
        
        state["success"] = False
        if not state["reasoning"]:
            state["reasoning"] = "Orchestration failed due to validation or execution errors."
        
        return state
    
    def _should_execute_tools(self, state: OrchestrationState) -> str:
        """Determine whether to proceed with tool execution or handle errors."""
        
        if state["error_message"]:
            return "error"
        
        # Check if any tools passed validation
        valid_tools = [
            tool for tool, (valid, _) in state["validation_results"].items() if valid
        ]
        
        if valid_tools:
            return "execute"
        else:
            return "error"
    
    def _adapt_for_teaching_style(self, parameters: Dict[str, Dict[str, Any]], 
                                teaching_style: TeachingStyle, user_info: UserInfo) -> Dict[str, Dict[str, Any]]:
        """Adapt parameters based on teaching style and student context."""
        
        adapted_params = parameters.copy()
        
        for tool_name, params in adapted_params.items():
            if teaching_style == TeachingStyle.VISUAL:
                # Visual style adaptations
                if tool_name == "note_maker":
                    params["include_analogies"] = True
                    params["include_examples"] = True
                elif tool_name == "concept_explainer":
                    # Request more visual explanations
                    pass
            
            elif teaching_style == TeachingStyle.SOCRATIC:
                # Socratic style adaptations
                if tool_name == "flashcard_generator":
                    # Increase question complexity
                    if params.get("difficulty") == "easy":
                        params["difficulty"] = "medium"
            
            elif teaching_style == TeachingStyle.DIRECT:
                # Direct style adaptations
                if tool_name == "note_maker":
                    params["note_taking_style"] = "outline"
                    params["include_analogies"] = False
            
            # Adapt based on emotional state
            if "anxious" in user_info.emotional_state_summary.lower():
                if tool_name == "flashcard_generator":
                    params["difficulty"] = "easy"
                    params["count"] = min(params.get("count", 5), 3)
                elif tool_name == "concept_explainer":
                    params["desired_depth"] = "basic"
            
            elif "focused" in user_info.emotional_state_summary.lower():
                if tool_name == "flashcard_generator":
                    params["count"] = min(params.get("count", 5) + 2, 20)
        
        return adapted_params