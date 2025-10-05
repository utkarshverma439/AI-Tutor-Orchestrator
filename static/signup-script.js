// MentorOS Signup Script - Professional Account Creation
console.log('🚀 MentorOS Signup Loading...');

class MentorOSSignup {
    constructor() {
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.particles = [];
        this.mouseX = 0;
        this.mouseY = 0;
        
        this.init();
    }
    
    init() {
        this.initThreeJS();
        this.createParticleNetwork();
        this.bindEvents();
        this.animate();
        
        // Initialize Lucide icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
        
        console.log('✅ MentorOS Signup initialized');
    }
    
    initThreeJS() {
        const canvas = document.getElementById('bg-canvas');
        if (!canvas) {
            console.log('⚠️ Canvas not found, skipping 3D background');
            return;
        }
        
        if (typeof THREE === 'undefined') {
            console.log('⚠️ Three.js not loaded, skipping 3D background');
            return;
        }
        
        try {
            // Scene setup
            this.scene = new THREE.Scene();
            this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            this.renderer = new THREE.WebGLRenderer({ canvas, alpha: true });
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
            
            console.log('✅ 3D Background initialized successfully');
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
        const container = document.getElementById('particle-network');
        if (!container) return;
        
        // Create floating particles
        for (let i = 0; i < 40; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.top = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 6 + 's';
            particle.style.animationDuration = (Math.random() * 4 + 4) + 's';
            container.appendChild(particle);
        }
        
        // Create connecting lines
        for (let i = 0; i < 15; i++) {
            const line = document.createElement('div');
            line.className = 'particle-line';
            line.style.left = Math.random() * 100 + '%';
            line.style.top = Math.random() * 100 + '%';
            line.style.width = (Math.random() * 200 + 100) + 'px';
            line.style.transform = `rotate(${Math.random() * 360}deg)`;
            line.style.animationDelay = Math.random() * 3 + 's';
            container.appendChild(line);
        }
    }
    
    bindEvents() {
        // Mouse movement for parallax effect
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
        
        // Form submission
        const signupForm = document.getElementById('signupForm');
        if (signupForm) {
            signupForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleSignup();
            });
        }
        
