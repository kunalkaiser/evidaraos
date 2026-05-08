# Website and Workspace Build Order

## Build After Product Layer

1. Create shared content loaders for module manifests and demo project manifests.
2. Build public website routes using `product/content/website-content.json`.
3. Build solution pages from `product/manifests/*.json`.
4. Build workspace shell from `product/content/workspace-content.json`.
5. Add module cards and demo project cards using fixture-only warning badges.
6. Wire buttons to existing DeerFlow workspace/runtime only where execution is real.
7. Add attribution/legal surfaces that clearly credit DeerFlow as the MIT-licensed runtime.

## First Frontend Slice

- Homepage
- Platform page
- One reusable solution page template
- Governance page
- Workspace module index
- Project/demo cards

## Do Not Build Yet

- Fake live data counters
- Fake customer logos
- Fake regulatory-grade claims
- Fake RWD network coverage
- Fake benchmark results
- Generic DeerFlow skill marketplace pages as product pages
