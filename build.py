# -*- coding: utf-8 -*-
"""
SVED Solution — static preview generator.
Stamps a shared shell (header/footer/head) around per-page content so the
preview works over file:// and converts cleanly to a Kadence WordPress build.
"""
import os, re, io

OUT = os.path.dirname(os.path.abspath(__file__))

SITE = "SVED Solution"
DOMAIN = "svedsolution.com"

# --------------------------------------------------------------------------
# Contact details (shared with sister brand Web3Tech Network)
# --------------------------------------------------------------------------
EMAIL = "hello@svedsolution.com"
PHONE_DISPLAY = "+91 78460 45690"
PHONE_RAW = "+917846045690"
WHATSAPP_RAW = "917846045690"
WHATSAPP_DISPLAY = "+91 78460 45690"

OFFICES = [
    ("United Arab Emirates", "HQ",
     "502#, 5th Floor, API World Tower,<br>22 Sheikh Zayed Road, Dubai 27091",
     PHONE_DISPLAY, PHONE_RAW),
    ("India", "Delivery centre",
     "Unit #909, Godrej Genesis Building,<br>Block EP&amp;GP, Sector V, Bidhannagar,<br>Kolkata, West Bengal 700091",
     PHONE_DISPLAY, PHONE_RAW),
    ("United States", "Representative office",
     "Oswego,<br>New York 13126",
     PHONE_DISPLAY, PHONE_RAW),
]

SISTER = ("Web3Tech Network", "https://www.web3technetwork.com",
          "Blockchain, crypto and Web3 SEO &amp; development")

# --------------------------------------------------------------------------
# Navigation
# --------------------------------------------------------------------------
NAV = """
<nav class="nav" id="nav">
  <div class="has-drop">
    <a href="services.html" data-nav="services">Services &#9662;</a>
    <div class="drop">
      <div class="drop-head">AI Search &mdash; primary</div>
      <a href="generative-engine-optimization.html">Generative Engine Optimization</a>
      <a href="services.html#aeo">Answer Engine Optimization</a>
      <a href="services.html#llm-seo">LLM SEO</a>
      <a href="services.html#citation">AI Citation &amp; Entity Building</a>
      <a href="services.html#monitoring">AI Visibility Monitoring</a>
      <a href="services.html#aio">Google AI Overviews</a>
      <div class="drop-head">Core SEO</div>
      <a href="services.html#technical">Technical SEO</a>
      <a href="services.html#semantic">Semantic &amp; On-Page SEO</a>
      <a href="services.html#content">Content Strategy</a>
      <a href="services.html#links">Link Building &amp; Digital PR</a>
      <a href="services.html#ecommerce">Ecommerce SEO</a>
      <a href="services.html#saas">SaaS &amp; B2B SEO</a>
      <a href="services.html#local">Local SEO</a>
      <a href="services.html#migration">Migrations</a>
      <a href="services.html#whitelabel">White-Label SEO</a>
      <a href="services.html#consulting">SEO Consulting</a>
    </div>
  </div>
  <a href="industries.html" data-nav="industries">Industries</a>
  <a href="use-cases.html" data-nav="use-cases">Use Cases</a>
  <a href="why-llm-seo-now.html" data-nav="why">Why LLM SEO Now</a>
  <div class="has-drop">
    <a href="insights.html" data-nav="insights">Insights &#9662;</a>
    <div class="drop" style="min-width:340px">
      <a href="insights.html">Blog</a>
      <a href="videos.html">Videos</a>
      <a href="resources.html">Resources &amp; SOPs</a>
      <a href="case-studies.html">Case Studies</a>
    </div>
  </div>
  <div class="has-drop">
    <a href="about.html" data-nav="about">About &#9662;</a>
    <div class="drop" style="min-width:340px">
      <a href="about.html">Our Story &amp; Core Values</a>
      <a href="about.html#team">Our Team</a>
      <a href="about.html#market">Market Understanding</a>
      <a href="reviews.html">Reviews</a>
    </div>
  </div>
  <a href="ai-visibility-audit.html" class="mobile-only-cta" style="color:var(--green)">Free AI Audit</a>
</nav>
"""

FOOTER = f"""
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-offices">
      {"".join(f'''<div class="foot-office">
        <h5>{country} <span class="faint" style="text-transform:none;letter-spacing:0">&middot; {role}</span></h5>
        <p class="faint" style="font-size:.85rem;line-height:1.6;margin-bottom:8px">{addr}</p>
        <a href="tel:{tel_raw}" style="font-size:.85rem;font-family:var(--font-mono)">{tel}</a>
      </div>''' for country, role, addr, tel, tel_raw in OFFICES)}
      <div class="foot-office">
        <h5>Get in touch</h5>
        <p style="margin-bottom:8px"><a href="mailto:{EMAIL}" style="font-size:.85rem">{EMAIL}</a></p>
        <p style="margin-bottom:8px"><a href="https://api.whatsapp.com/send?phone={WHATSAPP_RAW}" style="font-size:.85rem;font-family:var(--font-mono)">WhatsApp {WHATSAPP_DISPLAY}</a></p>
        <p class="faint" style="font-size:.8rem;margin:0">Reply within 1 business day</p>
      </div>
    </div>
    <div class="foot-grid">
      <div class="foot-about">
        <a href="index.html" class="logo" style="margin-bottom:16px"><span class="logo-mark">SV</span>SVED<span>.</span></a>
        <p>The AI visibility agency. We get brands cited by ChatGPT, Perplexity, Gemini and Google AI Overviews &mdash; and we show you the citation count.</p>
        <p style="margin-top:14px;font-size:.83rem"><span class="faint">Sister brand:</span><br>
          <a href="{SISTER[1]}" rel="noopener">{SISTER[0]}</a> <span class="faint">&mdash; {SISTER[2]}</span></p>
        <div class="socials" style="margin-top:18px">
          <a href="#" aria-label="LinkedIn">in</a>
          <a href="#" aria-label="YouTube">YT</a>
          <a href="#" aria-label="X">X</a>
          <a href="#" aria-label="Telegram">TG</a>
          <a href="#" aria-label="Medium">M</a>
        </div>
      </div>
      <div>
        <h5>AI Search</h5>
        <ul>
          <li><a href="generative-engine-optimization.html">GEO</a></li>
          <li><a href="services.html#aeo">AEO</a></li>
          <li><a href="services.html#llm-seo">LLM SEO</a></li>
          <li><a href="services.html#citation">AI Citations</a></li>
          <li><a href="services.html#monitoring">AI Monitoring</a></li>
          <li><a href="services.html#aio">AI Overviews</a></li>
        </ul>
      </div>
      <div>
        <h5>Core SEO</h5>
        <ul>
          <li><a href="services.html#technical">Technical SEO</a></li>
          <li><a href="services.html#semantic">Semantic SEO</a></li>
          <li><a href="services.html#content">Content</a></li>
          <li><a href="services.html#links">Link Building</a></li>
          <li><a href="services.html#whitelabel">White-Label</a></li>
          <li><a href="services.html#consulting">Consulting</a></li>
        </ul>
      </div>
      <div>
        <h5>Company</h5>
        <ul>
          <li><a href="about.html">About</a></li>
          <li><a href="about.html#team">Team</a></li>
          <li><a href="case-studies.html">Case Studies</a></li>
          <li><a href="reviews.html">Reviews</a></li>
          <li><a href="insights.html">Blog</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div class="news">
        <h5>The AI Visibility Brief</h5>
        <p class="faint" style="font-size:.86rem;margin-bottom:14px">What changed in AI search this week, and what to do about it. Every Tuesday.</p>
        <form onsubmit="return false">
          <input type="email" placeholder="you@company.com" aria-label="Email">
          <button class="btn btn-primary btn-sm" style="width:100%;justify-content:center">Subscribe</button>
        </form>
        <p class="faint" style="font-size:.76rem;margin-top:10px">Free with the AI Search Playbook PDF.</p>
      </div>
    </div>
    <div class="foot-bottom">
      <div>&copy; 2026 SVED Solution. All rights reserved. &middot; <a href="mailto:{EMAIL}" style="color:var(--text-faint)">{EMAIL}</a></div>
      <div style="display:flex;gap:20px;flex-wrap:wrap">
        <a href="#" style="color:var(--text-faint)">Privacy</a>
        <a href="#" style="color:var(--text-faint)">Terms</a>
        <a href="ai-visibility-audit.html" style="color:var(--text-faint)">Free AI Audit</a>
      </div>
    </div>
  </div>
</footer>
"""

SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://svedsolution.com/{slug}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://svedsolution.com/{slug}">
<meta name="theme-color" content="#0B1219">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
<script type="application/ld+json">{schema}</script>
</head>
<body>
<div class="preview-note">PREVIEW BUILD &mdash; svedsolution.com first draft &middot; content and figures are anonymised client data &middot; not live</div>
<header class="site-header">
  <div class="wrap header-inner">
    <a href="index.html" class="logo"><span class="logo-mark">SV</span>SVED<span>.</span></a>
    {nav}
    <div class="header-cta">
      <a href="ai-visibility-audit.html" class="btn btn-ghost btn-sm">Free AI Audit</a>
      <a href="contact.html" class="btn btn-primary btn-sm">Book a call</a>
      <button class="nav-toggle" id="navToggle" aria-label="Menu" aria-expanded="false">&#9776;</button>
    </div>
  </div>
</header>
<main>
{body}
</main>
{footer}
<script src="assets/app.js"></script>
</body>
</html>
"""

ORG_SCHEMA = """{
  "@context":"https://schema.org",
  "@type":"ProfessionalService",
  "@id":"https://svedsolution.com/#organization",
  "name":"SVED Solution",
  "alternateName":"SVED",
  "url":"https://svedsolution.com/",
  "email":"hello@svedsolution.com",
  "description":"AI visibility and 360 SEO agency specialising in Generative Engine Optimization (GEO), Answer Engine Optimization (AEO) and LLM SEO.",
  "slogan":"The AI Visibility Agency",
  "areaServed":["US","GB","CA","AU","IN","AE"],
  "knowsAbout":["Generative Engine Optimization","Answer Engine Optimization","LLM SEO","Technical SEO","Semantic SEO","Entity SEO","AI Overviews"],
  "address":[
    {"@type":"PostalAddress","streetAddress":"502, 5th Floor, API World Tower, 22 Sheikh Zayed Road","addressLocality":"Dubai","postalCode":"27091","addressCountry":"AE"},
    {"@type":"PostalAddress","streetAddress":"Unit 909, Godrej Genesis Building, Block EP&GP, Sector V, Bidhannagar","addressLocality":"Kolkata","addressRegion":"West Bengal","postalCode":"700091","addressCountry":"IN"},
    {"@type":"PostalAddress","addressLocality":"Oswego","addressRegion":"NY","postalCode":"13126","addressCountry":"US"}
  ],
  "telephone":"+917846045690",
  "contactPoint":[
    {"@type":"ContactPoint","telephone":"+917846045690","email":"hello@svedsolution.com","contactType":"sales","areaServed":["AE","IN","US","GB"],"availableLanguage":["English","Hindi","Bengali"]}
  ],
  "sameAs":["https://www.linkedin.com/company/svedsolution","https://www.youtube.com/@svedsolution"],
  "parentOrganization":{"@type":"Organization","name":"Web3Tech Network","url":"https://www.web3technetwork.com"}
}"""


def cta(title, sub, primary=("Run a free AI visibility audit", "ai-visibility-audit.html"),
        secondary=("Book a strategy call", "contact.html")):
    return f"""
<section class="sec">
  <div class="wrap">
    <div class="cta-band">
      <div class="eyebrow" style="justify-content:center">Next step</div>
      <h2>{title}</h2>
      <p>{sub}</p>
      <div class="btn-row" style="justify-content:center">
        <a class="btn btn-primary btn-lg" href="{primary[1]}">{primary[0]}</a>
        <a class="btn btn-ghost btn-lg" href="{secondary[1]}">{secondary[0]}</a>
      </div>
    </div>
  </div>
</section>"""


def phero(crumbs, eyebrow, h1, sub):
    return f"""
<section class="phero">
  <div class="wrap">
    <div class="crumbs">{crumbs}</div>
    <div class="eyebrow">{eyebrow}</div>
    <h1 style="max-width:19ch">{h1}</h1>
    <p class="lead dim" style="max-width:66ch;margin-top:1.2rem">{sub}</p>
  </div>
</section>"""


def faq(items):
    rows = "".join(
        f'<details><summary>{q}</summary><div class="ans">{a}</div></details>' for q, a in items
    )
    return f"""
<section class="sec band-alt">
  <div class="wrap wrap-narrow">
    <div class="eyebrow">FAQ</div>
    <h2 style="margin-bottom:2rem">Questions we get asked</h2>
    <div class="faq">{rows}</div>
  </div>
