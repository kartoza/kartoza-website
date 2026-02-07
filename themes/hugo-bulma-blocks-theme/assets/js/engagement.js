/**
 * Kartoza Engagement Nudges
 * Delightful, non-intrusive prompts that appear after idle time
 * Designed to feel like discoveries, not interruptions
 */

(function() {
    'use strict';

    // Configuration
    const CONFIG = {
        idleThreshold: 45000,        // 45 seconds before first nudge
        nudgeInterval: 90000,        // 90 seconds between nudges
        maxNudges: 3,                // Maximum nudges per session
        fadeInDuration: 800,         // Animation duration in ms
        displayDuration: 12000,      // How long nudge stays visible
        storageKey: 'kartoza_nudges'
    };

    // Nudge content - rotating tips and CTAs (with regional variants)
    const NUDGES_BASE = [
        {
            type: 'tip',
            icon: 'fa-compass',
            title: 'Did you know?',
            message: 'We offer customized GIS training for teams of all sizes.',
            cta: 'Explore Courses',
            ctaUrl: '/training-courses/',
            accent: 'primary'
        },
        {
            type: 'discovery',
            icon: 'fa-map-location-dot',
            title: 'Discover',
            message: 'See how we\'ve helped organizations visualize their spatial data.',
            cta: 'View Portfolio',
            ctaUrl: '/portfolio/',
            accent: 'gold'
        },
        {
            type: 'tip',
            icon: 'fa-cloud',
            title: 'Need hosting?',
            message: 'GeoSpatial Hosting provides managed GIS infrastructure.',
            cta: 'Learn More',
            ctaUrl: 'https://geospatialhosting.com',
            accent: 'primary'
        },
        {
            type: 'discovery',
            icon: 'fa-handshake',
            title: 'Let\'s collaborate',
            message: 'From consulting to development, we\'re here to help.',
            cta: 'Get in Touch',
            ctaUrl: '/contact-us/',
            accent: 'gold'
        },
        {
            type: 'tip',
            icon: 'fa-city',
            title: 'MyCivitas',
            message: 'Our asset management solution for local governments.',
            cta: 'Discover MyCivitas',
            ctaUrl: '/solutions/mycivitas/',
            accent: 'primary'
        },
        {
            type: 'discovery',
            icon: 'fa-leaf',
            title: 'BIMS',
            message: 'Biodiversity Information Management for conservation.',
            cta: 'Explore BIMS',
            ctaUrl: '/solutions/bims/',
            accent: 'gold'
        }
    ];

    // Regional-specific nudges
    const NUDGES_REGIONAL = {
        ZA: [
            {
                type: 'regional',
                icon: 'fa-building',
                title: 'Local support',
                message: 'Our Cape Town team provides same-timezone support and ZAR billing.',
                cta: 'Contact SA Office',
                ctaUrl: '/contact-us/',
                accent: 'gold'
            }
        ],
        EU: [
            {
                type: 'regional',
                icon: 'fa-euro-sign',
                title: 'EU Operations',
                message: 'Kartoza LDA offers GDPR-compliant services with Euro billing from Portugal.',
                cta: 'Contact EU Office',
                ctaUrl: '/contact-us/',
                accent: 'gold'
            }
        ]
    };

    // Combined nudges based on region
    function getNudges() {
        let nudges = [...NUDGES_BASE];
        if (window.KartozaRegion) {
            const region = window.KartozaRegion.getRegion();
            if (region && NUDGES_REGIONAL[region.code]) {
                nudges = [...nudges, ...NUDGES_REGIONAL[region.code]];
            }
        }
        return nudges;
    }

    const NUDGES = NUDGES_BASE; // Fallback, will use getNudges() dynamically

    // State
    let idleTimer = null;
    let nudgeTimer = null;
    let nudgesShown = 0;
    let lastActivity = Date.now();
    let currentNudgeIndex = 0;
    let nudgeElement = null;
    let isNudgeVisible = false;

    // Initialize on DOM ready
    document.addEventListener('DOMContentLoaded', init);

    function init() {
        // Create nudge container first (needed for hotkey testing)
        createNudgeElement();

        // Set up debug hotkey (Alt+N) for testing
        setupDebugHotkey();

        // Don't run idle detection on search or contact pages
        if (isExcludedPage()) return;

        // Check session storage for nudge count
        loadNudgeState();

        // If max nudges reached, don't initialize idle detection
        if (nudgesShown >= CONFIG.maxNudges) return;

        // Set up activity listeners
        setupActivityListeners();

        // Start idle detection
        startIdleDetection();
    }

    function setupDebugHotkey() {
        document.addEventListener('keydown', (e) => {
            // Alt+N to trigger nudge for testing
            if (e.altKey && e.key.toLowerCase() === 'n') {
                e.preventDefault();
                // Reset limits temporarily for testing
                const originalCount = nudgesShown;
                nudgesShown = 0;
                showNudge();
                // Restore count after showing (but incremented by showNudge)
                nudgesShown = Math.min(originalCount + 1, CONFIG.maxNudges);
                saveNudgeState();
            }
        });
    }

    function isExcludedPage() {
        const path = window.location.pathname;
        const excluded = ['/search/', '/contact-us/', '/checkout/'];
        return excluded.some(p => path.includes(p));
    }

    function loadNudgeState() {
        try {
            const stored = sessionStorage.getItem(CONFIG.storageKey);
            if (stored) {
                const state = JSON.parse(stored);
                nudgesShown = state.count || 0;
                currentNudgeIndex = state.index || 0;
            }
        } catch (e) {
            // Ignore storage errors
        }
    }

    function saveNudgeState() {
        try {
            sessionStorage.setItem(CONFIG.storageKey, JSON.stringify({
                count: nudgesShown,
                index: currentNudgeIndex
            }));
        } catch (e) {
            // Ignore storage errors
        }
    }

    function createNudgeElement() {
        nudgeElement = document.createElement('div');
        nudgeElement.className = 'engagement-nudge';
        nudgeElement.innerHTML = `
            <div class="nudge-glow"></div>
            <div class="nudge-content">
                <div class="nudge-decoration">
                    <svg class="nudge-rings" viewBox="0 0 60 60">
                        <circle cx="30" cy="30" r="28" class="ring ring-outer"/>
                        <circle cx="30" cy="30" r="20" class="ring ring-middle"/>
                        <circle cx="30" cy="30" r="12" class="ring ring-inner"/>
                    </svg>
                </div>
                <button class="nudge-close" aria-label="Dismiss">
                    <i class="fa-solid fa-xmark"></i>
                </button>
                <div class="nudge-icon">
                    <i class="fa-solid fa-compass"></i>
                </div>
                <div class="nudge-body">
                    <h4 class="nudge-title">Did you know?</h4>
                    <p class="nudge-message">Loading...</p>
                </div>
                <a href="#" class="nudge-cta">
                    <span class="nudge-cta-text">Learn More</span>
                    <span class="nudge-cta-arrow"><i class="fa-solid fa-arrow-right"></i></span>
                </a>
            </div>
            <div class="nudge-progress">
                <div class="nudge-progress-bar"></div>
            </div>
        `;
        document.body.appendChild(nudgeElement);

        // Set up close button
        nudgeElement.querySelector('.nudge-close').addEventListener('click', (e) => {
            e.preventDefault();
            hideNudge();
            // Increase nudge count to reduce frequency after dismissal
            nudgesShown++;
            saveNudgeState();
        });
    }

    function setupActivityListeners() {
        const events = ['mousemove', 'mousedown', 'keydown', 'scroll', 'touchstart'];
        events.forEach(event => {
            document.addEventListener(event, onActivity, { passive: true });
        });
    }

    function onActivity() {
        lastActivity = Date.now();

        // If nudge is visible and user interacts, hide it gently
        if (isNudgeVisible) {
            hideNudge();
        }

        // Reset idle timer
        resetIdleTimer();
    }

    function startIdleDetection() {
        resetIdleTimer();
    }

    function resetIdleTimer() {
        if (idleTimer) clearTimeout(idleTimer);
        if (nudgeTimer) clearTimeout(nudgeTimer);

        if (nudgesShown >= CONFIG.maxNudges) return;

        // Set timer for idle threshold
        idleTimer = setTimeout(() => {
            showNudge();
        }, CONFIG.idleThreshold);
    }

    function showNudge() {
        if (isNudgeVisible || nudgesShown >= CONFIG.maxNudges) return;

        // Get nudges (including regional ones if available)
        const nudges = getNudges();

        // Get next nudge content
        const nudge = nudges[currentNudgeIndex % nudges.length];
        currentNudgeIndex++;
        nudgesShown++;
        saveNudgeState();

        // Update nudge content
        updateNudgeContent(nudge);

        // Show nudge with animation
        isNudgeVisible = true;
        nudgeElement.classList.add('is-visible');
        nudgeElement.classList.add(`accent-${nudge.accent}`);

        // Start progress bar animation
        const progressBar = nudgeElement.querySelector('.nudge-progress-bar');
        progressBar.style.transition = `width ${CONFIG.displayDuration}ms linear`;
        requestAnimationFrame(() => {
            progressBar.style.width = '100%';
        });

        // Auto-hide after display duration
        nudgeTimer = setTimeout(() => {
            hideNudge();

            // Schedule next nudge if allowed
            if (nudgesShown < CONFIG.maxNudges) {
                setTimeout(() => {
                    if (Date.now() - lastActivity > CONFIG.idleThreshold) {
                        showNudge();
                    }
                }, CONFIG.nudgeInterval);
            }
        }, CONFIG.displayDuration);
    }

    function updateNudgeContent(nudge) {
        const icon = nudgeElement.querySelector('.nudge-icon i');
        const title = nudgeElement.querySelector('.nudge-title');
        const message = nudgeElement.querySelector('.nudge-message');
        const cta = nudgeElement.querySelector('.nudge-cta');
        const ctaText = nudgeElement.querySelector('.nudge-cta-text');

        icon.className = `fa-solid ${nudge.icon}`;
        title.textContent = nudge.title;
        message.textContent = nudge.message;
        cta.href = nudge.ctaUrl;
        ctaText.textContent = nudge.cta;

        // Reset accent class
        nudgeElement.classList.remove('accent-primary', 'accent-gold');
    }

    function hideNudge() {
        if (!isNudgeVisible) return;

        isNudgeVisible = false;
        nudgeElement.classList.remove('is-visible');
        nudgeElement.classList.remove('accent-primary', 'accent-gold');

        // Reset progress bar
        const progressBar = nudgeElement.querySelector('.nudge-progress-bar');
        progressBar.style.transition = 'none';
        progressBar.style.width = '0%';

        if (nudgeTimer) {
            clearTimeout(nudgeTimer);
            nudgeTimer = null;
        }
    }

})();
