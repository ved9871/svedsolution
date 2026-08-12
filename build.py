# -*- coding: utf-8 -*-
"""
SVED Solution — static preview generator.
Stamps a shared shell (header/footer/head) around per-page content so the
preview works over file:// and converts cleanly to a Kadence WordPress build.
"""
import os, re, io, datetime as _dt

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
          "Blockchain, crypto and Web3 marketing &amp; SEO")

# Operating since 2018. Tax registration details are for invoicing only and are
# deliberately kept off the public site.
TRADE_NAME = "SVED Solution"
FOUNDED = "2018"

# Social profiles carried over from the Web3Tech Network group.
SOCIALS = [
    ("LinkedIn", "in", "https://www.linkedin.com/company/web3-tech-network/"),
    ("X", "X", "https://x.com/Web3TechNetwork"),
    ("YouTube", "YT", "https://www.youtube.com/channel/UCLEeUbTJUO4d7nALNrh1USQ"),
    ("Telegram", "TG", "https://t.me/web3tech_network"),
    ("Medium", "M", "https://medium.com/@web3technetwork"),
    ("Facebook", "f", "https://www.facebook.com/people/Web3-Tech-Network/61578176009714/"),
    ("Pinterest", "P", "https://pinterest.com/Web3technetwork/"),
]
FOUNDER_LINKEDIN = "https://www.linkedin.com/in/ved-prakash-s1990/"

# Team. Titles for Amit and Rahul are the ones they hold at RanqOne, the sister
# operation; confirm the SVED-specific titles before this goes into any pitch.
TEAM = [
    dict(name="Ved Prakash", initials="VP", role="Founder &amp; Head of Strategy",
         bio="Leads GEO and AI visibility strategy across every account. Runs the audits, "
             "sets the roadmaps and owns the monthly narrative reporting. Twelve years across "
             "SEO, paid search and analytics for brands in India, the UAE, the UK and the US.",
         focus=["Generative Engine Optimization", "Entity &amp; citation strategy", "Monthly narrative reporting"],
         links=[("LinkedIn", "https://www.linkedin.com/in/ved-prakash-s1990/")]),

    dict(name="Amit Kumar", initials="AK", role="Technical Head",
         bio="Owns everything under the content: crawl budget, index surgery, rendering "
             "strategy, Core Web Vitals and migrations. Builds the internal tooling the "
             "audits run on, including the AI visibility crawler behind our free audit.",
         focus=["Technical SEO &amp; site architecture", "Rendering &amp; Core Web Vitals", "Audit tooling &amp; automation"],
         links=[]),

    dict(name="Rahul Dhiman", initials="RD", role="Head of Growth",
         bio="Runs content, digital PR and the Tier-1 citation programme that gets clients "
             "named in AI answers. Leads white-label delivery for agency partners and manages "
             "the outreach relationships behind every placement.",
         focus=["Content &amp; digital PR", "Tier-1 citation placement", "White-label partnerships"],
         links=[]),
]


def team_cards():
    out = []
    for m in TEAM:
        focus = "".join(
            f'<div class="crow"><span class="lbl" style="text-align:left;flex:1">{f}</span></div>'
            for f in m["focus"])
        links = "".join(
            f'<a class="tlink" href="{u}" target="_blank" rel="noopener">{n} &rarr;</a>'
            for n, u in m["links"]) or \
            '<span class="faint" style="font-size:.78rem">Profile coming soon</span>'
        out.append(f'''<div class="card team-card">
          <div class="team-avatar">{m["initials"]}</div>
          <h3>{m["name"]}</h3>
          <p class="mono green" style="font-size:.78rem;margin-bottom:12px;letter-spacing:.06em;text-transform:uppercase">{m["role"]}</p>
          <p style="margin-bottom:16px">{m["bio"]}</p>
          <div style="margin-bottom:16px">{focus}</div>
          <div class="team-links">{links}</div>
        </div>''')
    return "".join(out)


TEAM_CARDS = team_cards()


def team_schema():
    people = ",".join(
        '{"@type":"Person","name":' + _j(m["name"]) +
        ',"jobTitle":' + _j(m["role"].replace("&amp;", "and")) +
        ',"worksFor":{"@type":"Organization","name":"SVED Solution","url":"https://svedsolution.com/"}' +
        (',"sameAs":[' + ",".join(_j(u) for _n, u in m["links"]) + ']' if m["links"] else '') +
        '}'
        for m in TEAM)
    return ('{"@context":"https://schema.org","@type":"AboutPage",'
            '"mainEntity":' + ORG_SCHEMA + ','
            '"about":[' + people + ']}')

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
      <a href="/services/answer-engine-optimization/">Answer Engine Optimization</a>
      <a href="/services/llm-seo/">LLM SEO</a>
      <a href="/services/ai-citation-entity-building/">AI Citation &amp; Entity Building</a>
      <a href="/services/ai-visibility-monitoring/">AI Visibility Monitoring</a>
      <a href="/services/google-ai-overviews-optimization/">Google AI Overviews</a>
      <div class="drop-head">Core SEO</div>
      <a href="/services/technical-seo/">Technical SEO</a>
      <a href="/services/semantic-on-page-seo/">Semantic &amp; On-Page SEO</a>
      <a href="/services/content-strategy/">Content Strategy</a>
      <a href="/services/link-building-digital-pr/">Link Building &amp; Digital PR</a>
      <a href="/services/ecommerce-seo/">Ecommerce SEO</a>
      <a href="/services/saas-b2b-seo/">SaaS &amp; B2B SEO</a>
      <a href="/services/local-seo/">Local SEO</a>
      <a href="/services/site-migrations/">Site Migrations</a>
      <a href="/services/white-label-seo/">White-Label SEO</a>
      <a href="/services/seo-consulting/">SEO Consulting</a>
      <a href="services.html">All 18 services &rarr;</a>
    </div>
  </div>
  <div class="has-drop">
    <a href="industries.html" data-nav="industries">Industries &#9662;</a>
    <div class="drop" style="min-width:460px">
      <div class="drop-head">Industries we deliver for</div>
      <a href="healthcare-ivf-seo.html">Healthcare, IVF &amp; Clinics</a>
      <a href="ecommerce-d2c-seo.html">Ecommerce &amp; D2C</a>
      <a href="saas-ai-product-seo.html">SaaS &amp; AI Products</a>
      <a href="web3-crypto-seo.html">Web3, Crypto &amp; Blockchain</a>
      <a href="it-services-app-development-seo.html">IT Services &amp; App Development</a>
      <a href="education-edtech-seo.html">Education &amp; EdTech</a>
      <a href="financial-services-seo.html">Financial Services</a>
      <a href="local-business-seo.html">Local, Retail &amp; Studios</a>
      <a href="agency-white-label-seo.html">Agencies &amp; White-Label</a>
      <a href="industries.html">All industries &rarr;</a>
    </div>
  </div>
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
          {"".join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}" title="{n}">{ic}</a>' for n, ic, u in SOCIALS)}
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
        <form class="sved-form" data-type="newsletter">
          <input type="email" name="email" placeholder="you@company.com" aria-label="Email" required>
          <button class="btn btn-primary btn-sm" type="submit" style="width:100%;justify-content:center">Subscribe</button>
          <p class="form-status" role="status"></p>
        </form>
        <p class="faint" style="font-size:.76rem;margin-top:10px">Free with the AI Search Playbook PDF.</p>
      </div>
    </div>
    <div class="foot-bottom">
      <div>&copy; 2026 {TRADE_NAME}. All rights reserved.</div>
      <div style="display:flex;gap:20px;flex-wrap:wrap">
        <a href="sitemap.html" style="color:var(--text-faint)">Sitemap</a>
        <a href="privacy.html" style="color:var(--text-faint)">Privacy Policy</a>
        <a href="terms.html" style="color:var(--text-faint)">Terms of Service</a>
        <a href="ai-visibility-audit.html" style="color:var(--text-faint)">Free AI Audit</a>
      </div>
    </div>
  </div>
</footer>
"""

# GA4 is configured inside GTM, not hardcoded in the page. Kept here only for
# reference — nothing substitutes it any more.
GA4_MEASUREMENT_ID = "G-JJXBTFSP4Z"
GTM_ID = "GTM-M94D8W4K"

# Injected via placeholder rather than inline in SHELL: the snippet is full of
# braces and SHELL goes through str.format(), where every { would need doubling.
#
# GOOGLE'S SNIPPET, VERBATIM. Do not modify it.
#
# A previous version deferred the container download to requestIdleCallback to
# save mobile LCP. That broke GTM's own "Test your website" verifier, which
# loads the page and looks for the gtm.js request during load — deferred, there
# is nothing for it to find, and it reports "Google tag wasn't detected".
# Tag Assistant and Google Ads/GA4 verification behave the same way.
#
# The performance cost is real (mobile LCP roughly 3.1s -> 5.8s) but detection
# and correct tag firing matter more. Reduce the cost inside the container
# instead: fewer tags, native GA4 rather than custom HTML tags, and triggers
# scoped to the pages that need them.
GTM_HEAD = """<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM_CONTAINER_ID');</script>
<!-- End Google Tag Manager -->"""

GTM_BODY = """<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM_CONTAINER_ID"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""
BOOKING_URL = "https://cal.com/sved-solution/15min"
CALENDLY = BOOKING_URL  # placeholder token name kept; every page substitutes BOOKING_URL
TAGLINE = "Top 1&#37; SEO Service Provider in India"

SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!--GTM-HEAD-->
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://svedsolution.com/{slug}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<meta name="author" content="Ved Prakash">
<meta name="keywords" content="{keywords}">
<meta property="og:site_name" content="SVED Solution">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_IN">
<meta property="og:url" content="https://svedsolution.com/{slug}">
<meta property="og:image" content="https://svedsolution.com/assets/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://svedsolution.com/assets/og-image.svg">
<meta name="geo.region" content="IN-WB">
<meta name="geo.placename" content="Kolkata">
<meta name="theme-color" content="#0B1219">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/assets/favicon-16.png">
<link rel="shortcut icon" href="/assets/favicon.ico">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://www.googletagmanager.com" crossorigin>
<link rel="dns-prefetch" href="https://www.googletagmanager.com">
<link rel="preload" href="/assets/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/poppins-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/style.css">
<script type="application/ld+json">{schema}</script>
</head>
<body>
<!--GTM-BODY-->
<a href="#main" class="skip-link">Skip to content</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a href="index.html" class="logo" aria-label="SVED Solution home">{logo}</a>
    {nav}
    <div class="header-cta">
      <a href="ai-visibility-audit.html" class="btn btn-ghost btn-sm">Free AI Audit</a>
      <a href="CALENDLY_URL" target="_blank" rel="noopener" class="btn btn-primary btn-sm">Book a call</a>
      <button class="nav-toggle" id="navToggle" aria-label="Open menu" aria-expanded="false">&#9776;</button>
    </div>
  </div>
</header>
<main id="main">
{body}
</main>
{footer}

<!-- WhatsApp: fixed bottom-right, opens a chat with the sales line -->
<a class="wa-fab" href="https://api.whatsapp.com/send?phone=WHATSAPP_NUMBER&amp;text=Hi%20SVED%20Solution%2C%20I%27d%20like%20to%20discuss%20SEO%20and%20AI%20visibility%20for%20my%20website."
   target="_blank" rel="noopener" aria-label="Chat with us on WhatsApp">
  <svg viewBox="0 0 32 32" width="28" height="28" aria-hidden="true">
    <path fill="currentColor" d="M16 3C8.8 3 3 8.8 3 16c0 2.3.6 4.5 1.7 6.4L3 29l6.8-1.8c1.9 1 4 1.6 6.2 1.6 7.2 0 13-5.8 13-13S23.2 3 16 3zm0 23.4c-2 0-3.9-.5-5.5-1.5l-.4-.2-4 1.1 1.1-3.9-.3-.4A10.4 10.4 0 0 1 5.6 16c0-5.7 4.7-10.4 10.4-10.4S26.4 10.3 26.4 16 21.7 26.4 16 26.4zm5.9-7.8c-.3-.2-2-1-2.3-1.1-.3-.1-.5-.2-.8.1l-.9 1.1c-.2.2-.4.2-.7.1-1.7-.7-3.1-2-4-3.6-.2-.3 0-.5.1-.7l.7-.9c.2-.2.1-.5 0-.7l-1-2.3c-.2-.4-.4-.4-.7-.4h-.7c-.3 0-.7.1-1 .4-1.1 1-1.4 2.6-.9 4.1.9 2.9 3.9 6.1 7.3 7 1.3.3 2.6.3 3.6-.4.5-.3.8-.9.9-1.5.1-.4.1-.9-.1-1.1z"/>
  </svg>
  <span>WhatsApp</span>
</a>

<script src="assets/app.js"></script>
</body>
</html>
"""

# Inline SVG wordmark — no external request, scales crisply, matches the palette.
LOGO_SVG = """<svg class="logo-svg" width="132" height="30" viewBox="0 0 132 30" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="SVED Solution">
  <defs><linearGradient id="svg-grad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#00FFB2"/><stop offset="100%" stop-color="#00A5FF"/>
  </linearGradient></defs>
  <rect x="0" y="2" width="26" height="26" rx="7" fill="url(#svg-grad)"/>
  <path d="M7.6 19.4c.9.8 2.2 1.3 3.5 1.3 1.5 0 2.4-.6 2.4-1.6 0-1-.8-1.4-2.4-1.8l-1-.2c-2.2-.5-3.4-1.6-3.4-3.5 0-2.2 1.8-3.7 4.4-3.7 1.5 0 2.9.5 3.8 1.3l-1.2 1.8c-.7-.6-1.7-1-2.7-1-1.2 0-2 .5-2 1.4 0 .8.6 1.2 2.1 1.6l1 .2c2.4.6 3.7 1.6 3.7 3.6 0 2.4-2 3.9-4.8 3.9-1.9 0-3.6-.6-4.7-1.7z" fill="#070C12"/>
  <path d="M18.4 9.9h2.6l-3.9 11h-2.4z" fill="#070C12" opacity=".55"/>
  <text x="34" y="21" font-family="Poppins, sans-serif" font-size="17" font-weight="700" letter-spacing="-.4" fill="currentColor">SVED</text>
  <circle cx="93" cy="19" r="2.6" fill="#00FFB2"/>
  <text x="101" y="21" font-family="Poppins, sans-serif" font-size="10.5" font-weight="500" letter-spacing=".4" fill="#8496A9">SEO</text>