        // Social signup buttons
        const socialBtns = document.querySelectorAll('.social-btn');
        socialBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleSocialSignup(btn.classList.contains('google-btn') ? 'google' : 'github');
            });
        });
        
        // Input focus effects
        const inputs = document.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.addEventListener('focus', () => {
                this.addInputGlow(input);
            });
            
            input.addEventListener('blur', () => {
                this.removeInputGlow(input);
            });
        });
        
        // Password confirmation validation
        const password = document.getElementById('password');
        const confirmPassword = document.getElementById('confirmPassword');
        
        if (confirmPassword) {
            confirmPassword.addEventListener('input', () => {
                if (password.value !== confirmPassword.value) {
                    confirmPassword.setCustomValidity('Passwords do not match');
                } else {
                    confirmPassword.setCustomValidity('');
                }
            });
        }
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        
        if (this.scene && this.camera && this.renderer) {
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
            this.camera.position.x += (this.mouseX * 0.5 - this.camera.position.x) * 0.05;
            this.camera.position.y += (this.mouseY * 0.5 - this.camera.position.y) * 0.05;
            this.camera.lookAt(this.scene.position);
            
            this.renderer.render(this.scene, this.camera);
        }
    }
    
    addInputGlow(input) {
        const wrapper = input.closest('.input-wrapper') || input.closest('.select-wrapper');
        if (wrapper) {
            gsap.to(wrapper.querySelector('.input-glow'), {
                opacity: 1,
                scale: 1,
                duration: 0.3,
                ease: "power2.out"
            });
        }
    }
    
    removeInputGlow(input) {
        const wrapper = input.closest('.input-wrapper') || input.closest('.select-wrapper');
        if (wrapper && !input.matches(':focus')) {
            gsap.to(wrapper.querySelector('.input-glow'), {
                opacity: 0,
                scale: 0.95,
                duration: 0.3,
                ease: "power2.out"
            });
        }
    }
    
    async handleSignup() {
        const fullName = document.getElementById('fullName').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        const gradeLevel = document.getElementById('gradeLevel').value;
        const agreeTerms = document.getElementById('agreeTerms').checked;
        
        // Validation
        if (!fullName || !email || !password || !confirmPassword || !gradeLevel) {
            this.showError('Please fill in all fields');
            return;
        }
        
        if (password !== confirmPassword) {
            this.showError('Passwords do not match');
            return;
        }
        
        if (password.length < 6) {
            this.showError('Password must be at least 6 characters long');
            return;
        }
        
        if (!agreeTerms) {
            this.showError('Please agree to the Terms of Service and Privacy Policy');
            return;
        }
        
        this.showLoading(true);
        
        try {
            // Send signup request to backend
            const response = await fetch('/auth/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: fullName,
                    email: email,
                    password: password,
                    grade_level: gradeLevel
                })
            });
            
            if (response.ok) {
                const data = await response.json();
                
                if (data.success) {
                    this.showSuccess('Account created successfully! Redirecting to MentorOS...');
                    
                    // Store user data and session
                    localStorage.setItem('mentorOS_user', JSON.stringify({
                        id: data.user.id,
                        email: data.user.email,
                        name: data.user.name,
                        grade_level: data.user.grade_level,
                        learning_style: data.user.learning_style,
                        emotional_state: data.user.emotional_state,
                        teaching_style: data.user.teaching_style,
                        loginTime: new Date().toISOString(),
                        sessionToken: data.session_token
                    }));
                    
                    // Redirect to main dashboard after animation
                    setTimeout(() => {
                        window.location.href = '/';
                    }, 2000);
                } else {
                    throw new Error(data.message || 'Signup failed');
                }
            } else {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Signup failed');
            }
        } catch (error) {
            console.error('❌ Signup error:', error);
            if (error.message.includes('already exists')) {
                this.showError('An account with this email already exists. Please sign in instead.');
            } else {
                this.showError('Signup failed. Please try again.');
            }
        } finally {
            this.showLoading(false);
        }
    }
    
    async handleSocialSignup(provider) {
        this.showLoading(true);
        
        try {
            // Send social signup request to backend
            const response = await fetch('/auth/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: `${provider.charAt(0).toUpperCase() + provider.slice(1)} User`,
                    email: `user@${provider}.com`,
                    password: 'social_signup',
                    provider: provider,
                    grade_level: '10'
                })
            });
            
            if (response.ok) {
                const data = await response.json();
                
                if (data.success) {
                    this.showSuccess(`${provider.charAt(0).toUpperCase() + provider.slice(1)} signup successful!`);
                    
                    // Store user data and session
                    localStorage.setItem('mentorOS_user', JSON.stringify({
                        id: data.user.id,
                        email: data.user.email,
                        name: data.user.name,
                        grade_level: data.user.grade_level,
                        learning_style: data.user.learning_style,
                        emotional_state: data.user.emotional_state,
                        teaching_style: data.user.teaching_style,
                        provider: provider,
                        loginTime: new Date().toISOString(),
                        sessionToken: data.session_token
                    }));
                    
                    setTimeout(() => {
                        window.location.href = '/';
                    }, 2000);
                } else {
                    throw new Error(data.message || 'Social signup failed');
                }
            } else {
                throw new Error('Social signup failed');
            }
        } catch (error) {
            console.error('❌ Social signup error:', error);
            this.showError(`${provider} signup failed. Please try again.`);
        } finally {
            this.showLoading(false);
        }
    }
    
    showLoading(show) {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            if (show) {
                overlay.classList.add('active');
            } else {
                overlay.classList.remove('active');
            }
        }
    }
    
    showError(message) {
        this.showToast(message, 'error');
    }
    
    showSuccess(message) {
        this.showToast(message, 'success');
    }
    
    showToast(message, type = 'info') {
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <i data-lucide="${type === 'error' ? 'alert-circle' : type === 'success' ? 'check-circle' : 'info'}"></i>
                <span>${message}</span>
            </div>
        `;
        
        // Style the toast
        Object.assign(toast.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            background: type === 'error' ? 'rgba(255, 71, 87, 0.9)' : 
                       type === 'success' ? 'rgba(0, 255, 136, 0.9)' : 
                       'rgba(0, 212, 255, 0.9)',
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
        
        // Initialize icon
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

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new MentorOSSignup();
});