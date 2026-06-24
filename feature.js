/* ============================================================
   RunForm AI — Feature Page Interactivity
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
  initFeatureUpload();
  initViewSelector();
  initScoreRingsAnimation();
});

/* ---- Video Upload & Mock Analysis ---- */
function initFeatureUpload() {
  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('videoInput');
  const analyzeBtn = document.getElementById('analyzeBtn');
  const resultsPanel = document.getElementById('results-panel');
  const uploadCard = document.getElementById('upload-card');

  if (!dropzone || !fileInput || !analyzeBtn) return;

  let selectedFile = null;

  // Drag & drop
  ['dragenter', 'dragover'].forEach(ev => {
    dropzone.addEventListener(ev, (e) => {
      e.preventDefault();
      dropzone.classList.add('drag-over');
    });
  });

  ['dragleave', 'drop'].forEach(ev => {
    dropzone.addEventListener(ev, (e) => {
      e.preventDefault();
      dropzone.classList.remove('drag-over');
    });
  });

  dropzone.addEventListener('drop', (e) => {
    const files = e.dataTransfer.files;
    if (files.length && files[0].type.startsWith('video/')) {
      selectedFile = files[0];
      updateDropzoneUI(selectedFile.name);
      analyzeBtn.disabled = false;
    }
  });

  // File input change
  fileInput.addEventListener('change', () => {
    if (fileInput.files.length) {
      selectedFile = fileInput.files[0];
      updateDropzoneUI(selectedFile.name);
      analyzeBtn.disabled = false;
    }
  });

  // Analyze button
  analyzeBtn.addEventListener('click', () => {
    if (!selectedFile) return;
    runMockAnalysis();
  });

  function updateDropzoneUI(filename) {
    const textEl = dropzone.querySelector('.upload-card__text');
    const subEl = dropzone.querySelector('.upload-card__text-sub');
    if (textEl) textEl.textContent = `✓ ${filename}`;
    if (subEl) subEl.textContent = 'Ready to analyze';
    dropzone.style.borderColor = 'var(--color-primary)';
  }

  function runMockAnalysis() {
    // Show loading state
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = `
      <svg class="spin" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
        <path d="M21 12a9 9 0 11-6.219-8.56"/>
      </svg>
      Analyzing...
    `;

    // Simulate analysis delay
    setTimeout(() => {
      analyzeBtn.innerHTML = `
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="20 6 9 17 4 12"/>
        </svg>
        Analysis Complete
      `;
      analyzeBtn.style.background = '#34C759';

      // Show results
      if (resultsPanel) {
        resultsPanel.style.display = 'block';
        populateResults();
      }

      // Smooth scroll to results
      setTimeout(() => {
        resultsPanel?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 300);
    }, 2500);
  }
}

/* ---- Populate Mock Results ---- */
function populateResults() {
  const scoreCardsEl = document.getElementById('score-cards');
  const metricsGridEl = document.getElementById('metrics-grid');
  const coachingEl = document.getElementById('coaching-content');

  // Mock data
  const scores = [
    { name: 'Economy', score: 82, color: '#3D89EB', desc: 'Good cadence & ground contact' },
    { name: 'Landing', score: 88, color: '#34C759', desc: 'Near-optimal foot strike' },
    { name: 'Stability', score: 75, color: '#FF9F0A', desc: 'Mild trunk lateral sway' },
    { name: 'Symmetry', score: 91, color: '#BF5AF2', desc: 'Excellent L/R balance' },
  ];

  const metrics = [
    { name: 'Cadence', value: '178 spm', status: 'good' },
    { name: 'Foot Strike Angle', value: '3.2°', status: 'good' },
    { name: 'Knee Flexion at IC', value: '14.8°', status: 'good' },
    { name: 'Vertical Oscillation', value: '7.2 cm', status: 'good' },
    { name: 'Hip Flexion', value: '42.1°', status: 'good' },
    { name: 'Hip Extension', value: '11.5°', status: 'moderate' },
    { name: 'Trunk Lean', value: '8.7°', status: 'moderate' },
    { name: 'Ground Contact', value: '238 ms', status: 'good' },
    { name: 'Arm Swing Angle', value: '45°', status: 'good' },
    { name: 'Pelvic Drop', value: '6.2°', status: 'moderate' },
    { name: 'Shank Angle', value: '92.4°', status: 'good' },
    { name: 'Swing Knee Recovery', value: '130°', status: 'good' },
  ];

  const coaching = [
    '<strong>Reduce trunk lateral sway:</strong> Focus on engaging your core muscles during the stance phase. Try plank variations and single-leg deadlifts to build lateral stability.',
    '<strong>Increase hip extension:</strong> Your hip extension is slightly limited. Add hip flexor stretches and glute activation drills (hip bridges, clamshells) to your warm-up routine.',
    '<strong>Monitor pelvic drop:</strong> A 6.2° pelvic drop suggests mild gluteus medius weakness on the stance side. Single-leg squats and lateral band walks can help strengthen this area.',
    '<strong>Overall:</strong> Your running form is quite efficient with good cadence and foot strike. Focus on the stability improvements above to reduce injury risk and improve economy.',
  ];

  // Render score cards
  if (scoreCardsEl) {
    scoreCardsEl.innerHTML = scores.map(s => `
      <div class="result-score-card" style="--score-color:${s.color}">
        <div class="result-score-card__ring">
          <svg viewBox="0 0 80 80">
            <circle cx="40" cy="40" r="34" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="6"/>
            <circle class="result-ring-progress" cx="40" cy="40" r="34" fill="none" stroke="${s.color}" stroke-width="6"
              stroke-linecap="round" stroke-dasharray="214" stroke-dashoffset="${214 - (214 * s.score / 100)}"
              style="transform:rotate(-90deg);transform-origin:center;transition:stroke-dashoffset 1.5s ease"/>
          </svg>
          <span class="result-score-card__value">${s.score}</span>
        </div>
        <h4 class="result-score-card__name">${s.name}</h4>
        <p class="result-score-card__desc">${s.desc}</p>
      </div>
    `).join('');
  }

  // Render metrics grid
  if (metricsGridEl) {
    metricsGridEl.innerHTML = `
      <h3 style="font-family:var(--font-heading);font-weight:700;font-size:1.125rem;color:var(--color-text);margin-bottom:20px;">
        Detailed Metrics
      </h3>
      <div class="results-metrics-grid">
        ${metrics.map(m => `
          <div class="result-metric">
            <span class="result-metric__status result-metric__status--${m.status}"></span>
            <div class="result-metric__info">
              <span class="result-metric__name">${m.name}</span>
              <span class="result-metric__value">${m.value}</span>
            </div>
          </div>
        `).join('')}
      </div>
    `;
  }

  // Render coaching
  if (coachingEl) {
    coachingEl.innerHTML = `
      <ul>
        ${coaching.map(c => `<li>${c}</li>`).join('')}
      </ul>
    `;
  }

  // Trigger reveal animations
  document.querySelectorAll('.results-panel .reveal, .results-panel .reveal-stagger').forEach(el => {
    el.classList.add('visible');
  });
}

/* ---- View Selector ---- */
function initViewSelector() {
  const viewBtns = document.querySelectorAll('.view-btn');
  viewBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      viewBtns.forEach(b => b.classList.remove('view-btn--active'));
      btn.classList.add('view-btn--active');
    });
  });
}

