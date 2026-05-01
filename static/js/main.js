/* ============================================
   IABE Platform — main.js v2.0
   Animations · Interactions · Dynamic UX
   ============================================ */

document.addEventListener('DOMContentLoaded', function () {

    /* ========================================
       1. NAVBAR — Scroll shadow + backdrop
       ======================================== */
    const navbar = document.getElementById('main-navbar');
    let lastScroll = 0;
    if (navbar) {
        window.addEventListener('scroll', function () {
            const y = window.scrollY;
            navbar.classList.toggle('scrolled', y > 30);
            lastScroll = y;
        }, { passive: true });
    }

    /* ========================================
       2. MOBILE MENU — Smooth toggle
       ======================================== */
    const toggle = document.getElementById('mobile-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    const navLinks = document.getElementById('nav-links');

    function applyMobileLayout() {
        if (window.innerWidth < 900) {
            if (toggle) toggle.style.display = 'block';
            if (navLinks) navLinks.style.display = 'none';
        } else {
            if (toggle) toggle.style.display = 'none';
            if (navLinks) navLinks.style.display = 'flex';
            if (mobileMenu) { mobileMenu.style.display = 'none'; mobileMenu.style.maxHeight = '0'; }
        }
    }
    applyMobileLayout();
    window.addEventListener('resize', applyMobileLayout);

    if (toggle && mobileMenu) {
        mobileMenu.style.overflow = 'hidden';
        mobileMenu.style.transition = 'max-height 0.35s ease, opacity 0.35s ease';
        mobileMenu.style.maxHeight = '0';
        mobileMenu.style.opacity = '0';

        toggle.addEventListener('click', function () {
            const isOpen = mobileMenu.style.maxHeight !== '0px' && mobileMenu.style.maxHeight !== '0';
            if (isOpen) {
                mobileMenu.style.maxHeight = '0';
                mobileMenu.style.opacity = '0';
                setTimeout(() => { mobileMenu.style.display = 'none'; }, 350);
            } else {
                mobileMenu.style.display = 'block';
                requestAnimationFrame(() => {
                    mobileMenu.style.maxHeight = mobileMenu.scrollHeight + 'px';
                    mobileMenu.style.opacity = '1';
                });
            }
            toggle.setAttribute('aria-expanded', !isOpen);
            // Toggle icon
            const icon = toggle.querySelector('i');
            if (icon) icon.className = isOpen ? 'fas fa-bars' : 'fas fa-times';
        });
    }

    /* ========================================
       3. ACTIVE NAV LINK
       ======================================== */
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(function (link) {
        const href = link.getAttribute('href');
        if (href && currentPath.startsWith(href) && href !== '/') {
            link.classList.add('active');
        } else if (href === '/' && currentPath === '/') {
            link.classList.add('active');
        }
    });

    /* ========================================
       4. SCROLL REVEAL — IntersectionObserver
       ======================================== */
    const revealElements = document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale');
    if (revealElements.length > 0 && 'IntersectionObserver' in window) {
        const revealObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
        revealElements.forEach(el => revealObserver.observe(el));
    }

    // Auto-apply reveal to sections and cards for pages that don't manually add the class
    document.querySelectorAll('section > .container, section > .max-w-7xl, section > .max-w-2xl, section > .max-w-3xl, section > .max-w-md').forEach(function (el, i) {
        if (!el.classList.contains('reveal') && !el.closest('.hero') && !el.closest('.page-header') && !el.closest('.gradient-hero')) {
            el.classList.add('reveal');
            el.style.transitionDelay = '0.05s';
        }
    });
    // Re-observe after auto-apply
    document.querySelectorAll('.reveal:not(.revealed)').forEach(function (el) {
        if ('IntersectionObserver' in window) {
            const obs = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('revealed');
                        obs.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
            obs.observe(el);
        }
    });

    /* ========================================
       5. ANIMATED COUNTERS
       ======================================== */
    function animateCounter(el) {
        const text = el.textContent.trim();
        const match = text.match(/^([\d,.]+)(\+?)$/);
        if (!match) return;
        const target = parseInt(match[1].replace(/[,.\s]/g, ''), 10);
        const suffix = match[2] || '';
        if (isNaN(target) || target === 0) return;

        const duration = 1800;
        const startTime = performance.now();

        function easeOutCubic(t) { return 1 - Math.pow(1 - t, 3); }

        function tick(now) {
            const elapsed = now - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const current = Math.round(easeOutCubic(progress) * target);
            el.textContent = current.toLocaleString('fr-FR') + suffix;
            if (progress < 1) requestAnimationFrame(tick);
        }
        el.textContent = '0' + suffix;
        requestAnimationFrame(tick);
    }

    const statValues = document.querySelectorAll('.stat-value');
    if (statValues.length > 0 && 'IntersectionObserver' in window) {
        const counterObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    counterObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        statValues.forEach(el => counterObserver.observe(el));
    }

    /* ========================================
       6. STAGGERED CARD ENTRANCE
       ======================================== */
    function staggerChildren(parentSelector, childSelector) {
        document.querySelectorAll(parentSelector).forEach(function (parent) {
            const children = parent.querySelectorAll(childSelector);
            if (children.length === 0) return;
            if ('IntersectionObserver' in window) {
                const obs = new IntersectionObserver(function (entries) {
                    entries.forEach(function (entry) {
                        if (entry.isIntersecting) {
                            children.forEach(function (child, index) {
                                child.style.opacity = '0';
                                child.style.transform = 'translateY(20px)';
                                child.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                                child.style.transitionDelay = (index * 0.1) + 's';
                                requestAnimationFrame(() => {
                                    child.style.opacity = '1';
                                    child.style.transform = 'translateY(0)';
                                });
                            });
                            obs.unobserve(entry.target);
                        }
                    });
                }, { threshold: 0.1 });
                obs.observe(parent);
            }
        });
    }
    staggerChildren('.grid', '.card, .bg-white.rounded-2xl, .bg-white.rounded-xl');

    /* ========================================
       7. AUTO-DISMISS ALERTS
       ======================================== */
    document.querySelectorAll('.alert').forEach(function (el) {
        setTimeout(function () {
            el.style.transition = 'opacity 0.5s ease, transform 0.5s ease, max-height 0.5s ease';
            el.style.opacity = '0';
            el.style.transform = 'translateY(-10px)';
            el.style.maxHeight = '0';
            el.style.overflow = 'hidden';
            el.style.marginBottom = '0';
            el.style.paddingTop = '0';
            el.style.paddingBottom = '0';
            setTimeout(function () { el.remove(); }, 520);
        }, 6000);
    });

    /* ========================================
       8. COUNTDOWN TIMER
       ======================================== */
    const countdownEl = document.getElementById('countdown');
    if (countdownEl) {
        const target = new Date(countdownEl.dataset.target);
        function updateCountdown() {
            const diff = target - new Date();
            if (diff <= 0) { countdownEl.textContent = 'Terminé'; return; }
            const d = Math.floor(diff / 86400000);
            const h = Math.floor((diff % 86400000) / 3600000);
            const m = Math.floor((diff % 3600000) / 60000);
            const s = Math.floor((diff % 60000) / 1000);
            const set = (id, val) => { const e = document.getElementById(id); if (e) e.textContent = String(val).padStart(2, '0'); };
            set('cd-days', d); set('cd-hours', h); set('cd-minutes', m); set('cd-seconds', s);
        }
        updateCountdown();
        setInterval(updateCountdown, 1000);
    }

    /* ========================================
       9. SMOOTH SCROLL ANCHORS
       ======================================== */
    document.querySelectorAll('a[href^="#"]').forEach(function (a) {
        a.addEventListener('click', function (e) {
            const sel = this.getAttribute('href');
            if (sel.length <= 1) return;
            const target = document.querySelector(sel);
            if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
        });
    });

    /* ========================================
       10. BUTTON RIPPLE EFFECT
       ======================================== */
    document.querySelectorAll('.btn, button[type="submit"]').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            ripple.style.cssText = 'position:absolute;border-radius:50%;background:rgba(255,255,255,.25);pointer-events:none;' +
                'width:' + size + 'px;height:' + size + 'px;' +
                'left:' + (e.clientX - rect.left - size / 2) + 'px;' +
                'top:' + (e.clientY - rect.top - size / 2) + 'px;' +
                'transform:scale(0);animation:ripple-expand 0.6s ease-out forwards;';
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 700);
        });
    });

    // Inject ripple keyframe
    if (!document.getElementById('ripple-style')) {
        const style = document.createElement('style');
        style.id = 'ripple-style';
        style.textContent = '@keyframes ripple-expand{to{transform:scale(2.5);opacity:0;}}';
        document.head.appendChild(style);
    }

    /* ========================================
       11. PARALLAX HERO (subtle)
       ======================================== */
    const heroSection = document.querySelector('.hero, .page-header');
    if (heroSection) {
        window.addEventListener('scroll', function () {
            const y = window.scrollY;
            if (y < 800) {
                heroSection.style.backgroundPositionY = (y * 0.3) + 'px';
            }
        }, { passive: true });
    }

    /* ========================================
       12. FORM ENHANCEMENT
       ======================================== */
    // Add focus animations to form fields
    document.querySelectorAll('input, select, textarea').forEach(function (field) {
        field.addEventListener('focus', function () {
            const parent = this.closest('div');
            if (parent) parent.style.transform = 'translateY(-1px)';
        });
        field.addEventListener('blur', function () {
            const parent = this.closest('div');
            if (parent) parent.style.transform = '';
        });
    });

    /* ========================================
       13. HOVER CARD TILT (subtle)
       ======================================== */
    document.querySelectorAll('.card, .bg-white.rounded-2xl.shadow-sm').forEach(function (card) {
        card.addEventListener('mousemove', function (e) {
            const rect = this.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width - 0.5;
            const y = (e.clientY - rect.top) / rect.height - 0.5;
            this.style.transform = 'perspective(600px) rotateX(' + (-y * 3) + 'deg) rotateY(' + (x * 3) + 'deg) translateY(-4px)';
        });
        card.addEventListener('mouseleave', function () {
            this.style.transform = '';
        });
    });

    /* ========================================
       14. PAGE LOAD ANIMATION
       ======================================== */
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.4s ease';
    requestAnimationFrame(() => {
        document.body.style.opacity = '1';
    });

});
