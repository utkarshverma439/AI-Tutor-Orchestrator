// AI Tutor Orchestrator - Frontend JavaScript
console.log('🚀 Script loaded');

class TutorOrchestrator {
    constructor() {
        console.log('🏗️ Constructor called');
        this.apiBaseUrl = window.location.origin;
        this.isConnected = false;
        this.currentUser = this.getDefaultUser();
        this.chatHistory = [];
        
        console.log('🌐 API Base URL:', this.apiBaseUrl);
        
        // Initialize after a short delay to ensure DOM is ready
        setTimeout(() => {
            this.initializeElements();
            this.bindEvents();
            this.testConnection();
        }, 100);
    }

    getDefaultUser() {
        return {
            user_id: 'demo_user_' + Date.now(),
            name: 'Demo Student',
            grade_level: '10',
            learning_style_summary: 'Visual learner, prefers examples and structured content',
            emotional_state_summary: 'Focused and motivated to learn',
            mastery_level_summary: 'Level 5: Developing competence, ready for guided practice'
        };
    }

    initializeElements() {
        console.log('🔍 Initializing elements...');
        
        // Chat elements
        this.chatMessages = document.getElementById('chat-messages');
        this.chatInput = document.getElementById('chat-input');
        this.sendButton = document.getElementById('send-button');
        
        // Status elements
        this.connectionStatus = document.getElementById('connection-status');
        this.aiModelStatus = document.getElementById('ai-model-status');
        this.aiIndicator = document.getElementById('ai-indicator');
        
        // Profile elements
        this.studentName = document.getElementById('student-name');
        this.gradeLevel = document.getElementById('grade-level');
        this.learningStyle = document.getElementById('learning-style');
        this.emotionalState = document.getElementById('emotional-state');
        this.teachingStyle = document.getElementById('teaching-style');
        
        // Results elements
        this.resultsContainer = document.getElementById('results-container');
        
        // Loading elements
        this.loadingOverlay = document.getElementById('loading-overlay');
        this.toastContainer = document.getElementById('toast-container');
        
        // Suggestion chips
        this.suggestionChips = document.querySelectorAll('.suggestion-chip');
        
        console.log('✅ Element check:');
        console.log('  chatInput:', this.chatInput ? '✅' : '❌');
        console.log('  sendButton:', this.sendButton ? '✅' : '❌');
        console.log('  chatMessages:', this.chatMessages ? '✅' : '❌');
        console.log('  connectionStatus:', this.connectionStatus ? '✅' : '❌');
    }

    bindEvents() {
        console.log('🔗 Binding events...');
        
        if (!this.sendButton || !this.chatInput) {
            console.error('❌ Critical elements not found!');
            return;
        }
        
        // Send button click
        this.sendButton.addEventListener('click', () => {
            console.log('🖱️ Send button clicked');
            this.sendMessage();
        });
        
        // Enter key press
        this.chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                console.log('⌨️ Enter key pressed');
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Auto-resize textarea
        this.chatInput.addEventListener('input', () => {
            this.autoResizeTextarea();
        });
        
        // Suggestion chips
        this.suggestionChips.forEach(chip => {
            chip.addEventListener('click', () => {
                const text = chip.getAttribute('data-text');
                this.chatInput.value = text;
                this.autoResizeTextarea();
                this.chatInput.focus();
            });
        });
        
        // Profile updates
        if (this.studentName) {
            [this.studentName, this.gradeLevel, this.learningStyle, this.emotionalState, this.teachingStyle]
                .forEach(element => {
                    if (element) {
                        element.addEventListener('change', () => this.updateUserProfile());
                    }
                });
        }
        
        console.log('✅ Events bound successfully');
    }

