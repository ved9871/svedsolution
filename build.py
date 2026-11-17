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

# Team.
TEAM = [
    dict(name="Ved Prakash", initials="VP", role="Founder &amp; Head of Strategy",
         bio="Leads the SEO and AI search work on every account. Reviews the sites, sets the plans "
             "and writes the monthly reports. More than ten years in SEO, paid search and "
             "analytics for brands in India, the UAE, the UK and the US.",
         focus=["AI search (GEO)", "SEO and paid search", "Monthly written reports"],
         links=[("LinkedIn", FOUNDER_LINKEDIN)], photo="ved-prakash.webp"),
    dict(name="Amit Kumar", initials="AK", role="Technical Head",
         bio="Builds the shops, websites and apps, and the tracking and automation behind them.",
         focus=["Shops and websites", "Tracking and data", "Automation"],
         links=[], photo="amit-kumar.webp"),
    dict(name="Rahul Dhiman", initials="RD", role="Founder, commerce and automation",
         bio="Leads online shop builds, customer email programmes and automation.",
         focus=["Shop builds", "Customer email", "Automation"],
         links=[], photo="rahul-dhiman.webp"),
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
        if m.get("photo"):
            avatar = (f'<img class="team-photo" src="/assets/team/{m["photo"]}" width="720" height="900" '
                      f'alt="{m["name"]}" loading="lazy">')
        else:
            avatar = f'<div class="team-avatar">{m["initials"]}</div>'
        out.append(f'''<div class="card team-card">
          {avatar}
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
      <div class="drop-head">Paid ads, data and websites</div>
      <a href="/services/performance-marketing/">Performance Marketing</a>
      <a href="/services/marketing-automation/">Marketing Automation &amp; Data</a>
      <a href="/services/ecommerce-development/">Ecommerce &amp; App Development</a>
      <a href="use-cases.html">Use Cases</a>
      <a href="services.html">All 21 services &rarr;</a>
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
  <a href="case-studies.html" data-nav="case-studies">Case Studies</a>
  <div class="has-drop">
    <a href="insights.html" data-nav="insights">Insights &#9662;</a>
    <div class="drop" style="min-width:340px">
      <a href="insights.html">Blog</a>
      <a href="videos.html">Videos</a>
      <a href="resources.html">Resources &amp; guides</a>
      <a href="why-llm-seo-now.html">Why LLM SEO Now</a>
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
    <p class="foot-bye" aria-hidden="true">Bye<span class="logo-dot"></span></p>
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
        <a href="index.html" class="logo" style="margin-bottom:16px">SVED<span class="logo-dot" aria-hidden="true"></span></a>
        <p>Search, AI visibility and performance marketing. We get brands found on Google, named by AI and bought through paid media.</p>
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
        <p class="faint" style="font-size:.86rem;margin-bottom:14px">AI search news and what to do about it, by email.</p>
        <form class="sved-form" data-type="newsletter">
          <input type="email" name="email" placeholder="you@company.com" aria-label="Email" required>
          <button class="btn btn-primary btn-sm" type="submit" style="width:100%;justify-content:center">Subscribe</button>
          <p class="form-status" role="status"></p>
        </form>
        <p class="faint" style="font-size:.76rem;margin-top:10px">Free. Unsubscribe at any time.</p>
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
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_image}">
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
<link rel="preload" href="/assets/fonts/gabarito-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/onest-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/style.css">
<script type="application/ld+json">{schema}</script>
</head>
<body>
<!--GTM-BODY-->
<a href="#main" class="skip-link">Skip to content</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a href="index.html" class="logo" aria-label="SVED Solution home">SVED<span class="logo-dot" aria-hidden="true"></span></a>
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
  <span>Chat on WhatsApp</span>
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
  "description":"SEO, AI search and paid ads agency. Generative Engine Optimization (GEO), Answer Engine Optimization (AEO), LLM SEO, performance marketing, tracking and website builds.",
  "slogan":"Top 1% SEO Service Provider in India",
  "areaServed":["US","GB","CA","AU","IN","AE"],
  "knowsAbout":["Generative Engine Optimization","Answer Engine Optimization","LLM SEO","Technical SEO","Semantic SEO","Entity SEO","AI Overviews","Performance Marketing","Marketing Automation","Ecommerce Development"],
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
      <div class="eyebrow">Next step</div>
      <h2>{title}</h2>
      <p>{sub}</p>
      <div class="btn-row">
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
      <p class="faint" style="font-size:.85rem;margin-top:20px">No card. No call required. 20 checks in about a minute.</p>
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
      <div class="card"><span class="card-num">01</span><h3>Audit</h3><p>20-point AI visibility check, technical crawl, competitor citation reverse-engineering and an ICP interview.</p></div>
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
     "Twenty checks covering AI crawler access, how your business is described, how your content is laid out and the search basics. No card, no call.")}
""")

# ==========================================================================
# AUDIT TOOL
# ==========================================================================
PAGES["ai-visibility-audit"] = dict(
    title="Free AI Visibility Check | Can AI Tools Find Your Business? | SVED Solution",
    desc="Free 20-point check of your website: can ChatGPT, Perplexity, Gemini and Google's AI answers read it, tell who you are and quote you? Your score in about a minute.",
    slug="ai-visibility-audit/",
    body=f"""
<section class="phero">
  <div class="wrap">
    <div class="crumbs"><a href="index.html">Home</a> / Free AI Visibility Check</div>
    <div class="eyebrow">Free check &middot; no card &middot; no call</div>
    <h1 style="max-width:18ch">Can AI tools find and recommend your business?</h1>
    <p class="lead dim" style="max-width:64ch;margin-top:1.2rem">Enter your website and we run 20 checks on it. You see whether ChatGPT, Perplexity, Gemini and Google's AI answers can read your site, work out who you are and quote you. It takes about a minute.</p>

    <div style="max-width:860px;margin-top:36px">
      <form id="audit-form" class="audit-form audit-form-v2" novalidate>
        <!-- type=text, not url: type=url makes the browser reject "example.com"
             before it ever reaches the API. The API resolves the variations. -->
        <label class="af-field af-wide"><span>Your website</span>
          <input type="text" id="audit-url" name="website" inputmode="url" autocapitalize="off" spellcheck="false"
                 placeholder="example.com" required></label>
        <label class="af-field"><span>Your name</span>
          <input type="text" id="audit-name" name="name" autocomplete="name" required></label>
        <label class="af-field"><span>Work email</span>
          <input type="email" id="audit-email" name="email" autocomplete="email" required></label>
        <input class="af-hp" type="text" name="company_website" tabindex="-1" autocomplete="off" aria-hidden="true">
        <!-- Unticked by default and not required: marketing email needs a free, separate choice. -->
        <label class="af-consent af-wide"><input type="checkbox" id="audit-consent" name="consent">
          <span>Email me AI search news and tips from SVED Solution. Optional, and you can unsubscribe at any time.</span></label>
        <button class="btn btn-primary btn-lg af-wide" id="audit-run" type="submit">Check my site</button>
        <p id="audit-error" class="form-status err af-wide" role="alert"></p>
        <p class="af-note af-wide">We use your name and email to send your result and to follow up about it. We only add you to the newsletter if you tick the box. See our <a href="privacy.html">privacy policy</a>.</p>
      </form>
      <div id="audit-stage" style="display:none;font-size:.9rem;line-height:2;margin-top:24px;color:var(--text-dim)"></div>
      <div id="audit-results" style="display:none"></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">What we check</div>
      <h2>Twenty checks, in four groups</h2>
      <p class="lead dim">Each check comes back as good, needs work or a problem, with a plain explanation and what to do about it.</p>
    </div>
    <div class="grid g2">
      <div class="card"><span class="card-num">Group 1</span><h3>Can AI tools reach your site?</h3>
        <ul style="padding-left:1.1em;margin:14px 0 0;color:var(--text-dim)">
          <li>AI crawlers are allowed in</li><li>Your text can be read without JavaScript</li>
          <li>Nothing stops the page being indexed or quoted</li><li>A sitemap lists your pages</li>
          <li>A guide file for AI tools (llms.txt)</li><li>The page loads quickly on a phone</li></ul></div>
      <div class="card"><span class="card-num">Group 2</span><h3>Do they know who you are?</h3>
        <ul style="padding-left:1.1em;margin:14px 0 0;color:var(--text-dim)">
          <li>Your business is described in a way machines can read</li><li>A real person is named</li>
          <li>Your name is written the same way everywhere</li><li>You are on sites AI tools already trust</li></ul></div>
      <div class="card"><span class="card-num">Group 3</span><h3>Is your content easy to quote?</h3>
        <ul style="padding-left:1.1em;margin:14px 0 0;color:var(--text-dim)">
          <li>The page gets to the point</li><li>Headings ask the questions people ask</li>
          <li>Questions and answers are marked up</li><li>Facts are set out in lists and tables</li>
          <li>Headings are in a sensible order</li><li>The page shows it is kept up to date</li></ul></div>
      <div class="card"><span class="card-num">Group 4</span><h3>Search basics</h3>
        <ul style="padding-left:1.1em;margin:14px 0 0;color:var(--text-dim)">
          <li>Page title and description</li><li>The page names its official address</li>
          <li>Secure and set up for phones</li><li>Links to your page show a proper preview</li></ul></div>
    </div>
  </div>
</section>

<section class="sec band-green">
  <div class="wrap">
    <div class="grid g2" style="gap:52px;align-items:center">
      <div>
        <div class="eyebrow">Go deeper</div>
        <h2>The full AI visibility report</h2>
        <p class="lead dim">The free check tells you whether AI tools can read and trust your site. The full report shows whether they actually mention you, and who they recommend instead.</p>
        <ul style="list-style:none;padding:0;margin:1.6rem 0">
          <li style="padding:11px 0;border-bottom:1px solid var(--line)"><span class="green mono">&#10003;</span> &nbsp;Real questions tested on ChatGPT, Perplexity and Gemini</li>
          <li style="padding:11px 0;border-bottom:1px solid var(--line)"><span class="green mono">&#10003;</span> &nbsp;Five questions on five AI tools: 25 results in one table</li>
          <li style="padding:11px 0;border-bottom:1px solid var(--line)"><span class="green mono">&#10003;</span> &nbsp;Every site the AI tools recommend instead of you</li>
          <li style="padding:11px 0;border-bottom:1px solid var(--line)"><span class="green mono">&#10003;</span> &nbsp;A 90-day plan in priority order</li>
          <li style="padding:11px 0"><span class="green mono">&#10003;</span> &nbsp;A recorded walkthrough from the strategist who ran it</li>
        </ul>
        <a class="btn btn-primary btn-lg" href="contact.html">Request the full report</a>
      </div>
      <div class="panel">
        <div class="panel-bar"><i class="tdot"></i><i class="tdot"></i><i class="tdot"></i><span style="margin-left:8px">Sample: who the AI tools name</span></div>
        <div class="panel-body" style="font-size:.85rem">
          <div class="crow"><span class="lbl">&ldquo;best [product] for [customer]&rdquo;</span><span class="pill pill-bad">not named</span></div>
          <div class="crow"><span class="lbl">&ldquo;top tools for [problem]&rdquo;</span><span class="pill pill-warn">named 7th</span></div>
          <div class="crow"><span class="lbl">&ldquo;who do you recommend for [need]&rdquo;</span><span class="pill pill-bad">not named</span></div>
          <div class="crow"><span class="lbl">&ldquo;best brands in [category]&rdquo;</span><span class="pill pill-warn">named 4th</span></div>
          <div class="crow"><span class="lbl">&ldquo;[competitor] alternatives&rdquo;</span><span class="pill pill-ok">named 2nd</span></div>
          <div class="crow"><span class="lbl">Other sites named instead</span><span class="val">14</span></div>
        </div>
      </div>
    </div>
  </div>
</section>

{faq([
  ("Is this really free?",
   "Yes. The 20-point check is free and needs no card. It reads your public page and gives you a score with a plain reason for each result. The full report takes strategist time and paid tools to run, so we do that one on request."),
  ("Why do you ask for my name and email?",
   "So we can send you the result and follow up if you want help acting on it. We do not sell or share your details. The newsletter box is separate and optional: leave it unticked and we will not add you to any mailing list."),
  ("What is llms.txt, and do I need one?",
   "It is a plain-text file on your site that tells AI tools what your site contains and which pages matter. It is optional and still new, and no AI company has confirmed relying on it. It takes a few minutes to add, so we include it in every project."),
  ("Should I block AI crawlers to protect my content?",
   "It depends on what your business needs. Blocking them keeps your content out of AI tools, and also means they cannot recommend you. If you rely on being discovered, blocking usually hurts. If you earn from page views, the answer may be different, and you can block the crawlers that train AI models while still allowing the ones that fetch pages for live answers."),
  ("What do you store?",
   "Your name, email, the website you entered and its score, so we can follow up. The check result is kept for 24 hours so a repeat check is fast. If you tick the newsletter box we also add your email to our AI news list, and you can leave it at any time."),
])}

{cta("Twenty checks. About a minute.",
     "Most sites have a handful of gaps. Knowing which ones is the starting point.",
     primary=("Scroll up and check your site", "#audit-form"),
     secondary=("Talk to a strategist", "contact.html"))}
""")

# ==========================================================================
# WHY LLM SEO NOW
# ==========================================================================
PAGES["why-llm-seo-now"] = dict(
    title="Why You Need LLM SEO Services Now | SVED Solution",
    desc="AI tools are deciding now which brands they recommend in each industry. Why LLM SEO, GEO and AEO should not wait, how long it takes, and what being late costs.",
    slug="why-llm-seo-now/",
    body=f"""
{phero('<a href="index.html">Home</a> / Why LLM SEO Now',
       'Why now',
       'AI tools are choosing their favourite brands now.',
       'In every industry, AI tools end up recommending the same few brands. Those few are being picked today, and getting on the list is cheap while few businesses are trying. In eighteen months it will cost far more, if there is still room.')}

<section class="sec">
  <div class="wrap wrap-narrow prose">

    <div class="answer-block">
      <div class="q">The short answer</div>
      <p>You need LLM SEO now because AI tools such as ChatGPT and Gemini are deciding which brands to recommend in each industry, and early leads grow over time. It takes at least 90 days for AI tools to get to know a brand, and 9 to 12 months before that position is hard to take away. A brand that starts today is settled before its industry gets crowded. A brand that starts in eighteen months has to push out names the AI tools already trust.</p>
    </div>

    <h2>1. Few businesses are competing yet</h2>
    <p>Look at the Google results for the phrases that describe this kind of work:</p>
    <div class="tbl-wrap" style="margin:1.6rem 0">
      <table>
        <tr><th>What people search</th><th>Searches a month</th><th>How hard to rank (out of 100)</th><th>What the results look like</th></tr>
        <tr><td><strong>generative engine optimization</strong></td><td>12,000</td><td>62</td><td>Almost no other sites link to any page in the top ten. Big brands published thin pages in a hurry.</td></tr>
        <tr><td><strong>answer engine optimization</strong></td><td>3,700</td><td>45</td><td>Weaker competition again. A Reddit thread ranks second.</td></tr>
        <tr><td><strong>geo vs seo</strong></td><td>2,600</td><td>12</td><td>Every page in the top ten has very few links. Wide open.</td></tr>
        <tr><td><strong>llm seo</strong></td><td>1,400</td><td>14</td><td>Reddit ranks second. Anyone with real experience and a case study can compete.</td></tr>
      </table>
    </div>
    <p>A phrase searched 12,000 times a month, where the top results have almost nothing behind them, is unusual. It will not stay that way. Big brands publish a quick page first and a proper one later. When they do, the easy opening is gone.</p>

    <h2>2. Google ranks pages. AI recommends brands.</h2>
    <p>This is the real change, and it is why waiting costs more here than in ordinary SEO. In a list of links, a new page can overtake an old one on its own strength. In an AI answer, the tool is not comparing pages. It is recalling which brands it connects with the question. That connection comes from seeing the brand mentioned again and again, in the same way, on sites the AI tool already trusts.</p>
    <p><strong>You cannot buy that in three months.</strong> It builds slowly, which is exactly why it is hard for a competitor to take from you once you have it.</p>

    <h2>3. People already get answers without clicking</h2>
    <p>Google's AI summaries now sit above the normal results for a large share of searches. The click you used to earn in third place is increasingly lost to a summary that names two or three brands. If you are not one of them, third place is worth less than it was. Your report will show fewer clicks, and a better page title will not fix it.</p>
    <p>The way to defend your traffic and the way to grow it are the same: be a brand named in the answer.</p>

    <h2>4. What being late costs</h2>
    <ul>
      <li><strong>Three months of work today</strong> gets AI tools to know your brand and brings the first mentions, while few competitors are trying.</li>
      <li><strong>Three months of work in two years</strong> is the same work, but you are trying to push out brands the AI tools have named thousands of times. Replacing a known brand costs several times more than becoming one.</li>
      <li><strong>The gap keeps growing.</strong> Every month a competitor is mentioned and you are not, their position gets stronger and yours gets relatively weaker.</li>
    </ul>

    <h2>5. What this does not mean</h2>
    <p>It does not mean giving up ordinary SEO. Nearly everything that helps with AI tools also helps with Google: a site that can be read, clear structure, markup, links from trusted sites and fresh content. A site with technical faults cannot win at either. Anyone selling AI search work without looking at the health of your site is selling you a report.</p>
    <p>It also does not mean instant results. If someone promises AI mentions within two weeks, ask to see the data. We publish our timeline because the honest version is the one that holds up.</p>

    <h2>How long it really takes</h2>
    <div class="tl" style="margin-top:1.6rem">
      <div class="tl-item"><div class="tl-when">Days 30&ndash;45</div><h4>AI tools know who you are</h4><p>They can tell what your business is, what industry it is in and who runs it.</p></div>
      <div class="tl-item"><div class="tl-when">Day 60</div><h4>First mentions</h4><p>Your pages start to appear as sources for specific questions in your industry.</p></div>
      <div class="tl-item"><div class="tl-when">Day 90</div><h4>Named regularly</h4><p>Your brand is named in answers, not only linked, across several kinds of question.</p></div>
      <div class="tl-item"><div class="tl-when">Months 4&ndash;6</div><h4>Steady visibility</h4><p>The same results week after week, without spikes and drops.</p></div>
      <div class="tl-item"><div class="tl-when">Months 9&ndash;12</div><h4>A go-to brand</h4><p>One of the brands AI tools name by default in your industry. Costly to reach, cheap to keep.</p></div>
    </div>
  </div>
</section>

{faq([
  ("Is GEO a fad that will disappear when the hype dies?",
   "The name may change. The need will not. As long as a tool writes an answer instead of showing a list, something decides which brands and sources go into that answer. Influencing that is marketing work, whether it is called GEO, AEO, LLM SEO or just SEO."),
  ("We already rank #1 on Google. Do we still need this?",
   "Ranking first is a strong start, and it is not enough. AI tools rely heavily on what other sites say about you. A site can rank first and still be missing from the AI answer above it, which is now what people read first. If you rank first and are not named, the visitors go to whoever is."),
  ("Can we do this in-house?",
   "Partly, and you should. Markup, clear answers at the top of pages and keeping content fresh are jobs your own team can do once someone has set the standard. The harder parts are getting mentioned on outside sites, studying where competitors are mentioned, and checking AI answers every week. Those need outside relationships and steady routine. We are happy to set the standard and hand it over."),
])}

{cta("See where you stand today.",
     "The free check takes a minute and shows which of its 20 tests your site fails.")}
""")

# ==========================================================================
# GEO — flagship service page
# ==========================================================================
PAGES["generative-engine-optimization"] = dict(
    title="Generative Engine Optimization (GEO) Services | SVED Solution",
    desc="GEO services that help ChatGPT, Perplexity and Gemini name your brand. Clear brand details, mentions on trusted sites, quotable pages and monthly measurement.",
    # Must match where build() actually writes this page, or the canonical
    # points at a 404 and search engines drop the URL.
    slug="generative-engine-optimization/",
    body=f"""
{phero('<a href="index.html">Home</a> / <a href="services.html">Services</a> / Generative Engine Optimization',
       'AI search &middot; main service',
       'Generative Engine Optimization',
       'We help your brand become one of the names ChatGPT, Perplexity and Gemini recommend. We do it by making it clear who you are, getting you mentioned on sites AI tools trust, and writing pages they can quote.')}

<section class="sec">
  <div class="wrap">
    <div class="grid g2" style="gap:56px;align-items:start">
      <div class="prose">
        <div class="answer-block" style="margin-top:0">
          <div class="q">What is generative engine optimization?</div>
          <p>Generative engine optimization (GEO) is the work of getting AI tools such as ChatGPT, Perplexity and Gemini to find, trust and name your brand in their answers. SEO competes for a place in a list of links. GEO competes to be the brand the AI tool names. It rests on four things: a clear identity, mentions on trusted outside sites, pages that are easy to quote, and regular updates.</p>
        </div>

        <h2>Why most GEO work fails</h2>
        <p>Because it stops at the website. Teams add FAQ markup, tidy a few headings and wait. Nothing happens, because the AI tool was never unsure about your page. It was unsure about your <strong>brand</strong>.</p>
        <p>AI tools do not trust web pages. They trust brands and people they recognise: ones with a clear speciality, mentions on respected sites, and the same description wherever they appear. If your brand is not seen on several trusted sites, no change to your own pages will get you recommended.</p>

        <h2>The four things we build</h2>
        <h3>1. A clear identity</h3>
        <p>We make sure AI tools can tell exactly who you are. The same brand name everywhere, a clear business category, the founder linked to the company, one proper About page, and markup that connects it all to your real profiles. Then we get independent sites to describe you in the same words. That consistency is what builds trust.</p>

        <h3>2. Mentions on trusted sites</h3>
        <p>This is where most brands fall short, and it is the most valuable work we do. AI tools give more weight to what others say about you than to your own site.</p>
        <ul>
          <li><strong>Must-haves:</strong> G2, Capterra, Trustpilot, Crunchbase, Product Hunt, Reddit and Quora, or the equivalents for your industry.</li>
          <li><strong>Extras that add weight:</strong> guest articles by the founder, industry blogs, podcast notes, LinkedIn newsletters and community mentions.</li>
        </ul>
        <p>When an AI tool sees the same brand confirmed on several trusted, independent sites, it treats that as agreement. We build that agreement honestly and steadily.</p>

        <h3>3. Pages that are easy to quote</h3>
        <p>AI tools do not quote whole blog posts. They quote answers. Every page we write or rework follows the same shape: one sentence that states the problem, a straight answer, short points that explain it, examples with real figures, and a visible date showing when it was last updated.</p>
        <p>We stop writing long essays, pages stuffed with keywords, story-style introductions and opinion without evidence. We write lists, tables, comparisons, step-by-step guides and FAQs with full answers.</p>

        <h3>4. Updates every 30 days</h3>
        <p>Publishing once is not enough. AI tools prefer pages that were updated recently and carry current facts. Every thirty days we update the figures, add new questions and answers, improve the links between pages and share the page again on three platforms.</p>

        <h2>Learning from competitors who are already named</h2>
        <p>This is the first thing we do, and it saves a lot of guessing. We take the brands already appearing in AI answers for your industry and list every website quoted alongside them. We look at where they are mentioned, which pages the AI tools use and what words are used about them. Then we earn the same placements, publish stronger content and build a wider presence on the same platforms.</p>

        <h2>How we measure it</h2>
        <p>Two ways, reported every month. <strong>Tracking software</strong> shows how often AI tools use your site as a source and which pages they use. <strong>Weekly manual checks</strong> ask a fixed list of questions for your industry on ChatGPT, Perplexity and Gemini, and record which brands are named and which sources are used. Tracking software is unreliable alone. The manual checks are what make the numbers trustworthy.</p>
      </div>

      <aside style="position:sticky;top:96px">
        <div class="panel" style="margin-bottom:20px">
          <div class="panel-bar"><i class="tdot"></i><i class="tdot"></i><i class="tdot"></i><span style="margin-left:8px">one client &middot; 29 days</span></div>
          <div class="panel-body">
            <div class="crow"><span class="lbl">Times AI tools used the site</span><span class="val">2,923</span></div>
            <div class="crow"><span class="lbl">Pages used</span><span class="val">131</span></div>
            <div class="crow"><span class="lbl">Most-used page</span><span class="val">307</span></div>
            <div class="crow"><span class="lbl">Average per day</span><span class="val">101</span></div>
          </div>
        </div>
        <div class="card">
          <h4 style="margin-bottom:14px">What GEO work includes</h4>
          <ul style="list-style:none;padding:0;margin:0;font-size:.9rem">
            <li style="padding:8px 0;border-bottom:1px solid var(--line-soft)">Brand details and markup set up</li>
            <li style="padding:8px 0;border-bottom:1px solid var(--line-soft)">Profiles on the sites that matter</li>
            <li style="padding:8px 0;border-bottom:1px solid var(--line-soft)">Study of where competitors are mentioned</li>
            <li style="padding:8px 0;border-bottom:1px solid var(--line-soft)">Pages rewritten with clear answers</li>
            <li style="padding:8px 0;border-bottom:1px solid var(--line-soft)">llms.txt and AI crawler settings</li>
            <li style="padding:8px 0;border-bottom:1px solid var(--line-soft)">Weekly checks of AI answers</li>
            <li style="padding:8px 0">Written monthly report</li>
          </ul>
          <a class="btn btn-primary btn-sm" style="width:100%;justify-content:center;margin-top:18px" href="contact.html">Talk to us about GEO</a>
        </div>
      </aside>
    </div>
  </div>
</section>

<section class="sec band-alt">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">What you get</div>
      <h2>The first three months</h2>
    </div>
    <div class="grid g3">
      <div class="card"><span class="card-num">MONTH 1</span><h3>Where you stand</h3><p>How AI tools see your brand today, the 20-point visibility check, a study of where competitors are mentioned, and a 90-day plan in order of importance.</p></div>
      <div class="card"><span class="card-num">MONTH 2</span><h3>Pages and markup</h3><p>Markup for your organisation, people, services and FAQs goes live. Clear answers on every sales page. llms.txt added.</p></div>
      <div class="card"><span class="card-num">MONTH 3</span><h3>Mentions</h3><p>Main profiles created and verified. First guest articles and community mentions live. First AI mentions tracked.</p></div>
    </div>
  </div>
</section>

{faq([
  ("How is GEO different from AEO and LLM SEO?",
   "The terms overlap and people use them loosely, so here is how we separate them. GEO is about your brand being named in an AI answer. It depends mostly on what other sites say about you. AEO (answer engine optimization) is about one page being the direct answer to one question. It depends on how the page is written and marked up. LLM SEO is the technical part: making sure AI tools can read and quote your pages. We do all three. They are sold separately because the work and the timelines differ."),
  ("Can you guarantee we will be cited by ChatGPT?",
   "No, and be wary of anyone who does. We do not control the AI tools and there is nowhere to submit a site. What we control is everything that makes a mention more likely: a clear identity, mentions on trusted sites, quotable pages and fresh content. We report the numbers every month so you can see whether it is working."),
  ("Do we need to be on G2 and Capterra if we are not software?",
   "The sites change with the industry. Software brands need G2 and Capterra. An online shop needs Trustpilot, the marketplaces and mentions in its community. A local service business needs something different again. The principle stays the same: trusted, independent sites describing you in the same way. We build the list for your industry during the first review."),
  ("Will GEO work if our technical SEO is broken?",
   "No, and this is the most common reason the work fails elsewhere. If your pages cannot be reached, only load with JavaScript, or are lost among thousands of duplicate pages, AI tools never get to read them. A healthy site comes first. Our review covers it, and we will tell you if the technical work needs to be done before anything else."),
])}

{cta("See where your site stands.",
     "The free check tests whether AI tools can read and quote your pages.")}
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
    "paid": "/services/performance-marketing/",
    "automation": "/services/marketing-automation/",
    "builds": "/services/ecommerce-development/",
}


def svc(anchor, num, name, desc, bullets, tag="SEO"):
    lis = "".join(f"<li>{b}</li>" for b in bullets)
    url = SERVICE_URLS.get(anchor, "services.html")
    return f"""
<div class="card" id="{anchor}" style="scroll-margin-top:90px;display:flex;flex-direction:column">
  <span class="card-num">{num} &middot; {tag}</span>
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
        "Get your business named when people ask ChatGPT, Perplexity or Gemini for a recommendation. We make it clear who you are, get you mentioned on sites these tools trust, and keep your key pages up to date.",
        ["A clear, consistent description of your business across the web", "Mentions on the sites AI tools rely on",
         "A look at who gets recommended instead of you, and why", "Weekly tests of what the AI tools actually say"], "AI search"),
    svc("aeo", "02", "Answer Engine Optimization",
        "Become the answer, not one of ten links. We find the questions your customers ask and rewrite your pages to answer them directly.",
        ["The real questions your customers ask, grouped by topic", "A short, direct answer at the top of each page",
         "FAQ sections marked up so machines can read them", "A plan for searches that no longer send clicks"], "AI search"),
    svc("llm-seo", "03", "LLM SEO",
        "The technical side of being read by AI. We make sure AI crawlers can get in, read your pages and tell which part answers what.",
        ["Pages laid out in clear, self-contained sections", "A guide file for AI tools (llms.txt)",
         "Rules for AI crawlers such as GPTBot, ClaudeBot and PerplexityBot",
         "Product and category page templates rebuilt to match"], "AI search"),
    svc("citation", "04", "AI Citation &amp; Entity Building",
        "What other sites say about you counts for more than what you say yourself. We build your presence on the review sites, directories and communities AI tools trust.",
        ["Profiles on G2, Capterra, Trustpilot, Crunchbase and similar", "Useful answers on Reddit and Quora, done properly",
         "Articles, podcasts and newsletters under your founder's name", "Press coverage aimed at being mentioned, not just linked"], "AI search"),
    svc("monitoring", "05", "AI Visibility Monitoring &amp; Reporting",
        "Know how often AI tools mention you and which pages they use. One monthly report in plain English, next to your clicks and revenue.",
        ["Tracking of AI mentions, page by page", "The same questions tested every week on three or more AI tools",
         "How often you are named compared with competitors", "A written monthly report, not a dashboard to decode"], "AI search"),
    svc("aio", "06", "Google AI Overviews Optimization",
        "Win back the clicks Google's AI answers took. We find the searches where you lost traffic and work on getting you named in the answer.",
        ["A list of your searches that now show an AI answer", "Where the lost clicks went, from Search Console",
         "Pages rewritten so they can be quoted in the answer", "Stronger signals about who you are"], "AI search"),
])

CORE_SERVICES = "".join([
    svc("technical", "07", "Technical SEO",
        "The groundwork everything else relies on. We make sure search engines can reach, load and understand every page that matters.",
        ["Pages Google cannot reach, or should not index, found and fixed", "How Google really crawls your site, read from server logs",
         "Faster loading on phones", "A tidier site structure and internal links"]),
    svc("semantic", "08", "Semantic &amp; On-Page SEO",
        "Cover the whole topic, not one keyword. We map everything a buyer wants to know and make sure your pages answer it.",
        ["A topic map before anything is written", "The related subjects and terms your pages should cover",
         "A programme to lift pages stuck in positions 8 to 20", "Gaps in existing content found and filled"]),
    svc("content", "09", "Content Strategy &amp; Production",
        "Content that sells first. We start with the pages closest to a purchase, then build supporting articles around them.",
        ["A workshop to define your ideal customer", "A plan of main pages and supporting articles",
         "Briefs built around topics, not keyword lists", "Expert articles under your founder's name"]),
    svc("links", "10", "Link Building &amp; Digital PR",
        "Links from other sites still matter, and they now double as mentions AI tools pick up. Guest articles, press coverage and local listings, held to real editorial standards.",
        ["A study of where competitors get their links", "Guest articles on relevant sites",
         "Press stories built on your own data", "Consistent business listings across directories"]),
    svc("ecommerce", "11", "Ecommerce SEO",
        "More of your category and product pages found on Google and in shopping results, for retailers and direct-to-consumer brands.",
        ["The right search terms matched to the pages that sell", "Filters and sorting that do not create thousands of duplicate pages",
         "Product details marked up for richer search results", "Sales tracking set up in Google Analytics"]),
    svc("saas", "12", "SaaS &amp; B2B SEO",
        "Sales leads, not page views. We start with the pages buyers read just before choosing, such as comparisons and alternatives.",
        ["Buying-stage pages written first", "Comparison and alternative pages",
         "A page for each integration and use case", "Downloads and clear paths to an enquiry"]),
    svc("local", "13", "Local SEO",
        "Show up in Google Maps and local results. Google Business Profile, local listings, reviews and a page for each location.",
        ["Google Business Profile set up and kept active", "Name, address and phone number consistent everywhere",
         "A steady flow of new reviews", "Location pages for businesses with several sites"]),
    svc("international", "14", "International SEO",
        "Reach customers in other countries with the right page in the right language.",
        ["Language and country tags set up correctly (hreflang)", "The right domain structure for each market",
         "Keyword research in each market's own language", "Copy adapted to the culture, not just translated"]),
    svc("programmatic", "15", "Programmatic SEO",
        "Hundreds of useful pages from one well-built template and your own data, with checks so none are thin or duplicated.",
        ["Data sources and page templates designed together", "Quality checks before any page goes live",
         "Automatic internal links", "Watching for pages that compete with each other"]),
    svc("migration", "16", "Site Migrations",
        "Change platform, design or domain without losing your rankings.",
        ["A record of every ranking page before the move", "Every old address mapped to its new one",
         "A staged launch plan", "Daily checks for 30 days after launch"]),
    svc("whitelabel", "17", "White-Label SEO",
        "We do the work under your agency's name, under NDA. Audits, strategy, delivery and reports in your branding.",
        ["Delivery under NDA: your client never sees us", "Reports in your template",
         "From single audits to full ongoing work", "Your account manager, our delivery team"]),
    svc("consulting", "18", "SEO Consulting",
        "Talk to a strategist for $30 per hour. Site reviews, second opinions, team training and plan reviews.",
        ["$30 per hour, booked by the session", "A live review of your site, recorded for you",
         "Training and written processes for your team", "A review of your plan and suppliers"]),
])

GROWTH_SERVICES = "".join([
    svc("paid", "19", "Performance Marketing",
        "Paid ads judged by sales, not clicks. Google, Microsoft, Meta, TikTok, LinkedIn, Amazon and eBay run as one budget.",
        ["Search and shopping ads on Google and Microsoft", "Paid social on Meta, TikTok and LinkedIn",
         "Marketplace ads on Amazon and eBay", "One monthly report across every channel"], "Paid ads"),
    svc("automation", "20", "Marketing Automation &amp; Data",
        "Tracking you can trust, and the repetitive jobs done for you. Analytics, consent, reporting and automated workflows.",
        ["Google Analytics 4 and Tag Manager set up properly", "Tracking that meets UK and EU consent rules",
         "Your website, CRM and email tools connected", "Automations and AI assistants for follow-ups and reports"], "Data and automation"),
    svc("builds", "21", "Ecommerce &amp; App Development",
        "The shop, site or app your marketing sends people to. Built to load fast and to work with your tracking from day one.",
        ["Shopify and WooCommerce builds and redesigns", "Platform moves that protect your rankings",
         "Custom sites and mobile apps", "Email and SMS for abandoned baskets and repeat orders"], "Websites and apps"),
])

PAGES["services"] = dict(
    title="Services | AI Search, SEO, Paid Ads, Data &amp; Websites | SVED Solution",
    desc="Twenty-one services in three groups: AI search, SEO, and paid ads, marketing data and website builds. Take one, or run them together as a single plan.",
    slug="services/",
    body=f"""
{phero('<a href="index.html">Home</a> / Services',
       'Services',
       'Everything it takes to be found and chosen.',
       'Twenty-one services in three groups: AI search, SEO, and the paid ads, data and websites that turn attention into sales. Take one, or let us run them together as a single plan.')}

<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">Group 1</div>
      <h2>AI search</h2>
      <p class="lead dim">Getting your business named when people ask ChatGPT, Perplexity, Gemini or Google's AI answers for help.</p>
    </div>
    <div class="grid g3">{AI_SERVICES}</div>
  </div>
</section>

<section class="sec band-alt">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">Group 2</div>
      <h2>SEO</h2>
      <p class="lead dim">The groundwork that gets your pages found on Google. AI tools lean on the same foundations.</p>
    </div>
    <div class="grid g3">{CORE_SERVICES}</div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">Group 3</div>
      <h2>Paid ads, data and websites</h2>
      <p class="lead dim">Buying traffic that pays for itself, measuring it honestly, and building the shop or site it lands on.</p>
    </div>
    <div class="grid g3">{GROWTH_SERVICES}</div>
  </div>
</section>

<section class="sec band-alt">
  <div class="wrap">
    <div class="sec-head center">
      <div class="eyebrow">How we work together</div>
      <h2>Three ways to work with us</h2>
    </div>
    <div class="grid g3">
      <div class="card"><h3>A one-off review and plan</h3><p style="margin-bottom:16px">We check your site, your AI visibility and your competitors, then hand you a 90-day plan in priority order. You can carry it out with anyone.</p><p class="mono green" style="font-size:.85rem">Fixed fee &middot; 2&ndash;3 weeks</p></div>
      <div class="card"><h3>Ongoing delivery</h3><p style="margin-bottom:16px">We carry out the plan for you and report every month in plain English. Most clients start here.</p><p class="mono green" style="font-size:.85rem">Monthly &middot; agreed after the review</p></div>
      <div class="card"><h3>Advice by the hour</h3><p style="margin-bottom:16px">Time with a strategist for site reviews, second opinions and team training.</p><p class="mono green" style="font-size:.85rem">$30 per hour</p></div>
    </div>
  </div>
</section>

{cta("Not sure which service you need?",
     "Start with the free AI visibility check. It shows what is holding you back, which usually makes the first step obvious.")}
""")

# ==========================================================================
# INDUSTRIES
# ==========================================================================
# Industries are grounded in the real client roster, so every page can name the
# work rather than describe a hypothetical vertical.
INDUSTRIES = [
    dict(slug="healthcare-ivf-seo", name="Healthcare, IVF &amp; Clinics", icon="&#10010;",
         short="SEO and AI search for clinics, hospitals and fertility centres. Google and AI tools are most careful with health advice, so we show clearly who your doctors are and why patients can trust them.",
         clients=["2 &times; IVF &amp; fertility clinic groups, Delhi NCR",
                  "Laser &amp; cosmetic dermatology clinic, India",
                  "Physiotherapy &amp; rehabilitation practice"],
         kw="healthcare SEO India, IVF clinic SEO, fertility clinic SEO, dermatology SEO, medical SEO agency",
         pains=["Treatment pages that get visits but very few enquiries",
                "Other clinics appear above you for every treatment in your city",
                "Google's AI summaries answer patient questions without naming your clinic",
                "Your own branches compete with each other on Google"],
         plays=["Medical markup on every treatment page, so Google knows the page is about healthcare and who the doctor is",
                "Doctor profiles with qualifications, registrations and articles written under their names",
                "A page for each treatment in each city, planned so branches do not compete",
                "A steady flow of reviews on Google and Practo",
                "Clear, direct answers to the questions patients ask"]),

    dict(slug="ecommerce-d2c-seo", name="Ecommerce &amp; D2C", icon="&#9679;",
         short="SEO and AI search for online shops and direct-to-consumer brands. We organise categories, control filters and product options, and get your products into shopping results and AI answers.",
         clients=["Specialist hobby retailer, UK &mdash; 1,393 keywords",
                  "Bio-active skincare D2C brand, India",
                  "Ayurvedic &amp; herbal wellness brand, India",
                  "Fashion &amp; lifestyle label, London"],
         kw="ecommerce SEO India, D2C SEO agency, Shopify SEO, product page SEO, ecommerce GEO",
         pains=["Marketplaces you also sell on appear above your own category pages",
                "Thousands of near-duplicate pages for sizes and colours",
                "Your products are missing when people ask AI tools what to buy",
                "Visits are growing while revenue stays flat"],
         plays=["Decide which search each important page should win, before anything is written",
                "Product, price, rating and review markup across the catalogue",
                "Control filters and tracking codes so Google stops indexing duplicates",
                "Comparisons and buying guides, the kind of page AI tools quote most",
                "Analytics set up so you can see the revenue search brings in"]),

    dict(slug="saas-ai-product-seo", name="SaaS &amp; AI Products", icon="&#9636;",
         short="SEO and AI search for software and AI products, judged by sales leads and not page views. We start with the pages buyers read just before they choose, then add comparison and integration pages.",
         clients=["AI transcription &amp; translation platform &mdash; 55+ languages, used by global universities"],
         kw="SaaS SEO agency, B2B SaaS SEO, AI product SEO, SaaS GEO services",
         pains=["Buyers ask ChatGPT about you before they ever visit your site",
                "Competitors hold every &ldquo;best X&rdquo; and &ldquo;alternatives&rdquo; search",
                "Blog visitors who never start a trial",
                "No profile on G2, Capterra or Product Hunt"],
         plays=["Publish the pages closest to a sale first",
                "Comparison, alternatives and integration pages",
                "Software markup that shows your pricing to search engines",
                "Profiles and mentions on G2, Capterra, Product Hunt and Reddit",
                "Help documents tidied up, because AI tools read them heavily"]),

    dict(slug="web3-crypto-seo", name="Web3, Crypto &amp; Blockchain", icon="&#9672;",
         short="SEO and AI search for crypto and blockchain projects, delivered with our subsidiary Web3Tech Network. We build community, make your documents readable by search engines, and earn the trust a sceptical market asks for.",
         clients=["Web3Tech Network &mdash; our own subsidiary",
                  "Layer-2 staking &amp; node protocol on Polygon"],
         kw="Web3 SEO, crypto SEO agency, blockchain SEO, token marketing, NFT SEO",
         pains=["The big ad platforms ban or restrict crypto adverts",
                "Search engines look harder at token projects",
                "Your community is on Telegram and X, where search engines cannot see it",
                "Whitepapers and documents that search engines cannot read"],
         plays=["Community management and social campaigns on the crypto channels",
                "Influencer marketing matched to your stage and your chain",
                "SEO for token documents, whitepapers and explorer pages",
                "Mentions on Reddit, Medium and Telegram",
                "Proof of trust: audits, named team members and contract data anyone can check"]),

    dict(slug="it-services-app-development-seo", name="IT Services &amp; App Development", icon="&#9881;",
         short="SEO and AI search for IT and app development companies. Sales take months, deals are large, and buyers ask an AI tool to compare five suppliers at once. We build detailed service pages and make your founder a known name.",
         clients=["Mobile app development firm, Dubai UAE",
                  "Enterprise software &amp; GCC provider, Kolkata",
                  "Independent technology publishing platform"],
         kw="IT services SEO, app development company SEO, software company SEO, B2B tech SEO",
         pains=["You look the same as a hundred other development agencies in search",
                "Enquiries arrive asking only about price",
                "Directories like Clutch hold the top spots for searches in your city",
                "No named expert is linked to your company"],
         plays=["A page for each service, technology and location you cover",
                "Case studies with real engineering detail that can be checked",
                "Profiles on Clutch, GoodFirms and DesignRush",
                "A known founder: articles, podcasts and technical writing",
                "Documentation and open-source work that other sites link to"]),

    dict(slug="education-edtech-seo", name="Education &amp; EdTech", icon="&#9998;",
         short="SEO and AI search for universities, colleges and learning platforms. We help you appear when students search for courses and when they ask AI tools where to study.",
         clients=["UGC-recognised skills university &mdash; 650+ industry partners"],
         kw="education SEO India, university SEO, EdTech SEO, admissions SEO, course page SEO",
         pains=["Most admissions searches arrive in one short window each year",
                "Listing sites appear above your own course pages",
                "Students ask AI tools which university to choose",
                "Course pages with no markup to tell search engines what they are"],
         plays=["Course, programme and FAQ markup on every course page",
                "A page for each programme, specialisation and entry requirement",
                "Placement and results data published where it can be quoted",
                "Accreditation and recognition shown in a form search engines can read",
                "Clear, direct answers to the questions students ask"]),

    dict(slug="financial-services-seo", name="Financial Services &amp; Insurance", icon="&#9650;",
         short="SEO and AI search for finance, mortgage and insurance firms. We write content your compliance team can approve, build calculators people link to, and show who wrote and checked each page.",
         clients=["Mortgage &amp; insurance network group, United Kingdom"],
         kw="financial services SEO, fintech SEO agency, insurance SEO, mortgage broker SEO, YMYL SEO",
         pains=["Compliance checks slow down every piece of content",
                "Google holds money advice to a higher standard, and good pages do not rank",
                "You sell through advisers and brokers, which standard SEO overlooks",
                "Rules limit the claims and comparisons you can make"],
         plays=["A writing process with named reviewers, built around compliance",
                "Calculators and tools that other sites link to and quote",
                "Author qualifications and financial service markup",
                "Mentions from regulators and industry bodies",
                "Separate content for advisers and for consumers"]),

    dict(slug="local-business-seo", name="Local, Retail &amp; Studios", icon="&#8962;",
         short="Local SEO for shops, studios and service businesses. We look after your Google Business Profile, reviews and local pages so nearby customers find you on Google Search and Maps.",
         clients=["Creative arts &amp; play studio", "Trading &amp; distribution business"],
         kw="local SEO India, Google Business Profile optimization, local SEO agency, map pack SEO",
         pains=["You are missing from the map results even though you are the closest",
                "Your name, address and phone number differ between directories",
                "Competitors with more reviews win by default",
                "&ldquo;Near me&rdquo; searches go to listing sites"],
         plays=["Google Business Profile completed and posted to regularly",
                "Name, address and phone number corrected in every directory",
                "Local business markup with the right service areas",
                "A simple way to ask for reviews that stays within Google's rules",
                "A page for each branch and each area you serve"]),

    dict(slug="security-loss-prevention-seo", name="Security &amp; Loss Prevention", icon="&#9919;",
         short="SEO and AI search for security and loss-prevention companies. Few people search for these products, but each order is large. We publish content that explains the product type and product pages detailed enough for buyers and specifiers.",
         clients=["Security fog &amp; loss-prevention manufacturer, UK &mdash; 2 to 95 keywords in 12 months"],
         kw="security systems SEO, B2B security SEO, loss prevention marketing, security technology SEO",
         pains=["Too few searches for a normal keyword plan to work",
                "Specifiers and installers research differently from end users",
                "Buying takes months and involves several people",
                "Dictionary-style results hold the top spots for your product terms"],
         plays=["Content that explains the product type and creates interest",
                "Product pages with full specifications for technical buyers",
                "Content on standards and compliance, for example EN50131",
                "Pages for each use: retail, cash machines, warehouses, jewellers",
                "Mentions in trade publications and installer networks"]),

    dict(slug="agency-white-label-seo", name="Agencies &amp; White-Label", icon="&#9783;",
         short="SEO and AI search work delivered under your agency's brand, under a confidentiality agreement. From a single review to full monthly delivery, reported in your template. Your client never knows we exist.",
         clients=["Confidential &mdash; NDA"],
         kw="white label SEO India, white label GEO, SEO reseller, outsourced SEO agency",
         pains=["Clients ask for AI search work you cannot yet deliver",
                "You have no spare capacity to take on new clients",
                "A senior SEO hire costs too much",
                "Reporting eats the hours meant for delivery"],
         plays=["Delivery under your brand, under a confidentiality agreement",
                "Reports in your template and tone",
                "Start with a single review and grow to full monthly delivery",
                "Your account manager stays the only person the client speaks to",
                "AI search visibility as a service you can sell straight away"]),
]

PAGES["industries"] = dict(
    title="SEO &amp; AI Visibility by Industry | SVED Solution",
    desc="SEO and AI search services for healthcare, ecommerce, software, Web3, IT services, education, finance, local businesses, security and agencies.",
    slug="industries/",
    body=f"""
{phero('<a href="index.html">Home</a> / Industries',
       'Industries',
       'Every industry is found in a different way.',
       'AI tools trust different websites for each kind of business. A software company needs G2 and Capterra. A shop needs Trustpilot and the marketplaces. A clinic needs named, qualified doctors and local listings. We work out which sources matter for your industry and build your presence there.')}

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
      <h2>Standard advice rarely fits your industry.</h2>
    </div>
    <div class="grid g2" style="gap:44px">
      <div class="prose">
        <p>Most advice on AI search tells you to get listed on G2 and Product Hunt. That is right for software and wrong for nearly everyone else. If you sell industrial parts, no AI tool is checking Product Hunt. It is reading trade publications, distributor directories and technical documents.</p>
        <p>In the first review we look at the AI answers for <em>your</em> industry, note which brands are named, and list every website quoted alongside them. That list becomes your plan. It is different every time.</p>
      </div>
      <div class="panel">
        <div class="panel-bar"><i class="tdot"></i><i class="tdot"></i><i class="tdot"></i><span style="margin-left:8px">sites AI tools trust, by industry</span></div>
        <div class="panel-body" style="font-size:.79rem">
          <div class="crow"><span class="lbl">Software</span><span class="val">G2 &middot; Capterra &middot; Product Hunt</span></div>
          <div class="crow"><span class="lbl">Online shops</span><span class="val">Trustpilot &middot; Reddit</span></div>
          <div class="crow"><span class="lbl">Healthcare</span><span class="val">Medical directories &middot; associations</span></div>
          <div class="crow"><span class="lbl">Legal</span><span class="val">Avvo &middot; bar directories</span></div>
          <div class="crow"><span class="lbl">Manufacturing</span><span class="val">Trade press &middot; ThomasNet</span></div>
          <div class="crow"><span class="lbl">Local services</span><span class="val">Google profile &middot; Yelp &middot; Nextdoor</span></div>
        </div>
      </div>
    </div>
  </div>
</section>

{cta("Which websites do AI tools trust in your industry?",
     "Start with the free check. It runs 20 tests on your own site and takes about a minute.")}
""")

# ==========================================================================
# USE CASES
# ==========================================================================
USE_CASES = [
    ("&ldquo;ChatGPT never mentions us.&rdquo;",
     "You asked ChatGPT about your own industry. It named a competitor and not you.",
     "We check how AI tools see your brand, study where competitors are mentioned, build your profiles on the sites that matter and rewrite your main pages with clear answers. First mentions usually appear around day 60.",
     "GEO + AI Citation Building"),
    ("&ldquo;Google's AI summaries took our traffic.&rdquo;",
     "Your rankings are the same. So is the number of times you are shown. Clicks have dropped and nobody can say why.",
     "We check each search for an AI summary, measure the clicks you lost in Search Console, then rework the pages so your brand is named in the summary.",
     "AI Overviews Optimization"),
    ("&ldquo;Our pages are stuck in positions 8 to 20.&rdquo;",
     "The pages get seen, but they sit at the bottom of page one or on page two, where few people click.",
     "A step-by-step method: take each page's own search data, work out what is missing, rewrite the title and description, and link to it from related pages. Movement usually shows in 7 to 21 days, with no new backlinks.",
     "Semantic &amp; On-Page SEO"),
    ("&ldquo;We are moving to a new site and we are worried.&rdquo;",
     "A rebuild or platform change is coming, and the last one cost the business six months of traffic.",
     "We record every page and ranking before the move, map every old address to its new one and test it, launch in stages and check daily for 30 days after launch.",
     "Site Migrations"),
    ("&ldquo;Google is reading 400,000 pages we do not want.&rdquo;",
     "Filters and tracking codes have created endless duplicate pages, and Google spends its time on those instead of your real ones.",
     "We read your server logs to see what Google actually does, decide page by page what to keep and what to remove, and bring filters under control. Fewer pages, more traffic.",
     "Technical SEO"),
    ("&ldquo;New site. Nobody knows us. Where do we start?&rdquo;",
     "Nothing is on Google yet, nothing ranks, and you cannot wait eighteen months for content to pay off.",
     "We start with the pages closest to a sale and the searches that are easiest to win, and set up your brand details from day one so AI tools start to learn who you are.",
     "Content Strategy + GEO"),
    ("&ldquo;We need SEO but cannot hire in-house.&rdquo;",
     "A full-time senior SEO costs more than your whole budget for search.",
     "We work as your team for a monthly fee. Or you book us by the hour and use our written step-by-step guides, so your own marketer can do the work properly.",
     "Monthly Delivery / Consulting"),
    ("&ldquo;Our agency clients want AI search work and we cannot deliver it.&rdquo;",
     "Clients are asking how to appear in ChatGPT and you have no answer and no spare capacity.",
     "We do the work under your brand, under a confidentiality agreement, from a single review to full delivery, reported in your branding. Your client never sees us.",
     "White-Label SEO"),
]

PAGES["use-cases"] = dict(
    title="SEO &amp; AI Visibility Use Cases | SVED Solution",
    desc="Eight problems clients bring to us and what we do about each: missing from ChatGPT, traffic lost to AI summaries, stuck rankings, site moves, duplicate pages and more.",
    slug="use-cases/",
    body=f"""
{phero('<a href="index.html">Home</a> / Use Cases',
       'Use cases',
       'Eight common problems, and what we do about each.',
       'Nobody buys &ldquo;SEO services&rdquo;. They want a specific, costly problem fixed. These are the eight we hear most often.')}

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
     "The free check is the quickest way to confirm which problem you have. From the inside they often look alike.")}
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
       'What clients say.',
       'Names are withheld at the clients&rsquo; request. Before you sign anything, we can put you in touch with a client in your industry.')}

<section class="sec">
  <div class="wrap">
    <div class="kpis" style="margin-bottom:44px">
      <div class="kpi"><div class="kpi-val"><span data-count="4.9" data-dec="1">0</span></div><div class="kpi-lab">Average client rating</div></div>
      <div class="kpi"><div class="kpi-val"><span data-count="94">0</span><span class="u">&#37;</span></div><div class="kpi-lab">Monthly clients who renew</div></div>
      <div class="kpi"><div class="kpi-val"><span data-count="39">0</span></div><div class="kpi-lab">Written step-by-step guides</div></div>
      <div class="kpi"><div class="kpi-val"><span data-count="12">0</span></div><div class="kpi-lab">Industries served</div></div>
    </div>
    <div class="grid g3">
      {"".join(f'<div class="quote"><div class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div><p>&ldquo;{q}&rdquo;</p><div class="who">{w} &middot; {c}</div></div>' for q, w, c in REVIEWS)}
    </div>
  </div>
</section>

{cta("Talk to a client in your industry.",
     "Ask on the first call and we will put you in touch with a current client in a similar business.",
     primary=("Book a call", "contact.html"),
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
    desc="Guides on SEO, AI search (GEO, AEO, LLM SEO), technical SEO and measurement, written by the people who do the work on client accounts.",
    slug="insights/",
    body=f"""
{phero('<a href="index.html">Home</a> / Insights',
       'Insights',
       'What we are learning, written up as we learn it.',
       'The methods we use on real client accounts, explained in full. Nothing hidden behind a form. If we publish a method, it is the one we use.')}

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
    <p class="lead dim">AI search news and what to do about it, by email. Free, and you can unsubscribe at any time.</p>
    <form class="audit-form sved-form" data-type="newsletter" style="max-width:520px;margin:2rem auto 0;justify-content:center">
      <input type="email" name="email" placeholder="you@company.com" aria-label="Email" required style="flex:1 1 320px;width:auto">
      <button class="btn btn-primary" type="submit">Subscribe</button>
      <p class="form-status" role="status" style="flex:1 1 100%"></p>
    </form>
  </div>
</section>

{cta("Want to see your own numbers?",
     "Run the free check on your site. It takes about a minute.")}
""")

# ==========================================================================
# VIDEOS
# ==========================================================================
VIDEOS = [
    ("Live GEO teardown: why this brand is invisible in ChatGPT", "Teardown", "14:22"),
    ("The 20-point AI visibility check, run live", "Walkthrough", "18:05"),
    ("Index surgery: deleting pages to grow traffic", "Technical", "22:40"),
    ("Position 8-20 recovery, start to finish", "On-Page", "16:11"),
    ("Reverse-engineering a competitor's AI citations", "GEO", "12:58"),
    ("Reading a monthly SEO report the right way", "Reporting", "09:34"),
]

PAGES["videos"] = dict(
    title="SEO &amp; AI Visibility Videos | SVED Solution",
    desc="Videos on SEO, AI search and growth from the SVED Solution team. Watch how we find and fix the problems that keep a business from being found.",
    slug="videos/",
    body=f"""
{phero('<a href="index.html">Home</a> / Videos',
       'Videos',
       'Watch the work, not the pitch.',
       'Short videos on SEO, AI search and growth. Every client also gets a screen recording of their own review, because seeing the problem on screen is clearer than reading about it.')}

<section class="sec">
  <div class="wrap wrap-narrow">
    <div class="yt-embed yt-facade" data-yt="videoseries?list=UULFLEeUbTJUO4d7nALNrh1USQ"
         role="button" tabindex="0" aria-label="Play videos from the Web3Tech Network channel">
      <div class="yt-face">
        <div class="yt-play" aria-hidden="true">&#9654;</div>
        <div class="yt-label">
          <strong>SEO and growth, on video</strong>
          <span>Web3Tech Network &middot; YouTube</span>
        </div>
      </div>
    </div>
    <div class="center mt3">
      <a class="btn btn-ghost" href="https://www.youtube.com/channel/UCLEeUbTJUO4d7nALNrh1USQ" target="_blank" rel="noopener">Subscribe on YouTube</a>
    </div>
    <p class="faint center" style="font-size:.82rem;margin-top:16px">Hosted by <a href="{FOUNDER_LINKEDIN}" target="_blank" rel="noopener" style="color:var(--green)">Ved Prakash</a>, Founder and Head of Strategy at SVED Solution, on the channel of our sister brand.</p>
  </div>
</section>

{cta("Want a review of your own site?",
     "Every full review comes with a recorded walkthrough from the person who did it.")}
""")

# ==========================================================================
# RESOURCES
# ==========================================================================
PAGES["resources"] = dict(
    title="SEO Resources, Guides &amp; Tools | SVED Solution",
    desc="Free SEO and AI search guides from SVED Solution, the 39 written step-by-step guides we work from, and the tools behind every report.",
    slug="resources/",
    body=f"""
{phero('<a href="index.html">Home</a> / Resources',
       'Resources',
       'The guides we actually work from.',
       'These are the guides and written procedures our team follows every day. We publish them because a written process is the best proof that one exists.')}

<section class="sec">
  <div class="wrap">
    <div class="sec-head"><div class="eyebrow">Guides</div><h2>Free to read</h2></div>
    <div class="grid g3">
      <div class="card"><div class="card-icon">&#9670;</div><h3>How to rank in ChatGPT</h3><p style="margin-bottom:16px">How brands get named by ChatGPT, Perplexity and Gemini: what the AI tools look for, where to get mentioned and how long it takes.</p><a class="btn btn-ghost btn-sm" href="/insights/how-to-rank-in-chatgpt/">Read the guide</a></div>
      <div class="card"><div class="card-icon">&#9678;</div><h3>Schema markup for AI search</h3><p style="margin-bottom:16px">The code that tells search engines and AI tools what a page is about. Which types to add, and where.</p><a class="btn btn-ghost btn-sm" href="/insights/schema-markup-for-ai-search/">Read the guide</a></div>
      <div class="card"><div class="card-icon">&#8599;</div><h3>From positions 8&ndash;20 to the top 3</h3><p style="margin-bottom:16px">Eight steps for lifting pages that already rank, using their own search data and links from related pages. No backlinks needed.</p><a class="btn btn-ghost btn-sm" href="/insights/move-pages-position-8-20-to-top-3/">Read the guide</a></div>
    </div>
  </div>
</section>

<section class="sec band-alt">
  <div class="wrap">
    <div class="sec-head"><div class="eyebrow">How we work</div><h2>39 written step-by-step guides</h2>
      <p class="lead dim">Every task we repeat has a written procedure. Consulting clients get the full set. It is also why the quality of our work does not depend on who is doing it that month.</p></div>
    <div class="grid g4">
      <div class="card"><h4>Technical and setup</h4><p style="font-size:.87rem">WordPress setup, robots.txt, sitemaps, redirects, moving to cleaner web addresses, site speed, backup and restore.</p></div>
      <div class="card"><h4>On your pages</h4><p style="font-size:.87rem">Page reviews, improvements with Rank Math, Yoast and SEOPress, web address checks, article outlines, keyword research and planning.</p></div>
      <div class="card"><h4>On other sites</h4><p style="font-size:.87rem">Guest article campaigns, infographics, outreach to resource pages, link reviews, and studying competitors' links and keywords.</p></div>
      <div class="card"><h4>Measurement</h4><p style="font-size:.87rem">Google Analytics and Tag Manager setup, Search Console, tracking across domains, filtering out your own visits, automatic reports and dashboards.</p></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">Our tools</div>
      <h2>The tools behind every report</h2>
      <p class="lead dim">Nothing hidden. You get access to the same dashboards we use, and every figure in your report comes from one of these sources.</p>
    </div>
    <!--TOOLS-->
  </div>
</section>

<section class="sec band-dark">
  <div class="wrap">
    <div class="sec-head center">
      <div class="eyebrow">Credentials</div>
      <h2>Certified on the platforms we work with</h2>
    </div>
    <!--CERTS-->
  </div>
</section>

{cta("Want the guides for your own team?",
     "Consulting clients get all 39 guides and a handover session, at $30 per hour.",
     primary=("Book a consulting session", CALENDLY),
     secondary=("Run the free check", "ai-visibility-audit.html"))}
""")

# ==========================================================================
# ABOUT
# ==========================================================================
PAGES["about"] = dict(
    title="About SVED Solution | Our Story, Values &amp; Team",
    desc="Who we are, what we believe and who you will work with. SVED Solution helps businesses get found on Google and in AI answers, and turn that into sales.",
    slug="about/",
    body=f"""
{phero('<a href="index.html">Home</a> / About',
       'About',
       'We help businesses get found, and then get chosen.',
       'SVED Solution covers the whole route from first search to sale: SEO, AI search, paid ads, tracking and websites. We started in SEO, and one belief shapes everything we do: people now find businesses through Google and through AI tools, and most brands only work on one of them.')}

<section class="sec">
  <div class="wrap wrap-narrow prose">
    <h2 style="margin-top:0">Our story</h2>
    <p>We started as an SEO team doing what everyone else did: technical reviews, content and link building. The work brought results, and the results could be measured.</p>
    <p>Then a client's traffic fell while their rankings held. They were shown as often as before, in the same positions, and the clicks had gone. The cause was a Google AI summary sitting above their number-two ranking. It named three competitors and answered the question itself. Nothing in the usual SEO toolkit fixed it.</p>
    <p>So we rebuilt our work around the question that mattered: <strong>what makes an AI tool name one brand and not another?</strong> The answer became our method: a clear identity, mentions on trusted sites, pages that are easy to quote and regular updates. We now report AI mentions for every client in the same way we report clicks and revenue.</p>
    <p>Since then we have added the rest of the route to a sale: paid ads, tracking and automation, and website and shop builds. Being found is only useful if it leads to customers.</p>
  </div>
</section>

<section class="sec band-alt">
  <div class="wrap">
    <div class="sec-head"><div class="eyebrow">What we stand for</div><h2>Six things we do not compromise on</h2></div>
    <div class="grid g3">
      <div class="card"><span class="card-num">01</span><h3>Look first, quote second</h3><p>We do not quote a monthly fee before we have reviewed your site and accounts. Selling a fix for a problem nobody has checked is how agencies waste a client's year.</p></div>
      <div class="card"><span class="card-num">02</span><h3>Honest timelines</h3><p>First AI mentions around day 60. A settled position after 9 to 12 months. We publish the real timeline because the honest version is the one that holds up.</p></div>
      <div class="card"><span class="card-num">03</span><h3>We do the work</h3><p>Advice that sits in a spreadsheet changes nothing. We add the markup, write the content, earn the links and fix the site.</p></div>
      <div class="card"><span class="card-num">04</span><h3>Every claim carries a number</h3><p>From our own client work where we can, with names removed. Otherwise from a source we can point to. No unsupported claims in our reports or our marketing.</p></div>
      <div class="card"><span class="card-num">05</span><h3>Written down, not made up</h3><p>Thirty-nine written step-by-step guides. The quality of the work should not depend on who is doing it this month.</p></div>
      <div class="card"><span class="card-num">06</span><h3>We will tell you no</h3><p>If AI search is not what is holding you back, we will say so. If your site needs fixing first, we will do that first, even though it delays the more interesting work.</p></div>
    </div>
  </div>
</section>

<section class="sec" id="market" style="scroll-margin-top:90px">
  <div class="wrap">
    <div class="sec-head"><div class="eyebrow">How we see it</div><h2>Four things we believe about search</h2>
      <p class="lead dim">Each one shapes what we sell and what we refuse to sell.</p></div>
    <div class="grid g2" style="gap:36px">
      <div class="card"><h3>Search has split in two</h3><p>Google's list of links is not dying. It now sits beside AI answers, which work differently. Brands that drop Google for AI go too far. Brands that dismiss AI as hype fall behind. The sensible course is to work on both.</p></div>
      <div class="card"><h3>The easy opening will not last</h3><p>Today, the top Google results for the main phrases in AI search have very little behind them. Big brands published quick pages and have not yet improved them. They will, which is why we tell clients that waiting has a real cost.</p></div>
      <div class="card"><h3>What others say beats what you say</h3><p>Most AI search services sell markup and FAQ sections because they are easy to deliver. The hard part is getting independent sites to describe you in the same way. It is slower, and it is what makes the difference.</p></div>
      <div class="card"><h3>AI has made the work faster</h3><p>Research, briefs, technical checks and reports take far less time than they did two years ago. We pass that on in the price. It is why an hour with a strategist costs $30 and why a small team can maintain 39 written guides.</p></div>
    </div>
  </div>
</section>

<section class="sec band-alt" id="team" style="scroll-margin-top:90px">
  <div class="wrap">
    <div class="sec-head"><div class="eyebrow">Our team</div><h2>A small team. You know who does the work.</h2>
      <p class="lead dim">You work with the person who reviewed your site, not an account manager passing messages along.</p></div>
    <div class="grid g3">{TEAM_CARDS}</div>
  </div>
</section>

{cta("Work with the person who reviews your site.",
     "No account manager in between. Book time directly with the strategist.",
     primary=("Book a call", "contact.html"),
     secondary=("Run the free check", "ai-visibility-audit.html"))}
""")

# ==========================================================================
# CONTACT
# ==========================================================================
PAGES["contact"] = dict(
    title="Contact SVED Solution | Book an SEO &amp; AI Visibility Call",
    desc="Book a 15-minute call, send us a message, or book a $30 per hour consulting session with SVED Solution. We reply within one working day.",
    slug="contact/",
    body=f"""
{phero('<a href="index.html">Home</a> / Contact',
       'Contact',
       'Tell us what is not working.',
       'The more detail you give, the more useful the first call. If you have run the free check, paste your score and we will start from there.')}

<section class="sec">
  <div class="wrap">
    <div class="grid g2" style="gap:52px;align-items:start">
      <div>
        <form class="card sved-form" id="contact-form" style="padding:32px">
          <h3 style="margin-bottom:20px">Send us a message</h3>
          <div class="grid g2" style="gap:14px;margin-bottom:14px">
            <input name="name" type="text" placeholder="Full name" required aria-label="Full name">
            <input name="email" type="email" placeholder="Work email" required aria-label="Work email">
          </div>
          <input name="phone" type="tel" placeholder="Phone or WhatsApp (optional)" aria-label="Phone" style="margin-bottom:14px">
          <input name="website" type="text" placeholder="Website address" aria-label="Website" style="margin-bottom:14px">
          <select name="service" aria-label="Service" style="margin-bottom:14px">
            <option value="">What do you need help with?</option>
            <option>Being found in AI tools (GEO)</option>
            <option>Traffic lost to Google AI summaries</option>
            <option>SEO and content</option>
            <option>Technical SEO or a site move</option>
            <option>Paid ads</option>
            <option>Tracking and automation</option>
            <option>A new website, shop or app</option>
            <option>Local SEO</option>
            <option>White-label work for agencies</option>
            <option>Hourly consulting ($30/hr)</option>
          </select>
          <select name="revenue" aria-label="Monthly revenue" style="margin-bottom:14px">
            <option value="">Monthly revenue (helps us plan the work)</option>
            <option>Under $50k</option><option>$50k&ndash;$250k</option>
            <option>$250k&ndash;$1M</option><option>$1M+</option>
          </select>
          <textarea name="message" rows="4" placeholder="What is happening? Paste your free check score if you have one." aria-label="Message" style="margin-bottom:18px"></textarea>
          <input type="text" name="company_website" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px" >
          <button class="btn btn-primary btn-lg" type="submit" style="width:100%;justify-content:center">Send message</button>
          <p class="form-status" role="status"></p>
          <p class="faint" style="font-size:.78rem;margin-top:12px;text-align:center">We reply within one working day. Or <a href="CALENDLY_URL" target="_blank" rel="noopener">book a 15-minute call</a>.</p>
        </form>
      </div>
      <div>
        <div class="card" style="margin-bottom:20px">
          <h3>Book a call</h3>
          <p style="margin-bottom:18px">Skip the form. Pick a 15-minute slot with the strategist who will review your site.</p>
          <a class="btn btn-primary btn-lg" style="width:100%;justify-content:center" href="CALENDLY_URL" target="_blank" rel="noopener">Book a 15-minute call</a>
          <p class="faint" style="font-size:.8rem;margin-top:12px;text-align:center">Opens our booking page. Pick any time that suits you.</p>
        </div>
        <div class="card" style="margin-bottom:20px">
          <h3>Other ways to reach us</h3>
          <div class="crow"><span class="lbl">Email</span><span class="val"><a href="mailto:{EMAIL}">{EMAIL}</a></span></div>
          <div class="crow"><span class="lbl">WhatsApp</span><span class="val"><a href="https://api.whatsapp.com/send?phone={WHATSAPP_RAW}">{WHATSAPP_DISPLAY}</a></span></div>
          <div class="crow"><span class="lbl">LinkedIn</span><span class="val"><a href="{FOUNDER_LINKEDIN}" target="_blank" rel="noopener">Ved Prakash</a></span></div>
          <div class="crow"><span class="lbl">Consulting</span><span class="val">$30 / hour</span></div>
          <div class="crow"><span class="lbl">Reply time</span><span class="val">Within 1 working day</span></div>
          <div class="crow"><span class="lbl">White-label</span><span class="val">Confidentiality agreement on request</span></div>
        </div>
        <div class="card">
          <h3>Before you write</h3>
          <p style="margin-bottom:16px">Run the free check first. You will arrive at the call with a score and a list of findings, which makes the conversation far more useful.</p>
          <a class="btn btn-ghost btn-sm" href="ai-visibility-audit.html">Run the free check</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sec band-alt">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">Offices</div>
      <h2>Three locations. One team.</h2>
      <p class="lead dim">Head office in Dubai, delivery centre in Kolkata and a representative office in the US, so calls can happen in your time zone.</p>
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
        <p style="margin-bottom:0">{SISTER[2]}. If you are launching a token, a DeFi product, an NFT platform or other Web3 project, that team knows the market and the right places to be mentioned. We do the AI search work for both brands.</p>
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
            "image": meta.get("image", ""),
            "html": md_to_html(body),
        })
    # Publish-date gate: posts dated in the future stay hidden (not written,
    # not in the sitemap or listings) until their date arrives. A rebuild on
    # or after that date publishes them automatically.
    today = _dt.date.today().isoformat()
    posts = [p for p in posts if not p["date"] or p["date"] <= today]
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def post_schema(p):
    return ('{"@context":"https://schema.org","@type":"BlogPosting",'
            f'"headline":{_j(p["title"])},"description":{_j(p["desc"])},'
            f'"datePublished":{_j(p["date"])},"dateModified":{_j(p["date"])},'
            f'"author":{{"@type":"Person","name":{_j(p["author"])},"url":"{FOUNDER_LINKEDIN}","sameAs":["{FOUNDER_LINKEDIN}"]}},'
            '"publisher":{"@type":"Organization","name":"SVED Solution",'
            '"url":"https://svedsolution.com/"},'
            + (f'"image":"https://svedsolution.com/assets/{p["image"]}",' if p.get("image") else "")
            + f'"mainEntityOfPage":"https://svedsolution.com/insights/{p["slug"]}/"}}')


def _j(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def post_page(p):
    ans = ""
    if p["answer"]:
        ans = f'<div class="answer-block" style="margin-top:0"><div class="q">The short answer</div><p>{p["answer"]}</p></div>'
    hero = ""
    if p.get("image"):
        hero = (f'<figure style="margin:0 0 2rem"><img src="/assets/{p["image"]}" '
                f'alt="{p["title"]}" width="1200" height="630" '
                'style="width:100%;height:auto;border-radius:12px;display:block" loading="eager"></figure>')
    return f"""
<section class="phero">
  <div class="wrap wrap-narrow">
    <div class="crumbs"><a href="index.html">Home</a> / <a href="insights.html">Insights</a> / {p["category"]}</div>
    <div class="eyebrow">{p["category"]} &middot; {p["read"]} read</div>
    <h1 style="font-size:clamp(2rem,4vw,3rem)">{p["title"]}</h1>
    <p class="lead dim" style="margin-top:1.2rem">{p["desc"]}</p>
    <p class="mono faint" style="font-size:.78rem;margin-top:1.4rem">By <a href="{FOUNDER_LINKEDIN}" target="_blank" rel="noopener author" style="color:inherit;text-decoration:underline">{p["author"]}</a> &middot; Updated {p["date"]}</p>
  </div>
</section>
<section class="sec">
  <div class="wrap wrap-narrow prose">
    {hero}
    {ans}
    {p["html"]}
    <div class="card" style="margin-top:2.6rem">
      <div class="eyebrow" style="margin-bottom:.5rem">About SVED Solution</div>
      <h3 style="margin-bottom:.6rem">Outsource your organic marketing to a specialist</h3>
      <p>SVED Solution is a 360&deg; SEO and AI-visibility agency operating since 2018, helping brands get found on Google <em>and</em> named by ChatGPT, Perplexity, Gemini and Google AI Overviews. We run Generative Engine Optimization, Answer Engine Optimization, technical SEO, content and digital PR as one program, report AI citations as a measured number, and price for outcomes &mdash; consulting from $30/hour, with retainers scoped only after a diagnostic audit. If you want senior organic-marketing expertise, transparent reporting and global delivery without US-agency pricing, we are the team to outsource it to.</p>
      <div style="margin-top:1.1rem;display:flex;gap:10px;flex-wrap:wrap">
        <a class="btn btn-primary btn-sm" href="CALENDLY_URL" target="_blank" rel="noopener">Book a 15-min call</a>
        <a class="btn btn-ghost btn-sm" href="mailto:hello@svedsolution.com">hello@svedsolution.com</a>
      </div>
    </div>
  </div>
</section>
{cta("Find out where your own site stands.",
     "The free check runs 20 tests on your live page and takes about a minute.")}
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
    ("Google Search Console", "Clicks, rankings and page speed data, straight from Google."),
    ("Google Analytics 4", "Where visitors come from, what they do and what they buy."),
    ("Bing Webmaster Tools", "How Bing sees your site. Bing supplies the results for Microsoft Copilot."),
    ("Ahrefs", "Who links to you, how hard a keyword is and what competitors rank for."),
    ("Semrush", "Keyword research, rank tracking and gaps against competitors."),
    ("Screaming Frog", "Full technical checks of every page, redirects and server logs."),
    ("Google PageSpeed Insights", "Page speed, measured on real visits and in tests."),
    ("Schema Markup Validator", "Checks every piece of markup before it goes live."),
    ("Google Rich Results Test", "Confirms your markup qualifies for enhanced Google results."),
    ("Merkle Technical SEO Tools", "Tests for country tags, robots.txt and markup."),
    ("Google Tag Manager", "Tracks clicks, forms and sales without code changes."),
    ("Looker Studio", "Client dashboards that bring search, analytics and ranking data together."),
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


def industry_faqs(i):
    label = i["name"].replace("&amp;", "and")
    return [
      (f"How is {label} SEO different from generic SEO?",
       f"The technical groundwork is the same. What changes is where you need to be mentioned, which markup to add and what people are searching for. {label} buyers research in different places, and AI tools trust different outside websites when they answer questions in this field. In the first review we find out which websites are actually quoted for your industry. We do not work from a standard checklist."),
      ("How long before we see results?",
       "Google rankings usually improve within 60 to 90 days, sooner on pages already in positions 8 to 20. AI mentions follow a steady pattern: AI tools start to recognise the brand after 30 to 45 days, first mentions appear around day 60, regular mentions by day 90 and steady visibility after 4 to 6 months."),
      ("Do you have experience in this specific industry?",
       f"Yes. The work listed above is live or finished work in {lc(label)}. On a first call we will walk you through the real accounts, with names removed where the client asks for that."),
      ("What does it cost?",
       "One-off consulting is $30 per hour. Monthly work is priced after the first review, because quoting before we have looked is guesswork. Start with the free AI visibility check and what to do first usually becomes clear."),
    ]


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
    <p class="faint mono" style="font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;margin-bottom:18px">Who we have done this for</p>
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
          <span style="margin-left:8px">what we do</span></div>
        <div class="panel-body">{plays}</div>
      </div>
    </div>
  </div>
</section>

<section class="sec band-dark">
  <div class="wrap">
    <div class="sec-head center">
      <div class="eyebrow">Where people look</div>
      <h2>The AI tools and search engines people use to research {lc(label)}</h2>
    </div>
    {platform_strip()}
  </div>
</section>

{faq(industry_faqs(i))}

{cta("See how visible you are in AI answers.",
     "Twenty checks against your live page. No card and no call. It takes about a minute.")}
"""


# ==========================================================================
# Individual service pages
# ==========================================================================
def S(slug, name, cluster, icon, answer, kw, does, deliver, faqs, body="",
      title="", who="", surfaces=True, q=""):
    """One service page.

    title    overrides the default "<name> Services | SVED Solution" page title.
    who      overrides the "Who it is for" paragraph.
    surfaces False for services that are not about search or AI visibility: the
             AI-platform band, the ranking-timeline FAQ and the audit call to action
             are swapped for ones that fit.
    """
    return dict(slug=slug, name=name, cluster=cluster, icon=icon, answer=answer,
                kw=kw, does=does, deliver=deliver, faqs=faqs, body=body,
                title=title, who=who, surfaces=surfaces, q=q)


SERVICES = [
    S("answer-engine-optimization", "Answer Engine Optimization (AEO)", "AI Search", "&#9635;",
      "Answer engine optimization (AEO) means writing your pages so Google and AI tools can lift a clear answer straight from them. When someone asks a question, the search engine shows one answer at the top. We work to make that answer yours, by finding the questions your buyers ask and answering each one in the first few lines of the right page.",
      "answer engine optimization, AEO services, featured snippet optimization, FAQ schema, zero click SEO",
      ["List the real questions your buyers ask, grouped by how close they are to buying",
       "Rewrite your main sales pages so each one opens with a short, clear answer",
       "Add FAQ and how-to markup, the code that labels questions and answers for search engines",
       "Win the answer box and the &lsquo;People also ask&rsquo; section on Google",
       "Protect your sales on searches where people get the answer without clicking"],
      ["List of buyer questions, grouped by stage", "Short answers at the top of every sales page",
       "FAQ and how-to markup, tested", "Report on the answer boxes you now hold"],
      [("Is AEO the same as GEO?",
        "No. AEO works page by page. It makes one page the best answer to one question. GEO (generative engine optimization) works on your brand as a whole. It helps AI tools remember you and recommend you. AEO shows results sooner. GEO takes longer and is harder for a competitor to copy. Most clients need both, so we price them separately."),
       ("Does AEO help normal Google rankings too?",
        "Yes, and that is why we often start here. The same changes that let an AI tool quote your page also win the answer box and the &lsquo;People also ask&rsquo; section on Google. Of everything we offer, this is where you see feedback soonest.")]),

    S("llm-seo", "LLM SEO", "AI Search", "&#10022;",
      "LLM SEO is the technical side of being found by AI tools such as ChatGPT, Claude and Gemini. LLM stands for large language model, the technology behind them. If an AI tool cannot open your page, read it and pull out a clean passage, it will not quote you, however good the writing is. We fix the page templates, code and settings that get in the way.",
      "LLM SEO, LLM optimization, llms.txt, GPTBot, AI crawler optimization, chunk optimization",
      ["Rework page layouts so each section makes sense on its own and can be quoted",
       "Write and maintain llms.txt, a short guide to your site written for AI tools",
       "Set which AI crawlers may read your site: GPTBot, ClaudeBot, PerplexityBot and Google-Extended",
       "Fix pages that only load with JavaScript, which many AI crawlers see as blank",
       "Rebuild product and category pages so the main facts are easy for a machine to read"],
      ["Review of your page templates", "llms.txt written and kept up to date",
       "AI crawler settings", "Advice on how your pages should load"],
      [("What is llms.txt and does it matter yet?",
        "It is a plain text file on your site that tells AI tools what the site contains and which pages matter most. It is similar in spirit to robots.txt. Few AI tools read it so far and it does not improve rankings. It takes very little time to write and it removes guesswork, so we add it to every site we work on."),
       ("Should we block AI crawlers instead?",
        "Only if you earn money when people read content on your own pages, for example through adverts or paid subscriptions. If you earn money by being found and recommended, blocking AI crawlers means you will never be quoted. We will tell you plainly which group you are in.")]),

    S("ai-citation-entity-building", "AI Citation &amp; Entity Building", "AI Search", "&#9670;",
      "AI citation and entity building is the work we do away from your website so AI tools know your brand and feel safe recommending it. AI tools trust what other sites say about you more than what you say about yourself. So we get your business described the same way on review sites, directories, forums and trade publications. When many independent sources agree, a brand is far more likely to be named in an AI answer.",
      "AI citation building, entity SEO, brand entity optimization, G2 Capterra listing, digital PR for AI",
      ["Build your profiles on the review sites and directories that matter in your industry",
       "Find every site AI tools quote when they recommend your competitors",
       "Make your founder a known name through articles and podcast interviews",
       "Use one identical description of your business on every outside profile",
       "Run PR aimed at being mentioned in the right places, not at chasing link scores"],
      ["List of the sources that matter in your industry", "Main profiles created and verified",
       "Breakdown of where competitors get mentioned", "Plan for the founder, with named publications"],
      [("Why do other sites matter more than my own website?",
        "Because AI tools give more weight to what independent sources say than to what a business says about itself. When the same brand is described the same way on G2, Crunchbase, Reddit and three trade publications, the AI tool treats that as agreement. Nothing you write on your own site can create that."),
       ("We are not a software company. Do G2 and Capterra apply?",
        "No. Using one standard list for every business is the main reason this kind of work fails. The right sites change with the industry. Shops need Trustpilot and the marketplaces. Clinics need medical directories. Manufacturers need trade publications. We build your list during the first review, from the sources AI tools actually quote in your industry."),
       ("Is a citation the same as a backlink?",
        "No. A backlink is a link from another site to yours, and it helps a page rank on Google. A citation is a mention of your brand, and it helps AI tools recognise you. Ten relevant mentions that describe you the same way, on sites AI tools already read for your industry, do more for AI answers than a hundred links from unrelated sites."),
       ("How soon does this show results?",
        "AI tools usually start to recognise the brand after 30 to 45 days. The first mentions in AI answers tend to appear around day 60. Being named consistently takes 9 to 12 months. It is the slowest part of AI visibility and the hardest for a competitor to undo, so we start it early.")],
      body="""
<h2>Why AI tools trust brands, not web addresses</h2>
<p>When an AI tool answers a question, it does not compare your homepage with a competitor's homepage. It recalls which brands it connects with the topic, then looks for sources that back up naming them. That memory is built away from your own site, in places the AI tool already trusts. A brand described the same way on a review site, a business database, a forum thread and a few trade publications looks like agreement. A brand that is only described on its own website has nothing to back it up.</p>
<p>This is why changes to your own pages only take you so far. You can be first on Google and still be missing from the AI answer above it. Google's ranking measures your page. An AI mention measures your reputation.</p>
<h2>What the work involves</h2>
<ol>
  <li><strong>Agree one description.</strong> One brand name, one description and one category, used word for word on your site and on every profile. Most sites we review describe themselves three different ways, which confuses AI tools before anyone else gets involved.</li>
  <li><strong>Get listed where your industry is judged.</strong> The right sites are different for every industry. Software needs review sites. Clinics need medical directories. Shops need marketplaces and review platforms. Manufacturers need the trade press. We build the list from what AI tools actually quote in your industry.</li>
  <li><strong>Study where competitors are mentioned.</strong> We take the brands already named in AI answers for your questions, list every site quoted alongside them, and go after the same sources with better material.</li>
  <li><strong>Make your people known.</strong> Founders and experts with consistent bios, bylines and qualifications, because AI tools give more weight to writing with a real, identifiable author.</li>
  <li><strong>Run PR for mentions.</strong> We choose placements because they are relevant and describe you accurately, not because the site has a high authority score.</li>
</ol>
<h2>Mentions and backlinks do different jobs</h2>
<p>A backlink helps a page rank. A mention helps a brand get recognised. Ten relevant mentions that describe you the same way do more for AI answers than a hundred links from unrelated sites. This work goes hand in hand with <a href="/generative-engine-optimization/">generative engine optimization</a>, and we measure it through <a href="/services/ai-visibility-monitoring/">AI visibility monitoring</a>.</p>
<h2>How long it takes and how we measure it</h2>
<p>AI tools usually start to recognise the brand after 30 to 45 days. First mentions tend to appear around day 60. Being named consistently takes 9 to 12 months. Each month we report which sources describe you, how consistently they do it, and how often you are mentioned compared with named competitors.</p>
<p class="faint">Nobody controls what an AI tool writes, and there is nowhere to submit your site. What we can control is how widely and how consistently other sites describe you. We measure that and report it, so you can see the trend.</p>
"""),

    S("ai-visibility-monitoring", "AI Visibility Monitoring", "AI Search", "&#9678;",
      "AI visibility monitoring tells you whether AI tools are actually mentioning your brand. We combine tracking software with a fixed list of questions that we ask ChatGPT, Perplexity and Gemini every week, by hand. It is the only way to know whether the work on AI search is paying off.",
      "AI visibility tracking, LLM citation tracking, ChatGPT rank tracking, share of voice AI, GEO reporting",
      ["Count how often AI tools use your site as a source each month, and which pages they use",
       "Ask the same set of questions every week on three or more AI tools",
       "Compare how often you are mentioned with how often named competitors are",
       "Report in plain written English, not a wall of charts",
       "Show which outside sources the AI tools rely on, and why"],
      ["Monthly count of mentions, page by page", "Weekly log of the questions asked and the answers",
       "Comparison with named competitors", "Written monthly report"],
      [("Are AI visibility trackers reliable?",
        "Not very, on their own. The tools disagree with each other and with what you see when you check by hand. So we do both. Software gives us the totals and the pages used. Careful manual checks on a fixed list of questions tell us whether to believe the totals."),
       ("What does a report actually contain?",
        "How many times you were mentioned and whether that is rising or falling. Which of your pages were used and how often. The results of the weekly checks, with the exact questions asked. How you compare with competitors. A written note on what changed and what we will do next month. About two pages of writing, not forty tabs.")]),

    S("google-ai-overviews-optimization", "Google AI Overviews Optimization", "AI Search", "&#9650;",
      "Google AI Overviews optimization wins back the visits you lose when Google answers a search itself. An AI Overview is the summary Google writes at the top of the results. It names two or three brands, so your clicks can fall even though your ranking has not moved. We find which of your searches are affected and rework those pages so your brand is named in the summary.",
      "Google AI Overviews, AI Overview optimization, SGE optimization, zero click recovery, CTR loss",
      ["Check which of your searches now show an AI Overview",
       "Work out exactly how many clicks you have lost, using Google Search Console",
       "Rework your pages so Google can use them in the summary",
       "Strengthen the signals Google uses to decide which brands to name",
       "Shift effort toward the searches where people still click through"],
      ["List of your searches that show an AI Overview", "Breakdown of the clicks you have lost",
       "Ordered plan for reworking pages", "Monthly check on whether you are named"],
      [("Our rankings held but clicks collapsed. Is this why?",
        "Very often, yes. An AI Overview above your number-two ranking answers the question and names two or three brands. Your ranking and the number of times you are shown look the same, but fewer people click. The first thing we do is confirm whether that is what happened, search by search."),
       ("How is this different from ordinary SEO?",
        "Ordinary SEO competes for a place in the list of links. This competes for a place in the summary above that list. The groundwork is shared. What wins is different: a short, direct answer at the top of the page, FAQ markup that works, and a brand Google is confident enough to name. A page can rank second and still be missing from the summary above it."),
       ("Which pages should we start with?",
        "The ones losing clicks fastest. We open Search Console, find the pages that are still being shown but are getting fewer clicks, and fix the biggest losses first. On a newer site with little history, we start with the buying searches where an AI Overview is most likely to name a supplier."),
       ("There is no ranking position, so how do you measure it?",
        "We report whether you are there, not where you rank. Each month you see which of your searches show an AI Overview, whether your brand is named in each one, how that changed from last month, and how many clicks came back on the pages we reworked. The first signs usually show after 30 to 45 days and the picture settles over 4 to 6 months."),
       ("Can you guarantee inclusion in an AI Overview?",
        "No. Nobody controls what Google writes and there is nowhere to submit a page. What we control is everything that makes being included more likely, and we report it monthly so you can see whether it is working.")],
      q="What is Google AI Overviews optimization?",
      body="""
<h2>How AI Overviews changed the numbers</h2>
<p>An AI Overview is the summary Google writes above the normal results for a growing share of searches. When one appears, it answers the question and names two or three brands. Your page can hold the same position it held last quarter while its clicks fall, because the searcher has the answer before reaching the links. In Search Console this looks like fewer clicks while the number of times you were shown and your average position stay the same. That pattern points to an AI Overview, not a ranking problem.</p>
<p>This is not a niche issue. The phrase &lsquo;Google AI Overviews&rsquo; alone gets about 22,200 searches a month in the US, and the summaries keep appearing on more searches. For most sites the question is which searches have already been affected, and whether the brand is named in the summary or left out.</p>
<h2>How we work, step by step</h2>
<ol>
  <li><strong>Check every search.</strong> We find which of your ranking searches now show an AI Overview, and whether your brand is named in it, pushed below it or missing.</li>
  <li><strong>Measure the loss.</strong> Using Search Console, we find the pages where clicks fell while everything else held steady, so the effort goes where money was actually lost.</li>
  <li><strong>Rework the pages.</strong> We rewrite the affected pages so the answer comes first: a direct answer of 40 to 60 words at the top, headings written as questions, and short, complete blocks Google can lift into the summary.</li>
  <li><strong>Back up the brand.</strong> We add the markup that tells Google what the page and the business are, use one consistent description of your brand, and build the outside mentions that make Google confident enough to name you.</li>
  <li><strong>Go where the clicks still are.</strong> Some searches still send visitors and some no longer do. We move effort toward buying searches, where people still click, and defend the informational ones by getting your brand named.</li>
</ol>
<h2>Why one page is named and another is not</h2>
<p>Two pages can rank in the same place and get opposite results. The page that opens with a direct answer, carries working FAQ markup and is backed up by mentions on other sites is the one Google pulls into the summary. The page that opens with a long introduction, hides its answer far down the page and describes the brand inconsistently stays unread below it. This service is about being the first kind of page every time. It works alongside <a href="/services/answer-engine-optimization/">answer engine optimization</a>, <a href="/services/ai-citation-entity-building/">AI citation and entity building</a> and sound <a href="/services/technical-seo/">technical SEO</a>.</p>
<h2>What we measure</h2>
<p>There is no ranking position to report, so we report whether you are there. Every month you see which of your searches show an AI Overview, whether your brand is named in each one, how that changed from last month, and how many clicks came back on the pages we reworked. The first signs usually show after 30 to 45 days and the picture settles over 4 to 6 months. We track it through <a href="/services/ai-visibility-monitoring/">AI visibility monitoring</a>, and we report the numbers whether or not they make us look good.</p>
<p class="faint">We cannot guarantee a place in an AI Overview. Nobody controls what Google writes and there is nowhere to submit a page. What we control is everything that makes it more likely, measured and reported so you can see whether it is working.</p>
"""),

    S("technical-seo", "Technical SEO", "Core SEO", "&#9881;",
      "Technical SEO makes sure search engines and AI tools can reach, load and understand every page that matters on your site. It covers how Google moves through the site, which pages it stores, how fast pages load and how they link to each other. If a page cannot be reached or loaded, it cannot rank on Google or be quoted by an AI tool.",
      "technical SEO services, crawl budget, index bloat, Core Web Vitals, log file analysis, site architecture",
      ["Find where Google wastes its time on your site and remove pages that should not be in its index",
       "Read your server logs to see what Google's crawler actually does on the site",
       "Fix pages that only work with JavaScript, so search engines see the full content",
       "Improve Core Web Vitals, Google's three measures of speed and stability",
       "Reorganise the site structure and the links between your pages"],
      ["Full technical review with fixes in order of importance", "Report from your server logs",
       "Plan to fix page speed", "Map of the site structure and internal links"],
      [("How do we know if Google has indexed too many of our pages?",
        "Compare the number of pages you want on Google with the number Search Console reports. If Google has found many times more addresses than you have real pages, your filters or tracking codes are creating them. Google then spends its time on those instead of the pages that earn you money."),
       ("Is technical SEO worth it if our content is weak?",
        "It is needed first, but it is not enough alone. Great content on a broken site does not rank. A perfect site with thin content does not rank either. If content is what is really holding you back, we will say so and do that first.")]),

    S("semantic-on-page-seo", "Semantic &amp; On-Page SEO", "Core SEO", "&#9737;",
      "Semantic and on-page SEO means covering a topic properly instead of repeating one keyword. Google now understands subjects and how ideas relate to each other. A page that answers everything a buyer wants to know about a topic beats a page that repeats a single phrase. We plan each page around the full topic and fix the pages you already have.",
      "semantic SEO, on page SEO services, entity SEO, topical authority, keyword to concept mapping",
      ["Map each topic and everything it should cover, before anything is written",
       "List the related terms and ideas Google expects to see on the page",
       "Lift pages stuck in positions 8 to 20 with our step-by-step method",
       "Check your existing pages for what is missing and fill the gaps",
       "Write briefs around the whole topic, not one keyword"],
      ["Topic map for each subject area", "List of related terms and ideas for each page",
       "Worklist for pages in positions 8 to 20", "Review of your content with the gaps listed"],
      [("What is the position 8 to 20 method?",
        "Pages ranking between 8 and 20 are already trusted by Google. They are just not quite what the searcher wanted. We take that page's own search data, work out what is missing, rewrite the title and description so more people click, add the missing questions as real headings, and link to the page from related pages. Movement usually shows in 7 to 21 days, with no new backlinks."),
       ("Does keyword density still matter?",
        "No, and chasing it does harm. Covering the topic well beats repeating a phrase. Articles that properly cover fifteen or more related ideas do better than articles that repeat one keyword, because Google is judging how well you understand the subject, not counting words.")]),

    S("content-strategy", "Content Strategy &amp; Production", "Core SEO", "&#9998;",
      "Content strategy and production means deciding what to write, in what order, and then writing it. We start with the pages closest to a sale, such as service, product and comparison pages. Then we add the guides and articles around them, so the site becomes the place to go on your subject. Every piece is planned around a clear picture of your ideal customer.",
      "SEO content strategy, content marketing agency India, B2B content, pillar cluster content, ICP content",
      ["Define your ideal customer with your sales and support teams",
       "Publish the pages closest to a sale first",
       "Plan main guides and supporting articles, and how they link together",
       "Write a brief for every piece: the questions to answer and the gaps to fill",
       "Publish under a real, named expert, not as anonymous filler"],
      ["Written profile of your ideal customer", "12-month content plan with target searches",
       "Brief for every article", "Finished articles, published"],
      [("How much content do we actually need?",
        "In almost every industry we work in, fewer and deeper pieces beat a large number of thin ones. One thorough page that covers a subject fully will outrank six thin articles on versions of the same phrase. It also gives AI tools one solid source to quote."),
       ("Can we use AI to write it?",
        "For research, briefs, outlines and first drafts, yes, and we do. For publishing without editing, no. Writing with no expertise, no original data and no named author is exactly what Google and AI tools give little weight to. What sets you apart is your evidence, not how fast the draft was written.")]),

    S("link-building-digital-pr", "Link Building &amp; Digital PR", "Core SEO", "&#9741;",
      "Link building and digital PR means getting other websites to link to yours and to mention your brand. Links from trusted, relevant sites help you rank on Google. Mentions on those same sites help AI tools recognise you. We earn both through guest articles, PR built on your own data, and outreach to the sites that matter in your industry.",
      "link building services, digital PR agency, guest posting, backlink acquisition, citation building",
      ["Study where your competitors get their links and find the ones you can win too",
       "Write guest articles for relevant sites that have real editors",
       "Build PR stories around data that only you have",
       "Ask sites with resource lists or broken links to point to you",
       "Keep your name, address and phone number identical in every local listing"],
      ["List of links competitors have and you do not", "Monthly targets and a log of who we contacted",
       "One piece of original research for PR", "Report on every live link, with its quality"],
      [("Do you buy links?",
        "No. Paying for links breaks Google's rules. It also does not work for AI answers, because AI tools care about relevance and agreement between sources, not raw link strength. We earn placements through editors."),
       ("How many links per month?",
        "We do not sell links by the number, because that rewards the wrong behaviour. We aim for a small number of relevant placements each month, chosen by real editors, on sites that matter in your industry. Ten relevant mentions beat a hundred unrelated ones, on Google and in AI answers.")]),

    S("ecommerce-seo", "Ecommerce SEO", "Core SEO", "&#9679;",
      "Ecommerce SEO helps online shops get found on Google, in shopping results and in AI answers. We organise your categories, bring filters and product options under control, add product markup, and write the buying guides shoppers look for. It is built for retailers whose category pages compete with the marketplaces they also sell on.",
      "ecommerce SEO services, Shopify SEO, product page SEO, category page optimization, ecommerce GEO",
      ["Decide which search each important page should win, before any page is built",
       "Stop filters and tracking codes from creating thousands of duplicate pages",
       "Add product, price, review and option markup across the catalogue",
       "Write the buying guides and comparisons that AI tools like to quote",
       "Set up Google Analytics so you can see the revenue that search brings in"],
      ["Map of pages and the searches they target", "Plan to control filters and duplicate pages",
       "Product markup across the catalogue", "Analytics set up to show revenue from search"],
      [("Our traffic grew but revenue did not. Why?",
        "Usually because the new visitors land on category and blog pages, which sell at about half the rate of product pages. That is normal when category rankings improve first. The fix is to make the route from category to product clearer and to improve the product pages at the same time."),
       ("Should product variants have their own URLs?",
        "It depends on whether people search for the variant. If they search by size or colour, a separate page for each one can win that search. If they do not, separate pages create thousands of near copies that waste Google's time. We decide this for each catalogue, using real search data.")]),

    S("saas-b2b-seo", "SaaS &amp; B2B SEO", "Core SEO", "&#9636;",
      "SaaS and B2B SEO is search work for software and business-to-business companies, judged by sales leads and not by page views. We start with the pages buyers read just before they choose: pricing, comparisons and alternatives. Then we add pages for each integration and each use of the product.",
      "SaaS SEO agency, B2B SEO services, comparison page SEO, alternatives page, integration pages",
      ["Publish the pages closest to a sale first, so they rank first",
       "Build comparison, &lsquo;alternatives to&rsquo; and &lsquo;versus&rsquo; pages",
       "Add pages for each integration and use, built from one template",
       "List your product on G2, Capterra and Product Hunt",
       "Tidy up your help documents, which AI tools read heavily"],
      ["Set of pages for buyers ready to choose", "Plan for comparison and alternatives pages",
       "Plan for integration and use pages", "Profiles on the review sites"],
      [("Are comparison pages against competitors risky?",
        "Not if they are fair. Accurate comparisons that admit where a competitor is stronger build trust. AI tools quote them because they read as balanced. Overstated claims are a legal risk and work less well."),
       ("How long until SEO produces leads?",
        "For pages aimed at buyers who are ready to choose, where the competition is weak, the first good leads usually arrive within 60 to 90 days. Being known across the whole subject takes 9 to 12 months. That is why we do the buying pages first. They pay for the patience the rest needs.")]),

    S("local-seo", "Local SEO", "Core SEO", "&#8962;",
      "Local SEO helps nearby customers find you on Google Search and Google Maps. We look after your Google Business Profile, make sure your name, address and phone number match everywhere, help you earn reviews steadily, and build a page for each place you serve. It works for a single shop or clinic and for businesses with many branches.",
      "local SEO services India, Google Business Profile optimization, map pack ranking, near me SEO",
      ["Complete your Google Business Profile and post to it regularly",
       "Check and correct your name, address and phone number in every directory",
       "Set up a simple way to ask customers for reviews that stays within Google's rules",
       "Build a page for each branch and each area you serve",
       "Add local business markup with the right service areas"],
      ["Google Business Profile completed, with a posting calendar", "Report of directory listings corrected",
       "Review request process", "Plan for branch and area pages"],
      [("Why are we not in the map results?",
        "Usually one of three reasons. Your name, address and phone number differ between directories, so Google is not sure they are all you. You have fewer or older reviews than competitors. Or the area you have told Google you serve does not match how people search. The first review shows which one applies."),
       ("Can we rank in cities where we have no office?",
        "Not in the map results, which need a real address. You can rank in the normal results for searches like &lsquo;service in city&rsquo; with well-built area pages. For many businesses that is worth more than the map anyway.")]),

    S("international-seo", "International SEO", "Core SEO", "&#9757;",
      "International SEO helps the right version of your site appear in each country and language. We choose how to structure your web addresses, add the tags that tell Google which page is for which country, research what people search for in each market, and adapt the content so it reads as local.",
      "international SEO, hreflang implementation, multilingual SEO, global SEO agency, ccTLD strategy",
      ["Choose the right web address structure for your markets and set it up",
       "Add and test hreflang, the tag that tells Google which page is for which country and language",
       "Research what people search for in each market, not just translate your keywords",
       "Adapt content to local habits, not only the language",
       "Set up tracking and Search Console for each market"],
      ["Recommended address structure", "Hreflang added and tested",
       "Search research for each market", "Guidelines for adapting content"],
      [("Subfolders, subdomains or country domains?",
        "Subfolders, in almost every case. They keep all your authority on one domain and cost the least to maintain. Hreflang tags handle the country targeting. Separate country domains make sense when local trust matters a lot and you have the budget to build each one up separately."),
       ("Can we just translate our existing content?",
        "Translation alone nearly always does worse. What people want, who you compete with and the words people use all change by country. A straight translation often targets a phrase nobody searches for. We research each market in its own language and adapt the content to it.")]),

    S("programmatic-seo", "Programmatic SEO", "Core SEO", "&#9638;",
      "Programmatic SEO means creating many useful pages from one template and a set of data, for example a page for every city, product type or integration. Done badly, it produces thousands of near-identical pages that Google ignores. We build it on data you own, set a quality bar every page must pass, and control which pages Google is allowed to index.",
      "programmatic SEO, scaled content, template SEO, database driven SEO, pSEO agency",
      ["Find the data you own that can support useful pages in large numbers",
       "Design templates that give each page something of its own",
       "Set a quality bar and index rules before launch",
       "Link the pages to each other automatically",
       "Watch for pages competing with each other and remove the weak ones"],
      ["Data source and template design", "Written quality bar for publishing",
       "Automatic internal links", "Ongoing check for competing pages"],
      [("Will Google penalise pages made this way?",
        "Google marks down thin, unhelpful pages however they are made. Pages built on real data that answer a real search, and that differ from each other, do well. The mistake is making thousands of near-identical pages from very little data. Our quality bar stops those from being published."),
       ("How many pages is realistic?",
        "As many as your data can support well, and no more. Sometimes that is two hundred. Sometimes it is fifty thousand. We would sooner publish two hundred pages that rank than five thousand that drag down the whole site.")]),

    S("site-migrations", "Site Migrations", "Core SEO", "&#8644;",
      "A site migration is any big change to a website: a new platform, a redesign or a new domain. Done carelessly, it can wipe out your Google traffic. We record where you stand before anything changes, map every old address to its new one, launch in stages and check the site daily for 30 days after launch.",
      "SEO migration, site migration services, replatforming SEO, domain migration, redirect mapping",
      ["Record every page and ranking before anything changes",
       "Map every old address to its new one, and test each redirect",
       "Carry over markup, internal links, titles and descriptions",
       "Launch in stages, with a clear rule for when to roll back",
       "Check daily for 30 days after launch and fix problems quickly"],
      ["Record of pages and rankings before the move", "Full redirect map with test log",
       "Staged launch schedule", "30-day report after launch"],
      [("How far ahead should we involve you?",
        "Before the new site is built, not after. The most expensive failures come from structure decisions made months earlier that are costly to undo. Bringing us in at the design stage costs a fraction of fixing a site that has already launched."),
       ("What happens if rankings drop anyway?",
        "Some movement in the first weeks is normal while Google reads the new site. We check daily against the record we took before the move. Within days we can tell whether it is normal settling or a real fault, and fix the fault. Without that record, you cannot tell the two apart.")],
      q="What is a site migration?"),

    S("white-label-seo", "White-Label SEO", "Core SEO", "&#9783;",
      "White-label SEO means we do the SEO and AI search work and you present it to your client as your own. We work under your brand and under a confidentiality agreement, from a single review to full monthly delivery, and we report in your template. Your client never knows we exist.",
      "white label SEO India, SEO reseller, outsourced SEO agency, white label GEO, agency partnership",
      ["Deliver reviews, plans and the work itself under your brand",
       "Report in your template, tone and format",
       "Start with a single review and grow to full monthly delivery",
       "Add AI search visibility as a service you can sell straight away",
       "Keep your account manager as the only person the client speaks to"],
      ["Confidentiality and partnership agreement", "Review and report templates in your brand",
       "Agreed delivery times", "One named contact on our side"],
      [("How do you stay invisible?",
        "Everything is delivered in your branding. We never contact your client directly. Every document carries your name. The confidentiality agreement is signed before any work starts."),
       ("Can you join client calls?",
        "Yes, as a member of your team, if you want technical depth in the room. Many partners like this for larger pitches. It is your decision.")]),

    S("seo-consulting", "SEO Consulting", "Core SEO", "&#9998;",
      "SEO consulting is direct time with an experienced SEO strategist at $30 per hour. Use it for a review of your site, a second opinion on an agency or a plan, or training for your own team. Clients also get our library of 39 written step-by-step guides.",
      "SEO consultant India, SEO consulting services, hourly SEO consultant, SEO training, SEO audit consultant",
      ["Review your site live on a call, recorded so you can watch it again",
       "Give a second opinion on your current agency or plan",
       "Train your in-house team on AI search and technical SEO",
       "Hand over our 39 written step-by-step guides for your team to use",
       "Check agency proposals and quotes before you sign"],
      ["Recording of the session", "Written summary with actions in order of importance",
       "Access to the 39 guides", "Follow-up questions answered by email"],
      [("What can we realistically cover in an hour?",
        "One problem, looked at properly. Why a certain page is not ranking. Whether a planned site structure will work. A review of an agency proposal. Send us the background beforehand and the hour goes on answers, not on catching up."),
       ("Why is it only $30 an hour?",
        "AI tools have made research, diagnosis and reporting much faster than they were two years ago. We pass that saving on in the price. It is also the simplest way for us to meet businesses that later become monthly clients.")]),

    S("performance-marketing", "Performance Marketing", "Paid ads", "&#9650;",
      "Performance marketing is paid advertising that you judge by sales and enquiries, not by views or clicks. We plan, run and report your ads on Google, Microsoft, Meta, TikTok, LinkedIn, Amazon and eBay as one budget, and move money toward whatever is bringing in customers at a profit.",
      "performance marketing agency, performance marketing agency UK, performance marketing agency London, paid search, paid social, PPC management",
      ["Search and shopping ads on Google and Microsoft",
       "Paid social on Meta, TikTok and LinkedIn, with ads made for each platform",
       "Marketplace ads on Amazon and eBay",
       "Tracking fixed first, so every sale is counted once and in the right place",
       "Spend reviewed every month against profit, with budget moved to what is working"],
      ["Account review with a list of wasted spend", "Channel plan and monthly budget",
       "New ads and tests every month", "One monthly report across every channel"],
      [("How much do we need to spend on ads?",
        "There is no fixed minimum. We look at your margins and what a new customer is worth to you, then suggest a starting budget small enough to test safely. On one retail account a new channel was proven on under &pound;1,000 of spend before the budget was raised."),
       ("Which platform should we start with?",
        "Usually the one where people are already searching for what you sell, which for most businesses is Google. Social platforms such as Meta and TikTok work best once you have ads people want to watch and a way to follow up with visitors who did not buy the first time."),
       ("How do you report results?",
        "One monthly report covering every channel, checked against your own sales records and not each ad platform's count. Ad platforms often claim the same sale twice, so we never add their numbers together.")],
      body="""<h2>What this has looked like</h2>
<p>One UK specialist retailer, 1 January to 10 November 2026. The client's name is withheld.</p>
<div class="tbl-wrap"><table>
<tr><th>Channel</th><th>Ad spend</th><th>Sales tracked</th><th>Return</th></tr>
<tr><td>Google Ads</td><td>&pound;64,092</td><td>&pound;761,562</td><td><strong>11.9x</strong></td></tr>
<tr><td>Meta Ads</td><td>&pound;25,945</td><td>&pound;422,107</td><td><strong>16.3x</strong></td></tr>
<tr><td>eBay Promoted Listings</td><td>&pound;11,886</td><td>&pound;99,353</td><td><strong>8.4x</strong></td></tr>
<tr><td>Amazon Ads</td><td>&pound;4,362</td><td>&pound;27,107</td><td><strong>6.2x</strong></td></tr>
<tr><td>All paid channels</td><td>&pound;107,222</td><td>&pound;1,310,129</td><td><strong>12.2x</strong></td></tr>
</table></div>
<p>On Meta, spend fell from &pound;33,930 to &pound;25,945 while purchases rose from 671 to 1,080. These are one account's results, not a promise: yours depend on your margins, your market and where you start. <a href="case-studies.html#paid">See the full case study</a>.</p>""",
      title="Performance Marketing Agency | Google, Meta, TikTok &amp; Marketplace Ads | SVED Solution",
      who="Businesses that already sell something people want and can tell us what a new customer is worth. If you have never run ads, we start with one channel and a small test budget.",
      surfaces=False),

    S("marketing-automation", "Marketing Automation &amp; Data", "Data and automation", "&#9881;",
      "Marketing automation and data is the plumbing behind your marketing: tracking that counts every sale correctly, reports you can trust, and automatic workflows that do the repetitive jobs. We set up analytics, consent and tagging, connect your tools, and build automations for tasks such as lead follow-up, review requests and monthly reporting.",
      "marketing automation agency, email marketing automation agency, martech agency, GA4 setup, server-side tracking, Consent Mode v2",
      ["Google Analytics 4 and Tag Manager set up so sales and leads are tracked properly",
       "Tracking that meets UK and EU consent rules (Consent Mode v2, server-side tagging)",
       "Every channel in one monthly report, checked against your own sales records",
       "Your website, CRM and email tool connected, so data moves without copy and paste",
       "Automations and AI assistants for follow-ups, lead routing and reporting"],
      ["Tracking review with a fix list", "Working analytics, tags and consent setup",
       "One dashboard or monthly report", "Written-up automations your team can run"],
      [("Our numbers never match between tools. Is that normal?",
        "Small gaps are normal, large ones are not. On one retail account we found a fault at the payment step that was crediting &pound;23,814 of sales and 101 orders to the wrong source, and a further 16-point gap caused by phone and in-store orders that analytics could not see. Finding gaps like these is usually the first job."),
       ("Which tools do you work with?",
        "Google Analytics 4, Google Tag Manager, Looker Studio, Supermetrics, HubSpot, Klaviyo, Mailchimp, Zapier, Make and n8n are the most common. We work with what you already have before suggesting anything new."),
       ("Will automation replace people on our team?",
        "No. It takes over repeat jobs such as copying leads between tools, sending follow-ups and building the monthly report, so your team spends its time on customers. Every automation is written down, so you do not depend on us to keep it running.")],
      body="""<h2>What this has looked like</h2>
<p>Two examples from accounts our founder leads. Client names are withheld.</p>
<ul>
<li><strong>A UK retailer.</strong> A fault at the payment step was crediting &pound;23,814 of sales and 101 orders to the wrong source. Phone and in-store orders, which analytics could not see, explained a further 16-point gap between reported and real revenue.</li>
<li><strong>A UK industrial services firm.</strong> Analytics had recorded nothing at all. After the rebuild it recorded 14,000 users, and for the first time the business could see where its enquiries came from.</li>
</ul>
<p><a href="case-studies.html#measurement">See the full case study</a>.</p>""",
      title="Marketing Automation Agency | Tracking, Data &amp; Workflows | SVED Solution",
      who="Businesses whose reports do not match their bank account, or whose team loses hours each week copying data between tools.",
      surfaces=False),

    S("ecommerce-development", "Ecommerce &amp; App Development", "Websites and apps", "&#9635;",
      "Ecommerce and app development is building the online shop, website or mobile app your marketing sends people to. We build on Shopify, WooCommerce and custom code, move existing shops to a new platform without losing search traffic, and connect the shop to your email, stock and reporting tools.",
      "ecommerce development agency, Shopify development agency, WooCommerce development, ecommerce migration, mobile app development",
      ["Shops built and redesigned on Shopify and WooCommerce",
       "Moves to a new platform that protect your search rankings",
       "Fast custom sites and web apps (Next.js, Laravel) and mobile apps (React Native, Flutter)",
       "Email and SMS for abandoned baskets, repeat orders and reviews",
       "Extra sales channels opened, such as TikTok Shop, Amazon and eBay"],
      ["Build plan with fixed stages", "Design and build, tested before launch",
       "Redirect map and ranking check for any move", "Handover and training for your team"],
      [("How long does a build take?",
        "A full ecommerce build or platform move usually takes 90 to 115 days from the first workshop to launch. Smaller jobs, such as redesigning your key pages, are much quicker. We agree the stages and dates before work starts."),
       ("Will we lose our Google rankings if we move platform?",
        "Not if the move is planned. Before a move we record every page that ranks, map each old address to its new one, and check rankings daily after launch. One retail move was planned as 36 tracked tasks, 16 of them critical, to protect the shop's rankings and around 22,000 links from other sites."),
       ("Can our own team update the site afterwards?",
        "Yes. We set the site up so your team can change text, images and products without a developer, and we train them before handover.")],
      body="""<h2>What this has looked like</h2>
<p>One UK specialist retailer. The client's name is withheld.</p>
<ul>
<li><strong>A new sales channel.</strong> A TikTok Shop opened from nothing took &pound;23,836 in its first six months from 156 orders, with 89.8% of sales coming through affiliates.</li>
<li><strong>A platform move.</strong> A move to Shopify was planned as 36 tracked tasks, 16 of them critical, to protect the shop's rankings and around 22,000 links from other sites.</li>
</ul>
<p><a href="case-studies.html#commerce">See the full case study</a>.</p>""",
      title="Ecommerce Development Agency | Shopify, WooCommerce &amp; Apps | SVED Solution",
      who="Retailers and brands that need a new shop, a faster one or a move to a better platform, and businesses that need a website or app built properly the first time.",
      surfaces=False),
]


SERVICE_EXTRA_FAQS = [
  ("How long before we see results?",
   "Google rankings usually improve within 60 to 90 days, sooner on pages already in positions 8 to 20. AI mentions follow a steady pattern: AI tools start to recognise the brand after 30 to 45 days, first mentions appear around day 60, regular mentions by day 90 and steady visibility after 4 to 6 months."),
  ("What does it cost?",
   "One-off consulting is $30 per hour. Monthly work is priced after the first review, because quoting before we have looked is guesswork. Run the free check first and what to do first usually becomes clear."),
]


# Shared pieces of the service page. Services about search and AI visibility get the
# AI-platform band and the audit call to action; the others get ones that fit.
SERVICE_DEFAULT_WHO = 'Businesses that already have something worth promoting and need more people to find it. If you have not launched yet and have no product or site, start with a <a href="contact.html">consulting hour</a>. Monthly work would be too early, and we will tell you so.'

SERVICE_SURFACES_BAND = """<section class="sec band-dark">
  <div class="wrap">
    <div class="sec-head center">
      <div class="eyebrow">Where you show up</div>
      <h2>The AI tools and search engines this covers</h2>
    </div>
    <!--PLATFORMS-->
  </div>
</section>
"""

SERVICE_COST_FAQ = [
  ("What does it cost?",
   "We price the work after a first call and a look at your accounts, because quoting before we "
   "understand the problem is guesswork. One-off advice is $30 per hour."),
]


def service_page(s):
    does = "".join(f"<li>{d}</li>" for d in s["does"])
    deliver = "".join(
        f'<div class="crow"><span class="lbl">{n:02d}</span><span class="val" style="text-align:left;flex:1">{d}</span></div>'
        for n, d in enumerate(s["deliver"], 1))
    plain = s["name"].replace("&amp;", "and")
    seo = s.get("surfaces", True)
    who = s.get("who") or SERVICE_DEFAULT_WHO
    surfaces = SERVICE_SURFACES_BAND if seo else ""
    if seo:
        closing = cta(f"See where you stand before you buy {plain}.",
                      "The free check runs 20 tests on your live page and takes about a minute.")
    else:
        closing = cta(f"Talk to us about {lc(plain)}.",
                      "Tell us what you sell and where you are stuck. We will look at your "
                      "accounts before the call and bring two or three things you can act on.",
                      primary=("Book a 15-minute call", "contact.html"),
                      secondary=("Run the free AI check", "ai-visibility-audit.html"))
    return f"""
{phero(f'<a href="index.html">Home</a> / <a href="services.html">Services</a> / {s["name"]}',
       f'{s["cluster"]} service', s["name"], "")}

<section class="sec">
  <div class="wrap">
    <div class="grid g2" style="gap:52px;align-items:start">
      <div class="prose">
        <div class="answer-block" style="margin-top:0">
          <div class="q">{s.get("q") or ("What is " + lc(plain).replace(" (aeo)", "") + "?")}</div>
          <p>{s["answer"]}</p>
        </div>
        <h2 style="margin-top:2rem">What this service covers</h2>
        <ul>{does}</ul>
        <h2>Who it is for</h2>
        <p>{who}</p>
      </div>
      <aside style="position:sticky;top:96px">
        <div class="panel" style="margin-bottom:20px">
          <div class="panel-bar"><i class="tdot"></i><i class="tdot"></i><i class="tdot"></i>
            <span style="margin-left:8px">what you get</span></div>
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
{surfaces}

{faq(s["faqs"] + (SERVICE_EXTRA_FAQS if seo else SERVICE_COST_FAQ))}

{closing}
"""


LEGAL_UPDATED = "17 November 2026"


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
  "<p><strong>When you run the free AI visibility check.</strong> Your name, your email address, the website you enter and the score it gets. We fetch that site's public pages to score them, and keep the result for 24 hours so a repeat check is fast. We use your details to send you the result and to follow up about it.</p><p><strong>If you tick the newsletter box.</strong> We add your email address to our AI news list, with the date and the wording you agreed to. The box is optional and unticked by default; leaving it empty means we will not send you marketing email.</p>"
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
    other = [(s["name"], f'/services/{s["slug"]}/') for s in SERVICES
             if s["cluster"] not in ("AI Search", "Core SEO")]
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
          ("Resources &amp; guides", "/resources/"),
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
        <span class="card-num">PAID ADS, DATA AND WEBSITES</span>
        <ul class="sitemap-list">{links(other)}</ul>
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
      <a class="card card-link" href="services.html"><div class="card-icon">&#9670;</div><h3>Services</h3><p>Twenty-one services across AI search, SEO, paid ads, data and websites.</p><span class="card-more">Browse services &rarr;</span></a>
      <a class="card card-link" href="generative-engine-optimization.html"><div class="card-icon">&#10022;</div><h3>GEO</h3><p>Get named by ChatGPT, Perplexity and Gemini.</p><span class="card-more">Explore GEO &rarr;</span></a>
      <a class="card card-link" href="insights.html"><div class="card-icon">&#9998;</div><h3>Insights</h3><p>Guides on SEO and AI search, from the people who do the work.</p><span class="card-more">Read insights &rarr;</span></a>
      <a class="card card-link" href="case-studies.html"><div class="card-icon">&#9636;</div><h3>Case studies</h3><p>Results from paid ads, SEO, AI search and online shops.</p><span class="card-more">See results &rarr;</span></a>
      <a class="card card-link" href="use-cases.html"><div class="card-icon">&#9635;</div><h3>Use cases</h3><p>Eight common problems and what we do about each.</p><span class="card-more">Find yours &rarr;</span></a>
      <a class="card card-link" href="contact.html"><div class="card-icon">&#9993;</div><h3>Contact</h3><p>Talk to the person who will review your site.</p><span class="card-more">Get in touch &rarr;</span></a>
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


def render(title, desc, slug, body, schema=None, keywords=None, og_image=None):
    html = SHELL.format(title=title, desc=desc, slug=slug, keywords=keywords or DEFAULT_KEYWORDS,
                        schema=schema or ORG_SCHEMA, nav=NAV, logo=LOGO_SVG,
                        og_image=og_image or "https://svedsolution.com/assets/og-image.svg",
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
        sch = page_ld(p["slug"], p["title"],
                      base=team_schema() if slug == "about" else None)
        html = render(p["title"], p["desc"], p["slug"], p["body"], schema=sch)
        name = "index.html" if slug == "index" else os.path.join(slug, "index.html")
        written.append((name.replace("\\", "/"), write(name, html)))

    for p in posts:
        og = ("https://svedsolution.com/assets/" + p["image"]) if p.get("image") else None
        html = render(f'{p["title"]} | SVED Solution', p["desc"],
                      f'insights/{p["slug"]}/', post_page(p), post_ld(p), og_image=og)
        rel = os.path.join("insights", p["slug"], "index.html")
        written.append((rel.replace("\\", "/"), write(rel, html)))

    # One page per industry, described by sector rather than client name.
    for i in INDUSTRIES:
        plain = i["name"].replace("&amp;", "and")
        html = render(
            f'{plain} SEO Services India | SVED Solution',
            re.sub(r"<[^>]+>", "", i["short"])[:152],
            f'{i["slug"]}/', industry_page(i),
            schema=industry_ld(i), keywords=i["kw"])
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
                      schema=page_ld(f"{slug}/", title),
                      keywords=f"SVED Solution {title.lower()}")
        rel = os.path.join(slug, "index.html")
        written.append((rel.replace("\\", "/"), write(rel, html)))

    # Human-readable sitemap, built from the same data as sitemap.xml.
    written.append(("sitemap/index.html", write(
        os.path.join("sitemap", "index.html"),
        render("Sitemap | Every Page on SVED Solution",
               "Complete index of svedsolution.com: services, industries, insights and resources.",
               "sitemap/", sitemap_page(posts),
               schema=page_ld("sitemap/", "Sitemap")))))

    # One page per service.
    for s in SERVICES:
        plain = s["name"].replace("&amp;", "and")
        html = render(
            s.get("title") or f'{plain} Services | SVED Solution',
            re.sub(r"<[^>]+>", "", s["answer"])[:152],
            f'services/{s["slug"]}/', service_page(s),
            schema=service_ld(s), keywords=s["kw"])
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
    copy_tree("brand/social", "social")
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

    # Redesign preview: pages in site-v2/ replace the generated homepage and
    # case-studies page. Every other page is still generated above, unchanged.
    v2 = os.path.join(OUT, "site-v2")
    for rel in ("index.html", "case-studies/index.html"):
        src = os.path.join(v2, *rel.split("/"))
        if os.path.isfile(src):
            with io.open(src, encoding="utf-8") as f:
                page = f.read()
            if rel == "index.html":
                faqs = re.findall(r'<summary class="m-text-7">(.*?)<span.*?faq__answer">(.*?)</p>', page, flags=re.S)
                ld = bundle(ORG_SCHEMA, WEBSITE_SCHEMA, faq_schema(faqs))
            else:
                ld = page_ld("case-studies/", "Case Studies")
            page = (page
                    .replace("<!--GTM-HEAD-->", GTM_HEAD.replace("GTM_CONTAINER_ID", GTM_ID))
                    .replace("<!--GTM-BODY-->", GTM_BODY.replace("GTM_CONTAINER_ID", GTM_ID))
                    .replace("<!--SCHEMA-->", '<script type="application/ld+json">' + ld + "</script>"))
            write(rel, page)

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
            '"description":"Consulting from $30 per hour; monthly work priced after a first review"}}')


# ---- structured data: breadcrumbs, FAQ, and per-type JSON-LD bundles -----
def _u(path):
    return "https://svedsolution.com/" + path.lstrip("/")


def _plain(t):
    t = re.sub(chr(60) + "[^" + chr(62) + "]+" + chr(62), "", str(t))
    for a, b in (("&mdash;", "—"), ("&amp;", "&"), ("&lsquo;", "'"),
                 ("&rsquo;", "'"), ("&ldquo;", '"'), ("&rdquo;", '"'), ("&#37;", "%")):
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t).strip()


def breadcrumb_schema(trail):
    items = ",".join(
        '{"@type":"ListItem","position":%d,"name":%s,"item":%s}'
        % (n, _j(_plain(nm)), _j(_u(u))) for n, (nm, u) in enumerate(trail, 1))
    return ('{"@context":"https://schema.org","@type":"BreadcrumbList",'
            '"itemListElement":[%s]}' % items)


def faq_schema(faqs):
    if not faqs:
        return ""
    ent = ",".join(
        '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
        % (_j(_plain(q)), _j(_plain(a))) for q, a in faqs)
    return '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}' % ent


def bundle(*objs):
    return "[" + ",".join(o for o in objs if o) + "]"


def service_ld(s):
    name = s["name"].replace("&amp;", "and")
    trail = [("Home", ""), ("Services", "services/"), (name, "services/%s/" % s["slug"])]
    return bundle(service_schema(s), breadcrumb_schema(trail),
                  faq_schema(s["faqs"] + SERVICE_EXTRA_FAQS))


def industry_service_schema(i):
    name = i["name"].replace("&amp;", "and")
    return ('{"@context":"https://schema.org","@type":"Service",'
            f'"name":{_j(name + " SEO & AI Visibility")},"serviceType":{_j(name + " SEO")},'
            f'"description":{_j(_plain(i["short"]))},'
            '"provider":{"@type":"ProfessionalService","name":"SVED Solution",'
            '"url":"https://svedsolution.com/","telephone":"+917846045690","email":"hello@svedsolution.com"},'
            '"areaServed":["IN","US","GB","AE"],'
            f'"url":{_j(_u(i["slug"] + "/"))}}}')


def industry_ld(i):
    name = i["name"].replace("&amp;", "and")
    trail = [("Home", ""), ("Industries", "industries/"), (name, "%s/" % i["slug"])]
    return bundle(industry_service_schema(i), breadcrumb_schema(trail),
                  faq_schema(industry_faqs(i)))


def post_faq_pairs(html):
    seg = html.split("Frequently asked questions", 1)
    if len(seg) < 2:
        return []
    return re.findall(r"<p><strong>(.*?)</strong>\s*(.*?)</p>", seg[1], re.S)


def post_ld(p):
    trail = [("Home", ""), ("Insights", "insights/"),
             (_plain(p["title"]), "insights/%s/" % p["slug"])]
    return bundle(post_schema(p), breadcrumb_schema(trail),
                  faq_schema(post_faq_pairs(p["html"])))


WEBSITE_SCHEMA = ('{"@context":"https://schema.org","@type":"WebSite",'
                  '"name":"SVED Solution","url":"https://svedsolution.com/",'
                  '"publisher":{"@type":"Organization","name":"SVED Solution","url":"https://svedsolution.com/"}}')

_SEG_NAMES = {"services": "Services", "industries": "Industries", "insights": "Insights",
              "about": "About", "contact": "Contact", "reviews": "Reviews", "videos": "Videos",
              "resources": "Resources", "use-cases": "Use Cases", "case-studies": "Case Studies",
              "terms": "Terms of Service", "privacy": "Privacy Policy", "sitemap": "Sitemap"}


def _seg_name(seg):
    return _SEG_NAMES.get(seg, seg.replace("-", " ").title())


def page_breadcrumb(slug, name):
    parts = [p for p in slug.strip("/").split("/") if p]
    if not parts:
        return ""
    trail = [("Home", "")]
    acc = ""
    for i, seg in enumerate(parts):
        acc += seg + "/"
        trail.append((name if i == len(parts) - 1 else _seg_name(seg), acc))
    return breadcrumb_schema(trail)


def webpage_schema(name, slug):
    return ('{"@context":"https://schema.org","@type":"WebPage",'
            f'"name":{_j(_plain(name))},"url":{_j(_u(slug))},'
            '"isPartOf":{"@type":"WebSite","name":"SVED Solution","url":"https://svedsolution.com/"},'
            '"publisher":{"@type":"Organization","name":"SVED Solution","url":"https://svedsolution.com/"}}')


def page_ld(slug, title, base=None):
    name = re.sub(r"\s*\|.*$", "", title).strip()
    if not slug.strip("/"):
        return bundle(ORG_SCHEMA, WEBSITE_SCHEMA)
    return bundle(base or webpage_schema(name, slug), page_breadcrumb(slug, name))


if __name__ == "__main__":
    files, nposts, nstatic, nurls = build()
    for name, size in files:
        print("%-52s %8d bytes" % (name, size))
    print("\n%d core pages + %d services + %d industries + %d posts + %d static"
          % (len(PAGES), len(SERVICES), len(INDUSTRIES), nposts, nstatic))
    print("sitemap.xml: %d URLs -> %s" % (nurls, DIST))
