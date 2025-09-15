# GEO/AEO Plan for the Cluster

## A) Content & Structure (Answer Units)
**Concept:** Each paper exposes a few atomic “AnswerUnit” objects (claim-level Q&A with a stable anchor/permalink) so answer engines can cite precise fragments.

**AnswerUnit shape (example):**
```json
{
  "id": "au-identity-001",
  "question": "How do parents build a Muslim child's identity?",
  "answer": "Anchor daily routines in salah and dhikr, narrate fitrah-based stories, normalize halal role models, and create family rituals around Jumu‘ah and Ramadan. Pair warmth with consistent limits so values are practiced, not only preached.",
  "permalink": "https://yaqeeninstitute.org/read/islamic-parenting-identity#au-identity-001",
  "effective_date": "2025-09-14",
  "provenance": [
    {"type": "citation", "url": "https://yaqeeninstitute.org/read/islamic-parenting-identity#identity-section"},
    {"type": "source",   "url": "https://en.wikipedia.org/wiki/Fitra"}
  ],
  "entities": [
    "Fitrah (Islam)",
    "Muslim identity",
    "Parenting styles",
    "Attachment to Allah"
  ]
}

```html
<script type="application/ld+json">
{ … your ScholarlyArticle JSON-LD … }
</script>
```
```html
<script type="application/ld+json">
{ … your FAQPage JSON-LD … }
</script>
```
