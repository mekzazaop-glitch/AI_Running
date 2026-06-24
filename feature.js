/* ============================================================
   RunForm AI — Feature Page (3D Interactive Edition)
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {
  initCustomCursor();
  initTiltCards();
  initFloatingParticles();
  init3DRunner();
  initFeatureUpload();
  initViewSelector();
  initScoreRingsAnimation();
});

/* ============================================================
   CUSTOM CURSOR with Glow
   ============================================================ */
function initCustomCursor() {
  const glow = document.getElementById('cursor-glow');
  const dot = document.getElementById('cursor-dot');
  if (!glow || !dot) return;

  // Only on desktop
  if (window.matchMedia('(hover: none)').matches) {
    glow.style.display = 'none';
    dot.style.display = 'none';
    return;
  }

  let mouseX = 0, mouseY = 0;
  let glowX = 0, glowY = 0;
  let dotX = 0, dotY = 0;

  document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    glow.classList.add('active');
  });

  document.addEventListener('mouseleave', () => {
    glow.classList.remove('active');
  });

  // Hover effect on clickable elements
  const interactiveSelector = 'a, button, .tilt-card, input, .upload-card__dropzone';
  document.addEventListener('mouseover', (e) => {
    if (e.target.closest(interactiveSelector)) {
      dot.classList.add('hover');
    }
  });
  document.addEventListener('mouseout', (e) => {
    if (e.target.closest(interactiveSelector)) {
      dot.classList.remove('hover');
    }
  });

  function animateCursor() {
    // Smooth follow with lerp
    glowX += (mouseX - glowX) * 0.08;
    glowY += (mouseY - glowY) * 0.08;
    dotX += (mouseX - dotX) * 0.25;
    dotY += (mouseY - dotY) * 0.25;

    glow.style.left = glowX + 'px';
    glow.style.top = glowY + 'px';
    dot.style.left = dotX + 'px';
    dot.style.top = dotY + 'px';

    requestAnimationFrame(animateCursor);
  }
  animateCursor();
}

/* ============================================================
   3D TILT CARDS — Mouse-follow perspective
   ============================================================ */
function initTiltCards() {
  const cards = document.querySelectorAll('.tilt-card');
  if (window.matchMedia('(hover: none)').matches) return;

  cards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      // Tilt amount (max ±8 degrees)
      const tiltX = ((y - centerY) / centerY) * -8;
      const tiltY = ((x - centerX) / centerX) * 8;

      card.style.transform = `perspective(800px) rotateX(${tiltX}deg) rotateY(${tiltY}deg) scale3d(1.02,1.02,1.02)`;

      // Move shine
      const percentX = (x / rect.width) * 100;
      const percentY = (y / rect.height) * 100;
      card.style.setProperty('--mouse-x', percentX + '%');
      card.style.setProperty('--mouse-y', percentY + '%');
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = 'perspective(800px) rotateX(0deg) rotateY(0deg) scale3d(1,1,1)';
      card.style.transition = 'transform 0.5s ease';
      setTimeout(() => { card.style.transition = 'transform 0.1s ease'; }, 500);
    });

    card.addEventListener('mouseenter', () => {
      card.style.transition = 'transform 0.1s ease';
    });
  });
}

/* ============================================================
   FLOATING PARTICLES in Hero
   ============================================================ */
function initFloatingParticles() {
  const layer = document.getElementById('particles-layer');
  if (!layer) return;

  const count = 40;
  for (let i = 0; i < count; i++) {
    const particle = document.createElement('div');
    particle.className = 'particle';

    // Random position
    particle.style.left = Math.random() * 100 + '%';
    particle.style.top = Math.random() * 100 + '%';

    // Random size
    const size = Math.random() * 3 + 1;
    particle.style.width = size + 'px';
    particle.style.height = size + 'px';

    // Random motion
    particle.style.setProperty('--duration', (6 + Math.random() * 10) + 's');
    particle.style.setProperty('--delay', (Math.random() * 8) + 's');
    particle.style.setProperty('--tx', (Math.random() * 100 - 50) + 'px');
    particle.style.setProperty('--ty', -(100 + Math.random() * 200) + 'px');
    particle.style.setProperty('--max-opacity', (0.15 + Math.random() * 0.35).toFixed(2));

    // Random color
    const colors = [
      'rgba(61,137,235,0.8)',
      'rgba(90,200,250,0.7)',
      'rgba(191,90,242,0.6)',
      'rgba(255,255,255,0.3)',
    ];
    particle.style.background = colors[Math.floor(Math.random() * colors.length)];

    layer.appendChild(particle);
  }
}

