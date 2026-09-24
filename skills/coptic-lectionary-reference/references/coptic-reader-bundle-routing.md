---
title: Coptic Reader bundle route map for special services
created: 2026-05-19
---

# Coptic Reader bundle route map for special services

This note captures a useful scraping path for Coptic Reader when the Flutter UI is hard to traverse.

## What to inspect first

The app shell under `/app/` exposes:
- `/app/manifest.json`
- `/app/flutter_bootstrap.js`
- `/app/flutter_service_worker.js`
- `/app/main.dart.js`

## What the bundle reveals

Search `main.dart.js` for service-family names to find internal selector logic. In this session, the bundle surfaced these names in a selector block:
- `Unction`
- `Baptism`
- `Crowning`
- `FuneralPrayer`
- `AltarConsecration`
- `Cornerstone`
- `MyronConsecration`
- `HomeBlessing`
- `FirstProstration`
- `SecondProstration`
- `LiturgyOfTheWaters`
- `ChurchConsecrationSpecialPrayer`

## Practical use

1. Fetch `main.dart.js` directly.
2. Search for the service-family names above.
3. Use the selector block to discover internal document routes or gating logic.
4. Only fall back to browser automation after confirming the route map from the bundle.

## Recovery examples from this session

The bundle-route method helped confirm that the app contains special-service families beyond the ordinary lectionary, including sacramental and consecration documents.

Recovered/verified by direct PDF extraction in parallel:
- Ordinations
- Funeral services
- House blessing

## Guardrail

The bundle is a route map, not proof of page-level reading tables. Treat it as a discovery tool first, then verify the actual readings from the document pages or PDFs before promoting them into the master lectionary tables.
