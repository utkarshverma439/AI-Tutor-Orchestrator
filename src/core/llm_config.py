"""
LLM Configuration module for OpenRouter and OpenAI integration.
"""

import os
from typing import Optional
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def create_llm() -> ChatOpenAI:
    """Create and configure the LLM instance with OpenRouter or OpenAI."""
    
    # Try OpenRouter first (DeepSeek)
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    openrouter_base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    model_name = os.getenv("MODEL_NAME", "deepseek/deepseek-chat")
    
    if openrouter_api_key:
        print(f"🤖 Using OpenRouter with {model_name}")
        return ChatOpenAI(
            api_key=openrouter_api_key,
            base_url=openrouter_base_url,
            model=model_name,
            temperature=0.1,
            max_tokens=2000,
            timeout=30
        )
    
    # Fallback to OpenAI
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        print("🤖 Using OpenAI GPT-4")
        return ChatOpenAI(
            api_key=openai_api_key,
            model="gpt-4-turbo-preview",
            temperature=0.1,
            max_tokens=2000,
            timeout=30
        )
    
    raise ValueError(
        "No API key found. Please set either OPENROUTER_API_KEY or OPENAI_API_KEY in your .env file"
    )

def get_model_info() -> dict:
    """Get information about the currently configured model."""
    
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if openrouter_api_key:
        return {
            "provider": "OpenRouter",
            "model": os.getenv("MODEL_NAME", "deepseek/deepseek-chat"),
            "base_url": os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
            "api_key_set": True
        }
    elif openai_api_key:
        return {
            "provider": "OpenAI",
            "model": "gpt-4-turbo-preview",
            "base_url": "https://api.openai.com/v1",
            "api_key_set": True
        }
    else:
        return {
            "provider": "None",
            "model": "None",
            "base_url": "None",
            "api_key_set": False
        }

async def test_llm_connection() -> dict:
    """Test the LLM connection and return status."""
    
    try:
        llm = create_llm()
        
        # Simple test message
        test_response = await llm.ainvoke("Hello! Please respond with 'Connection successful'")
        
        return {
            "status": "success",
            "response": test_response.content,
            "model_info": get_model_info()
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "model_info": get_model_info()
        }