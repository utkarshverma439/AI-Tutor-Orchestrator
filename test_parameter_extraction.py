#!/usr/bin/env python3
"""
Test parameter extraction for specific cases.
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.append(str(Path(__file__).parent / "src"))

async def test_parameter_extraction():
    """Test parameter extraction for the Spanish vocabulary case."""
    
    print("🧪 Testing Parameter Extraction...")
    
    try:
        from core.context_analyzer import ContextAnalyzer
        from core.llm_config import create_llm
        from models.schemas import UserInfo, ChatMessage, MessageRole
        
        # Create test components
        llm = create_llm()
        analyzer = ContextAnalyzer(llm)
        
        # Create test user
        test_user = UserInfo(
            user_id="test_user",
            name="Test Student",
            grade_level="10",
            learning_style_summary="Visual learner, prefers examples",
            emotional_state_summary="Focused and motivated",
            mastery_level_summary="Level 5: Developing competence"
        )
        
        # Test cases
        test_cases = [
            "Make flashcards for Spanish vocabulary",
            "I need help with quantum mechanics",
            "Create notes on photosynthesis",
            "Generate flashcards for French words"
        ]
        
        for i, message in enumerate(test_cases, 1):
            print(f"\n{i}. Testing: '{message}'")
            
            # Test intent analysis
            intent = await analyzer.analyze_intent([], message, test_user)
            print(f"   Tools needed: {intent.get('tools_needed', [])}")
            print(f"   Subject: {intent.get('subject', 'unknown')}")
            print(f"   Topics: {intent.get('topics', [])}")
            
            # Test parameter extraction
            if intent.get('tools_needed'):
                params = await analyzer.extract_parameters(
                    intent['tools_needed'], [], message, test_user
                )
                
                for tool, tool_params in params.items():
                    print(f"   {tool} parameters:")
                    for key, value in tool_params.items():
                        print(f"     • {key}: {value}")
        
        print("\n✅ Parameter extraction test completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_parameter_extraction())