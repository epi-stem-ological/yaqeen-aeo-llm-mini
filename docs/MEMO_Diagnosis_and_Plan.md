MEMO — Diagnosis & Plan (2–3 pages)

Cluster: Parenting & Identity (5 Yaqeen papers)
Window: Last 90 days (GSC/GA4)
Goal: (a) Diagnose why answer engines may be under‑citing us, (b) propose a pragmatic GEO/AEO plan to recover share‑of‑answer.

1) Diagnosis (brief, evidence‑based)

Top hypotheses

Demand shift (query mix/intent): Mid‑tail searches skew toward practical phrasing (e.g., how to build resilience, Islamic parenting psychology) while our pages are optimized for theory/long‑form essays. Impact: lower intent match → weaker snippets → fewer citations/CTR.

Supply gaps (facts/entities/freshness): Pages lack atomic Answer Units (AUs) and explicit entities (about, mentions) like attachment theory, resilience, authoritative parenting. Impact: reduced snippetability and weaker KG/entity confidence; stale dateModified hints at low freshness.

Technical discoverability: Template likely needs ScholarlyArticle + FAQPage parity, canonical/hreflang hardening, and CWV polishing (LCP/INP). Impact: fewer rich results and ranking instability on mobile.

Baseline (compact)
Populate from GSC export filtered to the 5 paper URLs.

query	impressions	clicks	CTR	avg position	last updated	existing schema
muslim identity for youth	[#]	[#]	[#]%	[#].[#]	2025‑MM‑DD	Article
building resilient muslim children	[#]	[#]	[#]%	[#].[#]	2025‑MM‑DD	Article
islamic parenting strategies	[#]	[#]	[#]%	[#].[#]	2025‑MM‑DD	Article
attachment to God child resilience	[#]	[#]	[#]%	[#].[#]	2025‑MM‑DD	Article
authoritative parenting islam	[#]	[#]	[#]%	[#].[#]	2025‑MM‑DD	Article

How to fill quickly: From GSC, export queries for the five URLs → filter top 20 by impressions → add last updated from the DOCX → detect current schema type per URL via view‑source (look for application/ld+json).

2) Measurement — Share‑of‑Answer & Citation Rate

Share‑of‑Answer (SoA): For a fixed gold question set (N=20 → scale to 50), % where an answer surface includes a citation to yaqeeninstitute.org. Report weekly.

Citation rate: Total citations per week across engines (e.g., Perplexity, Bing Web); normalize by #questions probed.

Guardrails: Organic CTR (GSC), engagement/dwell (GA4), CWV Good URLs% (Search Console/CrUX).

3) Prototype — LLM Citation Checker (minimal but runnable)

CLI takes gold_questions.txt → calls a provider → outputs CSV (question,engine,cited,cited_urls,timestamp).

Providers: mock (deterministic fixtures), Bing Web (if reviewer has key). Pluggable for Perplexity/Brave later.

4) GEO/AEO Plan (cluster)

Answer Units (AUs): Add 2–3 AUs per paper (100–180 words each), each with a stable anchor and provenance to a section/footnote.

Schema: Add server‑side ScholarlyArticle + FAQPage. Populate about, mentions (e.g., Attachment theory; Resilience; Authoritative parenting), mainEntity, dateModified, citation (internal cross‑links).

llms.txt (discoverability): Publish AU permalinks and sitemaps; optionally advertise via header.

MCP/agent hook: /api/answers?query= returns AnswerUnit objects for deterministic citations by tools.

5) Experiments (90d)

FAQ + AU anchors (A/B) on 2 papers.
H: AUs improve snippetability and citations.
Metric: SoA ↑, citation rate ↑; guardrail: engagement stable.
Signal window: 2–3 weeks.

Intro refactor (MVT): connect Islamic terms ↔ psychology entities.
H: Improves CTR and average position.
Metric: CTR ↑, avg position ↓ (better); guardrail: bounce stable.

CWV sprint (template‑level A/B): inline critical CSS, lazy‑load images, preconnect fonts.
H: LCP < 2.5s, INP < 200ms; rank stability ↑.

6) 30/60/90 Rollout (with effort/impact)

30d (S/M): Ship AUs + FAQPage on 2 papers; publish llms.txt; run weekly SoA; fix top CWV offenders.

60d (M): Extend AUs/entities to all 5; add AnswerUnit API; add schema parity checks to CI.

90d (M/L): PR/backlink sprint for 3 expert roundups; add Perplexity/Brave provider; SoA dashboard.

Risks/Assumptions: Provider DOM changes; schema regressions; ensure theological accuracy in AUs and cite primary sources.