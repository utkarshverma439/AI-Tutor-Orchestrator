#!/usr/bin/env python3
"""
Simple test script to verify backend functionality.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the src directory to Python path
sys.path.append(str(Path(__file__).parent / "src"))

async def test_backend():
    """Test the backend components."""
    
    print("🧪 Testing AI Tutor Orchestrator Backend...")
    
    try:
        # Test LLM configuration
        print("\n1. Testing LLM Configuration...")
        from core.llm_config import get_model_info, test_llm_connection
        
        model_info = get_model_info()
        print(f"   Provider: {model_info['provider']}")
        print(f"   Model: {model_info['model']}")
        print(f"   API Key Set: {model_info['api_key_set']}")
        
        if model_info['api_key_set']:
            print("   Testing connection...")
            connection_result = await test_llm_connection()
            if connection_result['status'] == 'success':
                print("   ✅ LLM connection successful!")
            else:
                print(f"   ❌ LLM connection failed: {connection_result['error']}")
        else:
            print("   ⚠️ No API key configured, will use fallback responses")
        
        # Test orchestration components
        print("\n2. Testing Orchestration Components...")
        from core.orchestration_agent import OrchestrationAgent
        from models.schemas import OrchestrationRequest, UserInfo, ChatMessage, MessageRole, TeachingStyle
        
        # Create test user
        test_user = UserInfo(
            user_id="test_user",
            name="Test Student",
            grade_level="10",
            learning_style_summary="Visual learner, prefers examples",
            emotional_state_summary="Focused and motivated",
            mastery_level_summary="Level 5: Developing competence"
        )
        
        # Create test request
        test_request = OrchestrationRequest(
            user_info=test_user,
            chat_history=[],
            current_message="I need help understanding quantum mechanics",
            teaching_style=TeachingStyle.DIRECT
        )
        
        # Test orchestration
        print("   Creating orchestration agent...")
        agent = OrchestrationAgent()
        print("   ✅ Orchestration agent created successfully!")
        
        print("   Testing orchestration...")
        response = await agent.orchestrate(test_request)
        
        if response.success:
            print(f"   ✅ Orchestration successful!")
            print(f"   Selected tools: {response.selected_tools}")
            print(f"   Tool responses: {len(response.tool_responses)}")
        else:
            print(f"   ❌ Orchestration failed: {response.error_message}")
        
        # Test mock tools
        print("\n3. Testing Mock Tools...")
        from core.mock_tools import mock_tools
        
        test_params = {
            "concept_to_explain": "quantum mechanics",
            "current_topic": "physics",
            "desired_depth": "intermediate"
        }
        
        tool_result = await mock_tools.execute_concept_explainer(test_params, test_user)
        
        if tool_result.success:
            print("   ✅ Mock tools working correctly!")
            print(f"   Generated explanation with {len(tool_result.data.get('examples', []))} examples")
        else:
            print(f"   ❌ Mock tools failed: {tool_result.error_message}")
        
        print("\n🎉 Backend test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Backend test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_backend())
    sys.exit(0 if success else 1)