// MentorOS - Professional 3D AI Tutoring Dashboard
console.log('🚀 MentorOS Loading...');

class MentorOS {
    constructor() {
        console.log('🏗️ MentorOS Constructor called');
        this.apiBaseUrl = window.location.origin;
        this.isConnected = false;
        this.currentUser = this.getDefaultUser();
        this.chatHistory = [];
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.particles = [];
        this.mouseX = 0;
        this.mouseY = 0;
        
        console.log('🌐 API Base URL:', this.apiBaseUrl);
        
        // Initialize after a short delay to ensure DOM is ready
        setTimeout(() => {
            this.initializeElements();
            this.init3DBackground();
            this.createParticleNetwork();
            this.bindEvents();
            this.testConnection();
            this.updateTimeDisplay();
            this.initProgressRings();
            this.checkLoginState();
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
        console.log('🔍 Initializing MentorOS elements...');
        
        // Chat elements
        this.chatMessages = document.getElementById('chat-messages');
        this.chatInput = document.getElementById('chat-input');
        this.sendButton = document.getElementById('send-button');
        
        // Navigation elements
        this.navbar = document.getElementById('navbar');
        this.navItems = document.querySelectorAll('.nav-item');
        this.logoutBtn = document.getElementById('logoutBtn');
        
        // Status elements
        this.connectionStatus = document.getElementById('connection-status');
        this.timeDisplay = document.getElementById('timeDisplay');
        
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
        
        // 3D Background elements
        this.bgCanvas = document.getElementById('bg-canvas');
        this.particleNetwork = document.getElementById('particle-network');
        
        // Initialize Lucide icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
        
        console.log('✅ MentorOS Element check:');
        console.log('  chatInput:', this.chatInput ? '✅' : '❌');
        console.log('  sendButton:', this.sendButton ? '✅' : '❌');
        console.log('  chatMessages:', this.chatMessages ? '✅' : '❌');
        console.log('  navbar:', this.navbar ? '✅' : '❌');
        console.log('  bgCanvas:', this.bgCanvas ? '✅' : '❌');
    }

    init3DBackground() {
        if (!this.bgCanvas || typeof THREE === 'undefined') {
            console.log('⚠️ Three.js not available, skipping 3D background');
            return;
        }
        
        try {
            // Scene setup
            this.scene = new THREE.Scene();
            this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            this.renderer = new THREE.WebGLRenderer({ canvas: this.bgCanvas, alpha: true });
            this.renderer.setSize(window.innerWidth, window.innerHeight);
            this.renderer.setClearColor(0x000000, 0);
            
            // Camera position
            this.camera.position.z = 5;
            
            // Create floating geometric shapes
            this.createFloatingShapes();
            
            // Lighting
            const ambientLight = new THREE.AmbientLight(0x00d4ff, 0.3);
            this.scene.add(ambientLight);
            
            const pointLight = new THREE.PointLight(0x7c3aed, 1, 100);
            pointLight.position.set(10, 10, 10);
            this.scene.add(pointLight);
            
            // Start animation loop
            this.animate3D();
            
            console.log('✅ 3D Background initialized');
        } catch (error) {
            console.error('❌ 3D Background initialization failed:', error);
        }
    }
    
    createFloatingShapes() {
        const geometries = [
            new THREE.TetrahedronGeometry(0.5),
            new THREE.OctahedronGeometry(0.3),
            new THREE.IcosahedronGeometry(0.4),
            new THREE.DodecahedronGeometry(0.3)
        ];
        
        const materials = [
            new THREE.MeshPhongMaterial({ 
                color: 0x00d4ff, 
                transparent: true, 
                opacity: 0.6,
                wireframe: true 
            }),
            new THREE.MeshPhongMaterial({ 
                color: 0x7c3aed, 
                transparent: true, 
                opacity: 0.4,
                wireframe: true 
            }),
            new THREE.MeshPhongMaterial({ 
                color: 0x00ff88, 
                transparent: true, 
                opacity: 0.5,
                wireframe: true 
            })
        ];
        
        for (let i = 0; i < 12; i++) {
            const geometry = geometries[Math.floor(Math.random() * geometries.length)];
            const material = materials[Math.floor(Math.random() * materials.length)];
            const mesh = new THREE.Mesh(geometry, material);
            
            mesh.position.x = (Math.random() - 0.5) * 20;
            mesh.position.y = (Math.random() - 0.5) * 20;
            mesh.position.z = (Math.random() - 0.5) * 10;
            
            mesh.rotation.x = Math.random() * Math.PI;
            mesh.rotation.y = Math.random() * Math.PI;
            
            mesh.userData = {
                rotationSpeed: {
                    x: (Math.random() - 0.5) * 0.02,
                    y: (Math.random() - 0.5) * 0.02,
                    z: (Math.random() - 0.5) * 0.02
                },
                floatSpeed: Math.random() * 0.02 + 0.01,
                floatRange: Math.random() * 2 + 1
            };
            
            this.scene.add(mesh);
            this.particles.push(mesh);
        }
    }
    
    createParticleNetwork() {
        if (!this.particleNetwork) return;
        
        // Create floating particles
        for (let i = 0; i < 40; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.top = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 8 + 's';
            particle.style.animationDuration = (Math.random() * 6 + 6) + 's';
            this.particleNetwork.appendChild(particle);
        }
        
        // Create connecting lines
        for (let i = 0; i < 15; i++) {
            const line = document.createElement('div');
            line.className = 'particle-line';
            line.style.left = Math.random() * 100 + '%';
            line.style.top = Math.random() * 100 + '%';
            line.style.width = (Math.random() * 200 + 100) + 'px';
            line.style.transform = `rotate(${Math.random() * 360}deg)`;
            line.style.animationDelay = Math.random() * 4 + 's';
            this.particleNetwork.appendChild(line);
        }
    }
    
    animate3D() {
        if (!this.scene || !this.camera || !this.renderer) return;
        
        requestAnimationFrame(() => this.animate3D());
        
        // Animate floating shapes
        this.particles.forEach((particle, index) => {
            const userData = particle.userData;
            
            // Rotation
            particle.rotation.x += userData.rotationSpeed.x;
            particle.rotation.y += userData.rotationSpeed.y;
            particle.rotation.z += userData.rotationSpeed.z;
            
            // Floating motion
            particle.position.y += Math.sin(Date.now() * userData.floatSpeed + index) * 0.01;
            
            // Mouse interaction
            const distance = particle.position.distanceTo(this.camera.position);
            if (distance < 10) {
                particle.position.x += this.mouseX * 0.01;
                particle.position.y += this.mouseY * 0.01;
            }
        });
        
        // Camera slight movement based on mouse
        this.camera.position.x += (this.mouseX * 0.3 - this.camera.position.x) * 0.05;
        this.camera.position.y += (this.mouseY * 0.3 - this.camera.position.y) * 0.05;
        this.camera.lookAt(this.scene.position);
        
        this.renderer.render(this.scene, this.camera);
    }

    bindEvents() {
        console.log('🔗 Binding MentorOS events...');
        
        if (!this.sendButton || !this.chatInput) {
            console.error('❌ Critical elements not found!');
            return;
        }
        
        // Mouse movement for 3D parallax
        document.addEventListener('mousemove', (e) => {
            this.mouseX = (e.clientX / window.innerWidth) * 2 - 1;
            this.mouseY = -(e.clientY / window.innerHeight) * 2 + 1;
        });
        
        // Window resize
        window.addEventListener('resize', () => {
            if (this.camera && this.renderer) {
                this.camera.aspect = window.innerWidth / window.innerHeight;
                this.camera.updateProjectionMatrix();
                this.renderer.setSize(window.innerWidth, window.innerHeight);
            }
        });
        
        // Navigation
        this.navItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleNavigation(item.dataset.page);
            });
        });
        
        // Logout
        if (this.logoutBtn) {
            this.logoutBtn.addEventListener('click', () => {
                this.handleLogout();
            });
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
        
        // Chat controls
        const clearChatBtn = document.getElementById('clear-chat');
        const exportChatBtn = document.getElementById('export-chat');
        const toggleHistoryBtn = document.getElementById('toggle-history');
        
        if (clearChatBtn) {
            clearChatBtn.addEventListener('click', () => {
                this.clearChat();
            });
        }
        
        if (exportChatBtn) {
            exportChatBtn.addEventListener('click', () => {
                this.exportChat();
            });
        }
        
        if (toggleHistoryBtn) {
            toggleHistoryBtn.addEventListener('click', () => {
                this.toggleHistory();
            });
        }

        // Suggestion chips
        this.suggestionChips.forEach(chip => {
            chip.addEventListener('click', () => {
                const text = chip.getAttribute('data-text');
                this.chatInput.value = text;
                this.autoResizeTextarea();
                this.chatInput.focus();
                
                // Add visual feedback
                this.addChipClickEffect(chip);
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
        
        console.log('✅ MentorOS Events bound successfully');
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

    addMessage(content, role, removeWelcome = true) {
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
        
        // Remove welcome message if it exists and removeWelcome is true
        if (removeWelcome) {
            const welcomeMessage = this.chatMessages.querySelector('.welcome-message');
            if (welcomeMessage) {
                welcomeMessage.remove();
            }
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

    updateTimeDisplay() {
        if (!this.timeDisplay) return;
        
        const updateTime = () => {
            const now = new Date();
            const timeString = now.toLocaleTimeString('en-US', {
                hour12: false,
                hour: '2-digit',
                minute: '2-digit'
            });
            this.timeDisplay.textContent = timeString;
        };
        
        updateTime();
        setInterval(updateTime, 1000);
    }
    
    initProgressRings() {
        const progressRings = document.querySelectorAll('.progress-ring');
        progressRings.forEach(ring => {
            const progress = parseInt(ring.dataset.progress);
            const circle = ring.querySelector('.progress-fill');
            const circumference = 2 * Math.PI * 25; // radius = 25
            const offset = circumference - (progress / 100) * circumference;
            
            setTimeout(() => {
                circle.style.strokeDashoffset = offset;
            }, 500);
        });
    }
    
    checkLoginState() {
        const user = localStorage.getItem('mentorOS_user');
        if (user) {
            const userData = JSON.parse(user);
            console.log('👤 User logged in:', userData.email);
            
            // Update user profile display
            const userNameElement = document.querySelector('.user-name');
            if (userNameElement && userData.email) {
                userNameElement.textContent = userData.email.split('@')[0];
            }
        }
    }
    
    handleNavigation(page) {
        // Remove active class from all nav items
        this.navItems.forEach(item => item.classList.remove('active'));
        
        // Add active class to clicked item
        const activeItem = document.querySelector(`[data-page="${page}"]`);
        if (activeItem) {
            activeItem.classList.add('active');
        }
        
        // Handle navigation
        const pageNames = {
            dashboard: 'Dashboard',
            students: 'Student Management',
            sessions: 'Tutor Sessions',
            analytics: 'Learning Analytics',
            settings: 'System Settings'
        };
        
        if (page === 'dashboard') {
            // Already on dashboard, do nothing
            return;
        } else if (page === 'settings') {
            // Navigate to settings page
            window.location.href = '/settings';
            return;
        } else {
            // Show coming soon for other pages
            this.showToast(`${pageNames[page]} - Coming Soon!`, 'info');
        }
    }
    
    handleLogout() {
        // Clear login state
        localStorage.removeItem('mentorOS_user');
        localStorage.removeItem('mentorOS_remember');
        
        this.showToast('Logging out...', 'info');
        
        // Redirect to login after animation
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 1500);
    }
    
    addChipClickEffect(chip) {
        // Add temporary glow effect
        chip.style.transform = 'translateY(-3px) scale(1.05)';
        chip.style.boxShadow = '0 0 20px rgba(0, 212, 255, 0.5)';
        
        setTimeout(() => {
            chip.style.transform = '';
            chip.style.boxShadow = '';
        }, 300);
    }
    
    async clearChat() {
        if (!confirm('Are you sure you want to clear all chat history? This action cannot be undone.')) {
            return;
        }
        
        this.showLoading(true);
        
        try {
            const user = JSON.parse(localStorage.getItem('mentorOS_user') || '{}');
            const userId = user.id || 'demo';
            
            const response = await fetch(`${this.apiBaseUrl}/user/${userId}/chat/history`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                // Clear the chat messages display
                if (this.chatMessages) {
                    this.chatMessages.innerHTML = `
                        <div class="welcome-message">
                            <div class="welcome-animation">
                                <div class="hologram-ring"></div>
                                <div class="hologram-ring"></div>
                                <div class="hologram-ring"></div>
                                <div class="welcome-icon">
                                    <i data-lucide="brain-circuit"></i>
                                </div>
                            </div>
                            <h3>Chat Cleared!</h3>
                            <p>Your conversation history has been cleared. Start a new conversation below.</p>
                            <div class="feature-grid">
                                <div class="feature-card">
                                    <i data-lucide="file-text"></i>
                                    <span>Smart Notes</span>
                                </div>
                                <div class="feature-card">
                                    <i data-lucide="layers"></i>
                                    <span>Flashcards</span>
                                </div>
                                <div class="feature-card">
                                    <i data-lucide="lightbulb"></i>
                                    <span>Explanations</span>
                                </div>
                                <div class="feature-card">
                                    <i data-lucide="target"></i>
                                    <span>Adaptive Learning</span>
                                </div>
                            </div>
                        </div>
                    `;
                    
                    // Reinitialize Lucide icons
                    if (typeof lucide !== 'undefined') {
                        lucide.createIcons();
                    }
                }
                
                // Clear local chat history
                this.chatHistory = [];
                
                // Clear results container
                if (this.resultsContainer) {
                    this.resultsContainer.innerHTML = `
                        <div class="no-results">
                            <div class="empty-state">
                                <div class="empty-icon">
                                    <i data-lucide="inbox"></i>
                                </div>
                                <h4>No Activity Yet</h4>
                                <p>Start a conversation to see your learning orchestration results!</p>
                            </div>
                        </div>
                    `;
                    
                    // Reinitialize Lucide icons
                    if (typeof lucide !== 'undefined') {
                        lucide.createIcons();
                    }
                }
                
                this.showToast('Chat history cleared successfully!', 'success');
            } else {
                throw new Error('Failed to clear chat history');
            }
        } catch (error) {
            console.error('❌ Clear chat error:', error);
            this.showToast('Failed to clear chat history. Please try again.', 'error');
        } finally {
            this.showLoading(false);
        }
    }
    
    async exportChat() {
        this.showLoading(true);
        
        try {
            const user = JSON.parse(localStorage.getItem('mentorOS_user') || '{}');
            const userId = user.id || 'demo';
            
            const response = await fetch(`${this.apiBaseUrl}/user/${userId}/chat/export`);
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `mentoros_chat_export_${new Date().toISOString().split('T')[0]}.json`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
                
                this.showToast('Chat history exported successfully!', 'success');
            } else {
                // Fallback: export local chat history
                const exportData = {
                    user_id: userId,
                    export_date: new Date().toISOString(),
                    message_count: this.chatHistory.length,
                    messages: this.chatHistory.map(msg => ({
                        role: msg.role,
                        content: msg.content,
                        timestamp: new Date().toISOString()
                    }))
                };
                
                const dataStr = JSON.stringify(exportData, null, 2);
                const dataBlob = new Blob([dataStr], { type: 'application/json' });
                const url = window.URL.createObjectURL(dataBlob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `mentoros_chat_export_${new Date().toISOString().split('T')[0]}.json`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
                
                this.showToast('Chat history exported (local data)!', 'success');
            }
        } catch (error) {
            console.error('❌ Export chat error:', error);
            this.showToast('Failed to export chat history. Please try again.', 'error');
        } finally {
            this.showLoading(false);
        }
    }
    
    async toggleHistory() {
        this.showLoading(true);
        
        try {
            const user = JSON.parse(localStorage.getItem('mentorOS_user') || '{}');
            const userId = user.id || 'demo';
            
            const response = await fetch(`${this.apiBaseUrl}/user/${userId}/chat/history?limit=20`);
            
            if (response.ok) {
                const data = await response.json();
                
                if (data.success && data.messages.length > 0) {
                    // Clear current messages
                    if (this.chatMessages) {
                        this.chatMessages.innerHTML = '';
                        
                        // Add history messages
                        data.messages.forEach(msg => {
                            this.addMessage(msg.content, msg.role, false);
                        });
                        
                        this.showToast(`Loaded ${data.messages.length} previous messages`, 'info');
                    }
                } else {
                    this.showToast('No chat history found', 'info');
                }
            } else {
                this.showToast('Failed to load chat history', 'error');
            }
        } catch (error) {
            console.error('❌ Toggle history error:', error);
            this.showToast('Failed to load chat history', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    showToast(message, type = 'success') {
        console.log(`🍞 MentorOS Toast: ${type} - ${message}`);
        
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        const colors = {
            success: 'rgba(0, 255, 136, 0.9)',
            error: 'rgba(255, 71, 87, 0.9)',
            warning: 'rgba(255, 133, 0, 0.9)',
            info: 'rgba(0, 212, 255, 0.9)'
        };
        
        const icons = {
            success: 'check-circle',
            error: 'alert-circle',
            warning: 'alert-triangle',
            info: 'info'
        };
        
        toast.innerHTML = `
            <div class="toast-content">
                <i data-lucide="${icons[type] || 'info'}"></i>
                <span>${message}</span>
            </div>
        `;
        
        // Style the toast
        Object.assign(toast.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            background: colors[type] || colors.info,
            color: 'white',
            padding: '1rem 1.5rem',
            borderRadius: '12px',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            boxShadow: '0 10px 30px rgba(0, 0, 0, 0.3)',
            zIndex: '10000',
            transform: 'translateX(100%)',
            transition: 'transform 0.3s ease-out',
            maxWidth: '400px',
            fontSize: '0.9rem',
            fontWeight: '500'
        });
        
        toast.querySelector('.toast-content').style.cssText = `
            display: flex;
            align-items: center;
            gap: 0.5rem;
        `;
        
        document.body.appendChild(toast);
        
        // Initialize Lucide icon
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
        
        // Animate in
        setTimeout(() => {
            toast.style.transform = 'translateX(0)';
        }, 100);
        
        // Remove after delay
        setTimeout(() => {
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }, 4000);
    }
}

// Initialize MentorOS when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('📄 DOM loaded, initializing MentorOS...');
    
    // Check if user is logged in (but allow demo mode)
    const user = localStorage.getItem('mentorOS_user');
    if (!user) {
        console.log('🔒 No user session found, but continuing in demo mode...');
        // For demo purposes, create a temporary user session
        const demoUser = {
            email: 'demo@mentoros.ai',
            loginTime: new Date().toISOString(),
            demo: true
        };
        localStorage.setItem('mentorOS_user', JSON.stringify(demoUser));
    }
    
    window.mentorOS = new MentorOS();
    
    console.log(`
    🧠 MentorOS - Professional AI Tutoring System
    =============================================
    
    Welcome to the future of intelligent education!
    
    🎯 Features:
    • 3D Interactive Dashboard
    • AI-Powered Tool Orchestration  
    • Adaptive Learning Profiles
    • Real-time Progress Tracking
    
    ⌨️ Keyboard shortcuts:
    • Ctrl/Cmd + K: Focus chat input
    • Ctrl/Cmd + /: Toggle navigation
    • Enter: Send message
    • Shift + Enter: New line
    
    Built with ❤️ using advanced AI & 3D graphics
    `);
});

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey || e.metaKey) {
        switch(e.key) {
            case 'k':
                e.preventDefault();
                const chatInput = document.getElementById('chat-input');
                if (chatInput) {
                    chatInput.focus();
                    chatInput.select();
                }
                break;
            case '/':
                e.preventDefault();
                const navbar = document.getElementById('navbar');
                if (navbar) {
                    document.body.classList.toggle('nav-collapsed');
                }
                break;
        }
    }
});

// Handle page visibility for performance optimization
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        console.log('🔇 MentorOS paused (tab hidden)');
    } else {
        console.log('🔊 MentorOS resumed (tab visible)');
    }
});