    async testConnection() {
        console.log('🧪 Testing connection...');
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/test`);
            const data = await response.json();
            console.log('✅ Connection test successful:', data);
            
            this.isConnected = true;
            if (this.connectionStatus) {
                this.connectionStatus.textContent = 'Connected';
            }
            if (this.aiIndicator) {
                this.aiIndicator.className = 'status-indicator online';
            }
            if (this.aiModelStatus) {
                this.aiModelStatus.textContent = 'DeepSeek Ready';
            }
            
            this.showToast('Connected to AI Tutor Orchestrator!', 'success');
            
        } catch (error) {
            console.error('❌ Connection test failed:', error);
            this.isConnected = false;
            if (this.connectionStatus) {
                this.connectionStatus.textContent = 'Disconnected';
            }
            if (this.aiIndicator) {
                this.aiIndicator.className = 'status-indicator offline';
            }
            if (this.aiModelStatus) {
                this.aiModelStatus.textContent = 'Offline';
            }
            
            this.showToast('Connection failed, using demo mode', 'warning');
        }
    }

    async sendMessage() {
        console.log('📤 sendMessage called');
        
        if (!this.chatInput) {
            console.error('❌ Chat input not found');
            return;
        }
        
        const message = this.chatInput.value.trim();
        console.log('💬 Message:', message);
        
        if (!message) {
            console.log('❌ Empty message, returning');
            return;
        }

        console.log('🔗 Connection status:', this.isConnected);

        // Disable input
        this.chatInput.disabled = true;
        if (this.sendButton) {
            this.sendButton.disabled = true;
        }

        // Add user message to chat
        this.addMessage(message, 'user');
        this.chatInput.value = '';
        this.autoResizeTextarea();

        // Show loading
        this.showLoading(true);

        try {
            if (this.isConnected) {
                console.log('🌐 Using real orchestrator');
                await this.sendToOrchestrator(message);
            } else {
                console.log('🎭 Using simulated response');
                await this.simulateResponse(message);
            }
        } catch (error) {
            console.error('❌ Error sending message:', error);
            this.addMessage('Sorry, I encountered an error processing your request. Please try again.', 'assistant');
            this.showToast('Error processing message', 'error');
        } finally {
            // Re-enable input
            this.chatInput.disabled = false;
            if (this.sendButton) {
                this.sendButton.disabled = false;
            }
            this.chatInput.focus();
            this.showLoading(false);
        }
    }

    async sendToOrchestrator(message) {
        console.log('🚀 Sending to orchestrator:', message);
        
        const requestData = {
            user_info: this.currentUser,
            chat_history: this.chatHistory.slice(-10),
            current_message: message,
            teaching_style: this.teachingStyle ? this.teachingStyle.value : 'direct'
        };

        console.log('📦 Request data:', requestData);

        const response = await fetch(`${this.apiBaseUrl}/orchestrate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });

        console.log('📡 Response status:', response.status);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('❌ API Error:', response.status, errorText);
            throw new Error(`API Error ${response.status}: ${errorText}`);
        }
        
        const data = await response.json();
        console.log('📊 Response data:', data);

        // Format response with detailed analysis
        let responseText = `🧪 **Analysis Process:**\n\n`;
        
        // Show intent analysis details if available
        if (data.context_analysis) {
            responseText += `📊 **Intent Analysis:**\n`;
            responseText += `• Subject: ${data.context_analysis.subject || 'general'}\n`;
            responseText += `• Topics: ${JSON.stringify(data.context_analysis.topics || [])}\n`;
            responseText += `• Tools needed: ${JSON.stringify(data.context_analysis.tools_needed || [])}\n`;
            responseText += `• Confidence: ${(data.context_analysis.confidence_score || 0).toFixed(2)}\n\n`;
        }
        
        responseText += `🎯 **Selected Tools:** ${data.selected_tools.join(', ')}\n\n`;
        responseText += `🧠 **AI Reasoning:** ${data.reasoning}\n\n`;
        
        if (data.extracted_parameters && Object.keys(data.extracted_parameters).length > 0) {
            responseText += '🛠️ **Tool Execution:**\n';
            Object.entries(data.extracted_parameters).forEach(([tool, params]) => {
                responseText += `**${tool}** parameters:\n`;
                Object.entries(params).forEach(([key, value]) => {
                    responseText += `• ${key}: ${value}\n`;
                });
                responseText += '\n';
            });
        }

        // Display actual tool results content
        if (data.tool_responses && data.tool_responses.length > 0) {
            responseText += '📊 **Educational Content Generated:**\n\n';
            
            data.tool_responses.forEach(toolResponse => {
                if (toolResponse.success && toolResponse.data) {
                    const toolData = toolResponse.data;
                    
                    if (toolResponse.tool_name === 'concept_explainer') {
                        responseText += `💡 **Concept Explanation:**\n`;
                        responseText += `${toolData.explanation}\n\n`;
                        
                        if (toolData.examples && toolData.examples.length > 0) {
                            responseText += `📚 **Examples:**\n`;
                            toolData.examples.forEach((example, index) => {
                                responseText += `${index + 1}. ${example}\n`;
                            });
                            responseText += '\n';
                        }
                        
                        if (toolData.related_concepts && toolData.related_concepts.length > 0) {
                            responseText += `🔗 **Related Concepts:**\n`;
                            toolData.related_concepts.forEach(concept => {
                                responseText += `• ${concept}\n`;
                            });
                            responseText += '\n';
                        }
                        
                        if (toolData.practice_questions && toolData.practice_questions.length > 0) {
                            responseText += `❓ **Practice Questions:**\n`;
                            toolData.practice_questions.forEach((question, index) => {
                                responseText += `${index + 1}. ${question}\n`;
                            });
                            responseText += '\n';
                        }
                    }
                    
                    else if (toolResponse.tool_name === 'note_maker') {
                        responseText += `📝 **Study Notes: ${toolData.title}**\n\n`;
                        responseText += `**Summary:** ${toolData.summary}\n\n`;
                        
                        if (toolData.note_sections && toolData.note_sections.length > 0) {
                            toolData.note_sections.forEach(section => {
                                responseText += `**${section.title}**\n`;
                                responseText += `${section.content}\n\n`;
                                
                                if (section.key_points && section.key_points.length > 0) {
                                    responseText += `Key Points:\n`;
                                    section.key_points.forEach(point => {
                                        responseText += `• ${point}\n`;
                                    });
                                    responseText += '\n';
                                }
                                
                                if (section.examples && section.examples.length > 0) {
                                    responseText += `Examples:\n`;
                                    section.examples.forEach(example => {
                                        responseText += `• ${example}\n`;
                                    });
                                    responseText += '\n';
                                }
                            });
                        }
                        
                        if (toolData.key_concepts && toolData.key_concepts.length > 0) {
                            responseText += `🔑 **Key Concepts:** ${toolData.key_concepts.join(', ')}\n\n`;
                        }
                    }
                    
                    else if (toolResponse.tool_name === 'flashcard_generator') {
                        responseText += `🃏 **Flashcards (${toolData.difficulty} difficulty):**\n\n`;
                        
                        if (toolData.flashcards && toolData.flashcards.length > 0) {
                            toolData.flashcards.forEach((card, index) => {
                                responseText += `**Card ${index + 1}:** ${card.title}\n`;
                                responseText += `**Q:** ${card.question}\n`;
                                responseText += `**A:** ${card.answer}\n`;
                                if (card.example) {
                                    responseText += `**Example:** ${card.example}\n`;
                                }
                                responseText += '\n';
                            });
                        }
                        
                        if (toolData.adaptation_details) {
                            responseText += `📋 **Adaptation:** ${toolData.adaptation_details}\n\n`;
                        }
                    }
                } else {
                    responseText += `❌ **${toolResponse.tool_name}**: ${toolResponse.error_message}\n\n`;
                }
            });
        }

        if (data.error_message) {
            responseText += `⚠️ **Note:** ${data.error_message}`;
        } else if (data.success) {
            responseText += `🎉 **Success!** All educational tools executed successfully.`;
        }

        this.addMessage(responseText, 'assistant');
        
        // Add to results panel
        if (data.tool_responses) {
            data.tool_responses.forEach(toolResponse => {
                if (toolResponse.success) {
                    this.addResult({
                        title: `${toolResponse.tool_name.replace('_', ' ').toUpperCase()}`,
                        status: 'success',
                        content: this.formatToolResult(toolResponse),
                        timestamp: new Date().toLocaleTimeString()
                    });
                }
            });
        }

        // Update chat history
        this.chatHistory.push(
            { role: 'user', content: message },
            { role: 'assistant', content: responseText }
        );
    }

    async simulateResponse(message) {
        console.log('🎭 Simulating response for:', message);
        
        // Simulate processing delay
        await new Promise(resolve => setTimeout(resolve, 2000));

        const lowerMessage = message.toLowerCase();
        let response = `I understand you're asking about: "${message}"\n\n`;
        
        if (lowerMessage.includes('note') || lowerMessage.includes('summary')) {
            response += "🗒️ **Selected Tool:** Note Maker\n\n";
            response += "**Reasoning:** Detected request for note-taking assistance.\n\n";
            response += "**Extracted Parameters:**\n• Topic: " + this.extractTopic(message) + "\n• Style: Outline format\n• Include examples: Yes";
            
            this.addResult({
                title: 'Note Maker Tool',
                status: 'success',
                content: 'Would generate structured notes on ' + this.extractTopic(message),
                timestamp: new Date().toLocaleTimeString()
            });
        }
        else if (lowerMessage.includes('flashcard') || lowerMessage.includes('memorize') || lowerMessage.includes('quiz')) {
            response += "🃏 **Selected Tool:** Flashcard Generator\n\n";
            response += "**Reasoning:** Identified request for memorization materials.\n\n";
            response += "**Extracted Parameters:**\n• Topic: " + this.extractTopic(message) + "\n• Count: 5-10 cards\n• Difficulty: Medium";
            
            this.addResult({
                title: 'Flashcard Generator',
                status: 'success',
                content: 'Would create flashcards for ' + this.extractTopic(message),
                timestamp: new Date().toLocaleTimeString()
            });
        }
        else if (lowerMessage.includes('explain') || lowerMessage.includes('what is') || lowerMessage.includes('how')) {
            response += "💡 **Selected Tool:** Concept Explainer\n\n";
            response += "**Reasoning:** Detected request for conceptual explanation.\n\n";
            response += "**Extracted Parameters:**\n• Concept: " + this.extractTopic(message) + "\n• Depth: Intermediate\n• Include examples: Yes\n\n";
            
            // Add actual explanation content
            const topic = this.extractTopic(message);
            if (topic.toLowerCase().includes('quantum')) {
                response += "💡 **Concept Explanation:**\n";
                response += "Quantum mechanics is the branch of physics that describes the behavior of matter and energy at the atomic and subatomic level. Unlike classical physics, quantum mechanics shows that particles can exist in multiple states simultaneously (superposition) until they are observed.\n\n";
                response += "📚 **Examples:**\n";
                response += "1. Schrödinger's cat - demonstrates superposition where a cat can be both alive and dead until observed\n";
                response += "2. Double-slit experiment - shows light behaves as both wave and particle\n";
                response += "3. Quantum tunneling - particles can pass through barriers they shouldn't classically be able to cross\n\n";
                response += "🔗 **Related Concepts:**\n";
                response += "• Wave-particle duality\n• Uncertainty principle\n• Quantum entanglement\n\n";
                response += "❓ **Practice Questions:**\n";
                response += "1. What is superposition in quantum mechanics?\n";
                response += "2. How does observation affect quantum systems?\n";
                response += "3. What makes quantum mechanics different from classical physics?\n\n";
            } else {
                response += "💡 **Concept Explanation:**\n";
                response += `${topic} is a fundamental concept that involves several key principles and mechanisms. Understanding ${topic} requires breaking it down into its core components and examining how they interact.\n\n`;
                response += "📚 **Examples:**\n";
                response += `1. Practical application of ${topic}\n`;
                response += `2. Real-world instance of ${topic}\n`;
                response += `3. Common example demonstrating ${topic}\n\n`;
                response += "🔗 **Related Concepts:**\n";
                response += `• Fundamental principles of ${topic}\n• Applications of ${topic}\n• Advanced aspects of ${topic}\n\n`;
            }
            
            this.addResult({
                title: 'Concept Explainer',
                status: 'success',
                content: 'Explained ' + this.extractTopic(message) + ' with examples and practice questions',
                timestamp: new Date().toLocaleTimeString()
            });
        }
        else {
            response += "🤖 **Selected Tools:** Multiple tools detected\n\n";
            response += "**Reasoning:** Your request could benefit from multiple educational tools.\n\n";
            response += "**Note:** This is a demo response showing the orchestrator's capabilities.";
            
            this.addResult({
                title: 'Multi-tool Analysis',
                status: 'success',
                content: 'Complex request requiring multiple educational tools',
                timestamp: new Date().toLocaleTimeString()
            });
        }

        this.addMessage(response, 'assistant');
        
        // Update chat history
        this.chatHistory.push(
            { role: 'user', content: message },
            { role: 'assistant', content: response }
        );
    }

    extractTopic(message) {
        const words = message.split(' ');
        const topics = words.filter(word => 
            word.length > 4 && 
            !['about', 'with', 'need', 'help', 'please', 'could', 'would', 'explain'].includes(word.toLowerCase())
        );
        return topics[0] || 'general topic';
    }

    addMessage(content, role) {
        console.log('💬 Adding message:', role, content.substring(0, 50) + '...');
        
        if (!this.chatMessages) {
            console.error('❌ Chat messages container not found');
            return;
        }

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;
        
        const bubbleDiv = document.createElement('div');
        bubbleDiv.className = 'message-bubble';
        
        // Convert markdown-like formatting to HTML
        const formattedContent = content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');
        
        bubbleDiv.innerHTML = formattedContent;
        messageDiv.appendChild(bubbleDiv);
        
        // Remove welcome message if it exists
        const welcomeMessage = this.chatMessages.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.remove();
        }
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    addResult(result) {
        if (!this.resultsContainer) return;
        
        // Remove no-results message if it exists
        const noResults = this.resultsContainer.querySelector('.no-results');
        if (noResults) {
            noResults.remove();
        }

        const resultDiv = document.createElement('div');
        resultDiv.className = 'result-item';
        
        resultDiv.innerHTML = `
            <div class="result-header">
                <span class="result-title">${result.title}</span>
                <span class="result-status ${result.status}">${result.status}</span>
            </div>
            <div class="result-content">
                ${result.content}
                <br><small>Time: ${result.timestamp}</small>
            </div>
        `;
        
        this.resultsContainer.insertBefore(resultDiv, this.resultsContainer.firstChild);
        
        // Limit to 10 results
        const results = this.resultsContainer.querySelectorAll('.result-item');
        if (results.length > 10) {
            results[results.length - 1].remove();
        }
    }

    formatToolResult(toolResponse) {
        const data = toolResponse.data;
        const toolName = toolResponse.tool_name;
        
        if (toolName === 'note_maker') {
            const sections = data.note_sections?.length || 0;
            const concepts = data.key_concepts?.length || 0;
            return `Generated ${sections} note sections covering ${concepts} key concepts. Style: ${data.note_taking_style || 'structured'}`;
        } else if (toolName === 'flashcard_generator') {
            const cards = data.flashcards?.length || 0;
            const difficulty = data.difficulty || 'medium';
            return `Created ${cards} flashcards at ${difficulty} difficulty level. ${data.adaptation_details || ''}`;
        } else if (toolName === 'concept_explainer') {
            const examples = data.examples?.length || 0;
            const related = data.related_concepts?.length || 0;
            return `Provided detailed explanation with ${examples} examples and ${related} related concepts`;
        }
        
        return 'Tool executed successfully';
    }

    updateUserProfile() {
        const learningStyles = {
            'visual': 'Visual learner, prefers diagrams, examples, and structured notes',
            'auditory': 'Auditory learner, prefers verbal explanations and step-by-step guidance',
            'kinesthetic': 'Kinesthetic learner, prefers hands-on practice and interactive exercises',
            'reading': 'Reading/Writing learner, prefers detailed text and written materials'
        };

        const emotionalStates = {
            'focused': 'Focused and motivated, ready for challenging material',
            'anxious': 'Anxious about upcoming test, needs reassurance and simplified approach',
            'confused': 'Confused about recent topics, requires step-by-step clarification',
            'tired': 'Tired after long day, prefers gentle and minimal cognitive load'
        };

        this.currentUser = {
            user_id: this.currentUser.user_id,
            name: this.studentName?.value || 'Demo Student',
            grade_level: this.gradeLevel?.value || '10',
            learning_style_summary: learningStyles[this.learningStyle?.value] || learningStyles.visual,
            emotional_state_summary: emotionalStates[this.emotionalState?.value] || emotionalStates.focused,
            mastery_level_summary: `Level 5: Developing competence for grade ${this.gradeLevel?.value || '10'}`
        };

        this.showToast('Profile updated successfully!', 'success');
    }

    autoResizeTextarea() {
        if (!this.chatInput) return;
        this.chatInput.style.height = 'auto';
        this.chatInput.style.height = Math.min(this.chatInput.scrollHeight, 120) + 'px';
    }

    scrollToBottom() {
        if (this.chatMessages) {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }
    }

    showLoading(show) {
        if (this.loadingOverlay) {
            if (show) {
                this.loadingOverlay.classList.add('active');
            } else {
                this.loadingOverlay.classList.remove('active');
            }
        }
    }

    showToast(message, type = 'success') {
        console.log(`🍞 Toast: ${type} - ${message}`);
        
        if (!this.toastContainer) return;
        
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        
        this.toastContainer.appendChild(toast);
        
        // Trigger animation
        setTimeout(() => toast.classList.add('show'), 100);
        
        // Remove after 3 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }, 3000);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('📄 DOM loaded, initializing app...');
    window.tutorOrchestrator = new TutorOrchestrator();
    
    console.log(`
    🧠 AI Tutor Orchestrator
    ========================
    
    Welcome to the future of educational AI!
    
    Keyboard shortcuts:
    • Ctrl/Cmd + K: Focus chat input
    • Ctrl/Cmd + L: Clear chat
    • Enter: Send message
    • Shift + Enter: New line
    
    Built with ❤️ using DeepSeek AI
    `);
});

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey || e.metaKey) {
        switch(e.key) {
            case 'k':
                e.preventDefault();
                const chatInput = document.getElementById('chat-input');
                if (chatInput) chatInput.focus();
                break;
        }
    }
});