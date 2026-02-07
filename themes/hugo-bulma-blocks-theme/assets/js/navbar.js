/**
 * Kartoza Navbar and Search Overlay JavaScript
 * Beautiful, accessible search experience with keyboard support
 */

document.addEventListener("DOMContentLoaded", () => {
    // Search overlay elements
    const searchToggle = document.getElementById("navbar-search-toggle");
    const searchOverlay = document.getElementById("search-overlay");
    const searchCloseBtn = document.getElementById("search-close-btn");
    const searchOverlayBg = searchOverlay ? searchOverlay.querySelector(".search-overlay-bg") : null;
    const searchInput = document.getElementById("navbar-search-input");

    // Function to open search overlay
    function openSearchOverlay() {
        if (!searchOverlay) return;
        searchOverlay.classList.add("is-active");
        searchToggle.classList.add("is-active");
        document.body.style.overflow = "hidden";
        // Focus input after animation
        setTimeout(() => {
            if (searchInput) searchInput.focus();
        }, 300);
    }

    // Function to close search overlay
    function closeSearchOverlay() {
        if (!searchOverlay) return;
        searchOverlay.classList.remove("is-active");
        searchToggle.classList.remove("is-active");
        document.body.style.overflow = "";
        if (searchInput) searchInput.blur();
    }

    // Toggle button click handler
    if (searchToggle) {
        searchToggle.addEventListener("click", (e) => {
            e.preventDefault();
            if (searchOverlay.classList.contains("is-active")) {
                closeSearchOverlay();
            } else {
                openSearchOverlay();
            }
        });
    }

    // Close button click handler
    if (searchCloseBtn) {
        searchCloseBtn.addEventListener("click", closeSearchOverlay);
    }

    // Background click to close
    if (searchOverlayBg) {
        searchOverlayBg.addEventListener("click", closeSearchOverlay);
    }

    // Keyboard shortcuts
    document.addEventListener("keydown", (e) => {
        // Open search with Ctrl/Cmd + K
        if ((e.ctrlKey || e.metaKey) && e.key === "k") {
            e.preventDefault();
            if (searchOverlay && !searchOverlay.classList.contains("is-active")) {
                openSearchOverlay();
            }
        }
        // Close search with Escape
        if (e.key === "Escape" && searchOverlay && searchOverlay.classList.contains("is-active")) {
            closeSearchOverlay();
        }
        // Open search with "/" when not focused on input
        if (e.key === "/" && document.activeElement.tagName !== "INPUT" && document.activeElement.tagName !== "TEXTAREA") {
            e.preventDefault();
            if (searchOverlay && !searchOverlay.classList.contains("is-active")) {
                openSearchOverlay();
            }
        }
    });

    // Legacy search-icon handler (for contextmenu if still used)
    const legacyToggles = Array.prototype.slice.call(
        document.querySelectorAll(".search-icon"),
        0,
    );
    legacyToggles.forEach((el) => {
        el.addEventListener("click", () => {
            const $target = document.getElementById("search-control");
            if ($target) {
                el.classList.toggle("is-hidden");
                $target.classList.toggle("is-hidden");
            }
        });
    });
});

// Navbar burger menu toggle
document.addEventListener("DOMContentLoaded", () => {
    const $navbarBurgers = Array.prototype.slice.call(
        document.querySelectorAll(".navbar-burger"),
        0,
    );

    $navbarBurgers.forEach((el) => {
        el.addEventListener("click", () => {
            const target = el.dataset.target;
            const $target = document.getElementById(target);
            el.classList.toggle("is-active");
            $target.classList.toggle("is-active");
        });
    });
});

// Scroll-based context bar visibility
var prevScrollpos = window.scrollY;
var isTyping = false;

document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("search-query");
    const contextBar = document.getElementById("context");

    if (searchInput) {
        searchInput.addEventListener("focus", function() {
            isTyping = true;
        });
        searchInput.addEventListener("blur", function() {
            isTyping = false;
        });
    }

    window.onscroll = function () {
        if (!contextBar) return;
        var currentScrollPos = window.scrollY;

        if (prevScrollpos > currentScrollPos || isTyping) {
            contextBar.style.top = "4rem";
        } else {
            contextBar.style.top = "-2em";
        }
        prevScrollpos = currentScrollPos;
    };
});
