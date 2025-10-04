# 🧠 AI Tutor Orchestrator

**Intelligent middleware for autonomous AI tutoring systems with stunning 3D web interface**

An advanced system that autonomously connects conversational AI tutors to educational tools through context-aware parameter extraction and intelligent orchestration, featuring a modern dark 3D web interface with smooth animations.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-orange.svg)](https://langchain.com)
[![License](https://img.shields.io/badge/License-Apache-yellow.svg)](LICENSE)

## ✨ Features

### 🎨 **Stunning 3D Web Interface**
- **Dark Theme**: Professional dark mode with neon cyan/purple accents
- **3D Effects**: Perspective transforms, depth shadows, and glassmorphism
- **Smooth Animations**: 60fps fluid transitions and micro-interactions
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Real-time Chat**: Interactive conversation with AI orchestrator

### 🤖 **AI-Powered Orchestration**
- **DeepSeek Integration**: Powered by DeepSeek AI via OpenRouter (with OpenAI fallback)
- **Context Analysis**: Intelligent conversation understanding and intent detection
- **Parameter Extraction**: Automatic tool parameter inference from natural language
- **Multi-Tool Coordination**: Seamless orchestration of multiple educational tools
- **Adaptive Learning**: Personalized content based on student profile and learning style

### 📚 **Educational Tools**
- **📝 Note Maker**: Generates structured notes with examples and analogies
- **🃏 Flashcard Generator**: Creates study cards with adaptive difficulty levels
- **💡 Concept Explainer**: Provides detailed explanations with visual aids and practice questions

### 🎯 **Smart Features**
- **Language Learning Support**: Enhanced support for Spanish, French, German, English vocabulary
- **Teaching Style Adaptation**: Direct, Socratic, Visual, and Flipped Classroom methods
- **Emotional State Awareness**: Adapts content based on student's emotional state
- **Session Management**: Maintains conversation history and learning patterns
- **Health Monitoring**: Real-time system status and tool availability

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/utkarshverma439/AI-Tutor-Orchestrator.git
   cd ai-tutor-orchestrator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API keys** (Optional - works with fallback responses)
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env and add your API key (choose one):
   OPENROUTER_API_KEY=your_openrouter_key_here  # Recommended (includes DeepSeek)
   # OR
   OPENAI_API_KEY=your_openai_key_here          # Alternative
   ```

4. **Start the application**
   ```bash
   python start_server.py
   ```

5. **Open your browser**
   ```
   Navigate to: http://127.0.0.1:8000
   ```

That's it! The AI Tutor Orchestrator is now running with a beautiful 3D interface.

## 💬 Usage Examples

The orchestrator responds intelligently to natural language requests:

### 📝 **Note Taking**
- *"I need notes on photosynthesis for my biology class"*
- *"Create structured notes about quantum mechanics"*
- *"Make study notes on the French Revolution"*

### 🃏 **Flashcard Generation**
- *"Make flashcards for Spanish vocabulary"*
- *"Create flashcards to help me memorize chemistry formulas"*
- *"Generate quiz cards for calculus derivatives"*

### 💡 **Concept Explanation**
- *"Explain quantum mechanics in simple terms"*
- *"I'm confused about photosynthesis, can you help?"*
- *"What is machine learning and how does it work?"*

### 🆘 **General Help**
- *"I'm struggling with calculus derivatives"*
- *"Help me understand organic chemistry"*
- *"I need to study for my Spanish test tomorrow"*

## 🏗️ Architecture

### System Components
```
┌─────────────────┐    ┌──────────────────┐    ┌───────────────────────┐
│   3D Web UI     │    │  FastAPI Server  │    │  AI Orchestrator      │
│                 │◄──►│                  │◄──►│                       │
│ • Chat Interface│    │ • REST API       │    │ • Context Analysis    │
│ • 3D Animations │    │ • Static Files   │    │ • Tool Selection      │
│ • Real-time UI  │    │ • CORS Support   │    │ • Parameter Extraction│
└─────────────────┘    └──────────────────┘    └───────────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │ Educational Tools│
                       │                  │
                       │ • Note Maker     │
                       │ • Flashcard Gen  │
                       │ • Concept Explain│
                       └──────────────────┘
```

### Core Modules
- **Context Analyzer**: Analyzes conversation context and determines educational intent
- **Orchestration Agent**: Main coordination logic using LangGraph workflows
- **Tool Orchestrator**: Manages execution of educational tools with parameter validation
- **State Manager**: Maintains conversation history and student personalization
- **Mock Tools**: Provides realistic educational content for demonstration

## 📸 Screenshots

### 🧠 Backend Results

Shows backend orchestration, parameter extraction, and tool coordination in action.

![Backend Results](screenshot/backend.png)

---

### 🎨 3D Web UI Design

Modern dark-mode UI with glassmorphism, neon accents, and 3D effects.

![UI Design](screenshot/ui_design.png)

---

### ⚙️ AI Processing in Action

Live orchestration and decision-making pipeline visualized during a tutoring request.

![Processing](screenshot/processing.png)

---

### 💬 AI Conversation Interface

Side-by-side view of real-time AI conversation flow.

<p float="left">
  <img src="screenshot/conversation.png" width="48%" />
  <img src="screenshot/conversation2.png" width="48%" />
</p>

---


## 🔌 API Endpoints

### Main Endpoints
- `GET /` - Serves the 3D web interface
- `POST /orchestrate` - Main orchestration endpoint for educational requests
- `GET /health` - Health check for all system components
- `GET /tools` - List available educational tools and their capabilities

### Testing Endpoints
- `GET /test` - Simple connectivity test
- `POST /test-orchestrate` - Test orchestration without dependencies
- `POST /analyze` - Context analysis without tool execution (for debugging)

### User Management
- `GET /user/{user_id}/session` - Retrieve user session data
- `POST /user/{user_id}/preferences` - Update user learning preferences
- `DELETE /user/{user_id}/session` - Clear user session data

### LLM Integration
- `GET /llm/test` - Test LLM connection and configuration
- `GET /llm/info` - Get current LLM configuration information

## ⚙️ Configuration

### Environment Variables (.env)
```env
# AI Model Configuration (choose one)
OPENROUTER_API_KEY=your_openrouter_key_here    # Recommended
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
MODEL_NAME=deepseek/deepseek-chat

# OR OpenAI (alternative)
OPENAI_API_KEY=your_openai_key_here

# Server Configuration
API_HOST=127.0.0.1
API_PORT=8000
LOG_LEVEL=INFO

# Database (optional - uses in-memory by default)
DATABASE_URL=postgresql://user:password@localhost:5432/tutor_orchestrator

# External Tool APIs (optional - uses mock tools by default)
NOTE_MAKER_API_URL=http://localhost:8001/api/note-maker
FLASHCARD_API_URL=http://localhost:8002/api/flashcard-generator
CONCEPT_EXPLAINER_API_URL=http://localhost:8003/api/concept-explainer
```

### Supported LLM Providers
- **OpenRouter** (Recommended): Access to DeepSeek, Claude, GPT-4, and 100+ models
- **OpenAI**: Direct OpenAI API integration

## 🧪 Testing

### Backend Component Testing
```bash
# Test all backend components
python test_backend.py

# Test parameter extraction specifically
python test_parameter_extraction.py
```

### API Testing
```bash
# Test basic connectivity
curl http://127.0.0.1:8000/test

# Test health check
curl http://127.0.0.1:8000/health

# Test full orchestration
curl -X POST http://127.0.0.1:8000/orchestrate \
  -H "Content-Type: application/json" \
  -d '{
    "user_info": {
      "user_id": "test_user",
      "name": "Test Student",
      "grade_level": "10",
      "learning_style_summary": "Visual learner",
      "emotional_state_summary": "Focused",
      "mastery_level_summary": "Level 5"
    },
    "chat_history": [],
    "current_message": "Explain quantum mechanics",
    "teaching_style": "direct"
  }'
```

### Test Files Explanation

#### `test_backend.py`
Comprehensive backend testing that verifies:
- ✅ LLM configuration and connection
- ✅ Orchestration agent initialization
- ✅ Educational tool execution
- ✅ Mock tool functionality
- ✅ Error handling and fallbacks

#### `test_parameter_extraction.py`
Specific testing for parameter extraction accuracy:
- ✅ Language learning requests ("Spanish vocabulary")
- ✅ Science concepts ("quantum mechanics")
- ✅ Subject identification and topic extraction
- ✅ Tool parameter mapping and validation

## 🎨 Frontend Features

### 3D Design Elements
- **Perspective Effects**: Cards and panels with realistic depth
- **Animated Background**: Moving grid pattern and floating orbs
- **Glassmorphism**: Translucent panels with backdrop blur
- **Neon Accents**: Cyan and purple gradient highlights
- **Smooth Transitions**: Hardware-accelerated CSS animations

### Interactive Components
- **Real-time Chat**: Instant messaging with the AI orchestrator
- **Student Profile**: Customizable learning preferences and emotional state
- **System Status**: Live monitoring of AI model and tool availability
- **Results Panel**: Detailed orchestration results with reasoning
- **Suggestion Chips**: Quick-start conversation prompts

### Responsive Design
- **Desktop**: Full 3D effects with dual-panel layout
- **Tablet**: Optimized grid layout with maintained animations
- **Mobile**: Single-column layout with touch-friendly controls

### Keyboard Shortcuts
- `Ctrl/Cmd + K`: Focus chat input
- `Ctrl/Cmd + L`: Clear chat history
- `Enter`: Send message
- `Shift + Enter`: New line in message

## 📁 Project Structure

```
ai-tutor-orchestrator/
├── 📄 README.md                    # This comprehensive guide
├── 📄 requirements.txt             # Python dependencies
├── 📄 .env.example                 # Environment template
├── 📄 .env                         # Your configuration (create from template)
├── 📄 start_server.py              # Easy startup script with health checks
├── 📄 app.py                       # Main FastAPI application
├── 📄 main.py                      # Alternative entry point
├── 📄 test_backend.py              # Backend component testing
├── 📄 test_parameter_extraction.py # Parameter extraction testing
├── 📁 screenshot/
│   ├── backend.png
│   ├── ui_design.png
│   ├── processing.png
│   ├── conversation.png
│   └── conversation2.png
├── 📁 static/                      # Frontend files
│   ├── 📄 index.html              # 3D web interface
│   ├── 📄 script.js               # Frontend JavaScript logic
│   └── 📄 styles.css              # 3D dark theme CSS
└── 📁 src/                         # Backend source code
    ├── 📁 core/                    # Core orchestration logic
    │   ├── 📄 context_analyzer.py         # Intent analysis & parameter extraction
    │   ├── 📄 orchestration_agent.py      # Main orchestration workflow
    │   ├── 📄 tool_orchestrator.py        # Educational tool execution
    │   ├── 📄 state_manager.py            # Session & preference management
    │   ├── 📄 mock_tools.py               # Mock educational tools
    │   └── 📄 llm_config.py               # LLM configuration & testing
    └── 📁 models/
        └── 📄 schemas.py                   # Pydantic data models
```

## 🔧 Development

### Running in Development Mode
```bash
# With auto-reload and detailed logging
python start_server.py

# Or directly with uvicorn
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

### Adding New Educational Tools
1. Define tool schema in `src/models/schemas.py`
2. Add tool logic to `src/core/mock_tools.py`
3. Update parameter validation in `src/core/tool_orchestrator.py`
4. Add tool recognition patterns in `src/core/context_analyzer.py`

### Customizing the UI
- **Colors**: Edit CSS variables in `static/styles.css`
- **Animations**: Modify transition properties and keyframes
- **Layout**: Update HTML structure in `static/index.html`
- **Interactions**: Enhance JavaScript logic in `static/script.js`

## 🚀 Deployment

### Local Production
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "start_server.py"]
```

### Environment Setup for Production
- Set `LOG_LEVEL=WARNING` for production
- Configure proper database URL if using persistent storage
- Set up reverse proxy (nginx) for static file serving
- Configure SSL certificates for HTTPS

Ah, got it! You want to **add the collaborators and their roles** to the new project — **AI Tutor Orchestrator** — not copy the collaborator section from the old one.

Here’s how you can **add the collaborators section with roles** tailored for the new project:

---

## 🤝 Collaborators

This project is a joint effort by:

* **Utkarsh Verma**
  GitHub: [@utkarshverma439](https://github.com/utkarshverma439)
  *Role: System Architect, AI Orchestration Pipeline, LLM Integration, Context Analysis, Backend Lead*

* **Ankit Kumar**
  GitHub: [@ankit9412](https://github.com/ankit9412)
  *Role: 3D Web UI Development, Frontend Animation & Design, UX Implementation, Visualization Components, Presentation Assets*

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code style
- Add type hints for all functions
- Include docstrings for public methods
- Test new features with both test files
- Update README for new features

## 📝 License

This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Yophoria Innovation Challenge** – *Project built as part of the challenge under the role of AI Agent Engineer*
- **DeepSeek AI** for providing excellent language model capabilities
- **OpenRouter** for unified LLM API access
- **FastAPI** for the robust web framework
- **LangChain** for AI application development tools
- **LangGraph** for workflow orchestration

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/utkarshverma439/ai-tutor-orchestrator/issues)
- **Documentation**: This README and inline code comments

---

**🎉 Ready to experience the future of AI-powered education? Start with `python start_server.py` and open http://127.0.0.1:8000!**

*Built with ❤️ for educators, students, and AI enthusiasts*







