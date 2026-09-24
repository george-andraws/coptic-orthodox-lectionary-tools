---
title: Lectionary lookup normalization and Coptic Reader bundle routing
created: 2026-05-20
---

# Lectionary lookup normalization and Coptic Reader bundle routing

## Query normalization findings

From the local verification pass:
- `--date` works directly against the date-resolved cache.
- `--passage` matched shorthand forms already present in the data, especially `Jn 20` and `Ps 51`.
- `--cycle-passage` matched shorthand cycle forms already present in the CSV.
- Full-name queries like `John 20`, `Psalm 51`, and `Isaiah 53` did not hit the current normalized files in this pass.

### Practical implication
Prefer the data's shorthand forms when verifying or debugging the lookup script:
- `Jn 20`
- `Ps 51`
- other normalized refs already present in the CSVs

If a full-name query needs to work for a user-facing helper, extend the matcher rather than assuming the data will naturally normalize every Bible naming convention.

## Coptic Reader bundle routing clues

The Flutter web shell exposes:
- `/app/manifest.json`
- `/app/flutter_bootstrap.js`
- `/app/flutter_service_worker.js`
- `/app/main.dart.js`

The bundle is useful as a route map because it includes:
- service-family gate `b5u()`
- document metadata names such as `documentPath`, `documentTitle`, `menuHierarchyIds`, and `historyDocumentPaths`

### Service-family names surfaced in the bundle
- Unction
- Baptism
- Crowning
- FuneralPrayer
- AltarConsecration
- Cornerstone
- MyronConsecration
- HomeBlessing
- FirstProstration
- SecondProstration
- LiturgyOfTheWaters
- ChurchConsecrationSpecialPrayer

### Bundle discovery rule
Treat the bundle as a discovery tool, not proof of final readings. Use it to find the internal page or route first, then confirm the actual readings from the page view or a PDF source.
