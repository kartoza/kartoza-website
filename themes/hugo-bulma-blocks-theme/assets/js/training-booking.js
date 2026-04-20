/**
 * Training Booking Flow JavaScript
 * Handles multi-step booking widget for training courses
 */

(function() {
    'use strict';

    // State management
    const bookingState = {
        currentStep: 1,
        selectedSession: null,
        attendeeCount: 1,
        currency: 'ZAR',
        sessionData: null,
        venueType: null,
        pricePerPerson: 0,
        subtotal: 0,
        discount: 0,
        discountLabel: '',
        total: 0
    };

    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', initBookingWidget);

    function initBookingWidget() {
        const widget = document.querySelector('.booking-widget');
        if (!widget) return; // No booking widget on this page

        setupEventListeners();
        updateProgressIndicator();
    }

    function setupEventListeners() {
        // Session selection buttons
        document.querySelectorAll('.select-session-btn').forEach(btn => {
            btn.addEventListener('click', handleSessionSelection);
        });

        // Attendee controls
        const decreaseBtn = document.querySelector('.attendee-btn.decrease');
        const increaseBtn = document.querySelector('.attendee-btn.increase');
        if (decreaseBtn) decreaseBtn.addEventListener('click', () => adjustAttendees(-1));
        if (increaseBtn) increaseBtn.addEventListener('click', () => adjustAttendees(1));

        // Currency selection
        document.querySelectorAll('input[name="currency"]').forEach(radio => {
            radio.addEventListener('change', handleCurrencyChange);
        });

        // Navigation buttons
        document.querySelectorAll('.back-btn').forEach(btn => {
            btn.addEventListener('click', () => navigateToStep(bookingState.currentStep - 1));
        });

        document.querySelectorAll('.next-btn').forEach(btn => {
            btn.addEventListener('click', () => navigateToStep(bookingState.currentStep + 1));
        });

        // Proceed to checkout button
        const checkoutBtn = document.querySelector('.proceed-checkout-btn');
        if (checkoutBtn) checkoutBtn.addEventListener('click', handleCheckout);

        // Smooth scroll for booking buttons
        document.querySelectorAll('.booking-scroll-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const bookingSection = document.querySelector('#booking-section');
                if (bookingSection) {
                    bookingSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
    }

    function handleSessionSelection(e) {
        const sessionCard = e.target.closest('.session-card');
        if (!sessionCard) return;

        // Store session data
        bookingState.sessionData = {
            id: sessionCard.dataset.sessionId,
            startDate: sessionCard.dataset.startDate,
            endDate: sessionCard.dataset.endDate,
            instructor: sessionCard.dataset.instructor,
            venueName: sessionCard.dataset.venueName,
            venueType: sessionCard.dataset.venueType,
            seatsAvailable: parseInt(sessionCard.dataset.seatsAvailable)
        };

        bookingState.venueType = bookingState.sessionData.venueType;

        // Visual feedback
        document.querySelectorAll('.session-card').forEach(card => {
            card.classList.remove('selected');
        });
        sessionCard.classList.add('selected');

        // Navigate to next step
        setTimeout(() => {
            navigateToStep(2);
        }, 300);
    }

    function adjustAttendees(change) {
        const input = document.querySelector('.attendee-input');
        if (!input) return;

        const newValue = Math.max(1, Math.min(50, bookingState.attendeeCount + change));
        bookingState.attendeeCount = newValue;
        input.value = newValue;

        // Visual feedback for discount eligibility
        updateDiscountEligibility();
    }

    function handleCurrencyChange(e) {
        bookingState.currency = e.target.value;
    }

    function navigateToStep(step) {
        if (step < 1 || step > 3) return;

        // Validation
        if (step === 2 && !bookingState.sessionData) {
            alert('Please select a session first');
            return;
        }

        // Hide current step
        document.querySelectorAll('.booking-step').forEach(stepEl => {
            stepEl.classList.remove('active');
        });

        // Show target step
        const targetStep = document.querySelector(`.booking-step[data-step="${step}"]`);
        if (targetStep) {
            targetStep.classList.add('active');
            bookingState.currentStep = step;
            updateProgressIndicator();

            // If entering step 3, calculate and display summary
            if (step === 3) {
                calculatePricing();
                updateSummary();
            }

            // Scroll to booking widget
            setTimeout(() => {
                const widget = document.querySelector('.booking-widget');
                if (widget) {
                    widget.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }, 100);
        }
    }

    function updateProgressIndicator() {
        document.querySelectorAll('.progress-step').forEach(step => {
            const stepNum = parseInt(step.dataset.step);
            if (stepNum < bookingState.currentStep) {
                step.classList.add('completed');
                step.classList.remove('active');
            } else if (stepNum === bookingState.currentStep) {
                step.classList.add('active');
                step.classList.remove('completed');
            } else {
                step.classList.remove('active', 'completed');
            }
        });
    }

    function updateDiscountEligibility() {
        // This is just visual feedback - actual calculation happens in step 3
        const discountItems = document.querySelectorAll('.discount-item');
        const attendeeCount = bookingState.attendeeCount;

        discountItems.forEach(item => {
            // You could add visual highlighting here
        });
    }

    function calculatePricing() {
        if (!window.trainingScheduleData || !window.currentCourse) {
            console.error('Training schedule data not available');
            return;
        }

        const schedule = window.trainingScheduleData;
        const courseSlug = window.currentCourse;
        const pricing = schedule.pricing[courseSlug];

        if (!pricing) {
            console.error('Pricing not found for course:', courseSlug);
            return;
        }

        // Get base price
        const currencyPricing = pricing[bookingState.currency];
        if (!currencyPricing) {
            console.error('Currency pricing not found:', bookingState.currency);
            return;
        }

        const basePricePerPerson = currencyPricing[bookingState.venueType];
        if (!basePricePerPerson) {
            console.error('Venue type pricing not found:', bookingState.venueType);
            return;
        }

        bookingState.pricePerPerson = basePricePerPerson;
        bookingState.subtotal = basePricePerPerson * bookingState.attendeeCount;

        // Calculate group discount
        let groupDiscountPercent = 0;
        let groupDiscountLabel = '';

        schedule.group_discounts.forEach(discount => {
            const min = discount.min_attendees;
            const max = discount.max_attendees;

            if (bookingState.attendeeCount >= min) {
                if (!max || bookingState.attendeeCount <= max) {
                    groupDiscountPercent = discount.discount_percent;
                    groupDiscountLabel = discount.label;
                }
            }
        });

        // Calculate early bird discount (simplified - in real app, check actual date difference)
        const earlyBirdPercent = schedule.early_bird.discount_percent;
        const earlyBirdDays = schedule.early_bird.days_before;

        // For now, assume early bird applies if more than 30 days away
        const sessionDate = new Date(bookingState.sessionData.startDate);
        const today = new Date();
        const daysUntilSession = Math.floor((sessionDate - today) / (1000 * 60 * 60 * 24));

        let earlyBirdApplies = false;
        if (daysUntilSession >= earlyBirdDays) {
            earlyBirdApplies = true;
        }

        // Calculate total discount (group + early bird)
        let totalDiscountPercent = groupDiscountPercent;
        let discountLabels = [];

        if (groupDiscountLabel) {
            discountLabels.push(`${groupDiscountLabel} ${groupDiscountPercent}%`);
        }

        if (earlyBirdApplies) {
            totalDiscountPercent += earlyBirdPercent;
            discountLabels.push(`Early Bird ${earlyBirdPercent}%`);
        }

        const discountAmount = bookingState.subtotal * (totalDiscountPercent / 100);
        bookingState.discount = discountAmount;
        bookingState.discountLabel = discountLabels.join(' + ');
        bookingState.total = bookingState.subtotal - discountAmount;
    }

    function updateSummary() {
        const currencySymbol = window.trainingScheduleData.currencies[bookingState.currency].symbol;

        // Format dates
        const formatDate = (dateStr) => {
            const date = new Date(dateStr);
            return date.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
        };

        // Update session details
        document.getElementById('summary-date').textContent =
            `${formatDate(bookingState.sessionData.startDate)} - ${formatDate(bookingState.sessionData.endDate)}`;
        document.getElementById('summary-venue').textContent = bookingState.sessionData.venueName;
        document.getElementById('summary-instructor').textContent = bookingState.sessionData.instructor;

        // Update attendees
        document.getElementById('summary-attendees').textContent = bookingState.attendeeCount;

        // Update pricing
        document.getElementById('summary-price-per').textContent =
            `${currencySymbol}${bookingState.pricePerPerson.toLocaleString()}`;
        document.getElementById('summary-subtotal').textContent =
            `${currencySymbol}${bookingState.subtotal.toLocaleString()}`;
        document.getElementById('summary-total').textContent =
            `${currencySymbol}${bookingState.total.toLocaleString()}`;

        // Show/hide discount row
        if (bookingState.discount > 0) {
            document.getElementById('summary-discount-row').style.display = '';
            document.getElementById('summary-discount-label').textContent = bookingState.discountLabel;
            document.getElementById('summary-discount').textContent =
                `-${currencySymbol}${bookingState.discount.toLocaleString()}`;
        } else {
            document.getElementById('summary-discount-row').style.display = 'none';
        }
    }

    function handleCheckout() {
        // Prepare booking data for API call
        const bookingData = {
            course: window.currentCourse,
            sessionId: bookingState.sessionData.id,
            attendeeCount: bookingState.attendeeCount,
            currency: bookingState.currency,
            pricePerPerson: bookingState.pricePerPerson,
            subtotal: bookingState.subtotal,
            discount: bookingState.discount,
            total: bookingState.total,
            timestamp: new Date().toISOString()
        };

        // Store booking data in session storage for the checkout page
        sessionStorage.setItem('pendingBooking', JSON.stringify(bookingData));

        // In a real implementation, this would redirect to your e-commerce checkout
        // For now, we'll create a booking request via the contact form or API

        // Option 1: Redirect to e-commerce API (when available)
        // window.location.href = '/api/v1/training/checkout';

        // Option 2: For now, redirect to contact form with pre-filled data
        const courseName = document.querySelector('h1')?.textContent || window.currentCourse;
        const dateDisplay = `${formatDate(bookingState.sessionData.startDate)} - ${formatDate(bookingState.sessionData.endDate)}`;
        const location = bookingState.sessionData.venueName || 'Online';
        const contactUrl = `/contact-us/?booking=true&course=${encodeURIComponent(courseName)}&date=${encodeURIComponent(dateDisplay)}&location=${encodeURIComponent(location)}&session=${bookingData.sessionId}&attendees=${bookingData.attendeeCount}&currency=${bookingData.currency}&total=${bookingData.total}`;

        // Show confirmation dialog
        if (confirm(`You're about to book ${bookingData.attendeeCount} seat(s) for ${bookingState.sessionData.venueName}. Total: ${window.trainingScheduleData.currencies[bookingData.currency].symbol}${bookingData.total.toLocaleString()}\n\nProceed to checkout?`)) {
            // TODO: Replace with actual e-commerce API call
            window.location.href = contactUrl;
        }
    }

})();
