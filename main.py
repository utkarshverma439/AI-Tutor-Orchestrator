#!/usr/bin/env python3
"""
Main entry point for the AI Tutor Orchestrator.
"""

import uvicorn
import os
from dotenv import load_dotenv

def main():
    """Main function to start the orchestrator service."""
    load_dotenv()
    
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", "8000"))
    log_level = os.getenv("LOG_LEVEL", "info").lower()
    
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
        log_level=log_level
    )

if __name__ == "__main__":
    main()