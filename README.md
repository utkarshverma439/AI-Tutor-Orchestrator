# 🧠 MentorOS - Professional AI Tutoring Platform

**Intelligent middleware for autonomous AI tutoring systems with professional 3D web interface**

A next-generation educational platform that autonomously orchestrates AI-powered tutoring tools through intelligent context analysis and parameter extraction. Features a stunning professional 3D web interface with glassmorphism design, user management, and persistent data storage.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-orange.svg)](https://langchain.com)
[![License](https://img.shields.io/badge/License-Apache-yellow.svg)](LICENSE)

> **Disclaimer:** This project was previously known as **"AI Tutor Orchestrator"**.  
> The name has been updated to **MentorOS** to better represent its expanded capabilities in user management, intelligent orchestration, and professional 3D web interface design.


## ✨ Features

### 🎨 **Professional 3D Web Interface**
- **Futuristic Design**: Deep space theme with neon blue, cyan, and violet gradients
- **3D Glassmorphism**: Semi-transparent panels with backdrop blur and glowing edges
- **Advanced Animations**: Three.js powered 3D backgrounds with floating geometric shapes
- **Interactive Elements**: Particle networks, holographic effects, and smooth transitions
- **Responsive Design**: Mobile-first approach with adaptive layouts for all devices
- **Professional Login**: Secure authentication with 3D animated login interface

### 👤 **Complete User Management System**
- **User Registration**: Full signup flow with profile creation and database storage
- **Secure Authentication**: Session-based login with token management
- **Profile Management**: Comprehensive student profiles with learning preferences
- **Settings Dashboard**: Dedicated settings page for profile and system preferences
- **Data Management**: Export chat history, clear data, and reset settings
- **Social Login**: Google and GitHub authentication support

### 🤖 **AI-Powered Orchestration**
- **DeepSeek Integration**: Powered by DeepSeek AI via OpenRouter (with OpenAI fallback)
- **Context Analysis**: Intelligent conversation understanding and intent detection
- **Parameter Extraction**: Automatic tool parameter inference from natural language
- **Multi-Tool Coordination**: Seamless orchestration of multiple educational tools
- **Adaptive Learning**: Personalized content based on student profile and learning style
- **Persistent Storage**: SQLite database for user data, chat history, and preferences

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
- **Learning Analytics**: Progress tracking with animated progress rings
- **Data Export**: Download conversation history and learning data as JSON
- **Chat Controls**: Clear history, export data, and toggle previous conversations

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

That's it! MentorOS is now running with a professional 3D interface.

### 🎯 **First Time Setup**
1. **Experience the Login**: Visit the 3D animated login page
2. **Create Account**: Click "Create Account" to register with your details
3. **Explore Dashboard**: Navigate through the futuristic interface
4. **Customize Settings**: Visit Settings to personalize your learning profile
5. **Start Learning**: Begin conversations with the AI tutor orchestrator

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
### Login Page
![Login](screenshot/login.png)

### Signup Page
![Signup](screenshot/sign_up.png)

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
- `GET /` - Serves the main dashboard interface
- `GET /login.html` - Professional 3D login page
- `GET /signup.html` - User registration page
- `GET /settings` - Settings and profile management page
- `POST /orchestrate` - Main orchestration endpoint for educational requests
- `GET /health` - Health check for all system components
- `GET /tools` - List available educational tools and their capabilities

### Authentication Endpoints
- `POST /auth/login` - User login with database storage
- `POST /auth/signup` - User registration and account creation
- `POST /auth/logout` - User logout and session invalidation
- `GET /auth/verify` - Session token verification

### User Management
- `GET /user/{user_id}/session` - Retrieve user session data
- `POST /user/{user_id}/profile` - Update user profile information
- `POST /user/{user_id}/preferences` - Update user learning preferences
- `GET /user/{user_id}/chat/history` - Get user's chat history
- `DELETE /user/{user_id}/chat/history` - Clear user's chat history
- `GET /user/{user_id}/chat/export` - Export user's chat history as JSON
- `DELETE /user/{user_id}/session` - Clear user session data

### Testing Endpoints
- `GET /test` - Simple connectivity test
- `POST /test-orchestrate` - Test orchestration without dependencies
- `POST /analyze` - Context analysis without tool execution (for debugging)

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

# Database Configuration
DATABASE_URL=sqlite:///./mentoros.db           # SQLite (default)
ASYNC_DATABASE_URL=sqlite+aiosqlite:///./mentoros.db
# OR PostgreSQL for production
# DATABASE_URL=postgresql://user:password@localhost:5432/mentoros
# ASYNC_DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/mentoros

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
- **Three.js Integration**: Real-time 3D geometric shapes and particle systems
- **Glassmorphism**: Semi-transparent panels with backdrop blur effects
- **Neon Gradients**: Blue, cyan, violet, and pink gradient accents
- **Perspective Transforms**: Cards with realistic 3D depth and rotation
- **Particle Networks**: Animated floating particles with connecting lines
- **Holographic Effects**: Rotating rings and glowing animations

### Professional Interface Components
- **3D Login System**: Animated login card with floating geometric shapes
- **Navigation Sidebar**: Glassmorphism navigation with hover effects
- **Settings Dashboard**: Comprehensive profile and preference management
- **Learning Analytics**: Animated SVG progress rings and statistics
- **Chat Interface**: Real-time messaging with visual feedback
- **Data Management**: Export, clear, and manage user data

### Advanced Interactions
- **Mouse Parallax**: 3D background responds to cursor movement
- **Smooth Animations**: GSAP-powered transitions and micro-interactions
- **Visual Feedback**: Glowing effects, particle bursts, and hover states
- **Responsive Design**: Adaptive layouts for desktop, tablet, and mobile
- **Accessibility**: High contrast mode and reduced motion support

### User Experience Features
- **Onboarding Flow**: Guided signup and profile setup process
- **Real-time Status**: Live connection indicators and system health
- **Toast Notifications**: Professional notification system with icons
- **Loading States**: Animated spinners and progress indicators
- **Error Handling**: Graceful error messages and fallback states

### Keyboard Shortcuts
- `Ctrl/Cmd + K`: Focus chat input
- `Ctrl/Cmd + /`: Toggle navigation sidebar
- `Enter`: Send message
- `Shift + Enter`: New line in message

## 📁 Project Structure

```
mentoros/
├── 📄 README.md                    # This comprehensive guide
├── 📄 requirements.txt             # Python dependencies with database support
├── 📄 .env.example                 # Environment template
├── 📄 .env                         # Your configuration (create from template)
├── 📄 start_server.py              # Easy startup script with health checks
├── 📄 app.py                       # Main FastAPI application with auth
├── 📄 main.py                      # Alternative entry point
├── 📄 test_backend.py              # Backend component testing
├── 📄 test_parameter_extraction.py # Parameter extraction testing
├── 📁 screenshot/
│   ├── signup.png
│   ├── login.png
│   ├── backend.png
│   ├── ui_design.png
│   ├── processing.png
│   ├── conversation.png
│   └── conversation2.png
├── 📁 static/                      # Frontend files
│   ├── 📄 index.html              # Main dashboard interface
│   ├── 📄 login.html              # 3D login page
│   ├── 📄 signup.html             # User registration page
│   ├── 📄 settings.html           # Settings and profile management
│   ├── �  welcome.html            # Welcome/navigation page
│   ├── 📄 script.js               # Main dashboard JavaScript
│   ├── 📄 login-script.js         # Login page functionality
│   ├── 📄 signup-script.js        # Signup page functionality
│   ├── � settings-scripgt.js      # Settings page functionality
│   ├── 📄 styles.css              # Main 3D theme CSS
│   ├── 📄 login-styles.css        # Login/signup specific styles
│   └── � favilcon.png             # MentorOS logo icon
└── � src/                         # Backend source code
    ├── 📁 core/                    # Core orchestration logic
    │   ├── 📄 context_analyzer.py         # Intent analysis & parameter extraction
    │   ├── 📄 orchestration_agent.py      # Main orchestration workflow
    │   ├── 📄 tool_orchestrator.py        # Educational tool execution
    │   ├── 📄 state_manager.py            # Session & preference management
    │   ├── 📄 mock_tools.py               # Mock educational tools
    │   └── 📄 llm_config.py               # LLM configuration & testing
    ├── 📁 database/                # Database management
    │   ├── 📄 __init__.py                  # Package initialization
    │   ├── 📄 database.py                 # Database connection & session management
    │   ├── 📄 models.py                   # SQLAlchemy models for users, sessions, chat
    │   └── 📄 user_service.py             # User management service layer
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
- **Colors**: Edit CSS variables in `static/styles.css` and `static/login-styles.css`
- **3D Effects**: Modify Three.js configurations in JavaScript files
- **Animations**: Update GSAP animations and CSS keyframes
- **Layout**: Update HTML structure across multiple page templates
- **Database**: Extend models in `src/database/models.py` for new features

### Database Management
- **Models**: User, UserSession, ChatMessage, ToolUsage, UserPreferences
- **Services**: User authentication, session management, data persistence
- **Migrations**: Automatic table creation with SQLAlchemy
- **Export/Import**: JSON-based data export and backup functionality

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
RUN mkdir -p /app/data
EXPOSE 8000
ENV DATABASE_URL=sqlite:///./data/mentoros.db
ENV ASYNC_DATABASE_URL=sqlite+aiosqlite:///./data/mentoros.db
CMD ["python", "start_server.py"]
```

### Environment Setup for Production
- Set `LOG_LEVEL=WARNING` for production
- Configure PostgreSQL database URL for scalability
- Set up reverse proxy (nginx) for static file serving and SSL
- Configure SSL certificates for HTTPS
- Set up database backups and user data protection
- Configure session timeout and security headers

Ah, got it! You want to **add the collaborators and their roles** to the new project — **AI Tutor Orchestrator** — not copy the collaborator section from the old one.

Here’s how you can **add the collaborators section with roles** tailored for the new project:

---

## 🤝 Collaborators

This project is a joint effort by:

* **Utkarsh Verma**
  GitHub: [@utkarshverma439](https://github.com/utkarshverma439)
  *Role: System Architect, AI Orchestration Pipeline, LLM Integration, Database Design, User Management, Backend Lead*

* **Ankit Kumar**
  GitHub: [@ankit9412](https://github.com/ankit9412)
  *Role: 3D Web UI Development, Professional Interface Design, Three.js Integration, Animation Systems, Frontend Lead*

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
- **FastAPI** for the robust web framework with async support
- **LangChain** for AI application development tools
- **LangGraph** for workflow orchestration
- **Three.js** for 3D graphics and animations
- **SQLAlchemy** for database ORM and async support
- **GSAP** for smooth animations and transitions
- **Lucide** for beautiful icon system

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/utkarshverma439/mentoros/issues)
- **Documentation**: This README and inline code comments
- **Demo**: Live demo available at the deployed URL

---

## 🌟 **What's New in MentorOS v2.0**

### 🆕 **Major Updates**
- ✅ **Complete User Management** - Registration, login, profiles, and sessions
- ✅ **Professional 3D Interface** - Glassmorphism design with Three.js integration
- ✅ **Database Integration** - SQLite with async support for data persistence
- ✅ **Settings Dashboard** - Comprehensive profile and preference management
- ✅ **Data Export/Import** - Download and manage your learning data
- ✅ **Enhanced Security** - Session tokens and secure authentication
- ✅ **Mobile Optimization** - Responsive design for all devices
- ✅ **Learning Analytics** - Progress tracking with visual indicators

### 🎯 **Coming Soon**
- 📊 Advanced analytics dashboard
- 🎓 Multi-user classroom management
- 🔗 Integration with external learning platforms
- 📱 Mobile app companion
- 🌐 Multi-language support
- 🤖 Advanced AI tutoring models

---

**🎉 Ready to experience the future of AI-powered education? Start with `python start_server.py` and open http://127.0.0.1:8000!**

*Built with ❤️ for educators, students, and AI enthusiasts*