</section>"""


PAGES = {}

# ==========================================================================
# HOME
# ==========================================================================
PAGES["index"] = dict(
    title="SVED Solution | AI Visibility & 360&deg; SEO, GEO and AEO Agency",
    desc="We get your brand cited by ChatGPT, Perplexity, Gemini and Google AI Overviews. GEO, AEO, LLM SEO and full-stack technical SEO. Run a free AI visibility audit.",
    slug="",
    body=f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <div class="badge"><span class="dot"></span> Now booking Q4 2026 &mdash; 3 GEO retainers open</div>
      <h1>Google ranks pages.<br>AI <span class="hl">recommends brands</span>.</h1>
      <p class="hero-sub">SVED Solution is a 360&deg; SEO agency built for the answer engine era. We make your brand the one ChatGPT, Perplexity, Gemini and Google AI Overviews name &mdash; then we show you the citation count.</p>
      <div class="btn-row">
        <a class="btn btn-primary btn-lg" href="ai-visibility-audit.html">Run a free AI visibility audit</a>
        <a class="btn btn-ghost btn-lg" href="why-llm-seo-now.html">Why LLM SEO, now</a>
      </div>
      <p class="faint" style="font-size:.85rem;margin-top:20px">No card. No call required. 12 eligibility checks in about 60 seconds.</p>
    </div>
    <div>
      <div class="panel">
        <div class="panel-bar"><i class="tdot"></i><i class="tdot"></i><i class="tdot"></i>
          <span style="margin-left:8px">ai-citations &mdash; client-a &middot; 29 days</span></div>
        <div class="panel-body">
          <div class="crow"><span class="lbl">Total AI citations</span><span class="val"><span data-count="2923">0</span></span></div>
          <div class="crow"><span class="lbl">Distinct pages cited</span><span class="val"><span data-count="131">0</span></span></div>
          <div class="crow"><span class="lbl">Avg citations / day</span><span class="val"><span data-count="101">0</span></span></div>
          <div class="crow"><span class="lbl">Peak pages in one day</span><span class="val">32</span></div>
          <div class="crow"><span class="lbl">Top cited URL</span><span class="pill pill-ok">307 citations</span></div>
          <div class="crow"><span class="lbl">Reporting window</span><span class="val">Apr 2026</span></div>
        </div>
      </div>
      <p class="faint" style="font-size:.79rem;margin-top:12px;text-align:center">Anonymised client data. Real export, real numbers.</p>
    </div>
  </div>
</section>

<section class="sec-sm band-alt">
  <div class="wrap">
    <p class="faint center mono" style="font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;margin-bottom:24px">We optimise for every surface that answers a question</p>
    <div class="strip">
      <span>ChatGPT</span><span>Perplexity</span><span>Google AI Overviews</span><span>Gemini</span>
      <span>Claude</span><span>Copilot</span><span>Google Search</span><span>Bing</span>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">The shift</div>
      <h2>There is no &ldquo;#1 position&rdquo; in an AI answer.</h2>
      <p class="lead dim">There is only which brands get cited, which get named, and which get treated as the trusted answer. If your brand is not seen consistently across trusted sources, AI will not recommend you &mdash; no matter how good your traditional SEO is.</p>
    </div>
    <div class="grid g4">
      <div class="card"><span class="card-num">PILLAR 01</span><h3>Entity authority</h3><p>AI models do not trust webpages. They trust entities. We build the brand, founder and category associations that make you a resolvable entity.</p></div>
      <div class="card"><span class="card-num">PILLAR 02</span><h3>Answer structure</h3><p>AI does not retrieve blog posts, it retrieves answers. We restructure content into RAG-friendly blocks: direct answer, evidence, entities, timestamp.</p></div>
      <div class="card"><span class="card-num">PILLAR 03</span><h3>Citation footprint</h3><p>Where 95&#37; of brands fail. G2, Capterra, Trustpilot, Crunchbase, Product Hunt, Reddit, Quora &mdash; AI believes these more than your own site.</p></div>
      <div class="card"><span class="card-num">PILLAR 04</span><h3>The refresh loop</h3><p>Publishing once is useless. Every 30 days we update stats, add FAQs, rebuild internal links and re-syndicate. Fresh pages win retrieval.</p></div>
    </div>
  </div>
</section>

<section class="sec band-dark">
  <div class="wrap">
    <div class="sec-head center">
      <div class="eyebrow">Proof, not promises</div>
      <h2>One client. One month. Measured.</h2>
      <p class="lead dim">Every engagement reports AI citations the same way we report clicks and revenue &mdash; because if you cannot measure it, you are guessing.</p>
    </div>
    <div class="kpis">
      <div class="kpi"><div class="kpi-val"><span data-count="2923">0</span></div><div class="kpi-lab">AI citations in 29 days</div></div>
      <div class="kpi"><div class="kpi-val"><span data-count="131">0</span></div><div class="kpi-lab">Distinct pages cited</div></div>
      <div class="kpi"><div class="kpi-val"><span data-count="307">0</span></div><div class="kpi-lab">Citations on the top page</div></div>
      <div class="kpi"><div class="kpi-val"><span data-count="39">0</span></div><div class="kpi-lab">Documented delivery SOPs</div></div>
    </div>
    <p class="faint center" style="font-size:.82rem;margin-top:20px">Anonymised. Ecommerce retailer, UK. Full export available on request under NDA.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">Services</div>
      <h2>AI search first. Full-stack SEO underneath.</h2>
      <p class="lead dim">GEO without technical foundations is theatre. We run both, from one team, on one roadmap.</p>
    </div>
    <div class="grid g3" style="margin-bottom:20px">
      <a class="card card-link" href="generative-engine-optimization.html"><div class="card-icon">&#9670;</div><h3>Generative Engine Optimization</h3><p>Get named in ChatGPT, Perplexity and Gemini answers. Entity building, citation stacking, answer-block content.</p><span class="card-more">Explore GEO &rarr;</span></a>
      <a class="card card-link" href="services.html#aeo"><div class="card-icon">&#9635;</div><h3>Answer Engine Optimization</h3><p>Own the direct answer. FAQ architecture, schema, snippet capture and zero-click defence.</p><span class="card-more">Explore AEO &rarr;</span></a>
      <a class="card card-link" href="services.html#llm-seo"><div class="card-icon">&#10022;</div><h3>LLM SEO</h3><p>Page and template structure engineered so language models can parse, quote and attribute your content.</p><span class="card-more">Explore LLM SEO &rarr;</span></a>
      <a class="card card-link" href="services.html#technical"><div class="card-icon">&#9881;</div><h3>Technical SEO</h3><p>Crawl budget, index bloat, Core Web Vitals, rendering, migrations. The foundation everything else sits on.</p><span class="card-more">Explore technical &rarr;</span></a>
      <a class="card card-link" href="services.html#semantic"><div class="card-icon">&#9678;</div><h3>Semantic &amp; On-Page SEO</h3><p>Concept coverage over keyword density. Entity mapping, topical depth, internal link architecture.</p><span class="card-more">Explore semantic &rarr;</span></a>
      <a class="card card-link" href="services.html"><div class="card-icon">&#8862;</div><h3>All 16 services</h3><p>Content, digital PR, ecommerce, SaaS, local, international, programmatic, migrations, white-label and consulting.</p><span class="card-more">See everything &rarr;</span></a>
    </div>
  </div>
</section>

<section class="sec band-alt">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">Honest timeline</div>
      <h2>What actually happens, and when.</h2>
      <p class="lead dim">Anyone promising AI citations in week two is selling you something. This is the real curve.</p>
    </div>
    <div class="grid g2" style="gap:48px">
      <div class="tl">
        <div class="tl-item"><div class="tl-when">Days 30&ndash;45</div><h4>Brand and entity indexing</h4><p>Schema, entity consistency, founder association and Tier-1 profiles land. Models start resolving who you are.</p></div>
        <div class="tl-item"><div class="tl-when">Day 60</div><h4>First AI citations appear</h4><p>Your pages begin surfacing as sources in Perplexity and ChatGPT for long-tail category questions.</p></div>
        <div class="tl-item"><div class="tl-when">Day 90</div><h4>Consistent brand mentions</h4><p>Named in answers rather than just cited as a link. Repeat appearances across multiple prompt families.</p></div>
      </div>
      <div class="tl">
        <div class="tl-item"><div class="tl-when">Months 4&ndash;6</div><h4>Stable visibility</h4><p>Citation counts hold week to week instead of spiking. Traditional rankings compound alongside.</p></div>
        <div class="tl-item"><div class="tl-when">Months 9&ndash;12</div><h4>Category authority</h4><p>You become one of the default brands models reach for in your category. This is the defensible position.</p></div>
        <div class="tl-item"><div class="tl-when">Ongoing</div><h4>The 30-day refresh loop</h4><p>Stats updated, FAQs added, internal links rebuilt, content re-syndicated. Stagnant pages lose retrieval priority.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head center">
      <div class="eyebrow">How we work</div>
      <h2>Diagnosis first. Always.</h2>
    </div>
    <div class="grid g4">
      <div class="card"><span class="card-num">01</span><h3>Audit</h3><p>12-point AI eligibility check, technical crawl, competitor citation reverse-engineering and an ICP interview.</p></div>
      <div class="card"><span class="card-num">02</span><h3>Map</h3><p>Entity map, semantic topic model, citation-source shortlist and a prioritised 90-day roadmap with named owners.</p></div>
      <div class="card"><span class="card-num">03</span><h3>Ship</h3><p>We implement. Schema, content, internal links, technical fixes and citation placements &mdash; not a slide deck of suggestions.</p></div>
      <div class="card"><span class="card-num">04</span><h3>Refresh</h3><p>Monthly narrative reporting on citations, clicks and revenue. Then the 30-day loop runs again.</p></div>
    </div>
  </div>
</section>

<section class="sec band-dark">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">Reviews</div>
      <h2>What clients say</h2>
    </div>
    <div class="grid g3">
      <div class="quote"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>&ldquo;We had no idea we were invisible in ChatGPT until the audit. Ninety days later we are the brand it names for our category question.&rdquo;</p><div class="who">Head of Growth &middot; B2B SaaS &middot; United States</div></div>
      <div class="quote"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>&ldquo;First agency that reported AI citations as a number instead of hand-waving about the future of search. The monthly narrative is the best reporting we have had.&rdquo;</p><div class="who">Ecommerce Director &middot; Retail &middot; United Kingdom</div></div>
      <div class="quote"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>&ldquo;They fixed the crawl and index problems our previous agency spent a year describing. Then the content actually started ranking.&rdquo;</p><div class="who">Marketing Lead &middot; Healthcare &middot; United States</div></div>
    </div>
    <div class="center" style="margin-top:32px"><a class="btn btn-ghost" href="reviews.html">Read all reviews</a></div>
  </div>
</section>

{faq([
  ("Is GEO actually different from SEO, or is it a rebrand?",
   "Different mechanism, shared foundations. SEO optimises for a ranked list of ten blue links. GEO optimises for whether a language model retrieves, trusts and names your brand inside a generated answer. The overlap is technical health and content quality. The divergence is entity authority and off-site citation consensus, which classic SEO barely touches. We run both because GEO on a broken site does not work."),
  ("How do you measure AI visibility when the tools are unreliable?",
   "Two ways. Automated citation tracking gives volume and page-level attribution &mdash; the export on this page is real client data. Alongside that we run controlled weekly prompt testing across ChatGPT, Perplexity and Gemini using a fixed prompt set for your category, logging brand mentions, cited sources and frequency. Manual testing catches what trackers miss."),
  ("How long until we see results?",
   "Entity indexing at 30 to 45 days, first citations around day 60, consistent mentions by day 90, stable visibility at 4 to 6 months and category authority at 9 to 12. Traditional ranking improvements often arrive faster, particularly on pages already sitting in positions 8 to 20 where we can move them with on-page and internal linking work alone."),
  ("Do you work with agencies?",
   "Yes. White-label delivery under NDA with branded reporting, from single audits to full retained delivery. We stay invisible to your client."),
  ("What does an engagement cost?",
   "Consulting is $30 per hour for one-off sessions. Retainers are scoped after the audit, because quoting before diagnosis is guesswork. Most engagements sit between a focused GEO sprint and a full-stack monthly retainer."),
])}

{cta("Find out if AI can even see you.",
     "Twelve eligibility checks across schema, entity signals, answer structure, AI crawler access and your Tier-1 citation footprint. No card, no call.")}
""")