/* ============================================================
   THREE.JS 3D RUNNER SKELETON
   ============================================================ */
function init3DRunner() {
  const canvas = document.getElementById('hero-3d-canvas');
  if (!canvas || typeof THREE === 'undefined') return;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(60, canvas.clientWidth / canvas.clientHeight, 0.1, 100);
  camera.position.set(0, 0, 6);

  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
  renderer.setSize(canvas.clientWidth, canvas.clientHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  // --- Create wireframe runner skeleton ---
  const runnerGroup = new THREE.Group();
  scene.add(runnerGroup);

  // Material for skeleton
  const boneMat = new THREE.LineBasicMaterial({ color: 0x3D89EB, linewidth: 2, transparent: true, opacity: 0.7 });
  const jointMat = new THREE.MeshBasicMaterial({ color: 0x5AC8FA, transparent: true, opacity: 0.85 });
  const glowMat = new THREE.MeshBasicMaterial({ color: 0x3D89EB, transparent: true, opacity: 0.15 });

  // Joint positions for running pose (side view)
  const joints = {
    head: [0, 2.3, 0],
    neck: [0, 1.9, 0],
    rShoulder: [-0.35, 1.8, 0],
    lShoulder: [0.35, 1.8, 0],
    rElbow: [-0.6, 1.4, 0.2],
    lElbow: [0.7, 1.5, -0.15],
    rWrist: [-0.4, 1.1, 0.35],
    lWrist: [0.85, 1.3, -0.3],
    spine: [0, 1.5, 0],
    hip: [0, 1.0, 0],
    rHip: [-0.15, 0.95, 0],
    lHip: [0.15, 0.95, 0],
    rKnee: [-0.25, 0.45, 0.15],
    lKnee: [0.35, 0.55, -0.2],
    rAnkle: [-0.15, -0.05, -0.1],
    lAnkle: [0.5, 0.1, 0.15],
    rToe: [-0.15, -0.15, 0.15],
    lToe: [0.6, 0.05, 0.35],
  };

  // Store original positions for animation
  const originalJoints = {};
  Object.keys(joints).forEach(k => {
    originalJoints[k] = [...joints[k]];
  });

  // Create joints (spheres)
  const jointMeshes = {};
  Object.entries(joints).forEach(([name, pos]) => {
    const geo = new THREE.SphereGeometry(name === 'head' ? 0.15 : 0.06, 12, 12);
    const mesh = new THREE.Mesh(geo, jointMat.clone());
    mesh.position.set(...pos);
    runnerGroup.add(mesh);
    jointMeshes[name] = mesh;

    // Glow sphere
    const glowGeo = new THREE.SphereGeometry(name === 'head' ? 0.25 : 0.12, 12, 12);
    const glowMesh = new THREE.Mesh(glowGeo, glowMat.clone());
    glowMesh.position.set(...pos);
    runnerGroup.add(glowMesh);
    mesh.userData.glow = glowMesh;
  });

  // Bone connections
  const bones = [
    ['head', 'neck'],
    ['neck', 'rShoulder'], ['neck', 'lShoulder'],
    ['rShoulder', 'rElbow'], ['lShoulder', 'lElbow'],
    ['rElbow', 'rWrist'], ['lElbow', 'lWrist'],
    ['neck', 'spine'], ['spine', 'hip'],
    ['hip', 'rHip'], ['hip', 'lHip'],
    ['rHip', 'rKnee'], ['lHip', 'lKnee'],
    ['rKnee', 'rAnkle'], ['lKnee', 'lAnkle'],
    ['rAnkle', 'rToe'], ['lAnkle', 'lToe'],
  ];

  const boneLines = [];
  bones.forEach(([a, b]) => {
    const geo = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(...joints[a]),
      new THREE.Vector3(...joints[b]),
    ]);
    const line = new THREE.Line(geo, boneMat.clone());
    runnerGroup.add(line);
    boneLines.push({ line, a, b });
  });

  // Floating geometry around the runner
  const floatingGeo = [];
  for (let i = 0; i < 25; i++) {
    const shapes = [
      new THREE.TetrahedronGeometry(0.04 + Math.random() * 0.06, 0),
      new THREE.OctahedronGeometry(0.04 + Math.random() * 0.05, 0),
      new THREE.IcosahedronGeometry(0.03 + Math.random() * 0.04, 0),
    ];
    const geo = shapes[Math.floor(Math.random() * shapes.length)];
    const mat = new THREE.MeshBasicMaterial({
      color: new THREE.Color().setHSL(0.58 + Math.random() * 0.15, 0.7, 0.5 + Math.random() * 0.3),
      wireframe: true,
      transparent: true,
      opacity: 0.2 + Math.random() * 0.3,
    });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.set(
      (Math.random() - 0.5) * 6,
      (Math.random() - 0.5) * 5,
      (Math.random() - 0.5) * 3,
    );
    mesh.userData.speed = 0.3 + Math.random() * 0.8;
    mesh.userData.rotAxis = new THREE.Vector3(Math.random(), Math.random(), Math.random()).normalize();
    mesh.userData.orbitRadius = 2 + Math.random() * 3;
    mesh.userData.orbitSpeed = 0.2 + Math.random() * 0.5;
    mesh.userData.orbitOffset = Math.random() * Math.PI * 2;
    scene.add(mesh);
    floatingGeo.push(mesh);
  }

  // Mouse tracking for 3D rotation
  let targetRotX = 0, targetRotY = 0;
  let currentRotX = 0, currentRotY = 0;

  document.addEventListener('mousemove', (e) => {
    const normX = (e.clientX / window.innerWidth) * 2 - 1;
    const normY = (e.clientY / window.innerHeight) * 2 - 1;
    targetRotY = normX * 0.4;
    targetRotX = normY * 0.25;
  });

  // Animation loop
  let time = 0;
  function animate() {
    requestAnimationFrame(animate);
    time += 0.02;

    // Smooth mouse follow rotation
    currentRotX += (targetRotX - currentRotX) * 0.04;
    currentRotY += (targetRotY - currentRotY) * 0.04;

    runnerGroup.rotation.x = currentRotX;
    runnerGroup.rotation.y = currentRotY + Math.sin(time * 0.3) * 0.05;

    // Animate runner joints (subtle running motion)
    const runPhase = time * 2.5;

    // Legs - running cycle
    const legSwing = Math.sin(runPhase) * 0.3;
    animateJoint('rKnee', originalJoints.rKnee, [0, legSwing * 0.15, Math.sin(runPhase) * 0.15]);
    animateJoint('lKnee', originalJoints.lKnee, [0, -legSwing * 0.15, -Math.sin(runPhase) * 0.15]);
    animateJoint('rAnkle', originalJoints.rAnkle, [0, legSwing * 0.1, Math.sin(runPhase) * 0.2]);
    animateJoint('lAnkle', originalJoints.lAnkle, [0, -legSwing * 0.1, -Math.sin(runPhase) * 0.2]);
    animateJoint('rToe', originalJoints.rToe, [0, legSwing * 0.08, Math.sin(runPhase) * 0.15]);
    animateJoint('lToe', originalJoints.lToe, [0, -legSwing * 0.08, -Math.sin(runPhase) * 0.15]);

    // Arms - counter-swing
    animateJoint('rElbow', originalJoints.rElbow, [0, 0, -Math.sin(runPhase) * 0.2]);
    animateJoint('lElbow', originalJoints.lElbow, [0, 0, Math.sin(runPhase) * 0.2]);
    animateJoint('rWrist', originalJoints.rWrist, [0, 0, -Math.sin(runPhase) * 0.25]);
    animateJoint('lWrist', originalJoints.lWrist, [0, 0, Math.sin(runPhase) * 0.25]);

    // Head bob
    animateJoint('head', originalJoints.head, [0, Math.sin(runPhase * 2) * 0.03, 0]);

    // Update bone lines
    boneLines.forEach(({ line, a, b }) => {
      const posA = jointMeshes[a].position;
      const posB = jointMeshes[b].position;
      const positions = line.geometry.attributes.position.array;
      positions[0] = posA.x; positions[1] = posA.y; positions[2] = posA.z;
      positions[3] = posB.x; positions[4] = posB.y; positions[5] = posB.z;
      line.geometry.attributes.position.needsUpdate = true;
    });

    // Joint glow pulse
    Object.values(jointMeshes).forEach((mesh, i) => {
      if (mesh.userData.glow) {
        const scale = 1 + Math.sin(time * 2 + i) * 0.2;
        mesh.userData.glow.scale.set(scale, scale, scale);
        mesh.userData.glow.position.copy(mesh.position);
      }
    });

    // Floating geometry
    floatingGeo.forEach((mesh) => {
      mesh.rotation.x += 0.005 * mesh.userData.speed;
      mesh.rotation.y += 0.008 * mesh.userData.speed;

      const t = time * mesh.userData.orbitSpeed + mesh.userData.orbitOffset;
      mesh.position.y += Math.sin(t) * 0.002;
      mesh.material.opacity = 0.15 + Math.sin(t * 2) * 0.1;
    });

    renderer.render(scene, camera);
  }

  function animateJoint(name, original, offset) {
    const mesh = jointMeshes[name];
    if (!mesh) return;
    mesh.position.set(
      original[0] + offset[0],
      original[1] + offset[1],
      original[2] + offset[2],
    );
  }

  animate();

  // Resize handler
  window.addEventListener('resize', () => {
    camera.aspect = canvas.clientWidth / canvas.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(canvas.clientWidth, canvas.clientHeight);
  });
}