/* ---- Score Ring Animation ---- */
function initScoreRingsAnimation() {
  const scoreRings = document.querySelectorAll('.score-card__ring');
  if (!scoreRings.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const ring = entry.target;
        const score = parseInt(ring.dataset.score);
        const circumference = 2 * Math.PI * 52; // r=52
        const offset = circumference - (circumference * score / 100);
        const progress = ring.querySelector('.score-card__progress');
        if (progress) {
          setTimeout(() => {
            progress.style.strokeDashoffset = offset;
          }, 200);
        }
        observer.unobserve(ring);
      }
    });
  }, { threshold: 0.3 });

  scoreRings.forEach(ring => observer.observe(ring));
}

/* ---- Inline styles for dynamic result elements ---- */
const resultStyles = document.createElement('style');
resultStyles.textContent = `
  /* Loading spinner */
  @keyframes spin { to { transform: rotate(360deg); } }
  .spin { animation: spin 1s linear infinite; }

  /* Result score cards */
  .result-score-card {
    background: var(--color-bg-card);
    border-radius: var(--radius-md);
    padding: 20px;
    text-align: center;
    border: 1px solid var(--color-border-light);
    transition: all 0.3s ease;
  }
  .result-score-card:hover {
    border-color: var(--score-color);
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    transform: translateY(-2px);
  }
  .result-score-card__ring {
    position: relative;
    width: 80px;
    height: 80px;
    margin: 0 auto 12px;
  }
  .result-score-card__ring svg { width: 100%; height: 100%; }
  .result-score-card__value {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--font-heading);
    font-weight: 800;
    font-size: 1.25rem;
    color: var(--color-text);
  }
  .result-score-card__name {
    font-family: var(--font-heading);
    font-weight: 700;
    font-size: 0.875rem;
    color: var(--color-text);
    margin-bottom: 4px;
  }
  .result-score-card__desc {
    font-size: 0.75rem;
    color: var(--color-text-muted);
  }

  /* Metrics grid */
  .results-metrics-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
  @media (min-width: 768px) {
    .results-metrics-grid { grid-template-columns: repeat(3, 1fr); }
  }
  @media (min-width: 1024px) {
    .results-metrics-grid { grid-template-columns: repeat(4, 1fr); }
  }
  .result-metric {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 12px;
    background: var(--color-bg);
    border-radius: var(--radius-sm);
    border: 1px solid var(--color-border-light);
    transition: all 0.2s ease;
  }
  .result-metric:hover {
    border-color: var(--color-primary);
  }
  .result-metric__status {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
  }
  .result-metric__status--good { background: #34C759; }
  .result-metric__status--moderate { background: #FF9F0A; }
  .result-metric__status--poor { background: #FF3B30; }
  .result-metric__info {
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-width: 0;
  }
  .result-metric__name {
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--color-text-muted);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .result-metric__value {
    font-family: var(--font-mono);
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--color-text);
  }

  /* Dark mode result overrides */
  [data-theme="dark"] .result-score-card {
    background: var(--color-bg-card);
  }
  [data-theme="dark"] .result-metric {
    background: var(--color-bg-card);
  }
`;
document.head.appendChild(resultStyles);