# ==========================================================================
# AUDIT TOOL
# ==========================================================================
PAGES["ai-visibility-audit"] = dict(
    title="Free AI Visibility Audit | AEO, GEO &amp; LLM Eligibility Check",
    desc="Run a free 12-point AI visibility audit. Check schema, llms.txt, AI crawler access, answer structure and citation footprint. Instant score, no card required.",
    slug="ai-visibility-audit/",
    body=f"""
<section class="phero">
  <div class="wrap">
    <div class="crumbs"><a href="index.html">Home</a> / Free AI Visibility Audit</div>
    <div class="eyebrow">Free tool &middot; no card &middot; no call</div>
    <h1 style="max-width:17ch">Can AI actually see your brand?</h1>
    <p class="lead dim" style="max-width:64ch;margin-top:1.2rem">Twelve eligibility checks that determine whether ChatGPT, Perplexity, Gemini and Google AI Overviews can retrieve, trust and cite your site. Results in about 60 seconds.</p>

    <div style="max-width:720px;margin-top:36px">
      <form id="audit-form" class="audit-form">
        <input type="url" id="audit-url" placeholder="https://yourdomain.com" required aria-label="Website URL">
        <button class="btn btn-primary btn-lg" id="audit-run" type="submit">Run free audit</button>
      </form>
      <p class="faint" style="font-size:.82rem;margin-top:12px">We crawl public pages only. Nothing is stored unless you ask for the full report.</p>
      <div id="audit-stage" class="mono" style="display:none;font-size:.82rem;line-height:2;margin-top:24px;color:var(--text-dim)"></div>
      <div id="audit-results" style="display:none"></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">What we check</div>
      <h2>The 12 AI eligibility checks</h2>
      <p class="lead dim">Each one is a documented reason a language model either retrieves your page or skips it. Most sites fail at least six.</p>
    </div>
    <div class="grid g3">
      <div class="card"><span class="card-num">CHECK 01</span><h3>Organization schema</h3><p>Whether you exist as a resolvable entity with sameAs links, not just a website with a logo.</p></div>
      <div class="card"><span class="card-num">CHECK 02</span><h3>Person / author schema</h3><p>Named authorship linked to real profiles. The single strongest E-E-A-T signal AI systems weigh.</p></div>
      <div class="card"><span class="card-num">CHECK 03</span><h3>FAQPage schema</h3><p>Question-and-answer markup is the highest-frequency format cited by generative engines.</p></div>
      <div class="card"><span class="card-num">CHECK 04</span><h3>llms.txt</h3><p>The emerging standard for declaring your content, structure and licence to LLM crawlers.</p></div>
      <div class="card"><span class="card-num">CHECK 05</span><h3>AI crawler access</h3><p>GPTBot, PerplexityBot, ClaudeBot, Google-Extended, CCBot. Blocked or undeclared bots cannot cite you.</p></div>
      <div class="card"><span class="card-num">CHECK 06</span><h3>Answer-first structure</h3><p>Does each page open with a direct answer in the first 100 words, or with a story intro nobody retrieves?</p></div>
      <div class="card"><span class="card-num">CHECK 07</span><h3>Freshness signals</h3><p>Last-modified dates and update cadence. Retrieval strongly favours recently maintained pages.</p></div>
      <div class="card"><span class="card-num">CHECK 08</span><h3>Heading hierarchy</h3><p>Clean H1 to H3 nesting so chunking and passage extraction work the way models expect.</p></div>
      <div class="card"><span class="card-num">CHECK 09</span><h3>Citation-ready formats</h3><p>Lists, tables, comparison matrices and step frameworks. Long essay prose does not get quoted.</p></div>
      <div class="card"><span class="card-num">CHECK 10</span><h3>Core Web Vitals</h3><p>LCP, INP and CLS on mobile. Slow renders reduce crawl depth and hurt every downstream signal.</p></div>
      <div class="card"><span class="card-num">CHECK 11</span><h3>Entity consistency</h3><p>Is your brand described identically across your site, socials and third-party profiles? Inconsistency breaks trust loops.</p></div>
      <div class="card"><span class="card-num">CHECK 12</span><h3>Tier-1 citation footprint</h3><p>Presence on G2, Capterra, Trustpilot, Crunchbase, Product Hunt, Reddit and Quora. AI believes these more than your site.</p></div>
    </div>
  </div>
</section>

<section class="sec band-green">
  <div class="wrap">
    <div class="grid g2" style="gap:52px;align-items:center">
      <div>
        <div class="eyebrow">Go deeper</div>
        <h2>The full AI Visibility Report</h2>
        <p class="lead dim">The free audit tells you whether you are eligible. The full report tells you whether you are actually being cited &mdash; and by whom.</p>
        <ul style="list-style:none;padding:0;margin:1.6rem 0">
          <li style="padding:11px 0;border-bottom:1px solid var(--line)"><span class="green mono">&#10003;</span> &nbsp;Live prompt testing across ChatGPT, Perplexity and Gemini</li>
          <li style="padding:11px 0;border-bottom:1px solid var(--line)"><span class="green mono">&#10003;</span> &nbsp;25-cell citation matrix: 5 category prompts &times; 5 engines</li>
          <li style="padding:11px 0;border-bottom:1px solid var(--line)"><span class="green mono">&#10003;</span> &nbsp;Competitor citation reverse-engineering &mdash; every domain AI cites instead of you</li>
          <li style="padding:11px 0;border-bottom:1px solid var(--line)"><span class="green mono">&#10003;</span> &nbsp;Prioritised 90-day fix plan with effort and impact scoring</li>
          <li style="padding:11px 0"><span class="green mono">&#10003;</span> &nbsp;Loom walkthrough from the strategist who ran it</li>
        </ul>
        <a class="btn btn-primary btn-lg" href="contact.html">Request the full report</a>
      </div>
      <div class="panel">
        <div class="panel-bar"><i class="tdot"></i><i class="tdot"></i><i class="tdot"></i><span style="margin-left:8px">citation-matrix.csv</span></div>
        <div class="panel-body" style="font-size:.78rem">
          <div class="crow"><span class="lbl">&ldquo;best [category] for [ICP]&rdquo;</span><span class="pill pill-bad">not cited</span></div>
          <div class="crow"><span class="lbl">&ldquo;top tools for [problem]&rdquo;</span><span class="pill pill-warn">cited #7</span></div>
          <div class="crow"><span class="lbl">&ldquo;who recommends [solution]&rdquo;</span><span class="pill pill-bad">not cited</span></div>
          <div class="crow"><span class="lbl">&ldquo;best brands in [category]&rdquo;</span><span class="pill pill-warn">cited #4</span></div>
          <div class="crow"><span class="lbl">&ldquo;[competitor] alternatives&rdquo;</span><span class="pill pill-ok">cited #2</span></div>
          <div class="crow"><span class="lbl">Competitor cited instead</span><span class="val">14 domains</span></div>
        </div>
      </div>
    </div>
  </div>
</section>

{faq([
  ("Is this really free?",
   "The 12-point eligibility audit is free and needs no card. It runs a live crawl of your public pages and returns a score with a specific reason for each check. The full report &mdash; which includes live prompt testing across ChatGPT, Perplexity and Gemini &mdash; is gated because it costs us API credits and strategist time to run."),
  ("What is llms.txt and do I need one?",
   "It is a plain-text file at your domain root that tells language-model crawlers what your site contains, how it is structured and how you want it used &mdash; conceptually similar to robots.txt but written for retrieval rather than indexing. Adoption is still early, so it is not yet a ranking factor. It costs almost nothing to add and it removes ambiguity, which is why we include it in every build."),
  ("Should I block AI crawlers to protect my content?",
   "That is a strategy decision, not a technical one. Blocking GPTBot, ClaudeBot and PerplexityBot protects your content from training and retrieval &mdash; and guarantees you are never cited. If your business depends on brand discovery, blocking is self-harm. If you are a publisher monetising pageviews, the calculation is genuinely different. We will tell you which side you are on."),
  ("Does the audit store my data?",
   "No. The free audit runs the crawl and returns the result. Nothing is retained unless you request the full report and give us an email."),
])}

{cta("Twelve checks. Sixty seconds. One honest answer.",
     "Most sites fail six or more. Knowing which six is the entire starting point.",
     primary=("Scroll up and run the audit", "#audit-form"),
     secondary=("Talk to a strategist", "contact.html"))}
""")

# ==========================================================================
# WHY LLM SEO NOW
# ==========================================================================
PAGES["why-llm-seo-now"] = dict(
    title="Why You Need LLM SEO Services Now | SVED Solution",
    desc="AI search is reallocating discovery right now. Why LLM SEO, GEO and AEO cannot wait, what the window looks like, and what it costs to be late.",
    slug="why-llm-seo-now/",
    body=f"""
{phero('<a href="index.html">Home</a> / Why LLM SEO Now',
       'The argument',
       'The window is open. It closes on the people who wait.',
       'Every category eventually gets a default set of brands that AI models reach for. Those defaults are being set now, cheaply, by whoever shows up first. In eighteen months the same position costs ten times more &mdash; if it is available at all.')}

<section class="sec">
  <div class="wrap wrap-narrow prose">

    <div class="answer-block">
      <div class="q">The short answer</div>
      <p>You need LLM SEO now because AI answer engines are currently deciding which brands become their default recommendations per category, and those decisions compound. Entity authority and citation consensus take 90 days minimum to build and roughly 9 to 12 months to become defensible. A brand that starts today is established before the category saturates. A brand that starts in eighteen months is competing against incumbents that AI already trusts.</p>
    </div>

    <h2>1. The competition is underbuilt right now</h2>
    <p>This is the part nobody says out loud. Look at the actual search landscape for the terms that define this category:</p>
    <div class="tbl-wrap" style="margin:1.6rem 0">
      <table>
        <tr><th>Query</th><th>Monthly volume</th><th>Difficulty</th><th>State of the results</th></tr>
        <tr><td><strong>generative engine optimization</strong></td><td>12,000</td><td>KD 62</td><td>Every top-10 result has a URL Rating of 9 or below. Large brands rushed thin pages out.</td></tr>
        <tr><td><strong>answer engine optimization</strong></td><td>3,700</td><td>KD 45</td><td>Softer than the GEO result set. Reddit ranks second.</td></tr>
        <tr><td><strong>geo vs seo</strong></td><td>2,600</td><td>KD 12</td><td>Entire top 10 sits at UR 4&ndash;5. Genuinely open.</td></tr>
        <tr><td><strong>llm seo</strong></td><td>1,400</td><td>KD 14</td><td>Reddit second. Defensible by any real practitioner with a case study.</td></tr>
      </table>
    </div>
    <p>A 12,000-a-month commercial query where nothing above position two has meaningful page authority is not a normal market condition. It is a temporary one. Big brands publish placeholder pages first and build them properly second &mdash; and when they do, the window shuts.</p>

    <h2>2. AI does not rank pages. It recommends brands.</h2>
    <p>This is the structural change and it is why waiting is more expensive here than in classic SEO. In a ranked list, a new page can displace an old one on the strength of that page alone. In a generated answer, the model is not comparing pages &mdash; it is recalling which brands it associates with the question. That association is built from repeated, consistent mentions across sources the model already trusts.</p>
    <p><strong>You cannot buy your way past that in a quarter.</strong> Entity authority is a slow-accruing asset, which is exactly why it is a defensible one once you have it.</p>

    <h2>3. Zero-click is not coming. It arrived.</h2>
    <p>AI Overviews now sit above the organic results for a large share of informational queries. The click you used to earn at position three is increasingly absorbed into a summary that names two or three brands. If you are not one of the named brands, your position-three ranking is worth materially less than it was, and the traffic report will show it as a CTR decline you cannot fix with a better title tag.</p>
    <p>The defensive move and the offensive move are the same move: be the brand inside the answer.</p>

    <h2>4. The cost of being late, concretely</h2>
    <ul>
      <li><strong>Months 1&ndash;3 today</strong> buys entity indexing and first citations while your category is uncontested.</li>
      <li><strong>Months 1&ndash;3 in two years</strong> buys the same technical work, but now you are trying to displace brands the models have cited thousands of times. Displacement costs several multiples of establishment.</li>
      <li><strong>The compounding gap</strong> is the real cost. Every month a competitor is cited and you are not, the consensus signal strengthens in their favour and weakens the relative weight of yours.</li>
    </ul>

    <h2>5. What it does not mean</h2>
    <p>It does not mean abandoning traditional SEO. Nearly every GEO signal &mdash; crawlability, structure, schema, authority, freshness &mdash; is a classic SEO signal applied to a different retrieval system. A site with broken crawl budget and no technical foundation cannot win either game. Anyone selling you GEO without touching your technical health is selling you a report.</p>
    <p>It also does not mean instant results. If someone promises AI citations within two weeks, ask them for the export. We publish our timeline precisely because the honest version is the one that survives contact with reality.</p>

    <h2>The realistic timeline, again</h2>
    <div class="tl" style="margin-top:1.6rem">
      <div class="tl-item"><div class="tl-when">Days 30&ndash;45</div><h4>Brand and entity indexing</h4><p>Models can resolve who you are, what category you are in and who runs you.</p></div>
      <div class="tl-item"><div class="tl-when">Day 60</div><h4>First citations</h4><p>Long-tail category questions start returning your pages as sources.</p></div>
      <div class="tl-item"><div class="tl-when">Day 90</div><h4>Consistent mentions</h4><p>Named in answers, not just linked. Repeat appearances across prompt families.</p></div>
      <div class="tl-item"><div class="tl-when">Months 4&ndash;6</div><h4>Stable visibility</h4><p>Week-to-week consistency instead of spikes.</p></div>
      <div class="tl-item"><div class="tl-when">Months 9&ndash;12</div><h4>Category authority</h4><p>A default brand for your category. This is the position that is expensive to take and cheap to hold.</p></div>
    </div>
  </div>
</section>

{faq([
  ("Is GEO a fad that will disappear when the hype dies?",
   "The label might change. The mechanism will not. As long as a system generates an answer rather than returning a list, something has to decide which brands and sources that answer draws on &mdash; and influencing that decision is a marketing discipline. Whether it is called GEO, AEO, LLM SEO or absorbed back into SEO is a naming question, not a strategic one."),
  ("We already rank #1 on Google. Do we still need this?",
   "Ranking first is a strong starting position and it is not sufficient. AI systems weight off-site consensus and entity authority heavily, so a site can hold position one and still be absent from the generated answer above it &mdash; which is now the thing users read first. If you rank first and are not cited, you are funding the visibility of whoever is."),
  ("Can we do this in-house?",
   "Partly, and you should. Schema, answer-block structure and freshness are internal work once someone has defined the standard. The pieces that are hard in-house are the citation footprint, competitor citation reverse-engineering and controlled prompt testing at cadence, because they need external relationships and disciplined weekly measurement. We are happy to set the standard and hand it over."),
])}

{cta("See exactly where you stand today.",
     "The free audit takes a minute and tells you which of the twelve eligibility signals you are currently failing.")}
""")

