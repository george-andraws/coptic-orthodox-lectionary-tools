# Coptic Reader bundle route and query-helper verification

## Why this matters
This session added two durable improvements to the lectionary workflow:
1. a reliable bundle-first discovery path for Coptic Reader when the Flutter UI is not scrape-friendly
2. a stronger local query-helper normalization layer so full Bible names and shorthand forms both resolve

## Coptic Reader bundle route
Use the app shell under `/app/` as the discovery surface.

Most useful endpoints:
- `/app/main.dart.js`
- `/app/manifest.json`
- `/app/flutter_bootstrap.js`
- `/app/flutter_service_worker.js`

Best current route-discovery surface:
- `main.dart.js`

Less useful than expected in this session:
- `AssetManifest.json`
- `AssetManifest.bin.json`

Those asset-manifest paths currently fell through to the app shell instead of exposing a clean asset index, so do not depend on them as the primary enumeration route.

## Bundle findings worth reusing
The bundle exposed a special-service family selector block with these names:
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

It also exposed metadata field names that matter for future route probing:
- `documentPath`
- `documentTitle`
- `menuHierarchyIds`
- `historyDocumentPaths`

Practical lesson: when the UI is nearly empty, search the bundle for service-family names first, then search outward from metadata structures like `documentPath` rather than clicking around the app.

## Query-helper robustness improvement
The local helper script was improved so passage lookups now normalize common full book names and abbreviations more reliably.

Verified working pairs:
- `John 20` and `Jn 20`
- `Psalm 51` and `Ps 51`
- `John 20:1-18` and `Jn 20:1-18`
- `Psalm 51` and `Ps 51` for cycle lookups
- raw cycle references like `40.5`

The script now also suppresses duplicate output rows.

## Important caveat: distinguish query bug from real data absence
After the helper upgrade:
- `Isa 53`
- `Isaiah 53`

still returned no hits in:
- the date-resolved data
- the cycle data
- the reverse lookup crosswalk
- the reverse lookup summary

Treat that as a real absence in the current local package, not a query-helper failure.

## Reuse rule for future sessions
If a passage lookup fails:
1. try full-name and shorthand forms
2. check whether the reverse lookup crosswalk also lacks it
3. only call it a script bug if the passage clearly exists elsewhere in the local package but the helper misses it
