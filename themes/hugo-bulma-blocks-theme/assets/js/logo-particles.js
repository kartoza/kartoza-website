/**
 * Kartoza Logo Particle Effect
 * Creates GIS-themed particles when hovering over the Kartoza logo
 * Includes smooth rotation with gradual deceleration on mouse leave
 */

(function() {
    'use strict';

    // Particle types - GIS elements
    const PARTICLE_TYPES = [
        'marker',
        'compass',
        'north-arrow',
        'globe',
        'map',
        'layer',
        'satellite',
        'database'
    ];

    // Configuration
    const CONFIG = {
        particlesPerBurst: 3,       // Particles per emission
        burstInterval: 400,         // ms between bursts while hovering
        particleLifetime: 2000,     // ms before particle is removed
        maxParticles: 24,           // Max particles per logo
        spreadRadius: 80,           // How far particles spread
        rotationSpeed: 45,          // Degrees per second when spinning
        decelerationTime: 2000,     // ms to slow down after mouse leave
        accelerationTime: 800       // ms to reach full speed on hover
    };

    // Track active logos and their state
    const logoStates = new Map();

    // Initialize on DOM ready
    document.addEventListener('DOMContentLoaded', init);

    function init() {
        // Check for reduced motion preference
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            return;
        }

        // Find all logo wrappers
        const logoWrappers = document.querySelectorAll('.logo-wrapper');

        logoWrappers.forEach(wrapper => {
            const particlesContainer = wrapper.querySelector('.logo-particles');
            const logo = wrapper.querySelector('.kartoza-logo-animated');
            if (!particlesContainer || !logo) return;

            // Initialize state for this logo
            const state = {
                rotation: 0,
                velocity: 0,
                targetVelocity: 0,
                isHovered: false,
                animationFrame: null,
                particleInterval: null,
                container: particlesContainer,
                logo: logo,
                wrapper: wrapper,
                lastTime: null
            };
            logoStates.set(wrapper, state);

            // Mouse enter - start spinning and emitting particles
            wrapper.addEventListener('mouseenter', () => {
                state.isHovered = true;
                state.targetVelocity = CONFIG.rotationSpeed;
                wrapper.classList.add('is-spinning');
                wrapper.classList.remove('is-decelerating');
                startAnimation(state);
                startParticleEmission(state);
            });

            // Mouse leave - gradually slow down
            wrapper.addEventListener('mouseleave', () => {
                state.isHovered = false;
                state.targetVelocity = 0;
                wrapper.classList.add('is-decelerating');
                wrapper.classList.remove('is-spinning');
                stopParticleEmission(state);
                // Animation continues until fully stopped
            });

            // Touch support for mobile
            wrapper.addEventListener('touchstart', (e) => {
                e.preventDefault();
                wrapper.classList.add('active');
                state.isHovered = true;
                state.targetVelocity = CONFIG.rotationSpeed;
                wrapper.classList.add('is-spinning');
                wrapper.classList.remove('is-decelerating');
                startAnimation(state);
                startParticleEmission(state);
            }, { passive: false });

            wrapper.addEventListener('touchend', () => {
                wrapper.classList.remove('active');
                state.isHovered = false;
                state.targetVelocity = 0;
                wrapper.classList.add('is-decelerating');
                wrapper.classList.remove('is-spinning');
                stopParticleEmission(state);
            });
        });
    }

    function startAnimation(state) {
        // Don't start if already animating
        if (state.animationFrame) return;

        state.lastTime = performance.now();
        animate(state);
    }

    function animate(state) {
        const currentTime = performance.now();
        const deltaTime = (currentTime - state.lastTime) / 1000; // Convert to seconds
        state.lastTime = currentTime;

        // Smooth velocity changes using easing
        const accelerationRate = CONFIG.rotationSpeed / (CONFIG.accelerationTime / 1000);
        const decelerationRate = CONFIG.rotationSpeed / (CONFIG.decelerationTime / 1000);

        if (state.velocity < state.targetVelocity) {
            // Accelerating
            state.velocity = Math.min(
                state.velocity + accelerationRate * deltaTime,
                state.targetVelocity
            );
        } else if (state.velocity > state.targetVelocity) {
            // Decelerating - use easing for smoother stop
            const deceleration = decelerationRate * deltaTime * (state.velocity / CONFIG.rotationSpeed);
            state.velocity = Math.max(
                state.velocity - deceleration,
                state.targetVelocity
            );
        }

        // Update rotation
        state.rotation += state.velocity * deltaTime;

        // Keep rotation in reasonable bounds
        if (state.rotation >= 360) {
            state.rotation -= 360;
        }

        // Apply rotation via CSS custom property
        state.wrapper.style.setProperty('--logo-rotation', `${state.rotation}deg`);

        // Continue animation if still moving or hovered
        if (state.velocity > 0.1 || state.isHovered) {
            state.animationFrame = requestAnimationFrame(() => animate(state));
        } else {
            // Fully stopped
            state.velocity = 0;
            state.animationFrame = null;
            state.wrapper.classList.remove('is-spinning', 'is-decelerating');
        }
    }

    function startParticleEmission(state) {
        // Don't start if already emitting
        if (state.particleInterval) return;

        // Emit initial burst
        emitParticleBurst(state.container);

        // Set up interval for continuous emission
        state.particleInterval = setInterval(() => {
            emitParticleBurst(state.container);
        }, CONFIG.burstInterval);
    }

    function stopParticleEmission(state) {
        if (state.particleInterval) {
            clearInterval(state.particleInterval);
            state.particleInterval = null;
        }
    }

    function emitParticleBurst(container) {
        // Limit total particles
        const currentParticles = container.querySelectorAll('.logo-particle');
        if (currentParticles.length >= CONFIG.maxParticles) {
            return;
        }

        // Create several particles per burst
        for (let i = 0; i < CONFIG.particlesPerBurst; i++) {
            createParticle(container);
        }
    }

    function createParticle(container) {
        const particle = document.createElement('span');
        particle.className = 'logo-particle';

        // Random particle type
        const type = PARTICLE_TYPES[Math.floor(Math.random() * PARTICLE_TYPES.length)];
        particle.classList.add(type);

        // Random trajectory
        const angle = Math.random() * Math.PI * 2; // Random angle in radians
        const distance = CONFIG.spreadRadius * (0.5 + Math.random() * 0.5);

        // Calculate end positions
        const txMid = Math.cos(angle) * (distance * 0.4);
        const tyMid = Math.sin(angle) * (distance * 0.4) - 10; // Slight upward bias
        const txEnd = Math.cos(angle) * distance;
        const tyEnd = Math.sin(angle) * distance - 20; // Float upward at end
        const rotMid = (Math.random() - 0.5) * 90;
        const rotEnd = (Math.random() - 0.5) * 180;

        // Set CSS custom properties for animation
        particle.style.setProperty('--tx-mid', `${txMid}px`);
        particle.style.setProperty('--ty-mid', `${tyMid}px`);
        particle.style.setProperty('--tx-end', `${txEnd}px`);
        particle.style.setProperty('--ty-end', `${tyEnd}px`);
        particle.style.setProperty('--rot-mid', `${rotMid}deg`);
        particle.style.setProperty('--rot-end', `${rotEnd}deg`);

        // Add some randomness to size
        const scale = 0.8 + Math.random() * 0.4;
        particle.style.fontSize = `${12 * scale}px`;

        // Add slight delay for staggered effect
        particle.style.animationDelay = `${Math.random() * 100}ms`;

        // Add to container
        container.appendChild(particle);

        // Remove after animation completes
        setTimeout(() => {
            if (particle.parentNode) {
                particle.parentNode.removeChild(particle);
            }
        }, CONFIG.particleLifetime);
    }

})();