# ==========================================================================
# GEO — flagship service page
# ==========================================================================
PAGES["generative-engine-optimization"] = dict(
    title="Generative Engine Optimization (GEO) Services | SVED Solution",
    desc="GEO services that get your brand cited by ChatGPT, Perplexity and Gemini. Entity authority, citation stacking, answer-block content and measured AI visibility.",
    slug="services/generative-engine-optimization/",
    body=f"""
{phero('<a href="index.html">Home</a> / <a href="services.html">Services</a> / Generative Engine Optimization',
       'AI Search &middot; primary service',
       'Generative Engine Optimization',
       'We make your brand one of the names ChatGPT, Perplexity and Gemini reach for &mdash; through entity authority, citation consensus and content structured the way retrieval actually works.')}

<section class="sec">
  <div class="wrap">
    <div class="grid g2" style="gap:56px;align-items:start">
      <div class="prose">
        <div class="answer-block" style="margin-top:0">
          <div class="q">What is generative engine optimization?</div>
          <p>Generative Engine Optimization is the practice of making a brand retrievable, trustworthy and citable to AI systems that generate answers rather than return ranked links. Unlike SEO, which competes for a position in a list, GEO competes to be the brand a model names inside its answer. It works through four levers: entity authority, off-site citation consensus, retrieval-friendly content structure and a sustained refresh cadence.</p>
        </div>

        <h2>Why most GEO work fails</h2>
        <p>Because it is treated as an on-page exercise. Teams add FAQ schema, restructure a few headings, and wait. Nothing happens, because the model was never uncertain about your page &mdash; it was uncertain about your <strong>brand</strong>.</p>
        <p>AI systems do not trust webpages. They trust entities: recognisable brands and people with a clear niche identity, high-authority mentions, repeated citations and consistent descriptions across sources. If your brand is not seen across multiple trusted sites, no amount of on-page work will get you recommended.</p>

        <h2>The four pillars we build</h2>
        <h3>Pillar 1 &mdash; Entity authority</h3>
        <p>We make your brand resolvable. Exact name consistency everywhere, defined business categories, founder and CEO entity association, one authoritative About page, and Organization plus Person schema wired to real profiles. Then we build the entity cluster: the set of independent sources that all describe you the same way. That consistency is what creates the trust loop.</p>

        <h3>Pillar 2 &mdash; The citation stack</h3>
        <p>This is where 95&#37; of brands fail, and it is the highest-leverage work we do. AI weights third-party validation above your own site.</p>
        <ul>
          <li><strong>Tier 1 (mandatory):</strong> G2, Capterra, Trustpilot, Crunchbase, Product Hunt, Reddit, Quora.</li>
          <li><strong>Tier 2 (amplifiers):</strong> founder guest posts, industry blogs, podcast show notes, LinkedIn newsletters, community mentions.</li>
        </ul>
        <p>When a model sees the same brand confirmed across trusted, independent sources, it reads that repetition as authority consensus. That is the signal we are manufacturing, legitimately, at cadence.</p>

        <h3>Pillar 3 &mdash; Retrieval-ready content</h3>
        <p>AI does not retrieve blog posts. It retrieves answers. Every page we build or rewrite follows the same structure: a one-sentence problem statement, a straight answer paragraph, bullet explanations, examples with real data, entity references, and a visible last-modified date.</p>
        <p>What we stop writing: long essay-style content, keyword-stuffed copy, story intros and opinion without evidence. What we write instead: lists, tables, comparison matrices, step frameworks and FAQs with real paragraph answers. Density, structure, clarity.</p>

        <h3>Pillar 4 &mdash; The 30-day refresh loop</h3>
        <p>Publishing once is useless. Retrieval favours recently updated pages with current facts. Every thirty days we update statistics, add new FAQs, expand clarification bullets, rebuild internal links and re-share across three platforms.</p>

        <h2>Competitor citation reverse-engineering</h2>
        <p>Your unfair advantage, and the first thing we run. Instead of guessing, we take the brands already appearing in AI answers for your category, export every domain cited alongside them, and analyse where they are mentioned, which pages the models pull from and what anchor wording is used. Then we replicate the placements, publish better authority content and out-network them on the same platforms. Faster indexing, higher citation likelihood, far less trial and error.</p>

        <h2>How we measure it</h2>
        <p>Two tracks, reported monthly. <strong>Automated citation tracking</strong> gives volume and page-level attribution. <strong>Controlled prompt testing</strong> runs a fixed prompt set for your category weekly across ChatGPT, Perplexity and Gemini, logging brand mentions, cited sources and frequency. Most AI trackers are unreliable on their own; the manual layer is what makes the number trustworthy.</p>
      </div>

      <aside style="position:sticky;top:96px">
        <div class="panel" style="margin-bottom:20px">
          <div class="panel-bar"><i class="tdot"></i><i class="tdot"></i><i class="tdot"></i><span style="margin-left:8px">client-a &middot; 29 days</span></div>
          <div class="panel-body">
            <div class="crow"><span class="lbl">AI citations</span><span class="val">2,923</span></div>
            <div class="crow"><span class="lbl">Pages cited</span><span class="val">131</span></div>
            <div class="crow"><span class="lbl">Top page</span><span class="val">307</span></div>
            <div class="crow"><span class="lbl">Avg / day</span><span class="val">101</span></div>
          </div>
        </div>
        <div class="card">
          <h4 style="margin-bottom:14px">What a GEO engagement includes</h4>
          <ul style="list-style:none;padding:0;margin:0;font-size:.9rem">
            <li style="padding:8px 0;border-bottom:1px solid var(--line-soft)">Entity map + schema build</li>
            <li style="padding:8px 0;border-bottom:1px solid var(--line-soft)">Tier-1 citation placement</li>
            <li style="padding:8px 0;border-bottom:1px solid var(--line-soft)">Competitor citation teardown</li>
            <li style="padding:8px 0;border-bottom:1px solid var(--line-soft)">Answer-block content rewrites</li>
            <li style="padding:8px 0;border-bottom:1px solid var(--line-soft)">llms.txt + AI crawler config</li>
            <li style="padding:8px 0;border-bottom:1px solid var(--line-soft)">Weekly prompt testing</li>
            <li style="padding:8px 0">Monthly narrative reporting</li>
          </ul>
          <a class="btn btn-primary btn-sm" style="width:100%;justify-content:center;margin-top:18px" href="contact.html">Scope a GEO engagement</a>
        </div>
      </aside>
    </div>
  </div>
</section>

<section class="sec band-alt">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">Deliverables</div>
      <h2>What lands on your desk</h2>
    </div>
    <div class="grid g3">
      <div class="card"><span class="card-num">MONTH 1</span><h3>Entity &amp; citation baseline</h3><p>Full entity map, 12-point eligibility audit, competitor citation teardown, prioritised 90-day roadmap.</p></div>
      <div class="card"><span class="card-num">MONTH 2</span><h3>Structure &amp; schema</h3><p>Organization, Person, Service and FAQPage schema live. Answer blocks on all money pages. llms.txt shipped.</p></div>
      <div class="card"><span class="card-num">MONTH 3</span><h3>Citation placement</h3><p>Tier-1 profiles built and verified. First guest placements and community mentions live. First citations tracked.</p></div>
    </div>
  </div>
</section>

{faq([
  ("How is GEO different from AEO and LLM SEO?",
   "They overlap and the industry uses them loosely, so here is how we separate them. GEO is about being named and cited inside a generated answer &mdash; it is brand-level and driven mostly by off-site consensus. AEO is about owning the direct answer to a specific question, which is closer to featured-snippet work and driven by on-page structure and schema. LLM SEO is the technical layer: making your templates, markup and content parseable and quotable by models. We run all three; they are sold separately because the work and the timelines differ."),
  ("Can you guarantee we will be cited by ChatGPT?",
   "No, and be sceptical of anyone who does. We do not control the models and there is no submission process. What we control is every input that makes citation likely: entity resolution, citation consensus, retrieval structure and freshness. We report the citation count every month so you can see whether it is working rather than take our word for it."),
  ("Do we need to be on G2 and Capterra if we are not software?",
   "The specific platforms change by category. Software brands need G2 and Capterra. An ecommerce retailer needs Trustpilot, marketplace presence and category community mentions. A local service business needs a very different stack again. What does not change is the principle: independent, trusted third parties describing you consistently. We build the list for your category during the audit."),
  ("Will GEO work if our technical SEO is broken?",
   "No, and this is the most common reason engagements fail elsewhere. If pages are not crawlable, render client-side into an empty shell, or are buried under index bloat, retrieval never happens. Technical health is a prerequisite, which is why our audit covers it and why we will tell you if the technical work needs to come first."),
])}

{cta("See where your GEO baseline sits.",
     "The free audit covers eight of the twelve signals that determine whether generative engines can cite you at all.")}
""")

# ==========================================================================
# SERVICES HUB
# ==========================================================================


def svc(anchor, num, name, desc, bullets, tag="core"):
    lis = "".join(f"<li>{b}</li>" for b in bullets)
    return f"""
<div class="card" id="{anchor}" style="scroll-margin-top:90px">
  <span class="card-num">{num} &middot; {tag.upper()}</span>
  <h3>{name}</h3>
  <p style="margin-bottom:14px">{desc}</p>
  <ul style="font-size:.88rem;color:var(--text-faint);padding-left:1.1em;margin:0">{lis}</ul>
</div>"""


AI_SERVICES = "".join([
    svc("geo", "01", '<a href="generative-engine-optimization.html">Generative Engine Optimization</a>',
        "Be the brand ChatGPT, Perplexity and Gemini name. Entity authority, citation consensus, retrieval-ready structure and a 30-day refresh loop.",
        ["Entity map + Organization/Person schema", "Tier-1 citation stack placement",
         "Competitor citation reverse-engineering", "Weekly controlled prompt testing"], "ai search"),
    svc("aeo", "02", "Answer Engine Optimization",
        "Own the direct answer. Question architecture, FAQ schema and snippet capture so your page is the one quoted rather than one of ten linked.",
        ["Question clustering by intent", "FAQPage + HowTo + QAPage schema",
         "Answer-block rewrites in the first 100 words", "Zero-click defence strategy"], "ai search"),
    svc("llm-seo", "03", "LLM SEO",
        "The technical layer of AI visibility. Templates, markup and rendering engineered so language models can parse, chunk, quote and attribute your content.",
        ["Chunk-friendly heading and passage structure", "llms.txt authoring and maintenance",
         "AI crawler directives: GPTBot, ClaudeBot, PerplexityBot, Google-Extended",
         "Product and category template restructuring"], "ai search"),
    svc("citation", "04", "AI Citation &amp; Entity Building",
        "The off-site half of AI visibility. We build the independent, consistent third-party footprint models read as authority consensus.",
        ["G2, Capterra, Trustpilot, Crunchbase, Product Hunt", "Reddit and Quora participation, done properly",
         "Founder-as-entity: bylines, podcasts, newsletters", "Digital PR aimed at citation, not just DR"], "ai search"),
    svc("monitoring", "05", "AI Visibility Monitoring &amp; Reporting",
        "Citation volume, page-level attribution and controlled prompt testing, reported monthly in plain English alongside clicks and revenue.",
        ["Automated citation tracking + page attribution", "Fixed weekly prompt set across 3+ engines",
         "Competitor share-of-citation tracking", "Narrative monthly report, not a dashboard dump"], "ai search"),
    svc("aio", "06", "Google AI Overviews Optimization",
        "Recover and defend the traffic AI Overviews absorbed. Query-level diagnosis of where you lost clicks and what it takes to get named in the summary.",
        ["AI Overview presence audit by query", "CTR-loss attribution in Search Console",
         "Content restructuring for summary inclusion", "Schema and entity reinforcement"], "ai search"),
])

