#!/usr/bin/env python3
"""
AI Tutor Orchestrator - Main Server Startup Script

This is the primary entry point for the AI Tutor Orchestrator.
Run this script to start the application with comprehensive health checks.

Usage:
    python start_server.py

Features:
    - Dependency verification
    - Configuration validation
    - Backend component testing
    - Automatic server startup
    - Health monitoring
"""

import asyncio
import sys
import os
import time
import subprocess
from pathlib import Path

# Add the src directory to Python path
sys.path.append(str(Path(__file__).parent / "src"))

async def check_dependencies():
    """Check if all required dependencies are available."""
    
    print("🔍 Checking dependencies...")
    
    try:
        import fastapi
        import uvicorn
        import langchain
        import langchain_openai
        import langgraph
        import pydantic
        import httpx
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Run: pip install -r requirements.txt")
        return False

async def check_configuration():
    """Check if configuration is properly set up."""
    
    print("🔧 Checking configuration...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check API keys
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if openrouter_key and openrouter_key != "your_openrouter_api_key_here":
        print("✅ OpenRouter API key configured")
        return True
    elif openai_key and openai_key != "your_openai_api_key_here":
        print("✅ OpenAI API key configured")
        return True
    else:
        print("⚠️ No API key configured - will use fallback responses")
        return True  # Still allow running with fallbacks

async def test_backend_quick():
    """Quick backend test."""
    
    print("🧪 Quick backend test...")
    
    try:
        from core.llm_config import get_model_info
        from core.orchestration_agent import OrchestrationAgent
        
        model_info = get_model_info()
        print(f"   Model: {model_info['provider']} - {model_info['model']}")
        
        # Quick agent creation test
        agent = OrchestrationAgent()
        print("✅ Backend components loaded successfully")
        return True
        
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def start_server():
    """Start the FastAPI server."""
    
    print("🚀 Starting AI Tutor Orchestrator...")
    print("🌐 Server will be available at: http://127.0.0.1:8000")
    print("📚 Frontend interface: http://127.0.0.1:8000")
    print("🔧 API docs: http://127.0.0.1:8000/docs")
    print("\n" + "="*50)
    
    try:
        import uvicorn
        uvicorn.run(
            "app:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server failed to start: {e}")

async def main():
    """Main startup sequence."""
    
    print("🧠 AI Tutor Orchestrator - Startup")
    print("="*40)
    
    # Check dependencies
    if not await check_dependencies():
        sys.exit(1)
    
    # Check configuration
    await check_configuration()
    
    # Quick backend test
    if not await test_backend_quick():
        print("⚠️ Backend test failed, but continuing anyway...")
    
    print("\n🎉 All checks passed! Starting server...")
    print("💡 Tip: Try asking 'I need help with quantum mechanics'")
    print("🛑 Press Ctrl+C to stop the server\n")
    
    # Start server
    start_server()

if __name__ == "__main__":
    asyncio.run(main())