</svg>"""

ORG_SCHEMA = """{
  "@context":"https://schema.org",
  "@type":"ProfessionalService",
  "@id":"https://svedsolution.com/#organization",
  "name":"SVED Solution",
  "alternateName":"SVED",
  "url":"https://svedsolution.com/",
  "email":"hello@svedsolution.com",
  "description":"AI visibility and 360 SEO agency specialising in Generative Engine Optimization (GEO), Answer Engine Optimization (AEO) and LLM SEO.",
  "slogan":"Top 1% SEO Service Provider in India",
  "areaServed":["US","GB","CA","AU","IN","AE"],
  "knowsAbout":["Generative Engine Optimization","Answer Engine Optimization","LLM SEO","Technical SEO","Semantic SEO","Entity SEO","AI Overviews"],
  "address":[
    {"@type":"PostalAddress","streetAddress":"502, 5th Floor, API World Tower, 22 Sheikh Zayed Road","addressLocality":"Dubai","postalCode":"27091","addressCountry":"AE"},
    {"@type":"PostalAddress","streetAddress":"Unit 909, Godrej Genesis Building, Block EP&GP, Sector V, Bidhannagar","addressLocality":"Kolkata","addressRegion":"West Bengal","postalCode":"700091","addressCountry":"IN"},
    {"@type":"PostalAddress","addressLocality":"Oswego","addressRegion":"NY","postalCode":"13126","addressCountry":"US"}
  ],
  "telephone":"+917846045690",
  "foundingDate":"2018",
  "priceRange":"$$",
  "founder":{"@type":"Person","name":"Ved Prakash","jobTitle":"Founder & Head of Strategy","sameAs":["https://www.linkedin.com/in/ved-prakash-s1990/"]},
  "hasCredential":[
    {"@type":"EducationalOccupationalCredential","credentialCategory":"certification","name":"Semrush Certified"},
    {"@type":"EducationalOccupationalCredential","credentialCategory":"certification","name":"Microsoft Advertising Certified"},
    {"@type":"EducationalOccupationalCredential","credentialCategory":"certification","name":"Google Shopping Certified"},
    {"@type":"EducationalOccupationalCredential","credentialCategory":"certification","name":"Google Analytics 4 Certified"}
  ],
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
      <div class="badge"><span class="dot"></span> Top 1&#37; SEO Service Provider in India</div>
      <h1>Google ranks pages.<br>AI <span class="hl">recommends brands</span>.</h1>
      <p class="hero-sub">SVED Solution is a 360&deg; SEO agency built for the answer engine era. We make your brand the one ChatGPT, Perplexity, Gemini, Claude, DeepSeek and Copilot name &mdash; then we show you the citation count.</p>
      <div class="btn-row">
        <a class="btn btn-primary btn-lg" href="ai-visibility-audit.html">Run a free AI visibility audit</a>
        <a class="btn btn-ghost btn-lg" href="CALENDLY_URL" target="_blank" rel="noopener">Book a 15-min call</a>
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
    <!--PLATFORMS-->
  </div>
</section>

<section class="sec-sm">
  <div class="wrap">
    <p class="faint center mono" style="font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;margin-bottom:22px">Certified &amp; accredited</p>
    <!--CERTS-->
  </div>
</section>

<section class="sec-sm band-alt">
  <div class="wrap">
    <p class="faint center mono" style="font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;margin-bottom:22px">19 brands across 10 industries &middot; UK &middot; India &middot; UAE &middot; USA</p>
    <div class="clogos" style="justify-content:center">
      <span class="clogo">IVF &amp; fertility clinics</span>
      <span class="clogo">Cosmetic dermatology</span>
      <span class="clogo">Physiotherapy &amp; rehab</span>
      <span class="clogo">Specialist ecommerce, UK</span>
      <span class="clogo">Bio-active skincare D2C</span>
      <span class="clogo">Ayurvedic wellness</span>
      <span class="clogo">Fashion label, London</span>
      <span class="clogo">AI transcription SaaS</span>
      <span class="clogo">App development, Dubai</span>
      <span class="clogo">Enterprise software, India</span>
      <span class="clogo">Tech publishing platform</span>
      <span class="clogo">Skills university</span>
      <span class="clogo">Mortgage network, UK</span>
      <span class="clogo">Security systems, UK</span>
      <span class="clogo">Layer-2 crypto protocol</span>
      <span class="clogo">Web3 agency</span>
      <span class="clogo">Trading &amp; distribution</span>
      <span class="clogo">Creative arts studio</span>
    </div>
    <p class="faint center" style="font-size:.79rem;margin-top:18px">Client names withheld under NDA. We will introduce you to a reference in your category during scoping.</p>
  </div>
</section>

<section class="sec band-dark">
  <div class="wrap">
    <div class="sec-head center">
      <div class="eyebrow">The market</div>
      <h2>GEO is a $17 billion market by 2034.</h2>
      <p class="lead dim">Independent forecasting, not our opinion. The window to establish category authority is open now and closing as budgets move.</p>
    </div>
    <div class="stat-band">
      <div class="stat"><b>40.6&#37;</b><span>Global GEO market CAGR, 2026&ndash;2034</span></div>
      <div class="stat"><b>$17.1B</b><span>Forecast global GEO market by 2034, from $1.09B in 2026</span></div>
      <div class="stat"><b>45.1&#37;</b><span>Asia-Pacific CAGR &mdash; the fastest-growing region worldwide</span></div>
      <div class="stat"><b>65&#37;</b><span>Of digital enterprises already investing in generative AI optimisation</span></div>
      <div class="stat"><b>30&#37;</b><span>Potential reduction in customer acquisition cost via GEO</span></div>
    </div>
    <p class="faint center" style="font-size:.8rem;margin-top:18px">Source: Dimension Market Research, Generative Engine Optimization Market report.</p>
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

<section class="sec">
  <div class="wrap">
    <div class="sec-head" style="display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap;max-width:none">
      <div style="max-width:640px">
        <div class="eyebrow">Latest insights</div>
        <h2 style="margin-bottom:.6rem">What we are learning, published as we learn it</h2>
        <p class="lead dim mb0">Frameworks we run on live accounts, written up in full. If we publish a process, it is the one we use.</p>
      </div>
      <a class="btn btn-ghost" href="insights.html">All articles</a>
    </div>
    <!--LATEST-POSTS-->
  </div>
</section>

<section class="sec band-alt">
  <div class="wrap">
    <div class="grid g2" style="gap:48px;align-items:center">
      <div>
        <div class="eyebrow">Watch</div>
        <h2 style="margin-bottom:1rem">SEO and Web3 growth, on video</h2>
        <p class="lead dim">Teardowns, walkthroughs and strategy breakdowns from our group channel. Every full audit we run also ships with a private recorded walkthrough of your own site.</p>
        <div class="btn-row" style="margin-top:1.8rem">
          <a class="btn btn-primary" href="https://www.youtube.com/channel/UCLEeUbTJUO4d7nALNrh1USQ" target="_blank" rel="noopener">Subscribe on YouTube</a>
          <a class="btn btn-ghost" href="videos.html">More videos</a>
        </div>
      </div>
      <!-- Facade: a real iframe pulls roughly 1MB of player JavaScript on load
           even with loading=lazy. The embed is injected on click instead. -->
      <div class="yt-embed yt-facade" data-yt="videoseries?list=UULFLEeUbTJUO4d7nALNrh1USQ"
           role="button" tabindex="0" aria-label="Play video from the Web3Tech Network channel">
        <div class="yt-face">
          <div class="yt-play" aria-hidden="true">&#9654;</div>
          <div class="yt-label">
            <strong>SEO &amp; Web3 growth, on video</strong>
            <span>Web3Tech Network &middot; YouTube</span>
          </div>
        </div>
      </div>
    </div>
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
        <!-- type=text, not url: type=url makes the browser reject "example.com"
             before it ever reaches the API. The API resolves the variations. -->
        <input type="text" id="audit-url" inputmode="url" autocapitalize="off" spellcheck="false"
               placeholder="example.com" required aria-label="Website address">
        <button class="btn btn-primary btn-lg" id="audit-run" type="submit">Run free audit</button>
      </form>
      <p class="faint" style="font-size:.82rem;margin-top:12px">Enter it any way you like &mdash; <span class="mono">example.com</span>, <span class="mono">www.example.com</span> or the full https address. We work out which version resolves. We crawl public pages only, and store nothing unless you ask for the full report.</p>
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
    # Must match where build() actually writes this page, or the canonical
    # points at a 404 and search engines drop the URL.
    slug="generative-engine-optimization/",
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


SERVICE_URLS = {
    "aeo": "/services/answer-engine-optimization/",
    "llm-seo": "/services/llm-seo/",
    "citation": "/services/ai-citation-entity-building/",
    "monitoring": "/services/ai-visibility-monitoring/",
    "aio": "/services/google-ai-overviews-optimization/",
    "technical": "/services/technical-seo/",
    "semantic": "/services/semantic-on-page-seo/",
    "content": "/services/content-strategy/",
    "links": "/services/link-building-digital-pr/",
    "ecommerce": "/services/ecommerce-seo/",
    "saas": "/services/saas-b2b-seo/",
    "local": "/services/local-seo/",
    "international": "/services/international-seo/",
    "programmatic": "/services/programmatic-seo/",
    "migration": "/services/site-migrations/",
    "whitelabel": "/services/white-label-seo/",
    "consulting": "/services/seo-consulting/",
    "geo": "generative-engine-optimization.html",
}


def svc(anchor, num, name, desc, bullets, tag="core"):
    lis = "".join(f"<li>{b}</li>" for b in bullets)
    url = SERVICE_URLS.get(anchor, "services.html")
    return f"""
<div class="card" id="{anchor}" style="scroll-margin-top:90px;display:flex;flex-direction:column">
  <span class="card-num">{num} &middot; {tag.upper()}</span>
  <h3>{name}</h3>
  <p style="margin-bottom:14px">{desc}</p>
  <ul style="font-size:.88rem;color:var(--text-faint);padding-left:1.1em;margin:0 0 18px">{lis}</ul>
  <div style="margin-top:auto;display:flex;gap:8px;flex-wrap:wrap">
    <a class="btn btn-ghost btn-sm" href="{url}">Service details</a>
    <a class="btn btn-ghost btn-sm" href="ai-visibility-audit.html">Free audit</a>
    <a class="btn btn-primary btn-sm" href="CALENDLY_URL" target="_blank" rel="noopener">Book a call</a>
  </div>
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
# Industries are grounded in the real client roster, so every page can name the
# work rather than describe a hypothetical vertical.
INDUSTRIES = [
    dict(slug="healthcare-ivf-seo", name="Healthcare, IVF &amp; Clinics", icon="&#10010;",
         short="YMYL-grade E-E-A-T, credentialed authorship, treatment-page architecture and multi-location local visibility. AI is most conservative here, so entity trust decides everything.",
         clients=["2 &times; IVF &amp; fertility clinic groups, Delhi NCR",
                  "Laser &amp; cosmetic dermatology clinic, India",
                  "Physiotherapy &amp; rehabilitation practice"],
         kw="healthcare SEO India, IVF clinic SEO, fertility clinic SEO, dermatology SEO, medical SEO agency",
         pains=["Treatment pages that rank but never convert enquiries",
                "Competing clinics outranking you on every city + treatment query",
                "AI Overviews answering patient questions without naming your clinic",
                "Multiple locations cannibalising each other's rankings"],
         plays=["MedicalWebPage, Physician and MedicalClinic schema on every treatment page",
                "Doctor entity building: credentials, registrations, Person schema, authored content",
                "City + treatment landing architecture that scales without cannibalisation",
                "Review velocity systems on Google Business Profile and Practo",
                "Patient-question content built as direct answers for AI retrieval"]),

    dict(slug="ecommerce-d2c-seo", name="Ecommerce &amp; D2C", icon="&#9679;",
         short="Category architecture, faceted navigation, variant schema and shopping-surface visibility. Our deepest AI citation dataset comes from this vertical.",
         clients=["Specialist hobby retailer, UK &mdash; 1,393 keywords",
                  "Bio-active skincare D2C brand, India",
                  "Ayurvedic &amp; herbal wellness brand, India",
                  "Fashion &amp; lifestyle label, London"],
         kw="ecommerce SEO India, D2C SEO agency, Shopify SEO, product page SEO, ecommerce GEO",
         pains=["Category pages outranked by marketplaces you also sell on",
                "Thousands of variant URLs burning crawl budget",
                "Product pages invisible in AI shopping answers",
                "Traffic growing while revenue stays flat"],
         plays=["Money-page keyword mapping before a single page is written",
                "Product, Offer, AggregateRating and Review schema across the catalogue",
                "Faceted navigation and parameter control to end index bloat",
                "Comparison and buying-guide content — the format AI quotes most",
                "GA4 ecommerce measurement so organic revenue is provable"]),

    dict(slug="saas-ai-product-seo", name="SaaS &amp; AI Products", icon="&#9636;",
         short="Pipeline over pageviews. Bottom-of-funnel first, comparison and alternatives pages, then integration-led programmatic expansion.",
         clients=["AI transcription &amp; translation platform &mdash; 55+ languages, used by global universities"],
         kw="SaaS SEO agency, B2B SaaS SEO, AI product SEO, SaaS GEO services",
         pains=["Buyers evaluate you in ChatGPT before they ever load your site",
                "Competitors own every “best X” and “alternatives” query",
                "Blog traffic that never becomes a trial",
                "No presence on G2, Capterra or Product Hunt"],
         plays=["Inverted-funnel sequencing: BoFu commercial pages ship first",
                "Comparison, alternatives and integration page systems",
                "SoftwareApplication and Offer schema with pricing exposed",
                "G2, Capterra, Product Hunt and Reddit citation stack",
                "Documentation SEO, which AI models retrieve heavily"]),

    dict(slug="web3-crypto-seo", name="Web3, Crypto &amp; Blockchain", icon="&#9672;",
         short="Delivered with our subsidiary Web3Tech Network: community-first citation building, tokenomics documentation SEO and the credibility signals a sceptical category demands.",
         clients=["Web3Tech Network &mdash; our own subsidiary",
                  "Layer-2 staking &amp; node protocol on Polygon"],
         kw="Web3 SEO, crypto SEO agency, blockchain SEO, token marketing, NFT SEO",
         pains=["Paid channels ban crypto advertising outright",
                "Search engines apply extra scrutiny to token projects",
                "Community lives on Telegram and X, invisible to search",
                "Whitepapers and docs that no crawler can parse"],
         plays=["Community management and social campaigns across crypto channels",
                "Influencer marketing matched to project stage and chain",
                "SEO built for tokenomics docs, whitepapers and explorer pages",
                "Reddit, Medium and Telegram citation footprint",
                "Trust signals: audits, team entities, verifiable contract data"]),

    dict(slug="it-services-app-development-seo", name="IT Services &amp; App Development", icon="&#9881;",
         short="Long sales cycles, high deal values and buyers who compare five vendors in one AI prompt. Service-page depth plus founder authority.",
         clients=["Mobile app development firm, Dubai UAE",
                  "Enterprise software &amp; GCC provider, Kolkata",
                  "Independent technology publishing platform"],
         kw="IT services SEO, app development company SEO, software company SEO, B2B tech SEO",
         pains=["Indistinguishable from a hundred other dev agencies in search",
                "Enquiries arrive price-shopping, not pre-sold",
                "Geo-targeted queries dominated by directories like Clutch",
                "No named expert associated with the company"],
         plays=["Service × technology × geography page architecture",
                "Case-study content with real, verifiable engineering detail",
                "Clutch, GoodFirms and DesignRush citation placement",
                "Founder-as-entity: bylines, podcasts, technical writing",
                "Documentation and open-source artefacts as citation bait"]),

    dict(slug="education-edtech-seo", name="Education &amp; EdTech", icon="&#9998;",
         short="Course and programme schema, admissions-intent capture, and the institutional entity authority AI models require before recommending a place to study.",
         clients=["UGC-recognised skills university &mdash; 650+ industry partners"],
         kw="education SEO India, university SEO, EdTech SEO, admissions SEO, course page SEO",
         pains=["Admissions traffic concentrated into a short annual window",
                "Aggregator sites outranking the institution's own pages",
                "Prospective students asking AI which university to choose",
                "Course pages with no structured data at all"],
         plays=["Course, EducationalOccupationalProgram and FAQPage schema",
                "Programme × specialisation × eligibility page architecture",
                "Placement and outcome data published as citable evidence",
                "Accreditation and recognition signals made machine-readable",
                "Student-question content built for direct AI answers"]),

    dict(slug="financial-services-seo", name="Financial Services &amp; Insurance", icon="&#9650;",
         short="Regulatory-safe content, calculator and tool pages that earn citations, and the authorship signals YMYL categories demand before anything ranks.",
         clients=["Mortgage &amp; insurance network group, United Kingdom"],
         kw="financial services SEO, fintech SEO agency, insurance SEO, mortgage broker SEO, YMYL SEO",
         pains=["Compliance review slowing every piece of content",
                "YMYL scrutiny suppressing pages that would otherwise rank",
                "Intermediary and B2B audiences that generic SEO misses",
                "Regulatory constraints on claims and comparisons"],
         plays=["Compliance-aware editorial workflow with named reviewers",
                "Calculators and tools built as linkable, citable assets",
                "Author credentials and FinancialService schema",
                "Regulatory and industry-body citation footprint",
                "Adviser-facing content distinct from consumer content"]),

    dict(slug="local-business-seo", name="Local, Retail &amp; Studios", icon="&#8962;",
         short="Service-area architecture, Google Business Profile, review velocity and the local entity signals that decide map-pack placement.",
         clients=["Creative arts &amp; play studio", "Trading &amp; distribution business"],
         kw="local SEO India, Google Business Profile optimization, local SEO agency, map pack SEO",
         pains=["Invisible in the map pack despite being physically closest",
                "Inconsistent name, address and phone across directories",
                "Competitors with more reviews winning by default",
                "“Near me” queries going to aggregators"],
         plays=["Google Business Profile optimisation and posting cadence",
                "NAP consistency audit and citation cleanup",
                "LocalBusiness schema with accurate service-area markup",
                "Review generation systems that stay policy-compliant",
                "Location and service-area landing page architecture"]),

    dict(slug="security-loss-prevention-seo", name="Security &amp; Loss Prevention", icon="&#9919;",
         short="Niche B2B with tiny search volumes and very high deal values. Category-education content plus specification-grade product pages that procurement teams and AI both trust.",
         clients=["Security fog &amp; loss-prevention manufacturer, UK &mdash; 2 to 95 keywords in 12 months"],
         kw="security systems SEO, B2B security SEO, loss prevention marketing, security technology SEO",
         pains=["Search volumes too small for conventional keyword strategy",
                "Specifiers and installers research very differently from end users",
                "Long procurement cycles with several decision-makers",
                "Category terms dominated by generic dictionary results"],
         plays=["Category-education content that creates demand rather than chasing it",
                "Specification-grade product pages built for technical evaluation",
                "Standards and compliance content, for example EN50131",
                "Application-led architecture: retail, ATM, warehouse, jewellery",
                "Trade publication and installer-network citation building"]),

    dict(slug="agency-white-label-seo", name="Agencies &amp; White-Label", icon="&#9783;",
         short="Full delivery under your brand, under NDA. Audits through retained execution with branded reporting. We stay invisible to your client.",
         clients=["Confidential &mdash; NDA"],
         kw="white label SEO India, white label GEO, SEO reseller, outsourced SEO agency",
         pains=["Clients asking for GEO you cannot yet deliver",
                "Capacity ceiling blocking new retainers",
                "Cost of hiring senior SEO in-house",
                "Reporting that eats delivery hours"],
         plays=["NDA-backed anonymous delivery under your brand",
                "Branded reporting in your template and tone",
                "Scalable capacity from single audits to full retainers",
                "Your account manager stays the only client contact",
                "GEO and AI visibility as a new line you can sell tomorrow"]),
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
      {"".join(f'''<a class="card card-link" href="/{i["slug"]}/">
        <div class="card-icon">{i["icon"]}</div><h3>{i["name"]}</h3><p>{i["short"]}</p>
        <span class="card-more">{i["name"].split("&amp;")[0].strip()} SEO &rarr;</span></a>''' for i in INDUSTRIES)}
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

    <div class="card" style="padding:0;overflow:hidden;margin-bottom:24px">
      <div style="padding:36px 36px 0"><span class="card-num">CASE 02 &middot; CRAWFORD'S METAL DETECTING &middot; UK ECOMMERCE</span>
        <h2 style="margin-bottom:.4rem">Ranking #1 for a 27,100-a-month head term</h2>
        <p class="dim" style="max-width:70ch">A UK specialist retailer competing against manufacturer sites and national chains. Category architecture, product schema and a buying-guide content programme took the single most valuable term in the category outright.</p>
      </div>
      <div class="kpis" style="border:0;border-radius:0;margin-top:28px">
        <div class="kpi"><div class="kpi-val">#1</div><div class="kpi-lab">for &ldquo;metal detectors&rdquo; &mdash; 27,100 searches/mo</div></div>
        <div class="kpi"><div class="kpi-val">1,393</div><div class="kpi-lab">organic keywords ranking</div></div>
        <div class="kpi"><div class="kpi-val">853</div><div class="kpi-lab">referring domains</div></div>
        <div class="kpi"><div class="kpi-val">2,923</div><div class="kpi-lab">AI citations in 29 days</div></div>
      </div>
      <div style="padding:28px 36px 36px">
        <p style="font-size:.93rem;color:var(--text-dim);margin-bottom:0"><strong>Also holding position 1 for:</strong> &ldquo;metal detector shops near me&rdquo;, &ldquo;minelab manticore&rdquo;, &ldquo;waterproof metal detector&rdquo;, &ldquo;pinpointer metal detector&rdquo;, &ldquo;metal detecting shovels&rdquo; and &ldquo;gold panning kit&rdquo;. The buying-guide content also drives the AI citation volume in Case 01 &mdash; the same pages do both jobs.</p>
      </div>
    </div>

    <div class="card" style="padding:0;overflow:hidden;margin-bottom:24px">
      <div style="padding:36px 36px 0"><span class="card-num">CASE 03 &middot; SMOKE SCREEN &middot; UK B2B SECURITY</span>
        <h2 style="margin-bottom:.4rem">From 2 ranking keywords to 95 in twelve months</h2>
        <p class="dim" style="max-width:70ch">Security fog systems: a niche B2B category with low search volume, high deal values and long procurement cycles. We built category-education content and specification-grade product pages from a standing start.</p>
      </div>
      <div class="kpis" style="border:0;border-radius:0;margin-top:28px">
        <div class="kpi"><div class="kpi-val">2 &rarr; 95</div><div class="kpi-lab">ranking keywords, Aug 2025 to Jul 2026</div></div>
        <div class="kpi"><div class="kpi-val">0 &rarr; 213</div><div class="kpi-lab">monthly organic sessions</div></div>
        <div class="kpi"><div class="kpi-val">7</div><div class="kpi-lab">keywords now in the top 3</div></div>
        <div class="kpi"><div class="kpi-val">316</div><div class="kpi-lab">referring domains</div></div>
      </div>
      <div style="padding:28px 36px 36px">
        <p style="font-size:.93rem;color:var(--text-dim);margin-bottom:0"><strong>Why the numbers look small and are not:</strong> in a category where a single installation is a five-figure contract, 213 highly-qualified monthly sessions against a previous baseline of zero is a channel that pays for itself several times over. Volume is the wrong metric here; qualification is the right one.</p>
      </div>
    </div>

    <div class="grid g2">
      <div class="card">
        <span class="card-num">CASE 04 &middot; B2B SERVICES &middot; UNITED STATES</span>
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
    <form class="audit-form sved-form" data-type="newsletter" style="max-width:520px;margin:2rem auto 0;justify-content:center">
      <input type="email" name="email" placeholder="you@company.com" aria-label="Email" required style="flex:1 1 320px;width:auto">
      <button class="btn btn-primary" type="submit">Get the playbook</button>
      <p class="form-status" role="status" style="flex:1 1 100%"></p>
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

<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">Our stack</div>
      <h2>The tools every engagement runs on</h2>
      <p class="lead dim">No black boxes. You get access to the same dashboards we work from, and every claim in your report traces back to one of these sources.</p>
    </div>
    <!--TOOLS-->
  </div>
</section>

<section class="sec band-dark">
  <div class="wrap">
    <div class="sec-head center">
      <div class="eyebrow">Credentials</div>
      <h2>Certified across the platforms that matter</h2>
    </div>
    <!--CERTS-->
  </div>
</section>

{cta("Want the SOP library for your in-house team?",
     "Consulting engagements include the full 39-SOP library and a handover session at $30 per hour.",
     primary=("Book a consulting session", CALENDLY),
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
    <div class="grid g3">{TEAM_CARDS}</div>
    <p class="faint center" style="font-size:.83rem;margin-top:24px">Person schema is wired to every team member, because founder and specialist entity association is a direct AI visibility signal.</p>
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
        <form class="card sved-form" id="contact-form" style="padding:32px">
          <h3 style="margin-bottom:20px">Start a conversation</h3>
          <div class="grid g2" style="gap:14px;margin-bottom:14px">
            <input name="name" type="text" placeholder="Full name" required aria-label="Full name">
            <input name="email" type="email" placeholder="Work email" required aria-label="Work email">
          </div>
          <input name="phone" type="tel" placeholder="Phone or WhatsApp (optional)" aria-label="Phone" style="margin-bottom:14px">
          <input name="website" type="text" placeholder="Website URL" aria-label="Website" style="margin-bottom:14px">
          <select name="service" aria-label="Service" style="margin-bottom:14px">
            <option value="">What do you need help with?</option>
            <option>AI visibility / GEO</option>
            <option>AI Overviews traffic loss</option>
            <option>Technical SEO / migration</option>
            <option>Content &amp; rankings</option>
            <option>Ecommerce SEO</option>
            <option>Local SEO</option>
            <option>White-label delivery</option>
            <option>Hourly consulting ($30/hr)</option>
          </select>
          <select name="revenue" aria-label="Monthly revenue" style="margin-bottom:14px">
            <option value="">Monthly revenue (helps us scope)</option>
            <option>Under $50k</option><option>$50k&ndash;$250k</option>
            <option>$250k&ndash;$1M</option><option>$1M+</option>
          </select>
          <textarea name="message" rows="4" placeholder="What is happening? Paste your audit score if you have one." aria-label="Message" style="margin-bottom:18px"></textarea>
          <input type="text" name="company_website" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px" >
          <button class="btn btn-primary btn-lg" type="submit" style="width:100%;justify-content:center">Send message</button>
          <p class="form-status" role="status"></p>
          <p class="faint" style="font-size:.78rem;margin-top:12px;text-align:center">We reply within one business day. Or <a href="CALENDLY_URL" target="_blank" rel="noopener">book a 15-minute call</a>.</p>
        </form>
      </div>
      <div>
        <div class="card" style="margin-bottom:20px">
          <h3>Book directly</h3>
          <p style="margin-bottom:18px">Skip the form. Grab a 30-minute slot with the strategist who will run your audit.</p>
          <a class="btn btn-primary btn-lg" style="width:100%;justify-content:center" href="CALENDLY_URL" target="_blank" rel="noopener">Book a 15-minute call</a>
          <p class="faint" style="font-size:.8rem;margin-top:12px;text-align:center">Opens our booking page. Pick any slot that suits you.</p>
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


# ==========================================================================
# AI platforms, certifications and tooling
#
# Platform marks are drawn as inline SVG rather than hot-linked. The strict
# CSP blocks external images, third-party logo files carry trademark and
# hosting constraints, and inline SVG costs zero requests. Each is a simple
# geometric mark plus the platform name in text - referential use, not a
# reproduction of the official logo.
# ==========================================================================
AI_PLATFORMS = [
    ("ChatGPT", "OpenAI", "#10A37F",
     '<path d="M29.7 13.4a8 8 0 0 0-.7-6.6 8.1 8.1 0 0 0-8.7-3.9A8 8 0 0 0 14.2.2a8.1 8.1 0 0 0-7.7 5.6A8 8 0 0 0 1.2 9.7a8.1 8.1 0 0 0 1 9.5 8 8 0 0 0 .7 6.6 8.1 8.1 0 0 0 8.7 3.9 8 8 0 0 0 6.1 2.7 8.1 8.1 0 0 0 7.7-5.6 8 8 0 0 0 5.3-3.9 8.1 8.1 0 0 0-1-9.5zM17.7 29.9a6 6 0 0 1-3.9-1.4l.2-.1 6.5-3.7a1 1 0 0 0 .5-.9v-9.2l2.7 1.6v7.5a6 6 0 0 1-6 6.2zM4.8 24.4a6 6 0 0 1-.7-4l.2.1 6.5 3.8a1 1 0 0 0 1 0l8-4.6v3.2l-6.6 3.8a6 6 0 0 1-8.2-2.2zM3.1 10.8a6 6 0 0 1 3.1-2.6v7.7a1 1 0 0 0 .5.8l7.9 4.6-2.7 1.6-6.6-3.8a6 6 0 0 1-2.2-8.2zm22.5 5.2-8-4.6L20.3 10l6.6 3.8a6 6 0 0 1-.9 10.8v-7.7a1 1 0 0 0-.5-.9zm2.7-4-.2-.1-6.5-3.8a1 1 0 0 0-1.1 0l-7.9 4.6V9.4l6.6-3.8a6 6 0 0 1 8.9 6.2zM10.2 17.6l-2.7-1.5V8.6a6 6 0 0 1 9.8-4.6l-.2.1L10.7 7.8a1 1 0 0 0-.5.9zm1.5-3.2 3.6-2 3.6 2v4.1l-3.6 2-3.6-2z" fill="currentColor"/>'),

    ("Gemini", "Google", "#4285F4",
     '<path d="M16 0c.8 8.6 6.6 14.4 15.2 15.2v1.6C22.6 17.6 16.8 23.4 16 32h-1.6C13.6 23.4 7.8 17.6-.8 16.8v-1.6C7.8 14.4 13.6 8.6 14.4 0z" transform="translate(.8)" fill="currentColor"/>'),

    ("Claude", "Anthropic", "#D97757",
     '<path d="M16 1.5 18.9 11l7.4-6.5-4.6 8.9 9.6-2.1-8.5 4.7 8.5 4.7-9.6-2.1 4.6 8.9-7.4-6.5L16 30.5 13.1 21l-7.4 6.5 4.6-8.9-9.6 2.1L9.2 16 .7 11.3l9.6 2.1-4.6-8.9L13.1 11z" fill="currentColor"/>'),

    ("Perplexity", "Perplexity AI", "#20B8CD",
     '<path d="M16 2.4 5.6 10.2v2.1H2.4v11.4h3.2v6l10.4-7.6 10.4 7.6v-6h3.2V12.3h-3.2v-2.1zM14.6 8.1v5.2H7.7zm2.8 0 6.9 5.2h-6.9zM5.2 15.7h9.4v8.3l-1.2.9v-4.7H5.2zm12.2 0h9.4v4.5h-8.2v4.7l-1.2-.9z" fill="currentColor"/>'),

    ("DeepSeek", "DeepSeek", "#4D6BFE",
     '<path d="M30.4 7.3c-.4-.2-.6.1-.8.2-.3.2-.5.4-.7.7-.2.3-.4.5-.6.8-.9 1.1-1.9 1.8-3.2 1.7-1.9-.1-3.6.5-5 1.9-.3-1.8-1.3-2.9-2.9-3.6-.8-.4-1.7-.6-2.4-1.2-.5-.4-.6-.9-.8-1.4-.1-.4-.2-.7-.5-1-.4-.4-.8-.3-1 .2-.7 1.5-.4 3.7.9 4.9.1.1.2.3.4.4.5.4.5.8.1 1.4-.6 1-1.5 1.6-2.6 2C8 15.5 6.6 16.9 5.9 19c-.9 2.7-.6 5.3 1 7.7 1.7 2.6 4.2 4 7.3 4.3 3.6.3 7-.2 9.9-2.9 1.4-1.3 2.3-2.9 2.7-4.8.2-.9.2-1.9.1-2.8 0-.6.1-.8.6-1 .8-.4 1.5-.9 2-1.7 1.1-1.6 1.5-3.4 1.4-5.3-.1-1.7-.3-3.4-.5-5.2zM16.2 26.9c-3.5.1-6.4-2.3-6.8-5.6-.4-3.3 1.7-6.3 5-6.9 3.8-.7 7.3 1.9 7.6 5.7.3 3.6-2.3 6.7-5.8 6.8z" fill="currentColor"/><circle cx="16" cy="20.4" r="2.4" fill="currentColor"/>'),

    ("Copilot", "Microsoft", "#0078D4",
     '<path d="M11.6 4h8.1c2.6 0 4.9 1.7 5.7 4.2l2.4 7.6c.9 2.8-.4 5.8-3 7.1-1 .5-2 1.4-2.5 2.4l-.6 1.1c-.9 1.7-2.6 2.7-4.5 2.7h-2.1c-1.9 0-3.7-1-4.5-2.7l-.6-1.1c-.5-1-1.5-1.9-2.5-2.4-2.6-1.3-3.9-4.3-3-7.1l2.4-7.6C7.7 5.7 9.9 4 12.6 4z" fill="none" stroke="currentColor" stroke-width="2.3"/><path d="M12.4 14.6c1.2-1.4 3.2-1.5 4.6-.4l.6.5c1.4 1.1 3.4 1 4.6-.4" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round"/>'),

    ("AI Overviews", "Google Search", "#EA4335",
     '<path d="M11.8 2 14 8.2l6.2 2.2-6.2 2.2L11.8 19l-2.2-6.4L3.4 10.4l6.2-2.2z" fill="currentColor"/><path d="M23.4 15.5l1.4 3.9 3.9 1.4-3.9 1.4-1.4 3.9-1.4-3.9-3.9-1.4 3.9-1.4z" fill="currentColor" opacity=".75"/><path d="M6 22.5l.9 2.5 2.5.9-2.5.9-.9 2.5-.9-2.5-2.5-.9 2.5-.9z" fill="currentColor" opacity=".55"/>'),

    ("Grok", "xAI", "#E8EAED",
     '<path d="M8.4 24.6 20.1 8.9h4.4L12.8 24.6zM7.5 7.4h4.4l3.6 4.9-2.2 3zM17.8 21.3l2.2-3 4.5 6.3h-4.4z" fill="currentColor"/>'),
]

SEO_TOOLS = [
    ("Google Search Console", "Performance data, indexing and Core Web Vitals straight from Google."),
    ("Google Analytics 4", "Attribution, conversions and the revenue side of organic."),
    ("Bing Webmaster Tools", "Indexing and IndexNow. Bing is what feeds Microsoft Copilot."),
    ("Ahrefs", "Backlinks, keyword difficulty and competitor SERP reads."),
    ("Semrush", "Keyword research, position tracking and competitive gap analysis."),
    ("Screaming Frog", "Full technical crawls, redirect mapping and log-file analysis."),
    ("Google PageSpeed Insights", "Core Web Vitals field and lab data on every audit."),
    ("Schema Markup Validator", "Every JSON-LD block validated before it ships."),
    ("Google Rich Results Test", "Confirms structured data is actually eligible."),
    ("Merkle Technical SEO Tools", "Hreflang, robots.txt and structured-data testing."),
    ("Google Tag Manager", "Event tracking, conversion wiring and tag governance."),
    ("Looker Studio", "Client dashboards blended across GSC, GA4 and rank data."),
]

CERTIFICATIONS = [
    ("Semrush Certified", "SEO Toolkit &amp; Technical SEO"),
    ("Microsoft Advertising Certified", "Bing &amp; Copilot ecosystem"),
    ("Google Shopping Certified", "Merchant Center &amp; product feeds"),
    ("Google Analytics 4 Certified", "Measurement &amp; attribution"),
]


def platform_strip():
    marks = "".join(
        f'''<div class="pmark">
          <div class="pmark-ico" style="color:{c}">
            <svg viewBox="0 0 32 32" width="56" height="56" role="img" aria-label="{n}">{p}</svg>
          </div>
          <strong>{n}</strong><span>{maker}</span></div>'''
        for n, maker, c, p in AI_PLATFORMS)
    return f'<div class="pmarks">{marks}</div>'


def cert_strip():
    return '<div class="certs">' + "".join(
        f'''<div class="cert"><div class="cert-tick">&#10003;</div>
        <div><strong>{n}</strong><span>{d}</span></div></div>''' for n, d in CERTIFICATIONS) + '</div>'


def tools_grid():
    def initials(name):
        parts = [w for w in re.split(r"[\s&]+", name) if w and w[0].isalnum()]
        return "".join(w[0] for w in parts[:3]).upper()
    return '<div class="tools">' + "".join(
        f'''<div class="tool"><div class="tool-ico">{initials(n)}</div>
        <div><strong>{n}</strong><span>{d}</span></div></div>''' for n, d in SEO_TOOLS) + '</div>'


# Acronyms that must keep their casing when a label is used mid-sentence.
# A blanket .lower() rendered "IVF" as "ivf" and "IT Services" as "it services".
ACRONYMS = {"IVF", "IT", "AI", "SEO", "GEO", "AEO", "LLM", "SaaS", "D2C",
            "B2B", "UK", "USA", "UAE", "EdTech", "Web3"}
_ACRO_UPPER = {a.upper(): a for a in ACRONYMS}


def lc(label):
    """
    Lowercase a label for mid-sentence use, preserving acronyms and any
    trailing punctuation. Stripping the comma for the acronym lookup and then
    returning the match dropped it, turning "Web3, Crypto" into "Web3 crypto".
    """
    out = []
    for w in label.replace("&amp;", "and").split():
        core = w.rstrip(",.;:")
        tail = w[len(core):]
        out.append((_ACRO_UPPER[core.upper()] if core.upper() in _ACRO_UPPER
                    else core.lower()) + tail)
    return " ".join(out)


def industry_page(i):
    pains = "".join(f"<li>{p}</li>" for p in i["pains"])
    plays = "".join(f'<div class="crow"><span class="lbl">{n:02d}</span><span class="val" style="text-align:left;flex:1">{p}</span></div>'
                    for n, p in enumerate(i["plays"], 1))
    clients = "".join(f'<span class="clogo">{c}</span>' for c in i["clients"])
    label = i["name"].replace("&amp;", "and")
    return f"""
{phero(f'<a href="index.html">Home</a> / <a href="industries.html">Industries</a> / {i["name"]}',
       'Industry', f'{i["name"]} SEO &amp; AI visibility', i["short"])}

<section class="sec-sm band-alt">
  <div class="wrap">
    <p class="faint mono" style="font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;margin-bottom:18px">Clients we have delivered this for</p>
    <div class="clogos">{clients}</div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="grid g2" style="gap:52px;align-items:start">
      <div>
        <div class="eyebrow">The problem</div>
        <h2 style="margin-bottom:1.4rem">The problems we hear most in {lc(label)}</h2>
        <ul class="pain-list">{pains}</ul>
      </div>
      <div class="panel">
        <div class="panel-bar"><i class="tdot"></i><i class="tdot"></i><i class="tdot"></i>
          <span style="margin-left:8px">playbook &mdash; {i["slug"]}</span></div>
        <div class="panel-body">{plays}</div>
      </div>
    </div>
  </div>
</section>

<section class="sec band-dark">
  <div class="wrap">
    <div class="sec-head center">
      <div class="eyebrow">Where we make you visible</div>
      <h2>Every surface that answers a {lc(label)} question</h2>
    </div>
    {platform_strip()}
  </div>
</section>

{faq([
  (f"How is {label} SEO different from generic SEO?",
   f"The technical foundations are identical. What changes is the citation stack, the schema types and the intent mix. {label} buyers use different research surfaces, and AI models weight different third-party sources when answering questions in this category. We reverse-engineer which sources actually get cited for your specific vertical during the audit, rather than applying a generic checklist."),
  ("How long before we see results?",
   "Traditional ranking improvements typically show inside 60 to 90 days, faster on pages already sitting in positions 8 to 20. AI citations follow the same curve every time: entity indexing at 30 to 45 days, first citations around day 60, consistent mentions by day 90, stable visibility at 4 to 6 months."),
  ("Do you have experience in this specific industry?",
   f"Yes. The engagements listed above are live or completed work in {lc(label)}. We will walk you through the actual accounts, anonymised as the client requires, on a scoping call."),
  ("What does it cost?",
   "Consulting is $30 per hour for one-off sessions. Retainers are scoped after the audit, because quoting before diagnosis is guesswork. Start with the free AI visibility audit and the priority usually becomes obvious."),
])}

{cta(f"See how visible you are in {label} AI answers.",
     "Twelve eligibility checks against your live URL. No card, no call, about sixty seconds.")}
"""


# ==========================================================================
# Individual service pages
# ==========================================================================
def S(slug, name, cluster, icon, answer, kw, does, deliver, faqs, body=""):
    return dict(slug=slug, name=name, cluster=cluster, icon=icon, answer=answer,
                kw=kw, does=does, deliver=deliver, faqs=faqs, body=body)


SERVICES = [
    S("answer-engine-optimization", "Answer Engine Optimization (AEO)", "AI Search", "&#9635;",
      "Answer Engine Optimization is the practice of structuring content so it becomes the direct answer a search or AI system returns, rather than one of ten links below it. It works through question architecture, FAQ and QAPage schema, and a direct answer placed in the first 100 words of every page.",
      "answer engine optimization, AEO services, featured snippet optimization, FAQ schema, zero click SEO",
      ["Cluster every real question your buyers ask, by intent stage",
       "Rewrite money pages to open with a direct, quotable answer",
       "Ship FAQPage, QAPage and HowTo schema across the site",
       "Capture featured snippets and People Also Ask placements",
       "Defend revenue against zero-click and AI Overview absorption"],
      ["Question map clustered by intent", "Answer blocks on all commercial pages",
       "Validated FAQ and HowTo schema", "Snippet-capture tracking report"],
      [("Is AEO the same as GEO?",
        "No. AEO is page-level and structural: it makes an individual page the quotable answer to a specific question. GEO is brand-level and reputational: it makes a model recall your brand when answering at all. AEO shows results faster; GEO is more defensible. Most clients need both, which is why we scope them separately."),
       ("Does AEO help traditional rankings too?",
        "Yes, and this is why we usually start here. The same work that makes a page quotable by an AI system also wins featured snippets and People Also Ask boxes in classic search. It is the highest-overlap, fastest-feedback service we offer.")]),

    S("llm-seo", "LLM SEO", "AI Search", "&#10022;",
      "LLM SEO is the technical layer of AI visibility: making your templates, markup, rendering and content structure parseable, chunkable and quotable by large language models. If a model cannot cleanly extract a passage from your page and attribute it, it will not cite you regardless of how good the content is.",
      "LLM SEO, LLM optimization, llms.txt, GPTBot, AI crawler optimization, chunk optimization",
      ["Restructure page templates so passages chunk cleanly for retrieval",
       "Author and maintain llms.txt at your domain root",
       "Configure AI crawler directives across GPTBot, ClaudeBot, PerplexityBot and Google-Extended",
       "Fix client-side rendering that leaves AI crawlers an empty shell",
       "Rebuild product and category templates for machine extraction"],
      ["Template and chunking audit", "llms.txt shipped and maintained",
       "AI crawler access configuration", "Rendering strategy recommendation"],
      [("What is llms.txt and does it matter yet?",
        "It is a plain-text file at your domain root describing your content and structure for LLM crawlers, conceptually similar to robots.txt but written for retrieval rather than indexing. Adoption is still early so it is not a ranking factor. It costs almost nothing and removes ambiguity, which is why we ship it on every build."),
       ("Should we block AI crawlers instead?",
        "Only if your revenue comes from people landing on your pages and consuming content there, such as ad-supported publishing or paid archives. If your revenue comes from being discovered and recommended, blocking guarantees you are never cited. We will tell you honestly which side of that line you are on.")]),

    S("ai-citation-entity-building", "AI Citation &amp; Entity Building", "AI Search", "&#9670;",
      "AI citation and entity building is the off-site half of AI visibility. It creates a consistent, independent third-party footprint that language models read as authority consensus, which is the single strongest driver of whether a brand gets named in a generated answer.",
      "AI citation building, entity SEO, brand entity optimization, G2 Capterra listing, digital PR for AI",
      ["Build the Tier-1 citation stack for your specific category",
       "Reverse-engineer every domain cited alongside competitors in AI answers",
       "Establish the founder as a resolvable entity with bylines and podcasts",
       "Enforce identical brand description across every third-party profile",
       "Run digital PR aimed at citation frequency, not just domain rating"],
      ["Category-specific citation source list", "Tier-1 profiles built and verified",
       "Competitor citation teardown", "Founder entity plan with named placements"],
      [("Why does off-site matter more than my own website?",
        "Because language models weight independent confirmation above self-description. When a model sees the same brand described the same way across G2, Crunchbase, Reddit and three industry publications, it treats that repetition as consensus. Nothing you write on your own domain produces that signal."),
       ("We are not a software company. Do G2 and Capterra apply?",
        "No, and applying a generic list is why most GEO work fails. The platforms change entirely by category: retailers need Trustpilot and marketplace presence, clinics need credentialed directories, manufacturers need trade publications. We derive your list during the audit from what is actually cited in your category."),
       ("Is a citation the same as a backlink?",
        "No, and conflating them is a common mistake. A backlink passes ranking authority to a page. A citation passes recognition to a brand. Ten relevant, consistent mentions in sources a model already reads for your category do more for AI visibility than a hundred high-authority links from irrelevant sites, because retrieval weights contextual relevance and repeated description over raw link power."),
       ("How soon does entity building show results?",
        "Entity signals typically index at 30 to 45 days, first citations tend to appear around day 60, and consistent naming stabilises across 9 to 12 months. It is the slowest-compounding part of AI visibility and the most defensible once it holds, which is why we start it early rather than last.")],
      body="""
<h2>Why AI engines trust brands, not URLs</h2>
<p>When a generative engine answers a question, it does not weigh your homepage against a competitor's homepage. It recalls which brands it associates with the topic, then looks for sources that corroborate naming them. That recall is built off your own domain &mdash; in the third-party places the model already trusts. A brand described the same way across a review platform, a business database, a community thread and a handful of industry publications reads to the model as consensus. A brand that only describes itself, on its own site, has no consensus to read.</p>
<p>This is why on-page work alone plateaus. You can hold position one in Google and still be absent from the AI answer above it, because ranking measures your page and citation measures your reputation.</p>
<h2>What entity building actually involves</h2>
<ol>
  <li><strong>Resolve the entity.</strong> One canonical brand name, one description, one category &mdash; rendered identically across your site, your profiles and structured data (Organization and sameAs). Most sites we audit describe themselves three different ways and fragment their own entity before anyone else does.</li>
  <li><strong>Build the category-specific citation stack.</strong> The right platforms differ for every category: SaaS needs review databases, clinics need credentialed directories, retailers need marketplace and trust platforms, manufacturers need trade press. We derive the list from what is actually cited in your category, not a generic template.</li>
  <li><strong>Reverse-engineer competitor citations.</strong> We take the brands already named in AI answers for your queries, export every domain cited alongside them, and target the same sources with better material.</li>
  <li><strong>Establish the people.</strong> Founders and experts as resolvable entities &mdash; consistent bios, bylines and credentials &mdash; because models weight identifiable authorship.</li>
  <li><strong>Run citation-first digital PR.</strong> Placements chosen for descriptive consistency and topical relevance, not raw domain rating.</li>
</ol>
<h2>Citations versus backlinks: not the same job</h2>
<p>A backlink passes ranking authority; a citation passes recognition. Ten relevant, consistent mentions in sources a model already reads for your category do more for AI visibility than a hundred high-authority links from irrelevant sites, because retrieval weights contextual relevance and repeated description over raw link power. This work pairs directly with <a href="/generative-engine-optimization/">Generative Engine Optimization</a> and is measured through <a href="/services/ai-visibility-monitoring/">AI visibility monitoring</a>.</p>
<h2>Timeline and measurement</h2>
<p>Entity signals index at roughly 30 to 45 days, first citations tend to appear around day 60, and consistent naming stabilises across 9 to 12 months. We report the citation footprint monthly: which sources describe you, how consistently, and how your share of citation compares with named competitors.</p>
<p class="faint">No one controls what a model generates, and there is no submission process. What we control is the consistency and reach of your off-site footprint, measured and reported so the trend is visible.</p>
"""),

    S("ai-visibility-monitoring", "AI Visibility Monitoring", "AI Search", "&#9678;",
      "AI visibility monitoring measures whether your brand is actually being cited by generative engines, combining automated citation tracking with controlled weekly prompt testing across ChatGPT, Perplexity and Gemini. It is the only way to know whether GEO work is producing anything.",
      "AI visibility tracking, LLM citation tracking, ChatGPT rank tracking, share of voice AI, GEO reporting",
      ["Track citation volume and page-level attribution monthly",
       "Run a fixed prompt set weekly across three or more engines",
       "Measure share of citation against named competitors",
       "Report in written narrative form, not a dashboard dump",
       "Flag which specific sources models pull from, and why"],
      ["Monthly citation volume and page attribution", "Weekly controlled prompt log",
       "Competitor share-of-citation tracking", "Written monthly narrative report"],
      [("Are AI visibility trackers reliable?",
        "On their own, not very. Automated tools disagree with each other and with manual checks. That is why we run two tracks: automated tracking for volume and page attribution, plus disciplined manual prompt testing on a fixed prompt set. The manual layer is what makes the number trustworthy."),
       ("What does a report actually contain?",
        "Citation count and trend, which of your pages were cited and how often, results of the weekly prompt tests with the exact prompts used, competitor share of citation, and a written explanation of what changed and what we are doing next month. Roughly two pages of prose, not forty tabs.")]),

    S("google-ai-overviews-optimization", "Google AI Overviews Optimization", "AI Search", "&#9650;",
      "AI Overviews optimization recovers and defends the traffic Google's generated summaries absorb. An AI Overview answers the query above your listing and names two or three brands, so your clicks can fall while impressions and average position hold &mdash; the measurable fingerprint of absorption rather than a ranking loss. Demand is large and still growing: the term &lsquo;google ai overviews&rsquo; alone draws roughly 22,200 US searches a month. We diagnose exactly which of your queries are affected, then restructure content so your brand is named inside the summary rather than buried beneath it.",
      "Google AI Overviews, AI Overview optimization, SGE optimization, zero click recovery, CTR loss",
      ["Audit which of your queries now trigger an AI Overview",
       "Attribute CTR loss precisely in Search Console",
       "Restructure content for inclusion in the generated summary",
       "Reinforce entity and schema signals Google draws on",
       "Rebalance the content mix toward queries that still convert clicks"],
      ["Query-level AI Overview presence audit", "CTR-loss attribution analysis",
       "Prioritised content restructuring plan", "Monthly presence tracking"],
      [("Our rankings held but clicks collapsed. Is this why?",
        "Very often, yes. An AI Overview sitting above your number-two ranking answers the query outright and names two or three brands. Impressions and position look unchanged while clicks fall, so it reads as an unexplained CTR decline. The first thing we do is confirm whether that is what happened, query by query."),
       ("How is this different from ordinary SEO?",
        "Ordinary SEO competes for a position in the list of links. AI Overview optimization competes for inclusion in the generated summary that now sits above that list. The technical foundation is shared, but the winning move differs: a direct, quotable answer in the opening, valid FAQ schema, and a brand entity Google is confident enough to name. A page can rank in position two and still be absent from the Overview above it."),
       ("Which pages should we start with?",
        "The ones losing clicks fastest. We start from Search Console, rank your pages by the gap between held impressions and falling clicks, and fix the biggest measurable leaks first. On a newer site with little click history, we start instead with the commercial queries where an Overview is most likely to name a provider."),
       ("There is no ranking position, so how do you measure it?",
        "We report presence, not position. Each month you see which of your queries trigger an AI Overview, whether your brand is named in each, how that shifted from the prior month, and the click-through recovery on the pages we restructured. Entity indexing typically registers at 30 to 45 days and inclusion patterns settle across 4 to 6 months."),
       ("Can you guarantee inclusion in an AI Overview?",
        "No. Nobody controls what Google generates and there is no submission process. What we control is every input that makes inclusion likely, and we report presence monthly so you can see whether it is working.")],
      body="""
<h2>Why AI Overviews changed the click math</h2>
<p>An AI Overview is the summary Google generates above the traditional results for a growing share of queries. When one appears, it answers the question outright and names two or three brands inside the summary. Your page can hold the exact position it held last quarter while its clicks fall, because the searcher gets the answer without scrolling to the links. In Search Console this reads as a clean drop in click-through rate against flat impressions and unchanged average position &mdash; the signature of AI Overview absorption rather than a ranking loss.</p>
<p>The demand is not niche. &lsquo;Google AI Overviews&rsquo; alone draws roughly 22,200 US searches a month, and the surface keeps expanding into more informational and commercial queries. For most sites the question is no longer whether AI Overviews affect their traffic, but which specific queries have already been absorbed and whether the brand is named or buried.</p>
<h2>How we optimise for Google AI Overviews</h2>
<p>The work runs in five steps, in this order:</p>
<ol>
  <li><strong>Map presence, query by query.</strong> We identify which of your ranking queries now trigger an AI Overview, and whether your brand is named inside it, buried beneath it, or absent.</li>
  <li><strong>Attribute the loss.</strong> Using Search Console, we isolate the pages where clicks fell while impressions and position held &mdash; the measurable fingerprint of absorption &mdash; so effort goes where revenue actually leaked.</li>
  <li><strong>Restructure for inclusion.</strong> We rewrite the affected pages answer-first: a direct 40-to-60-word answer in the opening, question-shaped subheadings, and dense, extractable blocks Google can lift into the summary.</li>
  <li><strong>Reinforce entity and schema signals.</strong> FAQPage, Article and Organization structured data, a consistent brand description, and the off-site citation consensus that makes Google confident enough to name you rather than a competitor.</li>
  <li><strong>Rebalance toward click-worthy demand.</strong> Some queries keep the click and some do not. We shift the content mix toward the transactional and commercial queries where a click still happens, and defend the informational ones with brand-name inclusion.</li>
</ol>
<h2>What gets named versus what gets buried</h2>
<p>Two pages can rank in the same position and get opposite outcomes. The page that opens with a direct, quotable answer, carries valid FAQ schema and is corroborated by consistent third-party mentions is the one Google pulls into the summary. The page that opens with a story intro, hides its answer three scrolls down and has a fragmented brand entity is the one that sits unread below the fold. This service is the discipline of being consistently the former &mdash; and it pairs directly with <a href="/services/answer-engine-optimization/">Answer Engine Optimization</a>, <a href="/services/ai-citation-entity-building/">AI citation and entity building</a> and a sound <a href="/services/technical-seo/">technical foundation</a>.</p>
<h2>What we measure</h2>
<p>There is no position to report, so we report presence. Every month you see which of your queries trigger an AI Overview, whether your brand is named in each, how that changed from the prior month, and the click-through recovery on the pages we restructured. Entity indexing typically registers at 30 to 45 days and inclusion patterns stabilise across 4 to 6 months, tracked through <a href="/services/ai-visibility-monitoring/">AI visibility monitoring</a>. We report the numbers whether or not they flatter the work.</p>
<p class="faint">We cannot guarantee inclusion in an AI Overview &mdash; nobody controls what Google generates and there is no submission process. What we control is every input that makes inclusion likely, measured and reported so you can see whether it is working.</p>
"""),

    S("technical-seo", "Technical SEO", "Core SEO", "&#9881;",
      "Technical SEO is the foundation everything else depends on: crawl budget, index bloat, rendering, Core Web Vitals, site architecture and log-file analysis. A site that cannot be crawled or rendered cannot rank in classic search or be retrieved by an AI system.",
      "technical SEO services, crawl budget, index bloat, Core Web Vitals, log file analysis, site architecture",
      ["Audit crawl budget and perform index surgery on bloated sites",
       "Analyse real Googlebot behaviour from server log files",
       "Resolve rendering problems: SSR, SSG and CSR trade-offs",
       "Remediate Core Web Vitals across LCP, INP and CLS",
       "Restructure internal linking and site architecture"],
      ["Full technical crawl with prioritised fixes", "Log-file analysis report",
       "Core Web Vitals remediation plan", "Architecture and internal link map"],
      [("How do we know if we have an index bloat problem?",
        "Compare the number of pages you intend to have indexed against what Search Console reports. If Google has discovered many times more URLs than you have real pages, faceted navigation or URL parameters are generating them, and crawl budget is being spent on noise instead of your money pages."),
       ("Is technical SEO worth it if our content is weak?",
        "It is a prerequisite, not a substitute. Excellent content on a broken site does not rank. But a perfect technical foundation under thin content ranks no better. If your content is genuinely the constraint, we will tell you and sequence that first.")]),

    S("semantic-on-page-seo", "Semantic &amp; On-Page SEO", "Core SEO", "&#9737;",
      "Semantic SEO optimises for concepts and entities rather than keyword repetition. Modern search engines use natural language processing and entity recognition to understand topics, so pages that cover an entire concept ecosystem consistently outperform pages that target a single keyword.",
      "semantic SEO, on page SEO services, entity SEO, topical authority, keyword to concept mapping",
      ["Build semantic topic maps before any content is written",
       "Map entity relationships and co-occurrence terms",
       "Run the position 8-20 recovery programme on existing pages",
       "Audit content for semantic completeness and fill the gaps",
       "Replace keyword briefs with concept and entity briefs"],
      ["Semantic topic map per cluster", "Entity relationship model",
       "Position 8-20 recovery worklist", "Semantic content audit with gap list"],
      [("What is the position 8-20 programme?",
        "Pages ranking between positions 8 and 20 already have Google's trust and partial relevance; they are simply misaligned with the dominant intent. We extract that page's own query data, diagnose the intent gap, rewrite the title and meta for click-through, add the missing queries as real subheadings, then build contextual internal links. Movement usually shows in 7 to 21 days without new backlinks."),
       ("Is keyword density still relevant?",
        "No, and chasing it actively hurts. Concept coverage beats keyword frequency. Articles that thoroughly cover fifteen or more related concepts consistently outperform articles that repeat one keyword, because search engines are measuring topical understanding rather than term counts.")]),

    S("content-strategy", "Content Strategy &amp; Production", "Core SEO", "&#9998;",
      "Conversion-first content strategy built on a defined ICP. We invert the traditional funnel and start with bottom-of-funnel commercial pages where revenue is closest, then build topical depth around them so authority compounds.",
      "SEO content strategy, content marketing agency India, B2B content, pillar cluster content, ICP content",
      ["Define the ICP with your sales and customer success teams",
       "Sequence the inverted funnel: commercial pages ship first",
       "Design pillar and cluster architecture with an internal link plan",
       "Write semantic briefs specifying entities, questions and gaps",
       "Produce founder-bylined authority content, not anonymous filler"],
      ["ICP definition document", "12-month content roadmap with keyword targets",
       "Semantic brief per article", "Published, optimised articles"],
      [("How much content do we actually need?",
        "Fewer, deeper pieces beat volume in almost every category we work in. One comprehensive page that fully covers a concept ecosystem will outrank six thin articles targeting variations of the same term, and it gives AI systems a single authoritative source to cite rather than a diluted set."),
       ("Can we use AI to write it?",
        "For research, briefs, outlines and first drafts, yes, and we do. For publishing unedited, no. Content with no expertise, no original data and no named author is exactly what both Google's helpful-content systems and AI retrieval discount. The differentiator is your evidence, not the drafting speed.")]),

    S("link-building-digital-pr", "Link Building &amp; Digital PR", "Core SEO", "&#9741;",
      "Link building that doubles as AI citation building. We target placements that pass authority and get quoted by language models, through guest placement, digital PR built on original data, resource-page outreach and category-relevant citations.",
      "link building services, digital PR agency, guest posting, backlink acquisition, citation building",
      ["Reverse-engineer competitor backlink profiles for real opportunities",
       "Run guest posting and guestographic campaigns with editorial standards",
       "Build digital PR campaigns around original data you own",
       "Execute resource-page and broken-link outreach",
       "Maintain local citation and NAP consistency"],
      ["Backlink gap analysis", "Monthly placement targets and outreach log",
       "Original data asset for PR", "Live link report with authority metrics"],
      [("Do you buy links?",
        "No. Paid link schemes violate Google's guidelines and, more practically, purchased links from irrelevant sites do not produce AI citations because models weight contextual relevance and consensus rather than raw authority. We earn placements editorially."),
       ("How many links per month?",
        "We do not sell links by volume, because that incentivises the wrong behaviour. We target a small number of genuinely relevant, genuinely editorial placements per month in sources that matter for your category. Ten relevant citations beat a hundred irrelevant ones for both ranking and retrieval.")]),

    S("ecommerce-seo", "Ecommerce SEO", "Core SEO", "&#9679;",
      "Ecommerce SEO covering category architecture, faceted navigation, variant handling, product schema and shopping-surface visibility. Built for retailers whose category pages compete against the marketplaces they also sell on.",
      "ecommerce SEO services, Shopify SEO, product page SEO, category page optimization, ecommerce GEO",
      ["Map money-page keywords before a single page is built",
       "Control faceted navigation and URL parameters to end index bloat",
       "Ship Product, Offer, Review and variant schema across the catalogue",
       "Build buying guides and comparison content that AI quotes",
       "Configure GA4 ecommerce so organic revenue is provable"],
      ["Money-page keyword map", "Faceted navigation control plan",
       "Product schema rollout", "GA4 ecommerce measurement setup"],
      [("Our traffic grew but revenue did not. Why?",
        "Usually because new traffic is landing on category and blog pages that convert at roughly half the rate of product detail pages. That is the expected shape when category rankings improve first. The fix is deliberate: strengthen internal paths from category to product, and improve product page conversion in parallel."),
       ("Should product variants have their own URLs?",
        "It depends on whether people search for the variant. If they search by size or colour, dedicated indexable URLs with proper variant schema capture that demand. If they do not, separate URLs create thousands of near-duplicate pages that burn crawl budget. We decide this per catalogue, from real search data.")]),

    S("saas-b2b-seo", "SaaS &amp; B2B SEO", "Core SEO", "&#9636;",
      "SaaS and B2B SEO built for pipeline rather than pageviews. Bottom-of-funnel commercial pages first, then comparison and alternatives systems, then integration-led programmatic expansion.",
      "SaaS SEO agency, B2B SEO services, comparison page SEO, alternatives page, integration pages",
      ["Sequence the inverted funnel so commercial pages rank first",
       "Build comparison, alternatives and versus page systems",
       "Expand programmatically across integrations and use cases",
       "Place your product on G2, Capterra and Product Hunt",
       "Optimise documentation, which AI systems retrieve heavily"],
      ["BoFu commercial page set", "Comparison and alternatives architecture",
       "Programmatic expansion plan", "Review platform presence"],
      [("Are comparison pages against competitors risky?",
        "Handled fairly, no. Accurate, verifiable comparisons that acknowledge where a competitor is genuinely stronger build trust and get cited by AI systems precisely because they read as balanced. Overstated claims are both a legal risk and less effective."),
       ("How long until SEO produces pipeline?",
        "For bottom-of-funnel commercial pages in a soft SERP, first qualified leads typically appear within 60 to 90 days. Broad topical authority takes 9 to 12 months. This is why we sequence commercial pages first: it funds the patience the rest of the programme requires.")]),

    S("local-seo", "Local SEO", "Core SEO", "&#8962;",
      "Local SEO covering Google Business Profile, citation consistency, review velocity and location page architecture, for single-location practices through to multi-location and service-area businesses.",
      "local SEO services India, Google Business Profile optimization, map pack ranking, near me SEO",
      ["Optimise Google Business Profile with a real posting cadence",
       "Audit and clean up NAP consistency across every directory",
       "Build review generation systems that stay policy-compliant",
       "Architect location and service-area landing pages that scale",
       "Ship LocalBusiness schema with accurate service-area markup"],
      ["GBP optimisation and posting calendar", "Citation cleanup report",
       "Review generation system", "Location page architecture"],
      [("Why are we not in the map pack?",
        "Usually one of three things: inconsistent name, address and phone across directories, which fragments your entity; too few or too old reviews relative to competitors; or a service-area configuration that does not match how people actually search. The audit identifies which applies."),
       ("Can we rank in cities where we have no office?",
        "Not in the map pack, which requires a genuine physical presence. You can rank organically for city-plus-service queries with well-built service-area pages, and for many businesses that organic placement is worth more than the map pack anyway.")]),

    S("international-seo", "International SEO", "Core SEO", "&#9757;",
      "International SEO covering hreflang implementation, domain structure strategy, per-market keyword research and genuine localisation rather than literal translation.",
      "international SEO, hreflang implementation, multilingual SEO, global SEO agency, ccTLD strategy",
      ["Choose and implement the right domain structure for your markets",
       "Implement and validate hreflang across every language pair",
       "Run keyword research per market rather than translating keywords",
       "Adapt content culturally, not just linguistically",
       "Configure per-market tracking and Search Console properties"],
      ["Domain structure recommendation", "Validated hreflang implementation",
       "Per-market keyword research", "Localisation guidelines"],
      [("Subfolders, subdomains or ccTLDs?",
        "Subfolders in almost every case. They consolidate authority onto one domain, are cheapest to maintain, and hreflang handles the targeting. ccTLDs make sense when you need strong local trust signals and have the resources to build authority separately in each market."),
       ("Can we just translate our existing content?",
        "Translation alone reliably underperforms. Search intent, competitors and the terms people actually use differ by market, so a literal translation often targets a phrase nobody searches. We research each market natively and adapt the content to it.")]),

    S("programmatic-seo", "Programmatic SEO", "Core SEO", "&#9638;",
      "Programmatic SEO that survives helpful-content scrutiny: scaled page generation built on real proprietary data, strict quality thresholds and index control, rather than thin template spam.",
      "programmatic SEO, scaled content, template SEO, database driven SEO, pSEO agency",
      ["Identify data you own that can support genuinely useful pages at scale",
       "Design templates that produce distinct value per page",
       "Set quality thresholds and index controls before launch",
       "Automate internal linking across the generated set",
       "Monitor for cannibalisation and prune what underperforms"],
      ["Data source and template design", "Quality gate specification",
       "Internal link automation", "Cannibalisation monitoring"],
      [("Will Google penalise programmatic pages?",
        "Google penalises thin, unhelpful pages regardless of how they are made. Programmatic pages built on real data that answer a real query, with genuine differentiation between them, perform well. The failure mode is generating thousands of near-identical pages from a thin dataset. We set quality gates that refuse to publish those."),
       ("How many pages is realistic?",
        "As many as your data supports at quality, and not one more. Sometimes that is two hundred, sometimes fifty thousand. We would rather ship two hundred pages that rank than five thousand that trigger a sitewide quality problem.")]),

    S("site-migrations", "Site Migrations", "Core SEO", "&#8644;",
      "Replatforms, redesigns and domain moves executed without losing rankings: pre-migration crawl and ranking baselines, complete redirect mapping with QA, staged rollout and 30 days of daily post-launch monitoring.",
      "SEO migration, site migration services, replatforming SEO, domain migration, redirect mapping",
      ["Capture a full crawl and ranking baseline before anything changes",
       "Build and QA a complete redirect map, URL by URL",
       "Preserve schema, internal linking and metadata through the move",
       "Run a staged rollout with defined rollback criteria",
       "Monitor daily for 30 days post-launch and fix fast"],
      ["Pre-migration baseline", "Complete redirect map with QA log",
       "Staged rollout schedule", "30-day post-launch monitoring report"],
      [("How far ahead should we involve you?",
        "Before the new site is built, not after. The most expensive migration failures are architectural decisions made months earlier that cannot be undone cheaply. Involving us at wireframe stage costs a fraction of fixing a launched migration."),
       ("What happens if rankings drop anyway?",
        "Some short-term volatility is normal while search engines reprocess. We monitor daily against the baseline, so we can tell within days whether it is expected reprocessing or a genuine fault, and fix the fault. Without a baseline, that distinction is impossible to make.")]),

    S("white-label-seo", "White-Label SEO", "Core SEO", "&#9783;",
      "White-label SEO and GEO delivery under your brand and under NDA, from single audits through full retained execution, reported in your template. Your client never knows we exist.",
      "white label SEO India, SEO reseller, outsourced SEO agency, white label GEO, agency partnership",
      ["Deliver audits, strategy and execution entirely under your brand",
       "Report in your template, tone and format",
       "Scale from one-off audits to full retained delivery",
       "Add GEO and AI visibility as a line you can sell immediately",
       "Keep your account manager as the only client-facing contact"],
      ["NDA and partnership agreement", "Branded audit and reporting templates",
       "Agreed delivery SLAs", "Dedicated delivery contact"],
      [("How do you stay invisible?",
        "Everything is delivered in your branding, we never contact your client directly, and all documentation carries your identity. The NDA is signed before any work begins."),
       ("Can you join client calls?",
        "Yes, as a member of your team if you want technical depth in the room. Many partners prefer that for enterprise pitches. It is entirely your call.")]),

    S("seo-consulting", "SEO Consulting", "Core SEO", "&#9998;",
      "Direct strategist access at $30 per hour for teardowns, second opinions, in-house team training and roadmap review, including handover of our documented 39-SOP delivery library.",
      "SEO consultant India, SEO consulting services, hourly SEO consultant, SEO training, SEO audit consultant",
      ["Run live teardowns of your site with a recorded walkthrough",
       "Provide a second opinion on an existing agency or roadmap",
       "Train your in-house team on GEO and technical SEO",
       "Hand over our 39-SOP delivery library for internal use",
       "Review vendor proposals and scopes before you sign"],
      ["Recorded session walkthrough", "Written summary with prioritised actions",
       "39-SOP library access", "Follow-up questions answered by email"],
      [("What can we realistically cover in an hour?",
        "A focused teardown of one problem: why a specific page is not ranking, whether a proposed architecture will work, or a review of an agency proposal. Send context in advance and the hour is spent on answers rather than orientation."),
       ("Why is it only $30 an hour?",
        "Because AI tooling has made research, diagnosis and reporting dramatically faster than they were two years ago, and we pass that on as scope rather than margin. It is also the cheapest way for us to meet businesses that later become retainer clients.")]),
]


def service_page(s):
    does = "".join(f"<li>{d}</li>" for d in s["does"])
    deliver = "".join(
        f'<div class="crow"><span class="lbl">{n:02d}</span><span class="val" style="text-align:left;flex:1">{d}</span></div>'
        for n, d in enumerate(s["deliver"], 1))
    plain = s["name"].replace("&amp;", "and")
    return f"""
{phero(f'<a href="index.html">Home</a> / <a href="services.html">Services</a> / {s["name"]}',
       f'{s["cluster"]} service', s["name"], "")}

<section class="sec">
  <div class="wrap">
    <div class="grid g2" style="gap:52px;align-items:start">
      <div class="prose">
        <div class="answer-block" style="margin-top:0">
          <div class="q">What is {lc(plain).replace(" (aeo)", "")}?</div>
          <p>{s["answer"]}</p>
        </div>
        <h2 style="margin-top:2rem">What this service covers</h2>
        <ul>{does}</ul>
        <h2>Who it is for</h2>
        <p>Businesses that already have something worth promoting and need it found. If you are pre-launch with no product and no site, start with the <a href="contact.html">consulting hour</a> instead &mdash; a retainer would be premature and we will say so.</p>
      </div>
      <aside style="position:sticky;top:96px">
        <div class="panel" style="margin-bottom:20px">
          <div class="panel-bar"><i class="tdot"></i><i class="tdot"></i><i class="tdot"></i>
            <span style="margin-left:8px">deliverables</span></div>
          <div class="panel-body">{deliver}</div>
        </div>
        <div class="card">
          <h4 style="margin-bottom:14px">Start here</h4>
          <a class="btn btn-primary btn-sm" style="width:100%;justify-content:center;margin-bottom:10px" href="ai-visibility-audit.html">Run a free AI audit</a>
          <a class="btn btn-ghost btn-sm" style="width:100%;justify-content:center" href="CALENDLY_URL" target="_blank" rel="noopener">Book a 15-min call</a>
          <p class="faint" style="font-size:.78rem;margin-top:12px;text-align:center">No card. Consulting from $30/hour.</p>
        </div>
      </aside>
    </div>
  </div>
</section>
{('<section class="sec"><div class="wrap wrap-narrow prose">' + s["body"] + '</div></section>') if s.get("body") else ''}
<section class="sec band-dark">
  <div class="wrap">
    <div class="sec-head center">
      <div class="eyebrow">Surfaces</div>
      <h2>Where this makes you visible</h2>
    </div>
    <!--PLATFORMS-->
  </div>
</section>

{faq(s["faqs"] + [
  ("How long before we see results?",
   "Traditional ranking improvements typically appear within 60 to 90 days, faster on pages already ranking between positions 8 and 20. AI citations follow a consistent curve: entity indexing at 30 to 45 days, first citations around day 60, consistent mentions by day 90, stable visibility at 4 to 6 months."),
  ("What does it cost?",
   "Consulting is $30 per hour. Retainers are scoped after the audit, because quoting before diagnosis is guesswork. Run the free audit first and the priority usually becomes obvious."),
])}

{cta(f"See where you stand before you buy {plain}.",
     "Twelve AI eligibility checks against your live URL. No card, no call, about sixty seconds.")}
"""


LEGAL_UPDATED = "9 August 2026"


def legal_page(title, intro, sections):
    body = "".join(
        f'<h2 id="{sid}">{n}. {head}</h2>\n{copy}'
        for sid, n, head, copy in sections)
    toc = "".join(f'<li><a href="#{sid}">{n}. {head}</a></li>' for sid, n, head, _c in sections)
    return f"""
{phero(f'<a href="index.html">Home</a> / {title}', 'Legal', title, intro)}
<section class="sec">
  <div class="wrap wrap-narrow">
    <p class="mono faint" style="font-size:.78rem;letter-spacing:.08em;text-transform:uppercase">Last updated {LEGAL_UPDATED}</p>
    <div class="card" style="margin:26px 0 40px">
      <h4 style="margin-bottom:12px">On this page</h4>
      <ol class="sitemap-list" style="counter-reset:none;list-style:none;padding:0;margin:0">{toc}</ol>
    </div>
    <div class="prose legal">{body}</div>
  </div>
</section>
{cta("Questions about any of this?",
     "Email us and a person will answer. We would rather clarify a clause than have you guess.",
     primary=("Email hello@svedsolution.com", "mailto:hello@svedsolution.com"),
     secondary=("Book a 15-min call", CALENDLY))}
"""


TERMS_SECTIONS = [
 ("services", 1, "Services",
  "<p>We provide search and AI visibility services: Generative Engine Optimization, Answer Engine Optimization, LLM SEO, technical SEO, semantic content strategy, digital PR and measurement. The precise scope of any engagement is set out in the proposal or statement of work we agree with you, and that document takes precedence over this page wherever the two differ.</p>"
  "<p>Anything not expressly listed in your scope is outside it. If you want something added, ask &mdash; we will either include it or quote it, and we will tell you which.</p>"),

 ("term", 2, "Term, fees and billing",
  "<p>Retainers run month to month unless your agreement states a fixed term. Fees are invoiced in advance of each period and are due on receipt unless we have agreed different terms in writing.</p>"
  "<p>Consulting is billed at 30 USD per hour, in arrears, against logged time. Audits and other fixed-scope work are invoiced as set out in the proposal.</p>"
  "<p>If an invoice is more than 14 days overdue we may pause delivery until it is settled. We will always tell you before we pause anything.</p>"),

 ("changes", 3, "Changes, pauses and cancellation",
  "<p>Either of us may cancel a retainer with 30 days' written notice. Notice takes effect at the end of the current billing period, and we keep working normally through it.</p>"
  "<p>You may pause an engagement rather than cancel it. Paused engagements are not billed. If a pause runs beyond six months, resuming may be at our current rates rather than the ones you originally agreed.</p>"),

 ("refunds", 4, "Refunds",
  "<p>Fees for a billing period that has already started are non-refundable, because work is delivered continuously across the period rather than at the end of it.</p>"
  "<p>If we have not started work on a period you have paid for, tell us and we will refund it. We would rather return money than keep a client who does not want to be one.</p>"),

 ("ownership", 5, "Deliverables and ownership",
  "<p>Once an invoice is paid, you own the content, code, schema, documentation and reports we produce specifically for you, and you may use them however you wish.</p>"
  "<p>We retain ownership of our own methods, frameworks, checklists, internal tooling and standard operating procedures. Your engagement grants you the benefit of these, not title to them.</p>"
  "<p>Third-party editorial placements and citations are exactly that: editorial. The publisher controls them. We cannot guarantee any placement remains live indefinitely, and we do not control third-party platforms.</p>"),

 ("results", 6, "Results and what we do not guarantee",
  "<p>We do not guarantee rankings, traffic volumes, citation counts, revenue, or inclusion in any AI-generated answer. Nobody can, and anyone who does is either guessing or misleading you.</p>"
  "<p>We do not control Google, Bing, OpenAI, Anthropic, Google DeepMind, Perplexity, Microsoft or any other platform, and none of them offer a submission or guarantee mechanism. Algorithms change without notice.</p>"
  "<p>What we do commit to is method and reporting: the work described in your scope, executed to the standard in our documented procedures, measured honestly, and reported monthly whether the numbers are flattering or not.</p>"
  "<p>Any figures we share from past client work describe those engagements. They are not a forecast for yours.</p>"),

 ("client", 7, "What we need from you",
  "<p>Engagements depend on access and responsiveness. We will typically need access to your website or CMS, Google Search Console, Google Analytics, Google Business Profile where relevant, and any SEO tooling you already pay for.</p>"
  "<p>We also need decisions. Where a recommendation waits on your approval, the timeline moves with it. We will flag anything blocked rather than let it sit quietly.</p>"
  "<p>You confirm that content and assets you supply are yours to use, and that you have the right to grant us the access you give us.</p>"),

 ("acceptance", 8, "Reporting and acceptance",
  "<p>We report monthly on retained engagements. If something in a deliverable is wrong or outside scope, tell us within 14 days of delivery and we will correct it. After 14 days we treat it as accepted, which simply keeps revision cycles finite.</p>"),

 ("disputes", 9, "Billing disputes",
  "<p>If you disagree with an invoice, email us within 14 days and we will investigate before anything escalates. Please raise it with us before initiating a chargeback &mdash; almost every billing dispute we have seen was a misunderstanding that took one conversation to resolve.</p>"),

 ("confidentiality", 10, "Confidentiality",
  "<p>We treat your commercial data, analytics, strategy and internal information as confidential and do not share it outside our delivery team.</p>"
  "<p>We may describe engagement outcomes anonymously &mdash; for example &ldquo;a UK ecommerce retailer&rdquo; &mdash; in case studies and marketing. We will not name you, show your logo, or publish identifiable data without your written permission. Tell us at any time that you would prefer we did not reference the work at all, and we will stop.</p>"
  "<p>White-label engagements are covered by a separate NDA, and under those we never contact your client or identify ourselves to them.</p>"),

 ("liability", 11, "Limitation of liability",
  "<p>To the extent permitted by law, our total liability arising from an engagement is limited to the fees you paid us in the three months before the claim.</p>"
  "<p>Neither party is liable for indirect or consequential loss, including lost profits, lost revenue, lost data or loss of anticipated savings.</p>"
  "<p>Nothing here limits liability for fraud, or for anything that cannot lawfully be limited.</p>"),

 ("termination", 12, "Termination for cause",
  "<p>Either party may terminate immediately if the other materially breaches these terms and does not remedy it within 15 days of written notice. We may also terminate immediately for non-payment beyond 30 days, or if we are asked to do something we consider deceptive, unlawful, or in breach of a platform's guidelines.</p>"
  "<p>On termination we hand over deliverables paid for to date, and revoke our own access to your systems.</p>"),

 ("general", 13, "General",
  "<p>These terms are governed by the laws of India, and the courts of India have jurisdiction, unless your agreement states otherwise.</p>"
  "<p>We may update this page. Changes apply going forward, never retroactively, and material changes to an active engagement will be raised with you directly rather than quietly published.</p>"
  "<p>If any provision is unenforceable, the rest still stands.</p>"),

 ("contact", 14, "Contact",
  "<p>Questions about these terms, an invoice, or anything else: <a href=\"mailto:hello@svedsolution.com\">hello@svedsolution.com</a> or <a href=\"https://api.whatsapp.com/send?phone=917846045690\">+91 78460 45690</a>.</p>"),
]

PRIVACY_SECTIONS = [
 ("collect", 1, "What we collect",
  "<p><strong>When you submit a form.</strong> Your name, email address, website, phone number if you give it, and whatever you write in the message field. Nothing more.</p>"
  "<p><strong>When you run the free audit.</strong> The website address you enter. We fetch that site's public pages to score them. The URL is cached for 24 hours so repeat checks are fast. We do not keep the audit result against your identity unless you ask us for the full report.</p>"
  "<p><strong>When you browse.</strong> Google Analytics 4 records anonymised, aggregated usage &mdash; pages viewed, approximate region, device type, referrer. We do not use it to identify individuals.</p>"),

 ("why", 2, "Why we collect it",
  "<p>To reply to your enquiry, deliver services you have asked for, send the newsletter if you subscribed, and understand which pages are useful. That is the whole list.</p>"
  "<p>We do not sell your data, rent it, or share it with advertisers. We never will.</p>"),

 ("processors", 3, "Who processes it",
  "<p>We use a small number of third parties, each for a single purpose:</p>"
  "<ul>"
  "<li><strong>Cloudflare</strong> &mdash; hosting, security and email routing</li>"
  "<li><strong>Google Analytics 4</strong> &mdash; anonymised traffic measurement</li>"
  "<li><strong>Resend</strong> &mdash; transactional email delivery</li>"
  "<li><strong>Google Workspace and Google Sheets</strong> &mdash; where enquiries are received and recorded</li>"
  "<li><strong>Cal.com</strong> &mdash; call booking, if you book one</li>"
  "</ul>"
  "<p>Each holds only what it needs to do its job.</p>"),

 ("cookies", 4, "Cookies",
  "<p>We set no advertising or tracking cookies of our own. Google Analytics sets its own analytics cookies. The consultation popup uses your browser's session storage to remember it has already been shown, so it does not reappear on every page &mdash; that never leaves your device.</p>"),

 ("retention", 5, "How long we keep it",
  "<p>Enquiries are kept while the conversation is live and for up to 24 months after, so we have context if you come back. Newsletter subscriptions are kept until you unsubscribe. Audit URL caches expire after 24 hours. Analytics follows Google's retention setting.</p>"),

 ("rights", 6, "Your rights",
  "<p>Email <a href=\"mailto:hello@svedsolution.com\">hello@svedsolution.com</a> and we will, without argument: tell you what we hold about you, correct it, delete it, or send you a copy. Every newsletter has a one-click unsubscribe link.</p>"
  "<p>If you are in the EEA or UK, you have these rights under GDPR and we honour them regardless of where you are.</p>"),

 ("security", 7, "Security",
  "<p>The site is served over HTTPS with HSTS. Enquiry data sits in access-controlled storage, and the admin area requires authentication and is excluded from search indexing. We hold no card details at any point &mdash; payments are handled by the payment provider directly.</p>"),

 ("children", 8, "Children",
  "<p>Our services are for businesses. We do not knowingly collect data from anyone under 18.</p>"),

 ("changes", 9, "Changes and contact",
  "<p>If this policy changes materially we will update the date at the top and, where it affects an active client, tell you directly.</p>"
  "<p>Questions or requests: <a href=\"mailto:hello@svedsolution.com\">hello@svedsolution.com</a>.</p>"),
]


def sitemap_page(posts):
    """Human-readable index of every page, mirroring sitemap.xml."""
    def links(items):
        return "".join(f'<li><a href="{u}">{t}</a></li>' for t, u in items)

    ai = [(s["name"], f'/services/{s["slug"]}/') for s in SERVICES if s["cluster"] == "AI Search"]
    core = [(s["name"], f'/services/{s["slug"]}/') for s in SERVICES if s["cluster"] == "Core SEO"]
    inds = [(i["name"], f'/{i["slug"]}/') for i in INDUSTRIES]
    blog = [(p["title"], f'/insights/{p["slug"]}/') for p in posts]

    return f"""
{phero('<a href="index.html">Home</a> / Sitemap', 'Sitemap',
       'Every page on this site',
       'A complete index of svedsolution.com. Search engines use <a href="/sitemap.xml">sitemap.xml</a>; this page is for people.')}

<section class="sec">
  <div class="wrap">
    <div class="grid g2" style="gap:44px;align-items:start">

      <div class="card">
        <span class="card-num">MAIN PAGES</span>
        <ul class="sitemap-list">{links([
          ("Home", "/"),
          ("Free AI Visibility Audit", "/ai-visibility-audit/"),
          ("Why LLM SEO Now", "/why-llm-seo-now/"),
          ("All Services", "/services/"),
          ("All Industries", "/industries/"),
          ("Use Cases", "/use-cases/"),
          ("Case Studies", "/case-studies/"),
          ("Reviews", "/reviews/"),
          ("Insights (blog)", "/insights/"),
          ("Videos", "/videos/"),
          ("Resources &amp; SOPs", "/resources/"),
          ("About, Values &amp; Team", "/about/"),
          ("Contact", "/contact/"),
        ])}</ul>
      </div>

      <div class="card">
        <span class="card-num">AI SEARCH SERVICES</span>
        <ul class="sitemap-list">{links(
          [("Generative Engine Optimization (GEO)", "/generative-engine-optimization/")] + ai)}</ul>
      </div>

      <div class="card">
        <span class="card-num">CORE SEO SERVICES</span>
        <ul class="sitemap-list">{links(core)}</ul>
      </div>

      <div class="card">
        <span class="card-num">INDUSTRIES</span>
        <ul class="sitemap-list">{links(inds)}</ul>
      </div>

      <div class="card" style="grid-column:1/-1">
        <span class="card-num">INSIGHTS</span>
        <ul class="sitemap-list">{links(blog)}</ul>
      </div>

      <div class="card">
        <span class="card-num">LEGAL</span>
        <ul class="sitemap-list">{links([
          ("Terms of Service", "/terms/"),
          ("Privacy Policy", "/privacy/"),
        ])}</ul>
      </div>

      <div class="card" style="grid-column:1/-1">
        <span class="card-num">FOR MACHINES</span>
        <ul class="sitemap-list">{links([
          ("sitemap.xml &mdash; XML sitemap for search engines", "/sitemap.xml"),
          ("robots.txt &mdash; crawler directives, 15 AI crawlers allowed", "/robots.txt"),
          ("llms.txt &mdash; brand and content description for LLMs", "/llms.txt"),
        ])}</ul>
      </div>

    </div>
  </div>
</section>

{cta("Cannot find what you need?",
     "Run the free audit, or send us a message and we will point you at the right page.")}
"""


NOT_FOUND_BODY = """
<section class="phero" style="padding-bottom:40px">
  <div class="wrap">
    <div class="eyebrow">Error 404</div>
    <h1 style="max-width:16ch">This page does not exist.</h1>
    <p class="lead dim" style="max-width:60ch;margin-top:1.2rem">The link may be outdated, or the address may have a typo. Here is where most people were heading.</p>
    <div class="btn-row" style="margin-top:2rem">
      <a class="btn btn-primary btn-lg" href="ai-visibility-audit.html">Run a free AI visibility audit</a>
      <a class="btn btn-ghost btn-lg" href="index.html">Back to the homepage</a>
    </div>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="grid g3">
      <a class="card card-link" href="services.html"><div class="card-icon">&#9670;</div><h3>Services</h3><p>Eighteen services across AI search and core SEO.</p><span class="card-more">Browse services &rarr;</span></a>
      <a class="card card-link" href="generative-engine-optimization.html"><div class="card-icon">&#10022;</div><h3>GEO</h3><p>Get named by ChatGPT, Perplexity and Gemini.</p><span class="card-more">Explore GEO &rarr;</span></a>
      <a class="card card-link" href="insights.html"><div class="card-icon">&#9998;</div><h3>Insights</h3><p>Practitioner writing on GEO, AEO and technical SEO.</p><span class="card-more">Read insights &rarr;</span></a>
      <a class="card card-link" href="case-studies.html"><div class="card-icon">&#9636;</div><h3>Case studies</h3><p>2,923 AI citations in 29 days, and how.</p><span class="card-more">See results &rarr;</span></a>
      <a class="card card-link" href="use-cases.html"><div class="card-icon">&#9635;</div><h3>Use cases</h3><p>Eight problems, eight documented responses.</p><span class="card-more">Find yours &rarr;</span></a>
      <a class="card card-link" href="contact.html"><div class="card-icon">&#9993;</div><h3>Contact</h3><p>Talk to the strategist who runs your audit.</p><span class="card-more">Get in touch &rarr;</span></a>
    </div>
  </div>
</section>
"""


# --------------------------------------------------------------------------
# Render
# --------------------------------------------------------------------------
DIST = os.path.join(OUT, "dist")


# Content hashes for cache-busting.
#
# _headers serves /assets/* with `immutable, max-age=31536000`. On a filename
# that never changes, that means browsers and the CDN pin the first version
# they ever saw and no later edit is delivered. Hashing the content into the
# filename means an edit produces a new URL, so the long cache stays safe.
ASSET_HASHES = {}


def hash_assets():
    import hashlib
    for name in ("style.css", "app.js"):
        path = os.path.join(OUT, "assets", name)
        if not os.path.exists(path):
            continue
        with open(path, "rb") as f:
            digest = hashlib.sha256(f.read()).hexdigest()[:10]
        stem, ext = name.rsplit(".", 1)
        ASSET_HASHES[name] = f"{stem}.{digest}.{ext}"
    return ASSET_HASHES


def to_clean_urls(html, depth=0):
    """Rewrite flat .html links to root-absolute clean URLs for Cloudflare Pages."""
    html = re.sub(r'(href|src)="index\.html(#[^"]*)?"', lambda m: f'{m.group(1)}="/{m.group(2) or ""}"', html)
    html = re.sub(r'(href|src)="([a-z0-9\-]+)\.html(#[^"]*)?"',
                  lambda m: f'{m.group(1)}="/{m.group(2)}/{m.group(3) or ""}"', html)
    html = re.sub(r'(href|src)="assets/', r'\1="/assets/', html)
    for original, hashed in ASSET_HASHES.items():
        html = html.replace(f"/assets/{original}", f"/assets/{hashed}")
    return html


# Filled during build() once the markdown posts are loaded; a one-element list
# so render() reads the current value rather than a copy taken at import time.
LATEST_POSTS_HTML = [""]

DEFAULT_KEYWORDS = ("SEO services India, GEO services, generative engine optimization, "
                    "answer engine optimization, LLM SEO, AI SEO agency, ChatGPT SEO, "
                    "Perplexity SEO, AI visibility, technical SEO, SEO agency Kolkata")


def render(title, desc, slug, body, schema=None, keywords=None):
    html = SHELL.format(title=title, desc=desc, slug=slug, keywords=keywords or DEFAULT_KEYWORDS,
                        schema=schema or ORG_SCHEMA, nav=NAV, logo=LOGO_SVG,
                        body=body, footer=FOOTER)
    # Literal placeholders replaced after .format() so braces in the gtag
    # snippet never have to be escaped twice, and so page bodies can reference
    # component builders that are defined further down the file.
    html = (html
            .replace("<!--GTM-HEAD-->", GTM_HEAD.replace("GTM_CONTAINER_ID", GTM_ID))
            .replace("<!--GTM-BODY-->", GTM_BODY.replace("GTM_CONTAINER_ID", GTM_ID))
            .replace("CALENDLY_URL", CALENDLY)
            .replace("WHATSAPP_NUMBER", WHATSAPP_RAW)
            .replace("<!--TEAM-->", TEAM_CARDS)
            .replace("<!--PLATFORMS-->", platform_strip())
            .replace("<!--CERTS-->", cert_strip())
            .replace("<!--TOOLS-->", tools_grid())
            .replace("<!--LATEST-POSTS-->", LATEST_POSTS_HTML[0]))
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

    hash_assets()
    written = []
    posts = load_posts()

    def card(p):
        return (f'<a class="card card-link" href="/insights/{p["slug"]}/">'
                f'<span class="card-num">{p["category"].upper()} &middot; {p["read"]}</span>'
                f'<h3>{p["title"]}</h3><p>{p["desc"]}</p>'
                f'<span class="card-more">Read &rarr;</span></a>')

    # Blog listing is generated from the markdown files, not hardcoded.
    if posts:
        cards = "".join(card(p) for p in posts)
        PAGES["insights"]["body"] = re.sub(
            r'(<div class="grid g3">)(.*?)(</div>\s*<div class="center mt3">)',
            lambda m: m.group(1) + cards + m.group(3),
            PAGES["insights"]["body"], flags=re.S)
        # Three most recent, for the homepage strip.
        LATEST_POSTS_HTML[0] = ('<div class="grid g3">'
                                + "".join(card(p) for p in posts[:3]) + '</div>')

    # Directory-style output so clean URLs work identically on Cloudflare Pages
    # and on any plain static server used for local review.
    for slug, p in PAGES.items():
        html = render(p["title"], p["desc"], p["slug"], p["body"],
                      schema=team_schema() if slug == "about" else None)
        name = "index.html" if slug == "index" else os.path.join(slug, "index.html")
        written.append((name.replace("\\", "/"), write(name, html)))

    for p in posts:
        html = render(f'{p["title"]} | SVED Solution', p["desc"],
                      f'insights/{p["slug"]}/', post_page(p), post_schema(p))
        rel = os.path.join("insights", p["slug"], "index.html")
        written.append((rel.replace("\\", "/"), write(rel, html)))

    # One page per industry, described by sector rather than client name.
    for i in INDUSTRIES:
        plain = i["name"].replace("&amp;", "and")
        html = render(
            f'{plain} SEO Services India | SVED Solution',
            re.sub(r"<[^>]+>", "", i["short"])[:152],
            f'{i["slug"]}/', industry_page(i),
            keywords=i["kw"])
        rel = os.path.join(i["slug"], "index.html")
        written.append((rel.replace("\\", "/"), write(rel, html)))

    for slug, title, desc, intro, sections in [
        ("terms", "Terms of Service",
         "Terms of service for SVED Solution: scope, fees, cancellation, ownership, what we guarantee and what we do not.",
         "The commercial terms behind every engagement. Written to be read, not to be skipped &mdash; if a clause is unclear, ask and we will explain it.",
         TERMS_SECTIONS),
        ("privacy", "Privacy Policy",
         "What data SVED Solution collects, why, who processes it, how long we keep it and how to have it deleted.",
         "What we collect, why, and how to get rid of it. We do not sell your data and we never will.",
         PRIVACY_SECTIONS),
    ]:
        html = render(f"{title} | SVED Solution", desc, f"{slug}/",
                      legal_page(title, intro, sections),
                      keywords=f"SVED Solution {title.lower()}")
        rel = os.path.join(slug, "index.html")
        written.append((rel.replace("\\", "/"), write(rel, html)))

    # Human-readable sitemap, built from the same data as sitemap.xml.
    written.append(("sitemap/index.html", write(
        os.path.join("sitemap", "index.html"),
        render("Sitemap | Every Page on SVED Solution",
               "Complete index of svedsolution.com: services, industries, insights and resources.",
               "sitemap/", sitemap_page(posts)))))

    # One page per service.
    for s in SERVICES:
        plain = s["name"].replace("&amp;", "and")
        html = render(
            f'{plain} Services | SVED Solution',
            re.sub(r"<[^>]+>", "", s["answer"])[:152],
            f'services/{s["slug"]}/', service_page(s),
            schema=service_schema(s), keywords=s["kw"])
        rel = os.path.join("services", s["slug"], "index.html")
        written.append((rel.replace("\\", "/"), write(rel, html)))

    # Without a 404.html, Cloudflare Pages answers unknown paths with the
    # homepage and HTTP 200 — a soft 404 that lets search engines index
    # unlimited duplicates of the home page.
    written.append(("404.html", write("404.html", render(
        "Page not found | SVED Solution",
        "That page does not exist. Find our services, insights or the free AI visibility audit instead.",
        "404/", NOT_FOUND_BODY))))

    copy_tree("assets")
    copy_tree("admin")
    nstatic = copy_static()

    # Emit the hashed copies alongside the originals so a stale HTML page
    # cached by a browser still resolves its old stylesheet.
    import shutil
    for original, hashed in ASSET_HASHES.items():
        src = os.path.join(DIST, "assets", original)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(DIST, "assets", hashed))

    # ---- sitemap -------------------------------------------------------
    # Every generated URL, with priority and change frequency reflecting how
    # each page type actually behaves.
    today = _dt.date.today().isoformat()
    entries = []

    def add(loc, priority, freq, lastmod=today):
        entries.append((loc, priority, freq, lastmod))

    for slug, p in PAGES.items():
        loc = "https://svedsolution.com/" + (p["slug"] or "")
        if slug == "index":
            add(loc, "1.0", "weekly")
        elif slug in ("ai-visibility-audit", "services", "industries", "contact"):
            add(loc, "0.9", "weekly")
        elif slug in ("insights",):
            add(loc, "0.8", "daily")
        else:
            add(loc, "0.7", "monthly")

    add("https://svedsolution.com/generative-engine-optimization/", "0.9", "monthly")
    add("https://svedsolution.com/sitemap/", "0.3", "weekly")
    add("https://svedsolution.com/terms/", "0.3", "yearly")
    add("https://svedsolution.com/privacy/", "0.3", "yearly")
    for s in SERVICES:
        add(f'https://svedsolution.com/services/{s["slug"]}/', "0.8", "monthly")
    for i in INDUSTRIES:
        add(f'https://svedsolution.com/{i["slug"]}/', "0.8", "monthly")
    for p in posts:
        add(f'https://svedsolution.com/insights/{p["slug"]}/', "0.7", "monthly",
            p.get("date") or today)

    # De-duplicate while preserving order; GEO has both a bespoke page entry
    # and a PAGES entry.
    seen, rows = set(), []
    for loc, pr, freq, lm in entries:
        if loc in seen:
            continue
        seen.add(loc)
        rows.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lm}</lastmod>\n"
                    f"    <changefreq>{freq}</changefreq>\n    <priority>{pr}</priority>\n  </url>\n")

    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(rows) + "</urlset>\n")

    verify_canonicals()
    return written, len(posts), nstatic, len(rows)


def verify_canonicals():
    """
    Fail the build if any page's canonical points somewhere that was not
    written. A canonical aimed at a 404 quietly removes the page from the
    index, and nothing else in the pipeline would catch it.
    """
    problems = []
    for dirpath, _dirs, files in os.walk(DIST):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            path = os.path.join(dirpath, fn)
            with io.open(path, encoding="utf-8") as f:
                m = re.search(r'<link rel="canonical" href="https://svedsolution\.com/([^"]*)"', f.read())
            if not m:
                continue
            target = m.group(1)
            expected = DIST if not target else os.path.join(DIST, *target.strip("/").split("/"))
            if target and not (os.path.isfile(expected + ".html")
                               or os.path.isfile(os.path.join(expected, "index.html"))):
                problems.append(f"  {os.path.relpath(path, DIST)} -> /{target} (no such page)")

    if problems:
        raise SystemExit("Canonical URLs point at pages that do not exist:\n" + "\n".join(problems))
    print("canonical check: all canonicals resolve to real pages")


def service_schema(s):
    plain = s["name"].replace("&amp;", "and")
    return ('{"@context":"https://schema.org","@type":"Service",'
            f'"name":{_j(plain)},"serviceType":{_j(plain)},'
            f'"description":{_j(re.sub(chr(60) + "[^" + chr(62) + "]+" + chr(62), "", s["answer"]))},'
            '"provider":{"@type":"ProfessionalService","name":"SVED Solution",'
            '"url":"https://svedsolution.com/","telephone":"+917846045690",'
            '"email":"hello@svedsolution.com"},'
            '"areaServed":["IN","US","GB","AE","CA","AU"],'
            f'"url":"https://svedsolution.com/services/{s["slug"]}/",'
            '"offers":{"@type":"Offer","priceCurrency":"USD","price":"30",'
            '"description":"Consulting from $30 per hour; retainers scoped after audit"}}')


if __name__ == "__main__":
    files, nposts, nstatic, nurls = build()
    for name, size in files:
        print("%-52s %8d bytes" % (name, size))
    print("\n%d core pages + %d services + %d industries + %d posts + %d static"
          % (len(PAGES), len(SERVICES), len(INDUSTRIES), nposts, nstatic))
    print("sitemap.xml: %d URLs -> %s" % (nurls, DIST))