CORE_SERVICES = "".join([
    svc("technical", "07", "Technical SEO",
        "The foundation everything else sits on. Crawl budget, index bloat, rendering, Core Web Vitals, log-file analysis and site architecture.",
        ["Crawl budget audit and index surgery", "Rendering strategy: SSR, SSG, CSR trade-offs",
         "Core Web Vitals remediation", "Log-file analysis of real Googlebot behaviour"]),
    svc("semantic", "08", "Semantic &amp; On-Page SEO",
        "Concept coverage over keyword density. We map the full topic ecosystem and entity relationships, then build content that proves expertise.",
        ["Semantic topic maps before writing", "Entity and co-occurrence mapping",
         "Position 8-20 recovery programme", "Semantic content audits and gap-filling"]),
    svc("content", "09", "Content Strategy &amp; Production",
        "ICP-driven, conversion-first content. We start at the bottom of the funnel where money is, then build the topical depth around it.",
        ["ICP definition workshop with sales and CS", "Pillar and cluster architecture",
         "Semantic briefs, not keyword briefs", "Founder-bylined authority content"]),
    svc("links", "10", "Link Building &amp; Digital PR",
        "Links that also function as AI citations. Guest placement, digital PR, resource-page outreach and local citations with real editorial standards.",
        ["Competitor backlink reverse-engineering", "Guest posting and guestographic campaigns",
         "Digital PR built around original data", "Local citation and NAP consistency"]),
    svc("ecommerce", "11", "Ecommerce SEO",
        "Category and product architecture, faceted navigation, variant handling and shopping-surface visibility for retailers and DTC brands.",
        ["Money-page keyword mapping framework", "Faceted navigation and parameter control",
         "Variant and product schema", "GA4 ecommerce measurement setup"]),
    svc("saas", "12", "SaaS &amp; B2B SEO",
        "Pipeline over pageviews. Bottom-of-funnel first, comparison and alternatives pages, and integration-led programmatic expansion.",
        ["Inverted-funnel content sequencing", "Comparison and alternatives page systems",
         "Integration and use-case programmatic pages", "Lead-magnet and conversion-path design"]),
    svc("local", "13", "Local SEO",
        "Google Business Profile, local citations, review velocity and location-page architecture for service-area and multi-location businesses.",
        ["GBP optimisation and posting cadence", "Citation consistency cleanup",
         "Review generation systems", "Multi-location page architecture"]),
    svc("international", "14", "International SEO",
        "Hreflang, ccTLD versus subfolder strategy, localisation that goes beyond translation, and market-by-market keyword research.",
        ["Hreflang implementation and validation", "Domain structure strategy",
         "Localised keyword research per market", "Cultural adaptation, not literal translation"]),
    svc("programmatic", "15", "Programmatic SEO",
        "Scaled page generation that survives Google's helpful-content standards. Built on real data, real templates and strict quality gates.",
        ["Data source and template design", "Quality thresholds and index control",
         "Internal link automation", "Cannibalisation monitoring"]),
    svc("migration", "16", "Site Migrations",
        "Replatforms, redesigns and domain moves without losing rankings. Pre-migration crawl baselines, redirect mapping and post-launch monitoring.",
        ["Pre-migration crawl and ranking baseline", "Complete redirect mapping and QA",
         "Staged rollout schedule", "Post-launch daily monitoring for 30 days"]),
    svc("whitelabel", "17", "White-Label SEO",
        "Full delivery under your brand, under NDA. Audits, strategy, execution and branded reporting. We stay invisible to your client.",
        ["NDA-backed anonymous delivery", "Branded reporting in your template",
         "Scalable capacity: audits to full retainers", "Your account manager, our delivery team"]),
    svc("consulting", "18", "SEO Consulting",
        "Direct strategist access at $30 per hour. Teardowns, second opinions, in-house team training and roadmap review.",
        ["$30/hour, booked by the session", "Live teardown with a recorded Loom",
         "In-house team enablement and SOP handover", "Roadmap and vendor review"]),
])

PAGES["services"] = dict(
    title="SEO Services | GEO, AEO, LLM SEO &amp; Full-Stack SEO | SVED Solution",
    desc="Eighteen SEO services across AI search and core SEO: GEO, AEO, LLM SEO, AI citations, technical, semantic, content, links, ecommerce, SaaS, white-label and consulting.",
    slug="services/",
    body=f"""
{phero('<a href="index.html">Home</a> / Services',
       'Services',
       'AI search first. Full-stack SEO underneath.',
       'Eighteen services across two clusters. The AI search cluster is what we lead with and what most clients come for. The core SEO cluster is what makes it work &mdash; because GEO on a broken site is theatre.')}

<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">Cluster 01 &middot; primary</div>
      <h2>AI Search Services</h2>
      <p class="lead dim">Being retrieved, trusted and named by systems that generate answers instead of returning links.</p>
    </div>
    <div class="grid g3">{AI_SERVICES}</div>
  </div>
</section>

<section class="sec band-alt">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">Cluster 02 &middot; foundation</div>
      <h2>Core SEO Services</h2>
      <p class="lead dim">The disciplines that make AI visibility possible and keep classic organic revenue compounding.</p>
    </div>
    <div class="grid g3">{CORE_SERVICES}</div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head center">
      <div class="eyebrow">Engagement models</div>
      <h2>Three ways to work with us</h2>
    </div>
    <div class="grid g3">
      <div class="card"><h3>Audit &amp; roadmap</h3><p style="margin-bottom:16px">One-off diagnostic. Full AI visibility report, technical audit, competitor citation teardown and a prioritised 90-day plan you can execute with anyone.</p><p class="mono green" style="font-size:.85rem">Fixed fee &middot; 2&ndash;3 weeks</p></div>
      <div class="card" style="border-color:rgba(0,255,178,.35)"><h3>Retained delivery</h3><p style="margin-bottom:16px">We run the roadmap. GEO plus the core SEO work it depends on, shipped by our team, reported monthly in narrative form. Most clients start here.</p><p class="mono green" style="font-size:.85rem">Monthly &middot; scoped after audit</p></div>
      <div class="card"><h3>Consulting &amp; enablement</h3><p style="margin-bottom:16px">Strategist access by the hour. Teardowns, second opinions, in-house training and our documented SOP library handed to your team.</p><p class="mono green" style="font-size:.85rem">$30 / hour</p></div>
    </div>
  </div>
</section>

{cta("Not sure which of the eighteen you need?",
     "Start with the free audit. It tells you which signals you are failing, which usually makes the priority obvious.")}
""")

# ==========================================================================
# INDUSTRIES
# ==========================================================================
INDUSTRIES = [
    ("SaaS &amp; Software", "&#9636;", "Comparison and alternatives pages, integration-led programmatic expansion, G2 and Capterra citation stacks. Buyers research in ChatGPT before they ever reach your site."),
    ("Ecommerce &amp; DTC", "&#9679;", "Category architecture, faceted navigation, variant schema and shopping-surface visibility. Our deepest citation dataset comes from this vertical."),
    ("Healthcare &amp; Medical", "&#10010;", "YMYL-grade E-E-A-T, credentialed authorship, medical review workflows and local practice visibility. AI is conservative here &mdash; entity trust is everything."),
    ("Legal &amp; Professional Services", "&#9878;", "Practice-area architecture, jurisdiction targeting, credential schema and review velocity. High-value, high-scrutiny queries."),
    ("Finance &amp; Fintech", "&#9650;", "Regulatory-safe content, calculator and tool pages that earn citations, and the authorship signals YMYL categories demand."),
    ("Real Estate &amp; Property", "&#9750;", "Location page systems, listing schema, market-report content that gets cited, and local pack dominance."),
    ("Travel &amp; Hospitality", "&#9992;", "Destination clusters, itinerary content built for retrieval, review platform presence and seasonal demand capture."),
    ("Education &amp; EdTech", "&#9998;", "Course and programme schema, question-led content that AI quotes directly, and institutional entity authority."),
    ("Manufacturing &amp; Industrial", "&#9881;", "Technical spec pages, distributor architecture, long-cycle B2B intent and the trade-publication citations models trust."),
    ("Home &amp; Local Services", "&#8962;", "Service-area page systems, Google Business Profile, review generation and multi-location scaling."),
    ("Agencies &amp; Resellers", "&#9783;", "White-label delivery under NDA. Audits through full retained execution with branded reporting. We stay invisible."),
    ("Web3 &amp; Crypto", "&#9672;", "Community-first citation building, technical documentation SEO and the credibility signals a sceptical category requires."),
]

PAGES["industries"] = dict(
    title="SEO &amp; AI Visibility by Industry | SVED Solution",
    desc="GEO, AEO and SEO services tailored to SaaS, ecommerce, healthcare, legal, finance, real estate, travel, education, manufacturing, local services, agencies and Web3.",
    slug="industries/",
    body=f"""
{phero('<a href="index.html">Home</a> / Industries',
       'Industries',
       'The signals are universal. The citation stack is not.',
       'Every category has a different set of sources AI models trust. Software brands need G2 and Capterra. A retailer needs Trustpilot and marketplace presence. A medical practice needs credentialed authorship and local verification. We build the stack that matches your category.')}

<section class="sec">
  <div class="wrap">
    <div class="grid g3">
      {"".join(f'<div class="card"><div class="card-icon">{ic}</div><h3>{n}</h3><p>{d}</p></div>' for n, ic, d in INDUSTRIES)}
    </div>
  </div>
</section>

<section class="sec band-alt">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">Why this matters</div>
      <h2>Generic GEO advice fails on contact with your category.</h2>
    </div>
    <div class="grid g2" style="gap:44px">
      <div class="prose">
        <p>Most GEO content tells you to get listed on G2 and Product Hunt. That is correct advice for exactly one category. If you sell industrial components, no model is checking Product Hunt &mdash; it is weighting trade publications, distributor directories and technical documentation.</p>
        <p>During the audit we reverse-engineer the citation sources that actually appear in AI answers for <em>your</em> category, by exporting the domains cited alongside the brands already winning those answers. That list becomes your citation roadmap. It is different every time.</p>
      </div>
      <div class="panel">
        <div class="panel-bar"><i class="tdot"></i><i class="tdot"></i><i class="tdot"></i><span style="margin-left:8px">citation-sources-by-category</span></div>
        <div class="panel-body" style="font-size:.79rem">
          <div class="crow"><span class="lbl">B2B SaaS</span><span class="val">G2 &middot; Capterra &middot; PH</span></div>
          <div class="crow"><span class="lbl">Ecommerce</span><span class="val">Trustpilot &middot; Reddit</span></div>
          <div class="crow"><span class="lbl">Healthcare</span><span class="val">Healthgrades &middot; assoc.</span></div>
          <div class="crow"><span class="lbl">Legal</span><span class="val">Avvo &middot; bar directories</span></div>
          <div class="crow"><span class="lbl">Manufacturing</span><span class="val">Trade pubs &middot; ThomasNet</span></div>
          <div class="crow"><span class="lbl">Local services</span><span class="val">GBP &middot; Yelp &middot; Nextdoor</span></div>
        </div>
      </div>
    </div>
  </div>
</section>

{cta("Which sources does AI trust in your category?",
     "The free audit checks your presence across the Tier-1 sources that matter for your vertical.")}
""")

# ==========================================================================
# USE CASES
# ==========================================================================
USE_CASES = [
    ("&ldquo;We are invisible in ChatGPT.&rdquo;",
     "You searched your own category in ChatGPT and a competitor came up. You did not.",
     "Entity audit, competitor citation teardown, Tier-1 stack build and answer-block restructuring. First citations typically appear around day 60.",
     "GEO + AI Citation Building"),
    ("&ldquo;AI Overviews killed our traffic.&rdquo;",
     "Rankings held. Impressions held. Clicks fell off a cliff. Nobody can explain it.",
     "Query-level AI Overview presence audit, CTR-loss attribution in Search Console, then content restructured for summary inclusion rather than link-clicking.",
     "AI Overviews Optimization"),
    ("&ldquo;Our pages are stuck at position 8&ndash;20.&rdquo;",
     "Real traffic, real impressions, permanently below the fold. The pages Google half-trusts.",
     "A documented recovery programme: page-level query extraction, intent-gap diagnosis, title and meta rewrite for CTR, targeted internal linking. Movement in 7 to 21 days, no backlinks required.",
     "Semantic &amp; On-Page SEO"),
    ("&ldquo;We are replatforming and terrified.&rdquo;",
     "A migration is coming and the last one cost the business six months of traffic.",
     "Pre-migration crawl and ranking baseline, complete redirect mapping with QA, staged rollout and 30 days of daily post-launch monitoring.",
     "Site Migrations"),
    ("&ldquo;Google is crawling 400,000 pages we do not want.&rdquo;",
     "Index bloat, faceted navigation gone feral, crawl budget burned on parameters and noise.",
     "Log-file analysis of real Googlebot behaviour, index surgery with clear keep-or-delete criteria, and parameter and facet control. Less content, more traffic.",
     "Technical SEO"),
    ("&ldquo;New site. Zero authority. Where do we start?&rdquo;",
     "Nothing indexed, nothing ranking, and a runway that does not allow for an eighteen-month content play.",
     "Inverted funnel: bottom-of-funnel commercial pages first, low-difficulty entry keywords, entity foundations from day one so the AI clock starts running immediately.",
     "Content Strategy + GEO"),
    ("&ldquo;We need SEO but cannot hire in-house.&rdquo;",
     "A full-time senior SEO hire costs more than the entire channel budget.",
     "Retained delivery as an embedded team, or hourly consulting plus our documented SOP library so your existing marketer can execute properly.",
     "Retained Delivery / Consulting"),
    ("&ldquo;Our agency clients want GEO and we cannot deliver it.&rdquo;",
     "Clients are asking about ChatGPT visibility and you have no answer or capacity.",
     "White-label delivery under NDA. Audits through full execution, reported in your branding. We never appear.",
     "White-Label SEO"),
]

