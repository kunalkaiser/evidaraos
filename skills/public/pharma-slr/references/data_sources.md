# Data Sources

## PubMed

Primary biomedical literature source. Use NCBI E-utilities public endpoints through `scripts/pubmed_search.py`.

## Semantic Scholar

Broad scholarly metadata and citation signal source. Use `scripts/semantic_scholar_search.py`. Public API calls may return HTTP 429 during rate limiting; retry later or reduce result counts.

## Crossref

DOI-centered metadata enrichment source. Use `scripts/crossref_search.py`.

## Optional Sources

Clinical trial registries, regulatory labels, FAERS, and HTA sources may be added later. For this skill version, do not fabricate registry or safety database findings unless a dedicated tool retrieves them.
