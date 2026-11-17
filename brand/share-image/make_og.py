"""Render 1200x630 share images for blog posts in the site's own design.

Usage: python brand/share-image/make_og.py <output dir> [slug ...]
Needs: pip install playwright && playwright install chromium

Text wordmark only (no logo), navy canvas, the green orb from the homepage.
To make an image for a new post, add a line to CARDS (label, headline, one-line
summary), run the script, copy blog-<slug>.png into assets/ and set
image: "blog-<slug>.png" in the post's front matter.
"""
import os
import sys

from playwright.sync_api import sync_playwright

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONTS = "file:///" + os.path.join(REPO, "assets", "fonts").replace("\\", "/").replace(" ", "%20")

CARDS = {
    "ai-seo-agency-london": ("Local SEO · London", "AI SEO agency in London", "Rank on Google and get named by AI."),
    "ai-seo-company-kolkata": ("Local SEO · Kolkata", "AI SEO company in Kolkata", "Get named by ChatGPT and Google's AI answers."),
    "b2b-saas-seo-agency-london": ("Local SEO · London", "B2B & SaaS SEO agency in London", "Sales leads from search and AI."),
    "digital-marketing-agency-kolkata": ("Local SEO · Kolkata", "Digital marketing agency in Kolkata", "SEO and AI visibility you can measure."),
    "ecommerce-seo-agency-london": ("Local SEO · London", "Ecommerce SEO agency in London", "Get your products found and named by AI."),
    "ecommerce-seo-kolkata": ("Local SEO · Kolkata", "Ecommerce SEO in Kolkata", "Get your products found and named by AI."),
    "local-seo-agency-london": ("Local SEO · London", "Local SEO agency in London", "Win the map results and AI answers."),
    "local-seo-company-kolkata": ("Local SEO · Kolkata", "Local SEO company in Kolkata", "Win the map results and AI answers."),
    "move-pages-position-8-20-to-top-3": ("On-page SEO", "From position 8⁠–⁠20 to the top 3", "Eight steps. No new backlinks."),
    "seo-company-kolkata": ("Local SEO · Kolkata", "SEO company in Kolkata", "Rank on Google and get named by AI."),
    "should-you-block-gptbot": ("Technical SEO", "Should you block GPTBot?", "An honest look at the costs and benefits."),
    "technical-seo-agency-london": ("Local SEO · London", "Technical SEO agency in London", "The groundwork for Google and AI search."),
    # Posts whose image file name predates the blog-<slug>.png convention: the fourth
    # value is the file name the post's front matter already points at.
    "ai-citation-building": ("AI search", "AI citation building", "How brands get named by ChatGPT.", "blog-ai-citation-building.png"),
    "ai-seo-for-d2c-ecommerce-brands": ("Industry SEO", "AI SEO for D2C & ecommerce brands", "Get your products named in AI answers.", "blog-d2c-ecommerce-ai-seo.png"),
    "ai-seo-for-web3": ("Industry SEO", "AI SEO for Web3", "How crypto projects get named by AI.", "blog-ai-seo-web3.png"),
    "ai-seo-services-pricing-cost-guide": ("SEO pricing", "AI SEO pricing & cost guide", "About $500 to $25,000+ a month in 2026.", "blog-ai-seo-pricing.png"),
    "education-edtech-seo-india": ("Industry SEO", "EdTech & education SEO in India", "Rank on Google and get named by AI.", "blog-edtech-seo-india.png"),
    "generative-engine-optimization-agency-india": ("AI search", "GEO agency in India", "Get your brand named in AI answers.", "blog-geo-agency-india.png"),
    "geo-vs-seo": ("Strategy", "GEO vs SEO", "How they differ, and why you need both.", "blog-geo-vs-seo.png"),
    "how-to-appear-in-google-ai-overviews": ("AI search", "How to appear in Google AI Overviews", "A step-by-step guide for 2026.", "blog-google-ai-overviews.png"),
    "how-to-rank-in-chatgpt": ("AI search", "How to rank in ChatGPT", "A five-step method for 2026.", "blog-how-to-rank-in-chatgpt.png"),
    "saas-ai-product-seo": ("Industry SEO", "SaaS & AI product SEO", "Rank on Google and get named by AI.", "blog-saas-ai-seo.png"),
    "schema-markup-for-ai-search": ("AI search", "Schema markup for AI search", "Which markup to add, and where.", "blog-schema-for-ai.png"),
    "seo-for-fertility-ivf-clinics": ("Healthcare SEO", "SEO for fertility & IVF clinics", "Get found on Google and named by AI.", "blog-seo-for-fertility-ivf-clinics.png"),
    "seo-for-it-services-app-development": ("Industry SEO", "SEO for IT services & app development", "Win the buyers who are ready to hire.", "blog-it-app-dev-seo.png"),
    "seo-for-ivf-fertility-clinics-checklist": ("Healthcare SEO", "IVF clinic SEO checklist", "A 2026 checklist for fertility clinics.", "blog-fertility-clinic-checklist.png"),
    "seo-for-loss-prevention-companies": ("Industry SEO", "SEO for loss prevention companies", "A guide for the US and UK.", "blog-seo-for-loss-prevention-companies.png"),
    "web3-crypto-seo-agency": ("Industry SEO", "Web3 & crypto SEO agency", "Get found on Google and named by AI.", "blog-web3-crypto-seo.png"),
    "what-is-answer-engine-optimization": ("AI search", "What is answer engine optimization?", "AEO explained, with a 2026 guide.", "blog-what-is-aeo.png"),
    "what-is-generative-engine-optimization": ("AI search", "What is generative engine optimization?", "GEO explained, with a 2026 guide.", "blog-what-is-geo.png"),
    "what-is-llm-seo": ("AI search", "What is LLM SEO?", "How to be read and quoted by ChatGPT.", "blog-what-is-llm-seo.png"),
}

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face { font-family: 'Gabarito'; font-weight: 400 800; src: url('%(fonts)s/gabarito-var.woff2') format('woff2'); }
@font-face { font-family: 'Onest'; font-weight: 400 600; src: url('%(fonts)s/onest-var.woff2') format('woff2'); }
* { box-sizing: border-box; margin: 0; }
body { width: 1200px; height: 630px; overflow: hidden; position: relative; background: #0B1219;
       font-family: 'Onest', sans-serif; color: #fff; -webkit-font-smoothing: antialiased; }
.ring { position: absolute; width: 620px; height: 620px; right: -150px; top: 5px; border-radius: 50%%;
        border: 1.5px solid rgba(255,255,255,.13); }
.orb { position: absolute; width: 460px; height: 460px; right: -70px; top: 85px; border-radius: 50%%;
       background: radial-gradient(circle at 32%% 28%%, #9BFFE0 0%%, #00FFB2 30%%, #00C48A 62%%, #04795C 100%%); }
.orb::after { content: ""; position: absolute; inset: 0; border-radius: 50%%;
       background: repeating-radial-gradient(circle at 78%% 82%%, rgba(11,18,25,0) 0 26px, rgba(11,18,25,.10) 26px 28px); }
.moon { position: absolute; width: 46px; height: 46px; border-radius: 50%%; background: #00FFB2; left: 763px; top: 470px; }
.copy { position: absolute; left: 76px; top: 78px; width: 640px; }
.tag { display: inline-block; padding: 9px 20px; border: 1.5px solid rgba(255,255,255,.28); border-radius: 999px;
       font-weight: 600; font-size: 19px; letter-spacing: .12em; text-transform: uppercase; color: #00FFB2; }
h1 { margin-top: 34px; font-family: 'Gabarito', sans-serif; font-weight: 800; font-size: 84px; line-height: 1.0;
     letter-spacing: -.025em; text-wrap: balance; }
p { margin-top: 26px; font-size: 30px; line-height: 1.3; color: #B9C6D2; max-width: 600px; }
.foot { position: absolute; left: 76px; right: 76px; bottom: 54px; display: flex; align-items: baseline; }
.mark { font-family: 'Gabarito', sans-serif; font-weight: 800; font-size: 40px; letter-spacing: -.03em; }
.mark i { display: inline-block; width: 11px; height: 11px; border-radius: 50%%; background: #00FFB2; margin-left: 3px; }
.site { margin-left: 22px; font-size: 21px; color: #8696A5; }
</style></head><body>
<div class="ring"></div><div class="orb"></div><div class="moon"></div>
<div class="copy"><span class="tag">%(tag)s</span><h1>%(head)s</h1><p>%(sub)s</p></div>
<div class="foot"><span class="mark">SVED<i></i></span><span class="site">svedsolution.com</span></div>
<script>
  // Shrink the headline until it sits in three lines or fewer and clears the footer.
  document.fonts.ready.then(() => {
    const h = document.querySelector('h1'); let s = 84;
    const lines = () => Math.round(h.getBoundingClientRect().height / (s * 1.0));
    const set = v => { s = v; h.style.fontSize = s + 'px'; };
    // Prefer two lines if a slightly smaller size gets there; otherwise keep full size on three.
    // A short, one-line headline gets more presence.
    if (lines() === 1) { const span = document.createRange(); span.selectNodeContents(h);
      while (s < 108 && span.getBoundingClientRect().width < 560) set(s + 2);
      if (lines() > 1 || span.getBoundingClientRect().width > 600) set(s - 2); }
    if (lines() > 2) { let t = 84; while (t > 72) { t -= 2; set(t); if (lines() <= 2) break; } if (lines() > 2) set(84); }
    while ((lines() > 3 || document.querySelector('p').getBoundingClientRect().bottom > 500) && s > 48) set(s - 2);
    document.body.dataset.ready = s;
  });
</script></body></html>"""


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;")


out = sys.argv[1]
slugs = sys.argv[2:] or list(CARDS)
os.makedirs(out, exist_ok=True)
tmp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_card.html")
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
    for slug in slugs:
        tag, head, sub = CARDS[slug][:3]
        fname = CARDS[slug][3] if len(CARDS[slug]) > 3 else f"blog-{slug}.png"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(PAGE % {"fonts": FONTS, "tag": esc(tag), "head": esc(head), "sub": esc(sub)})
        page.goto("file:///" + tmp.replace("\\", "/").replace(" ", "%20"))
        page.wait_for_function("document.body.dataset.ready")
        fonts = page.evaluate("[document.fonts.check('800 84px Gabarito'), document.fonts.check('400 30px Onest')]")
        size = page.evaluate("document.body.dataset.ready")
        dest = os.path.join(out, fname)
        page.screenshot(path=dest)
        print(f"{slug}: headline {size}px, fonts loaded {fonts}, {os.path.getsize(dest) // 1024} KB")
    browser.close()
os.remove(tmp)