/* ============================================================
   VIDEO UPLOAD & MOCK ANALYSIS
   ============================================================ */
function initFeatureUpload() {
  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('videoInput');
  const analyzeBtn = document.getElementById('analyzeBtn');
  const resultsPanel = document.getElementById('results-panel');

  if (!dropzone || !fileInput || !analyzeBtn) return;

  let selectedFile = null;

  ['dragenter', 'dragover'].forEach(ev => {
    dropzone.addEventListener(ev, (e) => { e.preventDefault(); dropzone.classList.add('drag-over'); });
  });

  ['dragleave', 'drop'].forEach(ev => {
    dropzone.addEventListener(ev, (e) => { e.preventDefault(); dropzone.classList.remove('drag-over'); });
  });

  dropzone.addEventListener('drop', (e) => {
    const files = e.dataTransfer.files;
    if (files.length && files[0].type.startsWith('video/')) {
      selectedFile = files[0];
      updateDropzoneUI(selectedFile.name);
      analyzeBtn.disabled = false;
    }
  });

  fileInput.addEventListener('change', () => {
    if (fileInput.files.length) {
      selectedFile = fileInput.files[0];
      updateDropzoneUI(selectedFile.name);
      analyzeBtn.disabled = false;
    }
  });

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
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = `
      <svg class="spin" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
        <path d="M21 12a9 9 0 11-6.219-8.56"/>
      </svg>
      Analyzing...
    `;

    setTimeout(() => {
      analyzeBtn.innerHTML = `
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="20 6 9 17 4 12"/>
        </svg>
        Analysis Complete
      `;
      analyzeBtn.style.background = '#34C759';

      if (resultsPanel) {
        resultsPanel.style.display = 'block';
        populateResults();
      }

      setTimeout(() => {
        resultsPanel?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 300);
    }, 2500);
  }
}

