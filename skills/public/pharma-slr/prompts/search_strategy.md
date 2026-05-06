# Search Strategy

Generate transparent biomedical search strategies for PubMed, Semantic Scholar, and Crossref across high_recall, balanced, and high_precision modes.

For every source, return:
- Source name
- Exact query string
- Date filters
- Any study-design or outcome filters
- Rationale for synonyms and Boolean operators
- Expected recall/precision tradeoff
- Concepts included and concepts intentionally excluded

PubMed queries should use Boolean syntax and may include title/abstract terms, MeSH-like concepts, generic names, brand names, indication synonyms, and safety/efficacy outcome terms. Semantic Scholar and Crossref queries should be shorter natural-language metadata queries.
