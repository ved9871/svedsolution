"""Render the in-post graphics (numbered lists, price table, quote) in the site's design.

Usage: python brand/share-image/make_inline.py <output dir> [file name ...]
Needs: pip install playwright && playwright install chromium

Each entry in CARDS is keyed by the file name the post already points at, so
re-rendering replaces the image without touching the post. `alt` and `caption`
are the texts the post's <figure> line should carry; keep them in step with the
wording on the card.
"""
import os
import sys

from playwright.sync_api import sync_playwright

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONTS = "file:///" + os.path.join(REPO, "assets", "fonts").replace("\\", "/").replace(" ", "%20")


def steps(tag, title, rows, caption, height=820, lead=None):
    # Lower-case each step's first letter for the sentence, but leave acronyms such as "AI" alone.
    low = lambda r: (r[0].lower() + r[1:]) if len(r) > 1 and r[1].islower() else r
    alt = (lead or title) + ": " + ", ".join(low(r) for r in rows)
    return dict(kind="list", tag=tag, title=title, rows=rows, height=height, alt=alt, caption=caption)


CARDS = {
    "blog-ai-citation-building-inline.png": steps(
        "AI citation building", "Five steps to getting mentioned by AI",
        ["Settle your identity", "List the sites AI trusts in your industry", "Study where competitors are mentioned",
         "Make your people known", "Measure your share of mentions"],
        "AI citation building, in five steps.", lead="AI citation building in five steps"),
    "blog-d2c-ecommerce-ai-seo-inline.png": steps(
        "D2C & ecommerce", "The D2C & ecommerce AI SEO method",
        ["Fix the catalogue's technical problems", "Add commerce schema", "Answer buying questions",
         "Build mentions on review sites", "Measure your AI share"],
        "The D2C & ecommerce AI SEO method."),
    "blog-ai-seo-web3-inline.png": steps(
        "Web3", "The AI SEO for Web3 method",
        ["Make docs readable to AI", "Settle your identity", "Answer-first protocol content", "Add schema",
         "Get trusted mentions"],
        "The AI SEO for Web3 method."),
    "blog-ai-seo-pricing-inline.png": dict(
        kind="prices", tag="AI SEO cost · 2026", title="Typical monthly fees (USD)", height=760,
        rows=[("Starter", "$500 – $2,000"), ("Growth", "$2,000 – $5,000"), ("Professional", "$5,000 – $12,000"),
              ("Enterprise", "$12,000 – $25,000+")],
        alt="AI SEO cost by tier in 2026: Starter $500-2,000, Growth $2,000-5,000, Professional $5,000-12,000, Enterprise $12,000-25,000+ per month",
        caption="Typical 2026 AI SEO monthly fees (USD)."),
    "blog-edtech-seo-india-inline.png": steps(
        "Education & EdTech", "The EdTech SEO method",
        ["Answer the questions learners ask", "Add education schema", "Become the authority in each subject",
         "Win local and campus searches", "Get mentioned on trusted sources"],
        "The education & EdTech SEO method."),
    "blog-fertility-clinic-checklist-inline.png": steps(
        "Fertility clinics", "The fertility clinic SEO checklist",
        ["Name your clinicians and their credentials", "Have content medically reviewed", "Local SEO for each location",
         "Medical schema (MedicalClinic)", "Mentions on trusted health sites"],
        "The fertility clinic SEO checklist."),
    "blog-geo-agency-india-inline.png": steps(
        "GEO", "How we run GEO",
        ["Review before recommending", "Make your identity clear", "Build agreement across trusted sites",
         "Publish content AI can find and quote", "Report the number"],
        "How we run GEO."),
    "blog-google-ai-overviews-inline.png": steps(
        "Google AI Overviews", "Five steps to appear in AI Overviews",
        ["Rank the page first", "Answer first, in 40 to 60 words", "Make it easy to lift", "Add the schema",
         "Make your brand clear and backed up"],
        "Five steps to AI Overview visibility.", lead="Five steps to appear in Google AI Overviews"),
    "blog-it-app-dev-seo-inline.png": steps(
        "IT & app development", "The IT & app development SEO method",
        ["Build service and technology pages", "Show proof with case studies", "Win directories and reviews",
         "Answer buyer questions", "Fix the technical base"],
        "The IT & app development SEO method."),
    "blog-saas-ai-seo-inline.png": steps(
        "SaaS & AI products", "The SaaS SEO method",
        ["Start with the pages closest to a sale", "Build the comparison pages", "Make docs easy for AI to read",
         "Win on review sites", "Add SaaS schema markup"],
        "The SaaS & AI product SEO method."),
    "blog-schema-for-ai-inline.png": dict(
        kind="list", tag="Schema markup", title="Schema types that matter for AI search", height=820,
        rows=[("FAQPage & QAPage", "questions and answers"), ("Article", "who wrote it, and when"),
              ("Organization + sameAs", "who you are, and your profiles"),
              ("Product / Offer / Review", "price, stock and ratings"), ("HowTo", "step-by-step instructions")],
        alt="Schema that matters for AI: FAQPage and QAPage, Article, Organization with sameAs, Product Offer Review, HowTo",
        caption="The schema types that matter most for AI search."),
    "blog-seo-for-fertility-ivf-clinics-inline.png": dict(
        kind="quote", tag="Fertility search", height=675,
        quote="Patients now ask ChatGPT which clinic to trust, before they ever reach Google.",
        sub="Why fertility clinics need to be visible in AI answers, not only on Google.",
        alt="Patients now ask ChatGPT which fertility clinic to trust before they ever reach Google",
        caption="Patients now ask AI tools before they reach Google."),
    "blog-web3-crypto-seo-inline.png": steps(
        "Web3 & crypto", "The Web3 SEO method",
        ["Build trust in who you are", "Explain the protocol, answer first", "Get mentioned on trusted sources",
         "Clean technical SEO and schema", "Adapt for communities worldwide"],
        "The Web3 & crypto SEO method."),
    "blog-what-is-aeo-inline.png": dict(
        kind="list", tag="AEO", title="Answer engine optimization, in four moves", height=760,
        rows=["Answer first, in 40 to 60 words", "Build the page around questions", "Add FAQ and QAPage schema",
              "Win the answer spot and keep it"],
        alt="The AEO checklist: answer first in 40 to 60 words, build the page around questions, add FAQ and QAPage schema, win the answer spot and keep it",
        caption="Answer Engine Optimization, in four moves."),
    "blog-what-is-geo-inline.png": dict(
        kind="list", tag="GEO", title="The four levers of GEO", height=760,
        rows=["A clear brand identity", "Consistent mentions on other sites", "Content that is easy to find and quote",
              "Freshness"],
        alt="The four levers of Generative Engine Optimization: a clear brand identity, consistent mentions on other sites, content that is easy to find and quote, and freshness",
        caption="GEO works through four levers that support each other."),
    "blog-what-is-llm-seo-inline.png": steps(
        "LLM SEO", "What LLM SEO covers",
        ["Server-side rendering", "AI crawler access", "llms.txt at the root", "Clear passages", "Schema markup"],
        "What LLM SEO covers."),
}

