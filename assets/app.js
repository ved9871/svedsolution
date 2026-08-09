/* SVED Solution — preview interactions */
(function () {
  'use strict';

  /* ---- Mobile nav ---- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', nav.classList.contains('open'));
    });
  }

  /* ---- Scroll reveal ---- */
  var revealables = document.querySelectorAll('.sec > .wrap > *, .card, .kpi, .tl-item, .quote');
  revealables.forEach(function (el) { el.classList.add('rv'); });

  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
    revealables.forEach(function (el) { io.observe(el); });
  } else {
    revealables.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---- KPI counters ---- */
  function animateCount(el) {
    var target = parseFloat(el.dataset.count);
    var dec = (el.dataset.dec | 0);
    var dur = 1300, start = null;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = (target * eased).toFixed(dec).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  var counters = document.querySelectorAll('[data-count]');
  if (counters.length && 'IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { animateCount(e.target); cio.unobserve(e.target); }
      });
    }, { threshold: 0.5 });
    counters.forEach(function (el) { cio.observe(el); });
  }

  /* ---- Consultation modal ---- */
  var modal = document.getElementById('consultModal');
  if (modal) {
    var SEEN = 'sved_consult_seen';
    var lastFocus = null;

    function openModal(source) {
      if (!modal.hidden) return;
      lastFocus = document.activeElement;
      modal.hidden = false;
      document.body.classList.add('modal-open');
      var first = modal.querySelector('input');
      if (first) first.focus();
      try { sessionStorage.setItem(SEEN, '1'); } catch (e) {}
      if (window.gtag) gtag('event', 'consult_modal_open', { source: source || 'auto' });
    }

    function closeModal() {
      modal.hidden = true;
      document.body.classList.remove('modal-open');
      if (lastFocus) lastFocus.focus();
    }

    modal.addEventListener('click', function (e) {
      if (e.target.hasAttribute('data-close')) closeModal();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !modal.hidden) closeModal();
      // Keep tabbing inside the dialog while it is open.
      if (e.key === 'Tab' && !modal.hidden) {
        var f = modal.querySelectorAll('input:not([aria-hidden]), button, a[href]');
        if (!f.length) return;
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });

    // Any element can open it explicitly.
    document.querySelectorAll('[data-consult]').forEach(function (el) {
      el.addEventListener('click', function (e) { e.preventDefault(); openModal('button'); });
    });

    var seen = false;
    try { seen = !!sessionStorage.getItem(SEEN); } catch (e) {}

    if (!seen) {
      // Once per session, and only after the visitor has shown some interest.
      var fired = false;
      var trigger = function (src) {
        if (fired) return;
        fired = true;
        openModal(src);
      };
      setTimeout(function () { trigger('timer'); }, 35000);
      window.addEventListener('scroll', function onScroll() {
        var pct = (window.scrollY + window.innerHeight) / document.body.scrollHeight;
        if (pct > 0.55) { window.removeEventListener('scroll', onScroll); trigger('scroll'); }
      }, { passive: true });
      // Exit intent, desktop only.
      if (window.matchMedia('(min-width:861px)').matches) {
        document.addEventListener('mouseout', function (e) {
          if (!e.relatedTarget && e.clientY < 12) trigger('exit-intent');
        });
      }
    }
  }

  /* ---- Forms: contact + newsletter -> /api/contact ---- */
  document.querySelectorAll('.sved-form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = form.querySelector('button[type=submit]');
      var status = form.querySelector('.form-status');
      var data = { type: form.dataset.type || 'enquiry', page: location.pathname };
      new FormData(form).forEach(function (v, k) { if (v) data[k] = v; });

      if (!data.email) { status.textContent = 'Please enter your email address.'; status.className = 'form-status err'; return; }

      var label = btn.textContent;
      btn.disabled = true; btn.textContent = 'Sending...';
      status.textContent = ''; status.className = 'form-status';

      fetch('/api/contact', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(data)
      })
        .then(function (r) { return r.json(); })
        .then(function (j) {
          if (j.error) throw new Error(j.error);
          form.reset();
          status.textContent = data.type === 'newsletter'
            ? 'Subscribed. The AI Search Playbook is on its way.'
            : 'Thanks. We reply within one business day.';
          status.className = 'form-status ok';
          if (window.gtag) gtag('event', 'generate_lead', { form_type: data.type });
          // Give the confirmation a beat to be read before the dialog closes.
          if (form.id === 'consultForm' && modal) setTimeout(closeModal, 2600);
        })
        .catch(function (err) {
          status.textContent = err.message || 'Could not send. Please email hello@svedsolution.com.';
          status.className = 'form-status err';
        })
        .finally(function () { btn.disabled = false; btn.textContent = label; });
    });
  });

  /* ---- Audit tool demo ---- */
  var form = document.getElementById('audit-form');
  if (form) {
    var results = document.getElementById('audit-results');
    var runBtn = document.getElementById('audit-run');
    var urlInput = document.getElementById('audit-url');
    var stage = document.getElementById('audit-stage');

    var CHECKS = [
      ['Organization schema (JSON-LD)', 'bad', 'Missing. AI models resolve brands via structured entities. Without Organization + sameAs, you are not a known entity.'],
      ['Person / Author schema', 'bad', 'Missing. Named authorship is a primary E-E-A-T and AI-trust signal.'],
      ['FAQPage schema', 'warn', 'Found on 2 of 41 pages. FAQ blocks are the highest-frequency AI citation format.'],
      ['llms.txt file', 'bad', 'Not found at /llms.txt. Emerging standard for declaring content to LLM crawlers.'],
      ['AI crawler access (robots.txt)', 'warn', 'GPTBot allowed. PerplexityBot and ClaudeBot not declared. Google-Extended not declared.'],
      ['Answer-first content structure', 'warn', '11 of 41 pages open with a direct answer in the first 100 words.'],
      ['Content freshness signals', 'bad', 'Average last-modified age is 287 days. AI retrieval favours recently updated pages.'],
      ['Heading hierarchy (H1-H3)', 'ok', 'Clean on 38 of 41 pages. 3 pages have skipped levels.'],
      ['Citation-ready formats', 'warn', 'Lists and tables present. No comparison matrices or step frameworks detected.'],
      ['Core Web Vitals (mobile)', 'ok', 'LCP 2.1s / INP 180ms / CLS 0.04. Passing.'],
      ['Entity consistency (NAP + brand)', 'warn', 'Brand name rendered 3 different ways across the site and social profiles.'],
      ['External citation footprint', 'bad', 'Found on 2 of 12 Tier-1 citation sources (G2, Capterra, Trustpilot, Crunchbase, Product Hunt, Reddit, Quora).']
    ];

    var order = { bad: 0, warn: 1, ok: 2 };

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var raw = (urlInput.value || '').trim();
      if (!raw) { urlInput.focus(); return; }

      runBtn.disabled = true;
      runBtn.textContent = 'Running checks...';
      results.style.display = 'none';
      results.innerHTML = '';
      stage.style.display = 'block';
      stage.innerHTML = '';

      var lines = [
        'Fetching ' + raw + ' ...',
        'Resolving robots.txt and llms.txt ...',
        'Parsing JSON-LD and structured data ...',
        'Checking AI crawler directives ...',
        'Scoring answer-block structure and freshness ...',
        'Measuring Core Web Vitals ...',
        'Auditing entity consistency and citation footprint ...',
        'Compiling AI Visibility Score ...'
      ];
      var i = 0;
      var tick = setInterval(function () {
        if (i >= lines.length) { clearInterval(tick); return; }
        var d = document.createElement('div');
        d.innerHTML = '<span class="green">&rsaquo;</span> ' + lines[i];
        stage.appendChild(d);
        i++;
      }, 420);

      fetch('/api/audit', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ url: raw })
      })
        .then(function (r) { return r.json().then(function (j) { return { status: r.status, body: j }; }); })
        .then(function (res) {
          clearInterval(tick);
          if (res.body && res.body.error) { fail(res.body.error); return; }
          render(res.body);
        })
        .catch(function () {
          // No Worker available (local file preview) — fall back to the sample report.
          clearInterval(tick);
          render(demoReport(raw), true);
        });
    });

    function fail(msg) {
      stage.style.display = 'none';
      results.style.display = 'block';
      results.innerHTML = '<div class="card" style="margin-top:28px;border-color:rgba(255,92,92,.4)">' +
        '<h3 style="margin-bottom:.5rem">Could not complete the audit</h3>' +
        '<p style="margin-bottom:16px">' + msg + '</p>' +
        '<a class="btn btn-ghost btn-sm" href="/contact">Ask us to run it manually</a></div>';
      runBtn.disabled = false;
      runBtn.textContent = 'Run free audit';
    }

    function demoReport(url) {
      var checks = CHECKS.slice().sort(function (a, b) { return order[a[1]] - order[b[1]]; })
        .map(function (c) { return { label: c[0], state: c[1], detail: c[2] }; });
      var ok = checks.filter(function (c) { return c.state === 'ok'; }).length;
      var warn = checks.filter(function (c) { return c.state === 'warn'; }).length;
      var bad = checks.filter(function (c) { return c.state === 'bad'; }).length;
      return {
        url: url, host: url.replace(/^https?:\/\//, ''),
        score: Math.round((ok * 100 + warn * 50) / checks.length),
        verdict: 'Currently invisible to most AI search engines',
        summary: { ok: ok, warn: warn, bad: bad, total: checks.length },
        checks: checks, demo: true
      };
    }

    function render(data, forcedDemo) {
      var isDemo = forcedDemo || data.demo;
      var score = data.score;
      var turn = (score / 100).toFixed(2);

      var rows = data.checks.map(function (c) {
        var label = c.state === 'ok' ? 'PASS' : (c.state === 'warn' ? 'PARTIAL' : 'FAIL');
        return '<div style="padding:16px 0;border-bottom:1px solid var(--line-soft)">' +
          '<div style="display:flex;justify-content:space-between;gap:16px;align-items:center">' +
          '<strong style="color:var(--white);font-size:.95rem">' + c.label + '</strong>' +
          '<span class="pill pill-' + c.state + '">' + label + '</span></div>' +
          '<p style="font-size:.88rem;color:var(--text-dim);margin:6px 0 0">' + c.detail + '</p></div>';
      }).join('');

      var note = isDemo
        ? 'Sample output — the live Worker was not reachable from this preview. On svedsolution.com this crawls the real URL and returns measured values.'
        : 'Measured live against ' + data.host + (data.cached ? ' (cached within the last 24h)' : '') +
          '. LLM citation testing across ChatGPT, Perplexity and Gemini is included in the full report.';

      results.style.display = 'block';
      results.innerHTML =
        '<div class="panel" style="margin-top:28px">' +
          '<div class="panel-bar"><i class="tdot"></i><i class="tdot"></i><i class="tdot"></i>' +
          '<span style="margin-left:8px">ai-visibility-report — ' + data.host + '</span></div>' +
          '<div style="padding:32px;display:flex;gap:36px;align-items:center;flex-wrap:wrap;border-bottom:1px solid var(--line)">' +
            '<div class="score-ring" style="background:conic-gradient(var(--green) 0turn ' + turn + 'turn, var(--line) ' + turn + 'turn 1turn)">' +
              '<div><div class="score-num">' + score + '</div><div class="score-of">/ 100</div></div></div>' +
            '<div style="flex:1 1 300px">' +
              '<div class="eyebrow" style="margin-bottom:.6rem">AI Visibility Score</div>' +
              '<h3 style="margin-bottom:.5rem">' + data.verdict + '</h3>' +
              '<p style="color:var(--text-dim);font-size:.95rem;margin-bottom:1rem">' +
                data.summary.bad + ' critical gaps, ' + data.summary.warn + ' partial, ' +
                data.summary.ok + ' passing across ' + data.summary.total + ' eligibility checks.</p>' +
              '<a class="btn btn-primary btn-sm" href="/contact">Get the full report + fix plan</a>' +
            '</div>' +
          '</div>' +
          '<div style="padding:8px 32px 24px">' + rows + '</div>' +
        '</div>' +
        '<p class="faint" style="font-size:.8rem;margin-top:14px">' + note + '</p>';

      runBtn.disabled = false;
      runBtn.textContent = 'Run free audit';
      stage.style.display = 'none';
      results.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }
})();
