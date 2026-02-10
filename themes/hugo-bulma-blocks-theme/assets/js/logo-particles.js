/**
 * Kartoza Logo Particle Effect
 * Creates GIS-themed particles when hovering over the Kartoza logo
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
        particlesPerBurst: 3,      // Particles per emission
        burstInterval: 400,         // ms between bursts while hovering
        particleLifetime: 2000,     // ms before particle is removed
        maxParticles: 24,           // Max particles per logo
        spreadRadius: 80            // How far particles spread
    };

    // Track active logos and their intervals
    const activeLogos = new Map();

    // Initialize on DOM ready
    document.addEventListener('DOMContentLoaded', init);

    function init() {
        // Find all logo wrappers
        const logoWrappers = document.querySelectorAll('.logo-wrapper');

        logoWrappers.forEach(wrapper => {
            const particlesContainer = wrapper.querySelector('.logo-particles');
            if (!particlesContainer) return;

            // Mouse enter - start emitting particles
            wrapper.addEventListener('mouseenter', () => {
                startParticleEmission(wrapper, particlesContainer);
            });

            // Mouse leave - stop emitting (existing particles will fade out)
            wrapper.addEventListener('mouseleave', () => {
                stopParticleEmission(wrapper);
            });

            // Touch support for mobile
            wrapper.addEventListener('touchstart', (e) => {
                e.preventDefault();
                wrapper.classList.add('active');
                startParticleEmission(wrapper, particlesContainer);
            }, { passive: false });

            wrapper.addEventListener('touchend', () => {
                wrapper.classList.remove('active');
                stopParticleEmission(wrapper);
            });
        });
    }

    function startParticleEmission(wrapper, container) {
        // Don't start if already active
        if (activeLogos.has(wrapper)) return;

        // Check for reduced motion preference
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            return;
        }

        // Emit initial burst
        emitParticleBurst(container);

        // Set up interval for continuous emission
        const intervalId = setInterval(() => {
            emitParticleBurst(container);
        }, CONFIG.burstInterval);

        activeLogos.set(wrapper, {
            intervalId,
            container
        });
    }

    function stopParticleEmission(wrapper) {
        const data = activeLogos.get(wrapper);
        if (data) {
            clearInterval(data.intervalId);
            activeLogos.delete(wrapper);
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