CSS = """
@font-face { font-family: 'Gabarito'; font-weight: 400 800; src: url('%(fonts)s/gabarito-var.woff2') format('woff2'); }
@font-face { font-family: 'Onest'; font-weight: 400 600; src: url('%(fonts)s/onest-var.woff2') format('woff2'); }
* { box-sizing: border-box; margin: 0; }
body { width: 1200px; height: %(height)spx; overflow: hidden; position: relative; background: #0B1219;
       font-family: 'Onest', sans-serif; color: #fff; -webkit-font-smoothing: antialiased; }
.ring { position: absolute; width: 480px; height: 480px; right: -190px; top: -230px; border-radius: 50%%;
        border: 1.5px solid rgba(255,255,255,.13); }
.orb { position: absolute; width: 340px; height: 340px; right: -120px; top: -160px; border-radius: 50%%;
       background: radial-gradient(circle at 30%% 70%%, #9BFFE0 0%%, #00FFB2 30%%, #00C48A 62%%, #04795C 100%%); }
.orb::after { content: ""; position: absolute; inset: 0; border-radius: 50%%;
       background: repeating-radial-gradient(circle at 20%% 20%%, rgba(11,18,25,0) 0 22px, rgba(11,18,25,.10) 22px 24px); }
.moon { position: absolute; width: 30px; height: 30px; border-radius: 50%%; background: #00FFB2; right: 250px; top: 86px; }
.head { position: absolute; left: 76px; top: 62px; width: 820px; }
.tag { display: inline-block; padding: 8px 18px; border: 1.5px solid rgba(255,255,255,.28); border-radius: 999px;
       font-weight: 600; font-size: 17px; letter-spacing: .12em; text-transform: uppercase; color: #00FFB2; }
h1 { margin-top: 22px; font-family: 'Gabarito', sans-serif; font-weight: 800; font-size: 50px; line-height: 1.05;
     letter-spacing: -.02em; }
.rows { position: absolute; left: 76px; right: 76px; top: 212px; bottom: 128px; display: flex; flex-direction: column; }
.row { flex: 1; display: flex; align-items: center; border-top: 1.5px solid rgba(255,255,255,.11); min-height: 0; }
.row:last-child { border-bottom: 1.5px solid rgba(255,255,255,.11); }
.n { flex: none; width: 92px; font-family: 'Gabarito', sans-serif; font-weight: 700; font-size: 30px; color: #00FFB2; }
.l { font-family: 'Gabarito', sans-serif; font-weight: 700; font-size: 40px; letter-spacing: -.015em; white-space: nowrap; }
.d { margin-left: auto; padding-left: 28px; font-size: 25px; color: #9FAEBC; white-space: nowrap; }
.v { margin-left: auto; font-family: 'Gabarito', sans-serif; font-weight: 800; font-size: 44px; color: #00FFB2; white-space: nowrap; }
.prices .l { font-size: 44px; }
.q { position: absolute; left: 76px; top: 150px; width: 900px; }
.q b { display: block; font-family: 'Gabarito', sans-serif; font-weight: 800; font-size: 150px; line-height: .6; color: #00FFB2; height: 62px; }
.q p { font-family: 'Gabarito', sans-serif; font-weight: 800; font-size: 66px; line-height: 1.06; letter-spacing: -.02em; text-wrap: balance; }
.q span { display: block; margin-top: 28px; font-size: 27px; line-height: 1.35; color: #B9C6D2; max-width: 760px; }
.foot { position: absolute; left: 76px; right: 76px; bottom: 46px; display: flex; align-items: baseline; }
.mark { font-family: 'Gabarito', sans-serif; font-weight: 800; font-size: 36px; letter-spacing: -.03em; }
.mark i { display: inline-block; width: 10px; height: 10px; border-radius: 50%%; background: #00FFB2; margin-left: 3px; }
.site { margin-left: 20px; font-size: 20px; color: #8696A5; }
"""