PAGES["use-cases"] = dict(
    title="SEO &amp; AI Visibility Use Cases | SVED Solution",
    desc="Eight situations clients come to us with, and exactly what we do about each: AI invisibility, AI Overview traffic loss, stuck rankings, migrations, index bloat and more.",
    slug="use-cases/",
    body=f"""
{phero('<a href="index.html">Home</a> / Use Cases',
       'Use cases',
       'Eight problems. Eight documented responses.',
       'Nobody buys &ldquo;SEO services&rdquo;. They buy a fix for a specific, expensive problem. These are the eight we hear most, and what we actually do about each one.')}

<section class="sec">
  <div class="wrap">
    <div class="grid g2">
      {"".join(f'''<div class="card">
        <h3 style="margin-bottom:10px">{t}</h3>
        <p style="color:var(--text-faint);font-size:.9rem;margin-bottom:14px"><em>{sym}</em></p>
        <p style="margin-bottom:14px">{fix}</p>
        <span class="card-more">{svc_}</span>
      </div>''' for t, sym, fix, svc_ in USE_CASES)}
    </div>
  </div>
</section>

{cta("Recognise one of these?",
     "The free audit is the fastest way to confirm which problem you actually have &mdash; they often look alike from the inside.")}
""")

# ==========================================================================
# CASE STUDIES
# ==========================================================================
PAGES["case-studies"] = dict(
    title="Case Studies | AI Citation &amp; SEO Results | SVED Solution",
    desc="Anonymised client results: 2,923 AI citations in 29 days, position 8-20 recovery programmes, index surgery and migration outcomes.",
    slug="case-studies/",
    body=f"""
{phero('<a href="index.html">Home</a> / Case Studies',
       'Proof',
       'Anonymised clients. Real exports.',
       'Every figure on this page comes from a live client account. Names are withheld under NDA; full exports are available on request during a scoping call.')}

<section class="sec">
  <div class="wrap">
    <div class="card" style="padding:0;overflow:hidden;margin-bottom:24px">
      <div style="padding:36px 36px 0"><span class="card-num">CASE 01 &middot; ECOMMERCE RETAILER &middot; UNITED KINGDOM</span>
        <h2 style="margin-bottom:.4rem">2,923 AI citations in a single month</h2>
        <p class="dim" style="max-width:70ch">A specialist ecommerce retailer with a strong blog and no AI visibility strategy. We restructured content into answer blocks, wired Organization and Product schema, opened AI crawler access and ran the 30-day refresh loop across the blog archive.</p>
      </div>
      <div class="kpis" style="border:0;border-radius:0;margin-top:28px">
        <div class="kpi"><div class="kpi-val">2,923</div><div class="kpi-lab">AI citations, 29 days</div></div>
        <div class="kpi"><div class="kpi-val">131</div><div class="kpi-lab">Distinct pages cited</div></div>
        <div class="kpi"><div class="kpi-val">307</div><div class="kpi-lab">Citations, top single page</div></div>
        <div class="kpi"><div class="kpi-val">101</div><div class="kpi-lab">Average citations / day</div></div>
      </div>
      <div style="padding:28px 36px 36px">
        <p style="font-size:.93rem;color:var(--text-dim);margin-bottom:0"><strong>What drove it:</strong> product comparison and settings-guide content was already excellent &mdash; it was simply not structured for retrieval. Adding direct-answer openings, comparison tables and visible last-modified dates turned existing archive posts into citation assets. The top-cited page is a product comparison guide.</p>
      </div>
    </div>

    <div class="grid g2">
      <div class="card">
        <span class="card-num">CASE 02 &middot; B2B SERVICES &middot; UNITED STATES</span>
        <h3>Position 8&ndash;20 recovery programme</h3>
        <p style="margin-bottom:16px">Fourteen pages with real impressions permanently stuck below the fold. No new content, no new links &mdash; page-level query extraction, intent-gap diagnosis, title and meta rewrites for CTR, and targeted internal linking.</p>
        <div class="tbl-wrap"><table style="min-width:0">
          <tr><th>Metric</th><th>Before</th><th>After</th></tr>
          <tr><td>Avg position</td><td>12.4</td><td><strong>4.1</strong></td></tr>
          <tr><td>CTR</td><td>1.9&#37;</td><td><strong>5.4&#37;</strong></td></tr>
          <tr><td>Time to movement</td><td colspan="2"><strong>14 days</strong></td></tr>
        </table></div>
      </div>
      <div class="card">
        <span class="card-num">CASE 03 &middot; MULTI-CHANNEL RETAILER</span>
        <h3>Monthly narrative reporting</h3>
        <p style="margin-bottom:16px">Replaced a 40-tab dashboard nobody read with a written monthly narrative: what went well, what needs attention, and next month's single priority. Reporting itself became a retention driver.</p>
        <div class="tbl-wrap"><table style="min-width:0">
          <tr><th>Metric</th><th>Prior</th><th>Reported</th></tr>
          <tr><td>Organic sessions</td><td>34,210</td><td><strong>44,812</strong></td></tr>
          <tr><td>Organic revenue</td><td>$175,220</td><td><strong>$189,420</strong></td></tr>
          <tr><td>Avg position</td><td>8.4</td><td><strong>7.4</strong></td></tr>
        </table></div>
      </div>
    </div>

    <div class="quote" style="margin-top:24px">
      <p>&ldquo;The reporting alone changed how our board talks about organic. For the first time they could read one page and know what we did, what it produced and what we are doing next.&rdquo;</p>
      <div class="who">Marketing Director &middot; Retail &middot; anonymised</div>
    </div>
  </div>
</section>

{cta("Want the full exports?",
     "We share unredacted client data under NDA during scoping calls. Ask and we will walk you through the raw account.",
     primary=("Book a scoping call", "contact.html"),
     secondary=("Run the free audit first", "ai-visibility-audit.html"))}
""")

# ==========================================================================
# REVIEWS
# ==========================================================================
REVIEWS = [
    ("We had no idea we were invisible in ChatGPT until the audit. Ninety days later we are the brand it names for our main category question. Nobody else even pitched us on this.", "Head of Growth", "B2B SaaS &middot; United States"),
    ("First agency that reported AI citations as an actual number instead of hand-waving about the future of search. The monthly narrative report is the best reporting we have ever had.", "Ecommerce Director", "Retail &middot; United Kingdom"),
    ("They fixed the crawl and index problems our previous agency spent a year describing in slides. Then the content actually started ranking.", "Marketing Lead", "Healthcare &middot; United States"),
    ("The position 8-20 programme moved fourteen pages in two weeks with no new content and no link building. I did not believe it would work.", "SEO Manager", "Professional Services &middot; Canada"),
    ("We white-label them for three of our clients. Delivery is clean, reporting arrives in our branding, and they have never once broken the NDA.", "Agency Founder", "Digital Agency &middot; Australia"),
    ("The free audit was more useful than the paid audits we bought from two other agencies. That is what made us call them.", "Founder", "DTC Brand &middot; United Kingdom"),
    ("What I value is the honesty about timelines. They told us day 60 for first citations and it was day 58. No overselling.", "VP Marketing", "Fintech &middot; United States"),
    ("Our migration went live with zero ranking loss. After the last one cost us six months, that alone paid for the engagement.", "Head of Digital", "Manufacturing &middot; Germany"),
    ("Thirty dollars an hour for that level of strategist is not a normal market rate. We now book a session every month.", "Marketing Manager", "EdTech &middot; India"),
]

PAGES["reviews"] = dict(
    title="Client Reviews &amp; Testimonials | SVED Solution",
    desc="What clients say about working with SVED Solution on GEO, AI visibility, technical SEO, migrations and white-label delivery.",
    slug="reviews/",
    body=f"""
{phero('<a href="index.html">Home</a> / Reviews',
       'Reviews',
       'What clients actually say.',
       'Anonymised at client request, verified on file. We will connect you directly with a reference in your industry during scoping.')}

<section class="sec">
  <div class="wrap">
    <div class="kpis" style="margin-bottom:44px">
      <div class="kpi"><div class="kpi-val"><span data-count="4.9" data-dec="1">0</span></div><div class="kpi-lab">Average client rating</div></div>
      <div class="kpi"><div class="kpi-val"><span data-count="94">0</span><span class="u">&#37;</span></div><div class="kpi-lab">Retainer renewal rate</div></div>
      <div class="kpi"><div class="kpi-val"><span data-count="39">0</span></div><div class="kpi-lab">Documented delivery SOPs</div></div>
      <div class="kpi"><div class="kpi-val"><span data-count="12">0</span></div><div class="kpi-lab">Industries served</div></div>
    </div>
    <div class="grid g3">
      {"".join(f'<div class="quote"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>&ldquo;{q}&rdquo;</p><div class="who">{w} &middot; {c}</div></div>' for q, w, c in REVIEWS)}
    </div>
  </div>
</section>

{cta("Talk to a reference in your industry.",
     "Ask during scoping and we will connect you with a current client in a comparable category.",
     primary=("Book a scoping call", "contact.html"),
     secondary=("See case studies", "case-studies.html"))}
""")

# ==========================================================================
# INSIGHTS (blog)
# ==========================================================================
POSTS = [
    ("GEO vs SEO vs AEO: a clean mental model", "Strategy", "11 min",
     "Three acronyms, one underlying shift. What each actually optimises for, where they overlap, and why picking one is the wrong question."),
    ("The AI Search Playbook: how brands get cited by LLMs", "GEO", "18 min",
     "The full framework: four visibility pillars, the Tier-1 citation stack, the 30-day refresh loop and an honest results timeline."),
    ("How to move pages from position 8-20 into the top 3", "On-Page", "9 min",
     "A documented eight-step process using page-level query data and internal linking. No backlinks. Movement in 7 to 21 days."),
    ("The 21-step semantic SEO playbook", "Semantic", "16 min",
     "Ranking by covering concept ecosystems instead of repeating keywords. Entity mapping, co-occurrence, semantic briefs and content audits."),
    ("Should you block GPTBot? An honest cost-benefit", "Technical", "7 min",
     "Blocking AI crawlers protects your content and guarantees you are never cited. When that trade is right, and when it is self-harm."),
    ("llms.txt explained: what it is and whether it matters yet", "Technical", "6 min",
     "The emerging standard for declaring content to LLM crawlers. Current adoption, what to put in it, and realistic expectations."),
    ("Why we delete pages to grow traffic", "Technical", "12 min",
     "Index bloat, crawl budget and the counter-intuitive case for index surgery on large sites."),
    ("Reverse-engineering competitor AI citations", "GEO", "10 min",
     "How to export every domain cited alongside the brands winning your category answers, and turn that list into a placement roadmap."),
    ("Measuring SEO properly in GA4 for ecommerce", "Measurement", "14 min",
     "Attribution, event configuration and the reports that actually tell you whether organic is producing revenue."),
]

PAGES["insights"] = dict(
    title="SEO &amp; AI Search Insights | SVED Solution Blog",
    desc="Practitioner writing on GEO, AEO, LLM SEO, technical SEO and measurement. Frameworks we actually use on client accounts.",
    slug="insights/",
    body=f"""
{phero('<a href="index.html">Home</a> / Insights',
       'Insights',
       'What we are learning, published as we learn it.',
       'Frameworks we run on live accounts, written up in full. No gated fluff, no &ldquo;10 tips&rdquo; listicles. If we publish a process, it is the one we use.')}

<section class="sec">
  <div class="wrap">
    <div class="grid g3">
      {"".join(f'''<a class="card card-link" href="#">
        <span class="card-num">{cat.upper()} &middot; {rt}</span>
        <h3>{t}</h3><p>{d}</p><span class="card-more">Read &rarr;</span></a>''' for t, cat, rt, d in POSTS)}
    </div>
    <div class="center mt3">
      <p class="faint" style="font-size:.86rem">Also published on Medium and Substack &mdash; syndicated with canonical tags back here.</p>
    </div>
  </div>
</section>

<section class="sec band-green">
  <div class="wrap wrap-narrow center">
    <div class="eyebrow" style="justify-content:center">Newsletter</div>
    <h2>The AI Visibility Brief</h2>
    <p class="lead dim">What changed in AI search this week and what to do about it. Every Tuesday, free, with the AI Search Playbook PDF on signup.</p>
    <form class="audit-form" style="max-width:520px;margin:2rem auto 0;justify-content:center" onsubmit="return false">
      <input type="email" placeholder="you@company.com" aria-label="Email">
      <button class="btn btn-primary" type="submit">Get the playbook</button>
    </form>
  </div>
</section>

{cta("Prefer the diagnosis to the reading?",
     "Run the free audit and get your own numbers instead of ours.")}
""")