/* ============================================================
   POPULATE MOCK RESULTS
   ============================================================ */
function populateResults() {
  const scoreCardsEl = document.getElementById('score-cards');
  const metricsGridEl = document.getElementById('metrics-grid');
  const coachingEl = document.getElementById('coaching-content');

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

  if (coachingEl) {
    coachingEl.innerHTML = `<ul>${coaching.map(c => `<li>${c}</li>`).join('')}</ul>`;
  }

  document.querySelectorAll('.results-panel .reveal, .results-panel .reveal-stagger').forEach(el => {
    el.classList.add('visible');
  });
}

/* ============================================================
   VIEW SELECTOR
   ============================================================ */
function initViewSelector() {
  const viewBtns = document.querySelectorAll('.view-btn');
  viewBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      viewBtns.forEach(b => b.classList.remove('view-btn--active'));
      btn.classList.add('view-btn--active');
    });
  });
}

/* ============================================================
   SCORE RING ANIMATION
   ============================================================ */
function initScoreRingsAnimation() {
  const scoreRings = document.querySelectorAll('.score-card__ring');
  if (!scoreRings.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const ring = entry.target;
        const score = parseInt(ring.dataset.score);
        const circumference = 2 * Math.PI * 52;
        const offset = circumference - (circumference * score / 100);
        const progress = ring.querySelector('.score-card__progress');
        if (progress) {
          setTimeout(() => { progress.style.strokeDashoffset = offset; }, 200);
        }
        observer.unobserve(ring);
      }
    });
  }, { threshold: 0.3 });

  scoreRings.forEach(ring => observer.observe(ring));
}

/* ============================================================
   DYNAMIC RESULT STYLES
   ============================================================ */
const resultStyles = document.createElement('style');
resultStyles.textContent = `
  @keyframes spin { to { transform: rotate(360deg); } }
  .spin { animation: spin 1s linear infinite; }

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

  .results-metrics-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
  @media (min-width: 768px) { .results-metrics-grid { grid-template-columns: repeat(3, 1fr); } }
  @media (min-width: 1024px) { .results-metrics-grid { grid-template-columns: repeat(4, 1fr); } }
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
  .result-metric:hover { border-color: var(--color-primary); }
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

  [data-theme="dark"] .result-score-card { background: var(--color-bg-card); }
  [data-theme="dark"] .result-metric { background: var(--color-bg-card); }
`;
document.head.appendChild(resultStyles);