FIT = """<script>
document.fonts.ready.then(() => {
  // Keep every row on one line: shrink the label size for the whole card if any row is too wide.
  const rows = [...document.querySelectorAll('.row')];
  let s = parseFloat(getComputedStyle(document.querySelector('.l') || document.body).fontSize) || 40;
  const over = () => rows.some(r => r.scrollWidth > r.clientWidth + 1);
  while (rows.length && over() && s > 26) { s -= 1; document.querySelectorAll('.l').forEach(e => e.style.fontSize = s + 'px'); }
  // The title stays on one line so it never runs into the first row.
  const h = document.querySelector('h1'); let t = 50;
  if (h) { h.style.whiteSpace = 'nowrap'; while (h.scrollWidth > 820 && t > 34) { t -= 1; h.style.fontSize = t + 'px'; } }
  document.body.dataset.ready = String(s) + ' title ' + t + (over() || (h && h.scrollWidth > 820) ? ' OVERFLOW' : '');
});
</script>"""


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;")


def page(card):
    foot = '<div class="foot"><span class="mark">SVED<i></i></span><span class="site">svedsolution.com</span></div>'
    deco = '<div class="ring"></div><div class="orb"></div><div class="moon"></div>'
    css = "<style>" + CSS % {"fonts": FONTS, "height": card["height"]} + "</style>"
    if card["kind"] == "quote":
        body = (f'<div class="head"><span class="tag">{esc(card["tag"])}</span></div>'
                f'<div class="q"><b>&ldquo;</b><p>{esc(card["quote"])}</p><span>{esc(card["sub"])}</span></div>')
    else:
        rows = []
        for i, r in enumerate(card["rows"], 1):
            if card["kind"] == "prices":
                rows.append(f'<div class="row"><span class="l">{esc(r[0])}</span><span class="v">{esc(r[1])}</span></div>')
            elif isinstance(r, tuple):
                rows.append(f'<div class="row"><span class="n">{i:02d}</span><span class="l">{esc(r[0])}</span>'
                            f'<span class="d">{esc(r[1])}</span></div>')
            else:
                rows.append(f'<div class="row"><span class="n">{i:02d}</span><span class="l">{esc(r)}</span></div>')
        body = (f'<div class="head"><span class="tag">{esc(card["tag"])}</span><h1>{esc(card["title"])}</h1></div>'
                f'<div class="rows {card["kind"]}">{"".join(rows)}</div>')
    return f'<!doctype html><html><head><meta charset="utf-8">{css}</head><body>{deco}{body}{foot}{FIT}</body></html>'


if __name__ == "__main__":
    out = sys.argv[1]
    names = sys.argv[2:] or list(CARDS)
    os.makedirs(out, exist_ok=True)
    tmp = os.path.join(out, "_card.html")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name in names:
            card = CARDS[name]
            pg = browser.new_page(viewport={"width": 1200, "height": card["height"]}, device_scale_factor=1)
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(page(card))
            pg.goto("file:///" + tmp.replace("\\", "/").replace(" ", "%20"))
            pg.wait_for_function("document.body.dataset.ready")
            pg.screenshot(path=os.path.join(out, name))
            print(f'{name}: {card["height"]}px high, label size {pg.evaluate("document.body.dataset.ready")}')
            pg.close()
        browser.close()
    os.remove(tmp)
