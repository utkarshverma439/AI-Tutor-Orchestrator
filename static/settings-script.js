// MentorOS Settings - Professional Settings Management
console.log('🚀 MentorOS Settings Loading...');

class MentorOSSettings {
    constructor() {
        console.log('⚙️ Settings Constructor called');
        this.apiBaseUrl = window.location.origin;
        this.currentUser = null;
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.particles = [];
        this.mouseX = 0;
        this.mouseY = 0;
        
        // Initialize after a short delay to ensure DOM is ready
        setTimeout(() => {
            this.initializeElements();
            this.init3DBackground();
            this.createParticleNetwork();
            this.bindEvents();
            this.loadUserData();
            this.updateTimeDisplay();
            this.checkLoginState();
        }, 100);
    }
    
    initializeElements() {
        console.log('🔍 Initializing Settings elements...');
        
        // Navigation elements
        this.navbar = document.getElementById('navbar');
        this.navItems = document.querySelectorAll('.nav-item');
        this.logoutBtn = document.getElementById('logoutBtn');
        
        // Profile elements
        this.studentName = document.getElementById('student-name');
        this.studentEmail = document.getElementById('student-email');
        this.gradeLevel = document.getElementById('grade-level');
        this.learningStyle = document.getElementById('learning-style');
        this.emotionalState = document.getElementById('emotional-state');
        this.teachingStyle = document.getElementById('teaching-style');
        this.saveProfileBtn = document.getElementById('saveProfileBtn');
        
        // Preference elements
        this.themeRadios = document.querySelectorAll('input[name="theme"]');
        this.notificationsSwitch = document.getElementById('notifications');
        this.soundEffectsSwitch = document.getElementById('sound-effects');
        this.animationsSwitch = document.getElementById('animations');
        this.dataSharingSwitch = document.getElementById('data-sharing');
        
        // Action buttons
        this.exportDataBtn = document.getElementById('exportDataBtn');
        this.clearHistoryBtn = document.getElementById('clearHistoryBtn');
        this.resetSettingsBtn = document.getElementById('resetSettingsBtn');
        
        // Other elements
        this.timeDisplay = document.getElementById('timeDisplay');
        this.loadingOverlay = document.getElementById('loadingOverlay');
        this.bgCanvas = document.getElementById('bg-canvas');
        this.particleNetwork = document.getElementById('particle-network');
        
        // Initialize Lucide icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
        
        console.log('✅ Settings Elements initialized');
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
        
        for (let i = 0; i < 8; i++) {
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
        for (let i = 0; i < 30; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.top = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 8 + 's';
            particle.style.animationDuration = (Math.random() * 6 + 6) + 's';
            this.particleNetwork.appendChild(particle);
        }
        
        // Create connecting lines
        for (let i = 0; i < 10; i++) {
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
        console.log('🔗 Binding Settings events...');
        
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
        
        // Save Profile
        if (this.saveProfileBtn) {
            this.saveProfileBtn.addEventListener('click', () => {
                this.saveProfile();
            });
        }
        
        // Data Management Actions
        if (this.exportDataBtn) {
            this.exportDataBtn.addEventListener('click', () => {
                this.exportData();
            });
        }
        
        if (this.clearHistoryBtn) {
            this.clearHistoryBtn.addEventListener('click', () => {
                this.clearHistory();
            });
        }
        
        if (this.resetSettingsBtn) {
            this.resetSettingsBtn.addEventListener('click', () => {
                this.resetSettings();
            });
        }
        
        // Preference changes
        this.themeRadios.forEach(radio => {
            radio.addEventListener('change', () => {
                this.updatePreferences();
            });
        });
        
        [this.notificationsSwitch, this.soundEffectsSwitch, this.animationsSwitch, this.dataSharingSwitch]
            .forEach(element => {
                if (element) {
                    element.addEventListener('change', () => {
                        this.updatePreferences();
                    });
                }
            });
        
        console.log('✅ Settings Events bound successfully');
    }
    
    loadUserData() {
        const user = localStorage.getItem('mentorOS_user');
        if (user) {
            this.currentUser = JSON.parse(user);
            
            // Populate form fields
            if (this.studentEmail) {
                this.studentEmail.value = this.currentUser.email || 'demo@mentoros.ai';
            }
            
            // Load saved preferences
            const preferences = localStorage.getItem('mentorOS_preferences');
            if (preferences) {
                const prefs = JSON.parse(preferences);
                this.applyPreferences(prefs);
            }
        }
    }
    
    applyPreferences(preferences) {
        // Apply theme
        if (preferences.theme) {
            const themeRadio = document.getElementById(`theme-${preferences.theme}`);
            if (themeRadio) themeRadio.checked = true;
        }
        
        // Apply switches
        if (this.notificationsSwitch) this.notificationsSwitch.checked = preferences.notifications !== false;
        if (this.soundEffectsSwitch) this.soundEffectsSwitch.checked = preferences.soundEffects !== false;
        if (this.animationsSwitch) this.animationsSwitch.checked = preferences.animations !== false;
        if (this.dataSharingSwitch) this.dataSharingSwitch.checked = preferences.dataSharing === true;
    }
    
    async saveProfile() {
        if (!this.currentUser) {
            this.showToast('Please log in to save profile', 'error');
            return;
        }
        
        this.showLoading(true);
        
        try {
            const profileData = {
                name: this.studentName?.value || 'Demo Student',
                grade_level: this.gradeLevel?.value || '10',
                learning_style: this.learningStyle?.value || 'visual',
                emotional_state: this.emotionalState?.value || 'focused',
                teaching_style: this.teachingStyle?.value || 'direct'
            };
            
            // Save to backend
            const response = await fetch(`${this.apiBaseUrl}/user/${this.currentUser.id || 'demo'}/profile`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(profileData)
            });
            
            if (response.ok) {
                // Update local storage
                this.currentUser = { ...this.currentUser, ...profileData };
                localStorage.setItem('mentorOS_user', JSON.stringify(this.currentUser));
                
                this.showToast('Profile saved successfully!', 'success');
            } else {
                throw new Error('Failed to save profile');
            }
        } catch (error) {
            console.error('❌ Profile save error:', error);
            this.showToast('Failed to save profile. Please try again.', 'error');
        } finally {
            this.showLoading(false);
        }
    }
    
    updatePreferences() {
        const preferences = {
            theme: document.querySelector('input[name="theme"]:checked')?.value || 'dark',
            notifications: this.notificationsSwitch?.checked !== false,
            soundEffects: this.soundEffectsSwitch?.checked !== false,
            animations: this.animationsSwitch?.checked !== false,
            dataSharing: this.dataSharingSwitch?.checked === true
        };
        
        // Save to local storage
        localStorage.setItem('mentorOS_preferences', JSON.stringify(preferences));
        
        // Apply theme changes immediately
        if (preferences.theme === 'light') {
            document.body.classList.add('light-theme');
        } else {
            document.body.classList.remove('light-theme');
        }
        
        this.showToast('Preferences updated!', 'success');
    }
    
    async exportData() {
        if (!this.currentUser) {
            this.showToast('Please log in to export data', 'error');
            return;
        }
        
        this.showLoading(true);
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/user/${this.currentUser.id || 'demo'}/chat/export`);
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `mentoros_export_${new Date().toISOString().split('T')[0]}.json`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
                
                this.showToast('Data exported successfully!', 'success');
            } else {
                throw new Error('Failed to export data');
            }
        } catch (error) {
            console.error('❌ Export error:', error);
            this.showToast('Failed to export data. Please try again.', 'error');
        } finally {
            this.showLoading(false);
        }
    }
    
    async clearHistory() {
        if (!confirm('Are you sure you want to clear all chat history? This action cannot be undone.')) {
            return;
        }
        
        if (!this.currentUser) {
            this.showToast('Please log in to clear history', 'error');
            return;
        }
        
        this.showLoading(true);
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/user/${this.currentUser.id || 'demo'}/chat/history`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                this.showToast('Chat history cleared successfully!', 'success');
            } else {
                throw new Error('Failed to clear history');
            }
        } catch (error) {
            console.error('❌ Clear history error:', error);
            this.showToast('Failed to clear history. Please try again.', 'error');
        } finally {
            this.showLoading(false);
        }
    }
    
    resetSettings() {
        if (!confirm('Are you sure you want to reset all settings to default? This will clear your preferences and profile settings.')) {
            return;
        }
        
        // Reset form values
        if (this.studentName) this.studentName.value = 'Demo Student';
        if (this.gradeLevel) this.gradeLevel.value = '10';
        if (this.learningStyle) this.learningStyle.value = 'visual';
        if (this.emotionalState) this.emotionalState.value = 'focused';
        if (this.teachingStyle) this.teachingStyle.value = 'direct';
        
        // Reset preferences
        document.getElementById('theme-dark').checked = true;
        if (this.notificationsSwitch) this.notificationsSwitch.checked = true;
        if (this.soundEffectsSwitch) this.soundEffectsSwitch.checked = true;
        if (this.animationsSwitch) this.animationsSwitch.checked = true;
        if (this.dataSharingSwitch) this.dataSharingSwitch.checked = false;
        
        // Clear local storage
        localStorage.removeItem('mentorOS_preferences');
        
        // Apply changes
        this.updatePreferences();
        
        this.showToast('Settings reset to default!', 'success');
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
        if (page === 'dashboard') {
            window.location.href = '/';
            return;
        }
        
        // For other pages, show coming soon
        const pageNames = {
            students: 'Student Management',
            sessions: 'Tutor Sessions',
            analytics: 'Learning Analytics',
            settings: 'Settings'
        };
        
        if (page !== 'settings') {
            this.showToast(`${pageNames[page]} - Coming Soon!`, 'info');
        }
    }
    
    handleLogout() {
        // Clear login state
        localStorage.removeItem('mentorOS_user');
        localStorage.removeItem('mentorOS_remember');
        localStorage.removeItem('mentorOS_preferences');
        
        this.showToast('Logging out...', 'info');
        
        // Redirect to login after animation
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 1500);
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
        console.log(`🍞 Settings Toast: ${type} - ${message}`);
        
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

// Initialize Settings when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('📄 DOM loaded, initializing MentorOS Settings...');
    
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
    
    window.mentorOSSettings = new MentorOSSettings();
    
    console.log(`
    ⚙️ MentorOS Settings - Configuration Panel
    =========================================
    
    🎯 Features:
    • Student Profile Management
    • System Preferences
    • Data Export & Management
    • 3D Interactive Interface
    
    Built with ❤️ for intelligent education
    `);
});

// Handle page visibility for performance optimization
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        console.log('🔇 MentorOS Settings paused (tab hidden)');
    } else {
        console.log('🔊 MentorOS Settings resumed (tab visible)');
    }
});