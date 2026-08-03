---
title: "Should You Block GPTBot? An Honest Cost-Benefit"
slug: "should-you-block-gptbot"
description: "Blocking AI crawlers protects your content from training and retrieval — and guarantees you are never cited. When that trade makes sense, and when it is self-harm."
answer: "Block GPTBot only if your revenue comes from people landing on your pages and consuming content there — publishers, ad-supported media, paid archives. If your revenue comes from being discovered and recommended, blocking AI crawlers guarantees you are never cited and is self-harm. Most businesses fall into the second category. Note that blocking a training crawler and blocking a retrieval crawler are different decisions: GPTBot handles training, while OAI-SearchBot and ChatGPT-User handle live retrieval and citation."
category: "Technical"
date: "2026-07-15"
author: "Ved Prakash"
readtime: "7 min"
---

This question gets answered ideologically far more often than it gets answered commercially. Here is the commercial version.

## First: these are not one bot

The most common mistake is treating "AI crawlers" as a single decision. They do different jobs:

| Crawler | Operator | What it does | Blocking it means |
|---|---|---|---|
| **GPTBot** | OpenAI | Collects data for model training | Your content is not used in training |
| **OAI-SearchBot** | OpenAI | Indexes for ChatGPT search | **You cannot be cited in ChatGPT search** |
| **ChatGPT-User** | OpenAI | Fetches a page when a user's prompt needs it live | You cannot be fetched on demand |
| **Google-Extended** | Google | Controls Gemini training and grounding | Excluded from Gemini grounding |
| **PerplexityBot** | Perplexity | Indexes for Perplexity answers | **You cannot be cited in Perplexity** |
| **ClaudeBot** | Anthropic | Training and retrieval | Excluded from Claude |
| **CCBot** | Common Crawl | Open dataset used by many models | Excluded from a very wide range of downstream models |

Blocking `GPTBot` and blocking `OAI-SearchBot` are completely different business decisions. Many sites block both by accident, having intended only the first.

Also worth knowing: `Google-Extended` does **not** affect your normal Google Search ranking. Blocking it removes you from Gemini grounding only. Blocking `Googlebot` is what would destroy your search traffic, and nobody should be doing that.

## The case for blocking

It is a real case, and it applies to a specific business model:

- **You monetise pageviews.** Ad-supported publishing, where a summarised answer replaces the visit that pays you.
- **Your content is the product.** Paid archives, research reports, course material, subscription libraries.
- **You have a licensing strategy.** Several publishers have negotiated paid licensing deals; blocking is leverage in that negotiation.
- **Legal or contractual constraints.** Client-confidential or regulated material that should not enter a training corpus.

If you are in one of these categories, blocking is a defensible commercial decision, not paranoia.

## The case against blocking

For most businesses, the calculation inverts completely:

- **You monetise conversions, not visits.** A SaaS product, an agency, an ecommerce brand, a professional service. You do not need the pageview. You need to be the brand that gets named.
- **Discovery is your bottleneck.** Being cited in an AI answer is free distribution to a user at the exact moment they are evaluating options.
- **Your competitors are not blocking.** If you block and they do not, the model simply cites them. You have not protected anything; you have donated the category to whoever stayed open.

**Blocking retrieval crawlers guarantees zero citations.** There is no partial credit and no workaround. A model cannot cite what it cannot fetch.

## The middle path most people miss

You do not have to choose site-wide. Reasonable and common:

- **Allow retrieval crawlers, block training crawlers.** Allow `OAI-SearchBot`, `ChatGPT-User` and `PerplexityBot` so you can be cited; disallow `GPTBot` and `CCBot` so your content is not absorbed into training corpora.
- **Block selectively by path.** Open your marketing, product and blog content. Disallow gated research, member areas and premium archives.

```
User-agent: GPTBot
Disallow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /
Disallow: /research/
Disallow: /members/
```

## What we do on our own site

We allow everything. Our revenue comes from being recommended, our content is marketing rather than product, and the citation data we publish only exists because we are open to the crawlers.

That is a decision that follows from our business model, not a universal recommendation. Yours may differ.

## One thing to check today

Open `yourdomain.com/robots.txt` and read it properly. A surprising number of sites are blocking retrieval crawlers by accident — inherited from a template, a plugin default, or a well-meaning developer who read a headline in 2024. If you are wondering why you are never cited, this is the first thing to rule out.