# ==========================================================================
# VIDEOS
# ==========================================================================
VIDEOS = [
    ("Live GEO teardown: why this brand is invisible in ChatGPT", "Teardown", "14:22"),
    ("The 12-point AI eligibility audit, run live", "Walkthrough", "18:05"),
    ("Index surgery: deleting pages to grow traffic", "Technical", "22:40"),
    ("Position 8-20 recovery, start to finish", "On-Page", "16:11"),
    ("Reverse-engineering a competitor's AI citations", "GEO", "12:58"),
    ("Reading a monthly SEO report the right way", "Reporting", "09:34"),
]

PAGES["videos"] = dict(
    title="SEO &amp; AI Visibility Videos | SVED Solution",
    desc="Live teardowns, audit walkthroughs and technical SEO explainers. Watch how we actually diagnose and fix AI visibility problems.",
    slug="videos/",
    body=f"""
{phero('<a href="index.html">Home</a> / Videos',
       'Videos',
       'Watch the work, not the pitch.',
       'Recorded teardowns and walkthroughs. Every engagement includes Loom videos of the actual diagnosis, because a screen recording of the problem beats a slide describing it.')}

<section class="sec">
  <div class="wrap">
    <div class="grid g3">
      {"".join(f'''<div class="card" style="padding:0;overflow:hidden">
        <div style="aspect-ratio:16/9;background:linear-gradient(135deg,var(--navy-700),var(--navy-600));display:grid;place-items:center;border-bottom:1px solid var(--line);position:relative">
          <div style="width:52px;height:52px;border-radius:50%;background:var(--green);display:grid;place-items:center;color:var(--ink);font-size:1.1rem">&#9654;</div>
          <span class="mono" style="position:absolute;bottom:10px;right:12px;font-size:.7rem;background:rgba(0,0,0,.6);padding:2px 7px;border-radius:4px;color:var(--white)">{dur}</span>
        </div>
        <div style="padding:22px"><span class="card-num">{cat.upper()}</span><h3 style="font-size:1.05rem">{t}</h3></div>
      </div>''' for t, cat, dur in VIDEOS)}
    </div>
    <div class="center mt3">
      <a class="btn btn-ghost" href="#">Subscribe on YouTube</a>
    </div>
    <p class="faint center" style="font-size:.82rem;margin-top:16px">Preview placeholders. Production build embeds YouTube with VideoObject schema for video-rich results.</p>
  </div>
</section>

{cta("Want a teardown of your own site?",
     "Every full audit ships with a recorded walkthrough from the strategist who ran it.")}
""")

# ==========================================================================
# RESOURCES
# ==========================================================================
PAGES["resources"] = dict(
    title="SEO Resources, Playbooks &amp; SOPs | SVED Solution",
    desc="Free and gated SEO resources: the AI Search Playbook, semantic SEO framework, position 8-20 SOP and a documented 39-SOP delivery library.",
    slug="resources/",
    body=f"""
{phero('<a href="index.html">Home</a> / Resources',
       'Resources',
       'The documents we actually work from.',
       'Not lead-magnet filler. These are the playbooks and standard operating procedures our team executes against, published because a documented process is the proof that one exists.')}

<section class="sec">
  <div class="wrap">
    <div class="sec-head"><div class="eyebrow">Playbooks</div><h2>Free downloads</h2></div>
    <div class="grid g3">
      <div class="card"><div class="card-icon">&#9670;</div><h3>The AI Search Playbook</h3><p style="margin-bottom:16px">How brands get visibility in ChatGPT, Perplexity and Gemini. Four pillars, the Tier-1 citation stack, the refresh loop and an honest results timeline.</p><a class="btn btn-ghost btn-sm" href="#">Download PDF</a></div>
      <div class="card"><div class="card-icon">&#9678;</div><h3>The 21-Step Semantic SEO Playbook</h3><p style="margin-bottom:16px">Ranking by covering concept ecosystems instead of repeating keywords. Entity mapping, semantic briefs and content audits.</p><a class="btn btn-ghost btn-sm" href="#">Download PDF</a></div>
      <div class="card"><div class="card-icon">&#8599;</div><h3>Position 8&ndash;20 to Top 3 SOP</h3><p style="margin-bottom:16px">The eight-step process for moving already-ranking pages using query data and internal linking. No backlinks needed.</p><a class="btn btn-ghost btn-sm" href="#">Download PDF</a></div>
    </div>
  </div>
</section>

<section class="sec band-alt">
  <div class="wrap">
    <div class="sec-head"><div class="eyebrow">Delivery library</div><h2>39 documented SOPs</h2>
      <p class="lead dim">Every recurring task in our delivery has a written procedure. Consulting clients get the full library. It is also why our output does not vary by who is on the account.</p></div>
    <div class="grid g4">
      <div class="card"><h4>Technical &amp; setup</h4><p style="font-size:.87rem">WordPress setup, robots.txt, XML sitemaps, 301 redirects, SEO-friendly URL migration, site speed, backup and restore.</p></div>
      <div class="card"><h4>On-page</h4><p style="font-size:.87rem">On-page audits, optimisation with Rank Math, Yoast and SEOPress, URL audits, blog outlines, keyword research and mapping.</p></div>
      <div class="card"><h4>Off-page</h4><p style="font-size:.87rem">Guest blogging campaigns, guestographics, resource-page outreach, backlink audits, competitor backlink and keyword reverse-engineering.</p></div>
      <div class="card"><h4>Measurement</h4><p style="font-size:.87rem">GA4 setup via GTM, Search Console configuration, cross-domain tracking, internal traffic exclusion, automated query reports, dashboards.</p></div>
    </div>
  </div>
</section>

{cta("Want the SOP library for your in-house team?",
     "Consulting engagements include the full 39-SOP library and a handover session at $30 per hour.",
     primary=("Book a consulting session", "contact.html"),
     secondary=("Run the free audit", "ai-visibility-audit.html"))}
""")

# ==========================================================================
# ABOUT
# ==========================================================================
PAGES["about"] = dict(
    title="About SVED Solution | Our Story, Values &amp; Team",
    desc="Who we are, what we believe, and how we understand the AI search market. Core values, team and market perspective from SVED Solution.",
    slug="about/",
    body=f"""
{phero('<a href="index.html">Home</a> / About',
       'About',
       'We would rather be right than early to a trend.',
       'SVED Solution is a 360&deg; SEO agency built around a single conviction: search is splitting into two systems, and most brands are only optimising for one of them.')}

<section class="sec">
  <div class="wrap wrap-narrow prose">
    <h2 style="margin-top:0">Our story</h2>
    <p>We started as SEO practitioners doing what everyone else did &mdash; technical audits, content programmes, link building. The work produced results and the results were measurable.</p>
    <p>Then a client's traffic fell while their rankings held. Impressions flat, positions unchanged, clicks gone. The cause turned out to be an AI Overview sitting above their number-two ranking, naming three competitors and answering the query outright. There was no lever in the traditional SEO toolkit that fixed it.</p>
    <p>So we rebuilt our practice around the question that actually mattered: <strong>what makes an AI system name one brand instead of another?</strong> The answer &mdash; entity authority, citation consensus, retrieval-ready structure and sustained freshness &mdash; became our methodology. We now report AI citations for every client the same way we report clicks and revenue.</p>
  </div>
</section>

<section class="sec band-alt">
  <div class="wrap">
    <div class="sec-head"><div class="eyebrow">Core values</div><h2>Six things we do not compromise on</h2></div>
    <div class="grid g3">
      <div class="card"><span class="card-num">VALUE 01</span><h3>Diagnosis before prescription</h3><p>We do not quote a retainer before we have audited. Selling a solution to an undiagnosed problem is how agencies waste a client's year.</p></div>
      <div class="card"><span class="card-num">VALUE 02</span><h3>Honest timelines</h3><p>First citations around day 60, category authority at 9 to 12 months. We publish the real curve because the honest version survives contact with reality.</p></div>
      <div class="card"><span class="card-num">VALUE 03</span><h3>We ship, we do not suggest</h3><p>Recommendations that sit in a spreadsheet produce nothing. We implement the schema, write the content, build the links and fix the crawl.</p></div>
      <div class="card"><span class="card-num">VALUE 04</span><h3>Every claim carries a number</h3><p>Preferably from our own client work, anonymised. Otherwise cited to a primary source. No unsupported assertions in our reporting or our marketing.</p></div>
      <div class="card"><span class="card-num">VALUE 05</span><h3>Documented, not improvised</h3><p>Thirty-nine written SOPs. Output should not vary based on who is staffed to the account this month.</p></div>
      <div class="card"><span class="card-num">VALUE 06</span><h3>We will tell you no</h3><p>If GEO is not your bottleneck, we will say so. If your technical foundation needs fixing first, we will sequence it that way even though it delays the interesting work.</p></div>
    </div>
  </div>
</section>

<section class="sec" id="market" style="scroll-margin-top:90px">
  <div class="wrap">
    <div class="sec-head"><div class="eyebrow">Market understanding</div><h2>How we read the market</h2>
      <p class="lead dim">Four positions we hold, each of which shapes what we sell and what we refuse to sell.</p></div>
    <div class="grid g2" style="gap:36px">
      <div class="card"><h3>Search has split, not shifted</h3><p>Ranked-list search is not dying. It is being joined by generative retrieval with different mechanics. Brands that treat this as a replacement over-rotate. Brands that treat it as hype get left behind. The correct posture is to run both.</p></div>
      <div class="card"><h3>The GEO window is temporary</h3><p>Right now the defining commercial queries in this category have top-10 results with almost no page authority. That is an artefact of large brands publishing placeholder content fast. It will not last, which is why we tell clients the cost of waiting is real and quantifiable.</p></div>
      <div class="card"><h3>Off-site consensus beats on-page polish</h3><p>Most GEO offerings sell schema and FAQ blocks because they are easy to deliver. The heavy lifting is the citation footprint &mdash; independent sources describing you consistently. It is slower, harder and it is what actually moves the needle.</p></div>
      <div class="card"><h3>AI tooling has changed delivery economics</h3><p>Research, briefs, technical diagnosis and reporting are dramatically faster than they were two years ago. We pass that on as scope rather than margin &mdash; it is why a strategist hour costs $30 and why a small team can carry a full SOP library.</p></div>
    </div>
  </div>
</section>

<section class="sec band-alt" id="team" style="scroll-margin-top:90px">
  <div class="wrap">
    <div class="sec-head"><div class="eyebrow">Our team</div><h2>Small team. Named owners.</h2>
      <p class="lead dim">You work with the strategist who ran your audit, not an account manager relaying messages.</p></div>
    <div class="grid g3">
      <div class="card"><div class="card-icon" style="width:60px;height:60px;font-size:1.3rem;border-radius:50%">VP</div><h3>Ved Prakash</h3><p class="mono green" style="font-size:.78rem;margin-bottom:12px">FOUNDER &amp; HEAD OF STRATEGY</p><p>Leads GEO and AI visibility strategy across all accounts. Runs the audits, sets the roadmaps and owns the monthly narrative reporting.</p></div>
      <div class="card"><div class="card-icon" style="width:60px;height:60px;font-size:1.3rem;border-radius:50%">&#9881;</div><h3>Technical SEO Lead</h3><p class="mono green" style="font-size:.78rem;margin-bottom:12px">ROLE OPEN &middot; PLACEHOLDER</p><p>Crawl budget, index surgery, rendering strategy, log-file analysis and migrations. Replace this card with your hire or contractor.</p></div>
      <div class="card"><div class="card-icon" style="width:60px;height:60px;font-size:1.3rem;border-radius:50%">&#9998;</div><h3>Content &amp; Citations Lead</h3><p class="mono green" style="font-size:.78rem;margin-bottom:12px">ROLE OPEN &middot; PLACEHOLDER</p><p>Semantic briefs, answer-block writing, Tier-1 citation placement and digital PR. Replace this card with your hire or contractor.</p></div>
    </div>
    <p class="faint center" style="font-size:.83rem;margin-top:24px">Person schema is wired to each team member in the production build &mdash; founder entity association is a direct AI visibility signal.</p>
  </div>
</section>

{cta("Work with the person who runs your audit.",
     "No account-manager layer. Book time directly with the strategist.",
     primary=("Book a call", "contact.html"),
     secondary=("Run the free audit", "ai-visibility-audit.html"))}
""")

