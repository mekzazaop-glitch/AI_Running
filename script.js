/* ============================================================
   RunForm AI — Landing Page Interactivity
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initNavbar();
  initMobileMenu();
  initFAQ();
  initPricingToggle();
  initScrollReveal();
  initSmoothScroll();
});

/* ---- Dark / Light Theme Toggle ---- */
function initTheme() {
  const toggle = document.getElementById('theme-toggle');
  if (!toggle) return;

  // Check saved preference or system preference
  const saved = localStorage.getItem('runform-theme');
  if (saved) {
    document.documentElement.setAttribute('data-theme', saved);
    updateThemeIcon(toggle, saved);
  } else {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (prefersDark) {
      document.documentElement.setAttribute('data-theme', 'dark');
      updateThemeIcon(toggle, 'dark');
    }
  }

  toggle.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';

    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('runform-theme', next);
    updateThemeIcon(toggle, next);
  });
}

function updateThemeIcon(btn, theme) {
  if (theme === 'dark') {
    // Sun icon
    btn.innerHTML = `
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="5"/>
        <line x1="12" y1="1" x2="12" y2="3"/>
        <line x1="12" y1="21" x2="12" y2="23"/>
        <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
        <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
        <line x1="1" y1="12" x2="3" y2="12"/>
        <line x1="21" y1="12" x2="23" y2="12"/>
        <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
        <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
      </svg>`;
  } else {
    // Moon icon
    btn.innerHTML = `
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
      </svg>`;
  }
}

/* ---- Sticky Navbar Scroll Effect ---- */
function initNavbar() {
  const navbar = document.getElementById('navbar');
  if (!navbar) return;

  const onScroll = () => {
    if (window.scrollY > 10) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  };

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll(); // initial check
}

/* ---- Mobile Hamburger Menu ---- */
function initMobileMenu() {
  const hamburger = document.getElementById('hamburger');
  const mobileMenu = document.getElementById('mobile-menu');
  if (!hamburger || !mobileMenu) return;

  hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    mobileMenu.classList.toggle('open');
    document.body.style.overflow = mobileMenu.classList.contains('open') ? 'hidden' : '';
  });

  // Close menu when clicking a link
  mobileMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      hamburger.classList.remove('active');
      mobileMenu.classList.remove('open');
      document.body.style.overflow = '';
    });
  });
}

/* ---- FAQ Accordion ---- */
function initFAQ() {
  const items = document.querySelectorAll('.faq-item');

  items.forEach(item => {
    const question = item.querySelector('.faq-item__question');
    if (!question) return;

    question.addEventListener('click', () => {
      const isOpen = item.classList.contains('open');

      // Close all other items
      items.forEach(other => {
        if (other !== item) other.classList.remove('open');
      });

      // Toggle current
      item.classList.toggle('open', !isOpen);
    });
  });
}

/* ---- Pricing Toggle (Monthly / Annual) ---- */
function initPricingToggle() {
  const toggleBtn = document.getElementById('pricing-toggle');
  const monthlyLabel = document.getElementById('toggle-monthly');
  const annualLabel = document.getElementById('toggle-annual');
  if (!toggleBtn) return;

  let isAnnual = false;

  toggleBtn.addEventListener('click', () => {
    isAnnual = !isAnnual;
    toggleBtn.classList.toggle('active', isAnnual);

    // Update active label styles
    if (monthlyLabel && annualLabel) {
      monthlyLabel.classList.toggle('pricing__toggle-label--active', !isAnnual);
      annualLabel.classList.toggle('pricing__toggle-label--active', isAnnual);
    }

    // Update prices with animation
    const prices = document.querySelectorAll('.pricing-card__price');
    prices.forEach(el => {
      const monthly = el.getAttribute('data-monthly');
      const annual = el.getAttribute('data-annual');
      const value = isAnnual ? annual : monthly;

      // Fade out → update → fade in
      el.style.opacity = '0';
      el.style.transform = 'translateY(-4px)';
      setTimeout(() => {
        el.textContent = `$${value}`;
        el.style.opacity = '1';
        el.style.transform = 'translateY(0)';
      }, 180);
    });
  });

  // Make labels clickable too
  if (monthlyLabel) {
    monthlyLabel.addEventListener('click', () => {
      if (isAnnual) toggleBtn.click();
    });
  }
  if (annualLabel) {
    annualLabel.addEventListener('click', () => {
      if (!isAnnual) toggleBtn.click();
    });
  }
}

/* ---- Scroll Reveal (IntersectionObserver) ---- */
function initScrollReveal() {
  const revealElements = document.querySelectorAll('.reveal, .reveal-stagger');
  if (!revealElements.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target); // animate only once
        }
      });
    },
    {
      threshold: 0.15,
      rootMargin: '0px 0px -40px 0px',
    }
  );

  revealElements.forEach(el => observer.observe(el));
}

/* ---- Smooth Scroll for Anchor Links ---- */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const targetId = anchor.getAttribute('href');
      if (targetId === '#') return;

      const target = document.querySelector(targetId);
      if (!target) return;

      e.preventDefault();
      const navHeight = document.getElementById('navbar')?.offsetHeight || 0;
      const top = target.getBoundingClientRect().top + window.scrollY - navHeight;

      window.scrollTo({ top, behavior: 'smooth' });
    });
  });
}
