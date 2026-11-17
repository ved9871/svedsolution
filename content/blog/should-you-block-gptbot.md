---
title: "Should You Block GPTBot? An Honest Cost-Benefit"
slug: "should-you-block-gptbot"
description: "Should you block GPTBot? Blocking AI crawlers keeps your content out of AI training, but it also means AI never mentions you. When that trade is worth it."
keywords: "block GPTBot, GPTBot robots.txt, AI crawlers, OAI-SearchBot, should you block AI crawlers"
answer: "Block GPTBot only if you earn money from people reading content on your pages: publishers, ad-supported media, paid archives. If you earn by being found and recommended, blocking AI crawlers means you are never mentioned, and that only hurts you. Most businesses are in the second group. Training crawlers and answer crawlers are separate decisions: GPTBot handles training, while OAI-SearchBot and ChatGPT-User fetch pages for live AI answers."
category: "Technical"
date: "2026-07-15"
updated: "2026-11-17"
author: "Ved Prakash"
readtime: "7 min"
---

This question usually gets answered from principle and far less often from a business point of view. Here is the business version.

## First: these are not one bot

The most common mistake is treating "AI crawlers" as one decision. An AI crawler is a bot that an AI company sends to read websites. Different crawlers do different jobs:

| Crawler | Operator | What it does | Blocking it means |
|---|---|---|---|
| **GPTBot** | OpenAI | Collects data for training AI models | Your content is not used in training |
| **OAI-SearchBot** | OpenAI | Builds the index for ChatGPT search | **You cannot appear as a source in ChatGPT search** |
| **ChatGPT-User** | OpenAI | Fetches a page live when a user's question needs it | Your pages cannot be fetched on demand |
| **Google-Extended** | Google | Controls Gemini training and grounding (the live sources behind Gemini's answers) | Left out of Gemini grounding |
| **PerplexityBot** | Perplexity | Builds the index for Perplexity answers | **You cannot appear as a source in Perplexity** |
| **ClaudeBot** | Anthropic | Training, and finding pages for answers | Left out of Claude |
| **CCBot** | Common Crawl | Open dataset used by many AI models | Left out of a very wide range of later models |

Blocking `GPTBot` and blocking `OAI-SearchBot` are completely different business decisions. Many sites block both by accident when they only meant to block the first.

Also worth knowing: `Google-Extended` does **not** affect your normal Google Search ranking. Blocking it removes you from Gemini grounding only. Blocking `Googlebot` is what would destroy your search traffic, and nobody should be doing that.

## The case for blocking

It is a real case, and it applies to a specific kind of business:

- **You earn money from page views.** Ad-supported publishing, where an AI summary replaces the visit that pays you.
- **Your content is the product.** Paid archives, research reports, course material, subscription libraries.
- **You have a licensing strategy.** Several publishers have negotiated paid licensing deals. Blocking strengthens your hand in that negotiation.
- **Legal or contract limits.** Client-confidential or regulated material that should not end up in AI training data.

In any of these groups, blocking is a defensible commercial decision. It is not paranoia.

## The case against blocking

For most businesses, the sums come out the other way:

- **You earn money from sales and enquiries rather than visits.** A SaaS product, an agency, an ecommerce brand, a professional service. You do not need the page view. You need to be the brand that gets named.
- **Being found is your main problem.** A mention in an AI answer is free exposure to someone at the exact moment they are comparing options.
- **Your competitors are not blocking.** If you block and they do not, the AI tool simply names them. All you have done is hand the category to whoever stayed open.

**If you block the crawlers that fetch pages for AI answers, you will never be mentioned.** There is no half measure and no workaround. An AI tool cannot quote a page it cannot open.

## The middle path most people miss

You do not have to make one choice for the whole site. These options are reasonable and common:

- **Allow answer crawlers, block training crawlers.** Allow `OAI-SearchBot`, `ChatGPT-User` and `PerplexityBot` so you can be mentioned. Disallow `GPTBot` and `CCBot` so your content does not go into AI training data.
- **Block by section.** Open your marketing, product and blog content. Disallow gated research, member areas and premium archives.

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

We allow everything. We earn our money by being recommended. Our content is marketing rather than a product we sell. And the data on AI mentions that we publish only exists because we are open to the crawlers.

That decision follows from our business model. It is not advice for everyone, and yours may differ.

## One thing to check today

Open `yourdomain.com/robots.txt` and read it properly. This is the file that tells crawlers which parts of your site they may read. A surprising number of sites block the crawlers that fetch pages for AI answers by accident. The rule came from a template, a plugin default, or a well-meaning developer who read a headline in 2024. If you are wondering why AI never mentions you, this is the first thing to rule out.
