// ══════════════════════════════════════════
// NeuralBase — Main JavaScript
// ══════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
    initCounters();
    initFAQ();
    initMobileMenu();
    initSearch();
    initFlashAutoHide();
});

// ── ANIMATED COUNTERS ──
function initCounters() {
    const counters = document.querySelectorAll('[data-count]');
    if (!counters.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const target = parseInt(el.dataset.count);
                animateCounter(el, target);
                observer.unobserve(el);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => observer.observe(counter));
}

function animateCounter(el, target) {
    const duration = 1500;
    const start = performance.now();

    function update(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
        el.textContent = Math.floor(eased * target);

        if (progress < 1) {
            requestAnimationFrame(update);
        } else {
            el.textContent = target;
        }
    }

    requestAnimationFrame(update);
}

// ── FAQ ACCORDION ──
function initFAQ() {
    document.querySelectorAll('.faq-question').forEach(btn => {
        btn.addEventListener('click', () => {
            const item = btn.closest('.faq-item');
            const isActive = item.classList.contains('active');

            // Close all
            document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('active'));

            // Open clicked (if wasn't active)
            if (!isActive) {
                item.classList.add('active');
            }
        });
    });
}

// ── MOBILE MENU ──
function initMobileMenu() {
    const btn = document.querySelector('.mobile-menu-btn');
    const nav = document.querySelector('.mobile-nav');
    if (!btn || !nav) return;

    btn.addEventListener('click', () => {
        nav.classList.toggle('active');
        btn.textContent = nav.classList.contains('active') ? '✕' : '☰';
    });

    // Close on link click
    nav.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            nav.classList.remove('active');
            btn.textContent = '☰';
        });
    });
}

// ── SEARCH (Ctrl+K) ──
function initSearch() {
    const searchInput = document.querySelector('.nav-search input');
    if (!searchInput) return;

    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            searchInput.focus();
        }
        if (e.key === 'Escape') {
            searchInput.blur();
        }
    });

    // Live search redirect on Enter
    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && searchInput.value.trim()) {
            window.location.href = `/search?q=${encodeURIComponent(searchInput.value.trim())}`;
        }
    });
}

// ── FLASH AUTO HIDE ──
function initFlashAutoHide() {
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => alert.remove(), 300);
        }, 4000);
    });
}