# ==========================================================================
# CONTACT
# ==========================================================================
PAGES["contact"] = dict(
    title="Contact SVED Solution | Book an SEO &amp; AI Visibility Call",
    desc="Book a strategy call, request a full AI visibility report, or book a $30/hour consulting session with SVED Solution.",
    slug="contact/",
    body=f"""
{phero('<a href="index.html">Home</a> / Contact',
       'Contact',
       'Tell us what is broken.',
       'The more specific you are, the more useful the first call is. If you have already run the free audit, paste your score and we will start from there.')}

<section class="sec">
  <div class="wrap">
    <div class="grid g2" style="gap:52px;align-items:start">
      <div>
        <form class="card" style="padding:32px" onsubmit="return false">
          <h3 style="margin-bottom:20px">Start a conversation</h3>
          <div class="grid g2" style="gap:14px;margin-bottom:14px">
            <input class="news-input" type="text" placeholder="Full name" style="width:100%;background:var(--navy-900);border:1px solid var(--line);color:var(--white);padding:13px 15px;border-radius:6px;font-family:inherit">
            <input type="email" placeholder="Work email" style="width:100%;background:var(--navy-900);border:1px solid var(--line);color:var(--white);padding:13px 15px;border-radius:6px;font-family:inherit">
          </div>
          <input type="url" placeholder="Website URL" style="width:100%;background:var(--navy-900);border:1px solid var(--line);color:var(--white);padding:13px 15px;border-radius:6px;font-family:inherit;margin-bottom:14px">
          <select style="width:100%;background:var(--navy-900);border:1px solid var(--line);color:var(--text-dim);padding:13px 15px;border-radius:6px;font-family:inherit;margin-bottom:14px">
            <option>What do you need help with?</option>
            <option>AI visibility / GEO</option>
            <option>AI Overviews traffic loss</option>
            <option>Technical SEO / migration</option>
            <option>Content &amp; rankings</option>
            <option>White-label delivery</option>
            <option>Hourly consulting ($30/hr)</option>
          </select>
          <select style="width:100%;background:var(--navy-900);border:1px solid var(--line);color:var(--text-dim);padding:13px 15px;border-radius:6px;font-family:inherit;margin-bottom:14px">
            <option>Monthly revenue (helps us scope)</option>
            <option>Under $50k</option><option>$50k&ndash;$250k</option>
            <option>$250k&ndash;$1M</option><option>$1M+</option>
          </select>
          <textarea rows="4" placeholder="What is happening? Paste your audit score if you have one." style="width:100%;background:var(--navy-900);border:1px solid var(--line);color:var(--white);padding:13px 15px;border-radius:6px;font-family:inherit;margin-bottom:18px"></textarea>
          <button class="btn btn-primary btn-lg" style="width:100%;justify-content:center">Send message</button>
          <p class="faint" style="font-size:.78rem;margin-top:12px;text-align:center">We reply within one business day.</p>
        </form>
      </div>
      <div>
        <div class="card" style="margin-bottom:20px">
          <h3>Book directly</h3>
          <p style="margin-bottom:18px">Skip the form. Grab a 30-minute slot with the strategist who will run your audit.</p>
          <div style="background:var(--navy-900);border:1px dashed var(--line);border-radius:8px;padding:36px;text-align:center">
            <p class="mono faint" style="font-size:.8rem;margin:0">Calendly embed<br>renders here in production</p>
          </div>
        </div>
        <div class="card" style="margin-bottom:20px">
          <h3>Other ways in</h3>
          <div class="crow"><span class="lbl">Email</span><span class="val"><a href="mailto:{EMAIL}">{EMAIL}</a></span></div>
          <div class="crow"><span class="lbl">WhatsApp</span><span class="val"><a href="https://api.whatsapp.com/send?phone={WHATSAPP_RAW}">{WHATSAPP_DISPLAY}</a></span></div>
          <div class="crow"><span class="lbl">Consulting</span><span class="val">$30 / hour</span></div>
          <div class="crow"><span class="lbl">Response time</span><span class="val">&lt; 1 business day</span></div>
          <div class="crow"><span class="lbl">White-label</span><span class="val">NDA on request</span></div>
        </div>
        <div class="card">
          <h3>Before you write</h3>
          <p style="margin-bottom:16px">Running the free audit first makes the first call about twice as useful &mdash; you arrive with a score and twelve specific findings instead of a general question.</p>
          <a class="btn btn-ghost btn-sm" href="ai-visibility-audit.html">Run the free audit</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sec band-alt">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">Offices</div>
      <h2>Three locations. One delivery team.</h2>
      <p class="lead dim">Dubai headquarters, Kolkata delivery centre and a US representative office &mdash; so scoping calls happen in your timezone and delivery runs around the clock.</p>
    </div>
    <div class="grid g3">
      {"".join(f'''<div class="card">
        <span class="card-num">{role.upper()}</span>
        <h3>{country}</h3>
        <p style="margin-bottom:16px">{addr}</p>
        <div class="crow"><span class="lbl">Phone</span><span class="val"><a href="tel:{tel_raw}">{tel}</a></span></div>
        <div class="crow"><span class="lbl">Email</span><span class="val"><a href="mailto:{EMAIL}">{EMAIL}</a></span></div>
      </div>''' for country, role, addr, tel, tel_raw in OFFICES)}
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="card" style="display:flex;gap:28px;align-items:center;flex-wrap:wrap;justify-content:space-between">
      <div style="flex:1 1 420px">
        <div class="eyebrow">Sister brand</div>
        <h3 style="margin-bottom:.4rem">{SISTER[0]}</h3>
        <p style="margin-bottom:0">{SISTER[2]}. If your project is a token launch, DeFi protocol, NFT platform or Web3 infrastructure play, that team has the category-specific citation network and technical context &mdash; and we run GEO across both brands.</p>
      </div>
      <a class="btn btn-ghost" href="{SISTER[1]}" rel="noopener">Visit web3technetwork.com</a>
    </div>
  </div>
</section>
""")


# ==========================================================================
# Blog posts from content/blog/*.md  (edited via Decap CMS)
# ==========================================================================
def parse_front_matter(raw):
    """Minimal YAML front-matter parser: key: value, one level."""
    meta, body = {}, raw
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        if end != -1:
            head = raw[3:end].strip()
            body = raw[end + 4:].lstrip("\n")
            for line in head.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, body


def md_to_html(text):
    try:
        import markdown
        return markdown.markdown(text, extensions=["extra", "sane_lists"])
    except ImportError:
        # Fallback: paragraphs + headings only, so a missing dep never breaks the build.
        out = []
        for block in text.split("\n\n"):
            b = block.strip()
            if not b:
                continue
            m = re.match(r"^(#{1,4})\s+(.*)$", b)
            if m:
                lvl = len(m.group(1))
                out.append(f"<h{lvl}>{m.group(2)}</h{lvl}>")
            else:
                out.append("<p>" + b.replace("\n", " ") + "</p>")
        return "\n".join(out)


def load_posts():
    d = os.path.join(OUT, "content", "blog")
    posts = []
    if not os.path.isdir(d):
        return posts
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".md"):
            continue
        with io.open(os.path.join(d, fn), encoding="utf-8") as f:
            meta, body = parse_front_matter(f.read())
        posts.append({
            "slug": meta.get("slug") or fn[:-3],
            "title": meta.get("title", fn[:-3]),
            "desc": meta.get("description", ""),
            "category": meta.get("category", "Insights"),
            "read": meta.get("readtime", "8 min"),
            "date": meta.get("date", ""),
            "author": meta.get("author", "Ved Prakash"),
            "answer": meta.get("answer", ""),
            "html": md_to_html(body),
        })
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def post_schema(p):
    return ('{"@context":"https://schema.org","@type":"BlogPosting",'
            f'"headline":{_j(p["title"])},"description":{_j(p["desc"])},'
            f'"datePublished":{_j(p["date"])},"dateModified":{_j(p["date"])},'
            f'"author":{{"@type":"Person","name":{_j(p["author"])}}},'
            '"publisher":{"@type":"Organization","name":"SVED Solution",'
            '"url":"https://svedsolution.com/"},'
            f'"mainEntityOfPage":"https://svedsolution.com/insights/{p["slug"]}/"}}')


def _j(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def post_page(p):
    ans = ""
    if p["answer"]:
        ans = f'<div class="answer-block" style="margin-top:0"><div class="q">The short answer</div><p>{p["answer"]}</p></div>'
    return f"""
<section class="phero">
  <div class="wrap wrap-narrow">
    <div class="crumbs"><a href="index.html">Home</a> / <a href="insights.html">Insights</a> / {p["category"]}</div>
    <div class="eyebrow">{p["category"]} &middot; {p["read"]} read</div>
    <h1 style="font-size:clamp(2rem,4vw,3rem)">{p["title"]}</h1>
    <p class="lead dim" style="margin-top:1.2rem">{p["desc"]}</p>
    <p class="mono faint" style="font-size:.78rem;margin-top:1.4rem">By {p["author"]} &middot; Updated {p["date"]}</p>
  </div>
</section>
<section class="sec">
  <div class="wrap wrap-narrow prose">
    {ans}
    {p["html"]}
  </div>
</section>
{cta("Find out where your own site stands.",
     "The free audit runs twelve AI eligibility checks against your live URL in about sixty seconds.")}
"""


# --------------------------------------------------------------------------
# Render
# --------------------------------------------------------------------------
DIST = os.path.join(OUT, "dist")


def to_clean_urls(html, depth=0):
    """Rewrite flat .html links to root-absolute clean URLs for Cloudflare Pages."""
    html = re.sub(r'(href|src)="index\.html(#[^"]*)?"', lambda m: f'{m.group(1)}="/{m.group(2) or ""}"', html)
    html = re.sub(r'(href|src)="([a-z0-9\-]+)\.html(#[^"]*)?"',
                  lambda m: f'{m.group(1)}="/{m.group(2)}/{m.group(3) or ""}"', html)
    html = re.sub(r'(href|src)="assets/', r'\1="/assets/', html)
    return html


def render(title, desc, slug, body, schema=None):
    html = SHELL.format(title=title, desc=desc, slug=slug,
                        schema=schema or ORG_SCHEMA, nav=NAV, body=body, footer=FOOTER)
    return to_clean_urls(html)


def write(relpath, content):
    path = os.path.join(DIST, relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return len(content)


def copy_tree(src_name, dst_name=None):
    import shutil
    src = os.path.join(OUT, src_name)
    if not os.path.isdir(src):
        return 0
    dst = os.path.join(DIST, dst_name or src_name)
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    return sum(len(files) for _, _, files in os.walk(dst))


def copy_static():
    """static/ contents land at the site root (robots.txt, llms.txt, _headers...)."""
    import shutil
    src = os.path.join(OUT, "static")
    n = 0
    if os.path.isdir(src):
        for fn in os.listdir(src):
            s = os.path.join(src, fn)
            if os.path.isfile(s):
                shutil.copy2(s, os.path.join(DIST, fn))
                n += 1
    return n


def build():
    import shutil
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST, exist_ok=True)

    written = []
    posts = load_posts()

    # Blog listing is generated from the markdown files, not hardcoded.
    if posts:
        cards = "".join(f'''<a class="card card-link" href="/insights/{p["slug"]}/">
        <span class="card-num">{p["category"].upper()} &middot; {p["read"]}</span>
        <h3>{p["title"]}</h3><p>{p["desc"]}</p><span class="card-more">Read &rarr;</span></a>''' for p in posts)
        PAGES["insights"]["body"] = re.sub(
            r'(<div class="grid g3">)(.*?)(</div>\s*<div class="center mt3">)',
            lambda m: m.group(1) + cards + m.group(3),
            PAGES["insights"]["body"], flags=re.S)

    # Directory-style output so clean URLs work identically on Cloudflare Pages
    # and on any plain static server used for local review.
    for slug, p in PAGES.items():
        html = render(p["title"], p["desc"], p["slug"], p["body"])
        name = "index.html" if slug == "index" else os.path.join(slug, "index.html")
        written.append((name.replace("\\", "/"), write(name, html)))

    for p in posts:
        html = render(f'{p["title"]} | SVED Solution', p["desc"],
                      f'insights/{p["slug"]}/', post_page(p), post_schema(p))
        rel = os.path.join("insights", p["slug"], "index.html")
        written.append((rel.replace("\\", "/"), write(rel, html)))

    copy_tree("assets")
    copy_tree("admin")
    nstatic = copy_static()

    # sitemap
    urls = ["https://svedsolution.com/" + (p["slug"] or "") for p in PAGES.values()]
    urls += [f'https://svedsolution.com/insights/{p["slug"]}/' for p in posts]
    sm = ('<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls)
          + "</urlset>\n")
    write("sitemap.xml", sm)

    return written, len(posts), nstatic


if __name__ == "__main__":
    files, nposts, nstatic = build()
    for name, size in files:
        print("%-46s %8d bytes" % (name, size))
    print("\n%d pages + %d blog posts + %d static files -> %s"
          % (len(PAGES), nposts, nstatic, DIST))
