/* SVED Solution — preview interactions */
(function () {
  'use strict';

  /**
   * Push a custom event onto dataLayer for GTM to pick up.
   *
   * GA4 is configured inside GTM rather than hardcoded, so window.gtag does not
   * exist. Pushing to dataLayer works whether or not the container has finished
   * loading — the array is created by the GTM stub before this script runs, and
   * queued events are processed once the container arrives.
   *
   * Create matching Custom Event triggers in GTM for: generate_lead,
   * video_start.
   */
  function track(event, params) {
    try {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push(Object.assign({ event: event }, params || {}));
    } catch (e) { /* analytics must never break the page */ }
  }

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

  /* ---- YouTube facade: inject the iframe only on demand ---- */
  document.querySelectorAll('.yt-facade').forEach(function (el) {
    function load() {
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube.com/embed/' + el.dataset.yt +
        (el.dataset.yt.indexOf('?') > -1 ? '&' : '?') + 'autoplay=1';
      f.title = 'Web3Tech Network channel';
      f.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
      f.referrerPolicy = 'strict-origin-when-cross-origin';
      f.allowFullscreen = true;
      el.innerHTML = '';
      el.classList.remove('yt-facade');
      el.removeAttribute('role');
      el.removeAttribute('tabindex');
      el.appendChild(f);
      track('video_start', { provider: 'youtube' });
    }
    el.addEventListener('click', load);
    el.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); load(); }
    });
  });

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
          track('generate_lead', { form_type: data.type });
        })
        .catch(function (err) {
          status.textContent = err.message || 'Could not send. Please email hello@svedsolution.com.';
          status.className = 'form-status err';
        })
        .finally(function () { btn.disabled = false; btn.textContent = label; });
    });
  });

  /* ---- AI visibility check ---- */
  var form = document.getElementById('audit-form');
  if (form) {
    var results = document.getElementById('audit-results');
    var runBtn = document.getElementById('audit-run');
    var stage = document.getElementById('audit-stage');
    var errorBox = document.getElementById('audit-error');
    var RUN_LABEL = runBtn.textContent;
    var savedLeads = {};

    // The API returns text taken from the site being checked, so everything
    // is escaped before it goes into the page.
    var esc = function (s) {
      return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
        return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
      });
    };
    var STATE = { ok: ['Good', 'pill-ok'], warn: ['Needs work', 'pill-warn'], bad: ['Problem', 'pill-bad'] };
    var isLocal = location.protocol === 'file:' || /^(localhost|127\.0\.0\.1)$/.test(location.hostname);

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var site = form.elements.website.value.trim();
      var name = form.elements.name.value.trim();
      var email = form.elements.email.value.trim();
      errorBox.textContent = '';

      if (!site) return invalid('Please enter your website address.', 'website');
      if (name.length < 2) return invalid('Please enter your name.', 'name');
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(email)) return invalid('Please enter a valid email address.', 'email');

      var lead = {
        type: 'audit', page: location.pathname, name: name, email: email, website: site,
        // Ticked only if the visitor chose the newsletter. Never assumed.
        consent: form.elements.consent.checked,
        company_website: form.elements.company_website.value
      };

      runBtn.disabled = true;
      runBtn.textContent = 'Checking your site...';
      results.style.display = 'none';
      results.innerHTML = '';
      stage.style.display = 'block';
      stage.innerHTML = '';

      var lines = [
        'Opening ' + esc(site),
        'Checking which AI crawlers are allowed in',
        'Reading how your business is described',
        'Looking at how your content is laid out',
        'Measuring page speed on a phone',
        'Working out your score'
      ];
      var i = 0;
      var tick = setInterval(function () {
        if (i >= lines.length) { clearInterval(tick); return; }
        var d = document.createElement('div');
        d.innerHTML = '<span class="green">&rsaquo;</span> ' + lines[i];
        stage.appendChild(d);
        i++;
      }, 520);

      fetch('/api/audit', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ url: site })
      })
        .then(function (r) { return r.json(); })
        .then(function (body) {
          clearInterval(tick);
          if (body && body.error) { saveLead(lead, ''); fail(body.error); return; }
          saveLead(lead, body.score);
          render(body, false);
        })
        .catch(function () {
          clearInterval(tick);
          // With no API behind it (a local preview), show a sample so the page
          // can still be reviewed. On the live site a failure is reported as one.
          if (isLocal) { render(sampleReport(site), true); return; }
          saveLead(lead, '');
          fail('The check could not be completed just now. Please try again in a minute.');
        });
    });

    function invalid(message, fieldName) {
      errorBox.textContent = message;
      form.elements[fieldName].focus();
    }

    function saveLead(lead, score) {
      var key = lead.email + '|' + lead.website;
      if (savedLeads[key]) return;
      savedLeads[key] = true;
      var body = {};
      Object.keys(lead).forEach(function (k) { body[k] = lead[k]; });
      body.score = score === '' ? '' : String(score);
      fetch('/api/contact', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(body)
      }).then(function () { track('generate_lead', { form_type: 'audit' }); })
        .catch(function () { /* the result still shows; the lead is simply not recorded */ });
    }

    function done() {
      runBtn.disabled = false;
      runBtn.textContent = RUN_LABEL;
      stage.style.display = 'none';
    }

    function fail(message) {
      results.style.display = 'block';
      results.innerHTML = '<div class="card ar-fail">' +
        '<h3>We could not finish the check</h3>' +
        '<p>' + esc(message) + '</p>' +
        '<a class="btn btn-ghost btn-sm" href="/contact/">Ask us to run it for you</a></div>';
      done();
    }

    function row(c) {
      var s = STATE[c.state] || STATE.warn;
      return '<div class="ar-row">' +
        '<div class="ar-row-top"><strong>' + esc(c.label) + '</strong>' +
        '<span class="pill ' + s[1] + '">' + s[0] + '</span></div>' +
        '<p>' + esc(c.detail) + '</p>' +
        (c.fix ? '<p class="ar-fix"><strong>What to do:</strong> ' + esc(c.fix) + '</p>' : '') +
        '</div>';
    }

    function render(data, sample) {
      var turn = (data.score / 100).toFixed(2);
      var groups = data.groups || [];

      var bars = groups.map(function (g) {
        return '<div class="ar-group"><div class="ar-group-top"><span>' + esc(g.name) + '</span>' +
          '<strong>' + g.score + '</strong></div><div class="bar"><i style="width:' + g.score + '%"></i></div></div>';
      }).join('');

      var fixes = (data.topFixes || []).map(function (f) {
        return '<li><strong>' + esc(f.label) + '.</strong> ' + esc(f.fix) + '</li>';
      }).join('');

      var sections = groups.map(function (g) {
        return '<h4 class="ar-h">' + esc(g.name) + '</h4>' +
          data.checks.filter(function (c) { return c.group === g.id; }).map(row).join('');
      }).join('');

      var note = sample
        ? 'This is a sample result, shown because the checking service cannot be reached from this preview. On the live site the check reads your real page.'
        : 'Checked live against ' + esc(data.auditedUrl || data.host) +
          (data.cached ? ' (result saved within the last 24 hours)' : '') +
          '. This looks at one page. It does not test what AI assistants actually say about you; that is part of the full report.';

      results.style.display = 'block';
      results.innerHTML =
        '<div class="panel ar">' +
          '<div class="ar-top">' +
            '<div class="score-ring" style="background:conic-gradient(var(--green) 0turn ' + turn + 'turn, var(--line) ' + turn + 'turn 1turn)">' +
              '<div><div class="score-num">' + data.score + '</div><div class="score-of">out of 100</div></div></div>' +
            '<div class="ar-summary">' +
              '<h3>' + esc(data.verdict) + '</h3>' +
              '<p>' + data.summary.ok + ' good, ' + data.summary.warn + ' need work and ' + data.summary.bad +
                ' problems across ' + data.summary.total + ' checks.</p>' +
              '<a class="btn btn-primary btn-sm" href="/contact/">Talk through your results</a>' +
            '</div>' +
          '</div>' +
          '<div class="ar-groups">' + bars + '</div>' +
          (fixes ? '<div class="ar-fixes"><h4>Fix these first</h4><ol>' + fixes + '</ol></div>' : '') +
          '<div class="ar-checks">' + sections + '</div>' +
        '</div>' +
        '<p class="ar-note">' + note + '</p>';

      done();
      results.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function sampleReport(site) {
      var host = site.replace(/^https?:\/\//, '').replace(/\/.*$/, '');
      var c = function (group, label, state, detail, fix) {
        return { group: group, label: label, state: state, detail: detail, fix: state === 'ok' ? '' : fix };
      };
      var checks = [
        c('access', 'AI assistants are allowed in', 'ok', 'Your robots.txt does not block any of the AI crawlers we test for.'),
        c('access', 'Your text is readable without JavaScript', 'warn', 'Only 140 words of text are in the page before scripts run.', 'Send the main content from the server so the text is in the page itself.'),
        c('identity', 'Your business is described for machines', 'bad', 'The page does not describe your business in a machine-readable way.', 'Add Organization schema with your name, logo, contact details and profile links.'),
        c('identity', 'You are on sites AI tools already trust', 'warn', 'This page links to 3 of 12 well-known sites.', 'Create or claim profiles on the review and directory sites that fit your business.'),
        c('content', 'The page gets to the point', 'ok', 'The page opens with a clear 42-word statement.'),
        c('content', 'Questions and answers are marked up', 'warn', 'The page has no marked-up questions and answers.', 'Add a short FAQ section and mark it up with FAQ schema.'),
        c('basics', 'Page title and description', 'ok', 'Title 52 characters, description 148 characters. Both are a good length.'),
        c('basics', 'Links to your page show a proper preview', 'warn', '2 of 3 preview details are set.', 'Add Open Graph tags for the title, description and image.')
      ];
      var names = { access: 'Can AI tools reach your site?', identity: 'Do they know who you are?', content: 'Is your content easy to quote?', basics: 'Search basics' };
      var pts = function (x) { return x.state === 'ok' ? 100 : x.state === 'warn' ? 50 : 0; };
      var avg = function (list) { return Math.round(list.reduce(function (t, x) { return t + pts(x); }, 0) / list.length); };
      var groups = Object.keys(names).map(function (id) {
        return { id: id, name: names[id], score: avg(checks.filter(function (x) { return x.group === id; })) };
      });
      var count = function (s) { return checks.filter(function (x) { return x.state === s; }).length; };
      return {
        host: host, score: avg(checks), verdict: 'A solid base, with a few gaps to close',
        summary: { ok: count('ok'), warn: count('warn'), bad: count('bad'), total: checks.length },
        groups: groups, checks: checks,
        topFixes: checks.filter(function (x) { return x.fix; })
          .sort(function (a, b) { return pts(a) - pts(b); }).slice(0, 3)
          .map(function (x) { return { label: x.label, fix: x.fix }; })
      };
    }
  }
})();
