/**
 * Kartoza Regional Presence System
 * Detects user region and adapts content accordingly
 */

(function() {
    'use strict';

    // Regional configuration
    const REGIONS = {
        ZA: {
            code: 'ZA',
            name: 'South Africa',
            entity: 'Kartoza (Pty) Ltd.',
            currency: 'ZAR',
            currencySymbol: 'R',
            locale: 'en-ZA',
            timezone: 'Africa/Johannesburg',
            phone: '+27 21 813 8912',
            email: 'info@kartoza.com',
            address: 'Cape Town, South Africa',
            flag: '🇿🇦',
            vatLabel: 'VAT',
            priceMultiplier: 1, // Base currency
            office: {
                city: 'Cape Town',
                country: 'South Africa',
                description: 'Our headquarters and primary development hub'
            }
        },
        EU: {
            code: 'EU',
            name: 'Europe',
            entity: 'Kartoza LDA',
            currency: 'EUR',
            currencySymbol: '€',
            locale: 'en-EU',
            timezone: 'Europe/Lisbon',
            phone: '+351 XXX XXX XXX',
            email: 'europe@kartoza.com',
            address: 'Lisbon, Portugal',
            flag: '🇵🇹',
            vatLabel: 'IVA',
            priceMultiplier: 0.05, // Approximate ZAR to EUR
            office: {
                city: 'Lisbon',
                country: 'Portugal',
                description: 'European operations and EU client services'
            }
        },
        INTL: {
            code: 'INTL',
            name: 'International',
            entity: 'Kartoza',
            currency: 'USD',
            currencySymbol: '$',
            locale: 'en-US',
            timezone: 'UTC',
            phone: '+27 21 813 8912',
            email: 'info@kartoza.com',
            address: 'Global',
            flag: '🌍',
            vatLabel: 'Tax',
            priceMultiplier: 0.055, // Approximate ZAR to USD
            office: null
        }
    };

    // EU country codes
    const EU_COUNTRIES = [
        'AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR',
        'DE', 'GR', 'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL',
        'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE', 'GB', 'CH', 'NO',
        'IS', 'LI'
    ];

    // African country codes (prioritize SA office)
    const AFRICAN_COUNTRIES = [
        'ZA', 'BW', 'NA', 'ZW', 'MZ', 'ZM', 'MW', 'TZ', 'KE', 'UG',
        'RW', 'BI', 'CD', 'AO', 'SZ', 'LS', 'MG', 'MU', 'SC', 'RE',
        'NG', 'GH', 'SN', 'CI', 'CM', 'ET', 'EG', 'MA', 'DZ', 'TN'
    ];

    const CONFIG = {
        storageKey: 'kartoza_region',
        cookieExpiry: 30, // days
        apiTimeout: 3000
    };

    let currentRegion = null;
    let regionListeners = [];

    // Initialize on DOM ready
    document.addEventListener('DOMContentLoaded', init);

    async function init() {
        // Check for stored preference first
        const stored = loadStoredRegion();
        if (stored && REGIONS[stored]) {
            setRegion(stored);
        } else {
            // Detect region
            const detected = await detectRegion();
            setRegion(detected);
        }

        // Set up region selector if present
        setupRegionSelector();

        // Apply regional content
        applyRegionalContent();
    }

    function loadStoredRegion() {
        try {
            return localStorage.getItem(CONFIG.storageKey);
        } catch (e) {
            return null;
        }
    }

    function saveRegion(regionCode) {
        try {
            localStorage.setItem(CONFIG.storageKey, regionCode);
        } catch (e) {
            // Ignore storage errors
        }
    }

    async function detectRegion() {
        // Try timezone-based detection first (no API needed)
        const tzRegion = detectFromTimezone();
        if (tzRegion) return tzRegion;

        // Try IP-based geolocation as fallback
        try {
            const response = await Promise.race([
                fetch('https://ipapi.co/json/'),
                new Promise((_, reject) =>
                    setTimeout(() => reject(new Error('Timeout')), CONFIG.apiTimeout)
                )
            ]);

            if (response.ok) {
                const data = await response.json();
                return mapCountryToRegion(data.country_code);
            }
        } catch (e) {
            console.log('Region detection fallback to default');
        }

        // Default to international
        return 'INTL';
    }

    function detectFromTimezone() {
        try {
            const tz = Intl.DateTimeFormat().resolvedOptions().timeZone;

            if (tz.startsWith('Africa/')) {
                return 'ZA';
            }
            if (tz.startsWith('Europe/')) {
                return 'EU';
            }
        } catch (e) {
            // Ignore timezone detection errors
        }
        return null;
    }

    function mapCountryToRegion(countryCode) {
        if (!countryCode) return 'INTL';

        countryCode = countryCode.toUpperCase();

        if (countryCode === 'ZA' || AFRICAN_COUNTRIES.includes(countryCode)) {
            return 'ZA';
        }
        if (EU_COUNTRIES.includes(countryCode)) {
            return 'EU';
        }
        return 'INTL';
    }

    function setRegion(regionCode) {
        if (!REGIONS[regionCode]) {
            regionCode = 'INTL';
        }

        currentRegion = REGIONS[regionCode];
        saveRegion(regionCode);

        // Add region class to body
        document.body.classList.remove('region-ZA', 'region-EU', 'region-INTL');
        document.body.classList.add(`region-${regionCode}`);

        // Set data attribute for CSS selectors
        document.body.dataset.region = regionCode;

        // Notify listeners
        regionListeners.forEach(fn => fn(currentRegion));

        // Dispatch custom event
        window.dispatchEvent(new CustomEvent('regionChanged', {
            detail: currentRegion
        }));
    }

    function setupRegionSelector() {
        const selectors = document.querySelectorAll('.region-selector');
        selectors.forEach(selector => {
            selector.addEventListener('change', (e) => {
                setRegion(e.target.value);
                applyRegionalContent();
            });

            // Set current value
            if (currentRegion) {
                selector.value = currentRegion.code;
            }
        });

        // Region toggle buttons
        const toggles = document.querySelectorAll('[data-region-switch]');
        toggles.forEach(toggle => {
            toggle.addEventListener('click', (e) => {
                e.preventDefault();
                const region = toggle.dataset.regionSwitch;
                setRegion(region);
                applyRegionalContent();
            });
        });
    }

    function applyRegionalContent() {
        if (!currentRegion) return;

        // Update all regional text elements
        document.querySelectorAll('[data-regional]').forEach(el => {
            const field = el.dataset.regional;
            if (currentRegion[field]) {
                el.textContent = currentRegion[field];
            }
        });

        // Update prices
        document.querySelectorAll('[data-price-zar]').forEach(el => {
            const priceZAR = parseFloat(el.dataset.priceZar);
            if (!isNaN(priceZAR)) {
                const converted = convertPrice(priceZAR);
                el.textContent = formatPrice(converted);
            }
        });

        // Update phone links
        document.querySelectorAll('[data-regional-phone]').forEach(el => {
            el.href = `tel:${currentRegion.phone.replace(/\s/g, '')}`;
            el.textContent = currentRegion.phone;
        });

        // Update email links
        document.querySelectorAll('[data-regional-email]').forEach(el => {
            el.href = `mailto:${currentRegion.email}`;
            el.textContent = currentRegion.email;
        });

        // Show/hide region-specific content
        document.querySelectorAll('[data-show-region]').forEach(el => {
            const showFor = el.dataset.showRegion.split(',');
            el.style.display = showFor.includes(currentRegion.code) ? '' : 'none';
        });

        document.querySelectorAll('[data-hide-region]').forEach(el => {
            const hideFor = el.dataset.hideRegion.split(',');
            el.style.display = hideFor.includes(currentRegion.code) ? 'none' : '';
        });

        // Update active state on region cards
        document.querySelectorAll('.region-card').forEach(card => {
            card.classList.remove('is-active');
            if (card.dataset.region === currentRegion.code) {
                card.classList.add('is-active');
            }
        });
    }

    function convertPrice(priceZAR) {
        return priceZAR * currentRegion.priceMultiplier;
    }

    function formatPrice(amount) {
        const symbol = currentRegion.currencySymbol;
        const formatted = amount.toLocaleString(currentRegion.locale, {
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        });
        return `${symbol}${formatted}`;
    }

    // Public API
    window.KartozaRegion = {
        getRegion: () => currentRegion,
        setRegion: setRegion,
        getRegions: () => REGIONS,
        convertPrice: convertPrice,
        formatPrice: (priceZAR) => formatPrice(convertPrice(priceZAR)),
        onRegionChange: (callback) => {
            regionListeners.push(callback);
            if (currentRegion) callback(currentRegion);
        }
    };

})();
