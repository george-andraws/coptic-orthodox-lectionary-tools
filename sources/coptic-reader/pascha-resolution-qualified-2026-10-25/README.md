# Retained Pascha resolution evidence

This directory retains byte-identical copies of **three existing rendered-text
captures**, their document screenshots, and available selected-home, picker,
selected-date-panel and menu companions. The raw captures were not edited,
recaptured, translated or renumbered. The manifest records original paths as
provenance labels only; portable authentication never opens those locations.

`2026-10-25` is the retention label, **not a capture timestamp**. Selected civil
dates are preserved literally in the home/picker witnesses. The Hosanna selected
date panel separately displays its original live-clock label (October 7, 2026).
No app version or capture timestamp is inferred; those manifest fields are null.
This retention is not fresh app verification, ecclesiastical approval, new
appointment approval, or approval to broaden the existing repairs.

## Exact scope

- **`good_friday_twelfth`** — document title `Great Friday (The Twelfth Hour)`;
  selected home says Great Friday, Parmoute 2, 1742, April 10, 2026. Printed
  `Lamentations 3:1-66`; the complete retained hour has no Jonah reading. This
  supports the already-decided Reader-priority resolution, without rewriting
  Katameros Jonah 1:10-2:8 or Ottawa Jonah 1:10-2:7 historical witnesses.
- **`hosanna_sunday_day_ninth`** — document title `Hosanna Sunday (The Ninth
  Hour)`; selected home says Hosanna Sunday, Paremhotep 27, 1742, April 5, 2026.
  Sunday Day menu offers Ninth/Eleventh Hours; Sunday menu separately lists
  Monday Eve and General Funeral Prayer. The printed prophecy is
  `Lamentations 1:1-4`, **not 1:1-5**. Zephaniah 3:11-20 is retained as source
  context, not a newly approved addition.
- **`bright_saturday_matins`** — actual document title `Offering of Morning
  Incense`; selected home says Joyous Saturday, Parmoute 3, 1742, April 11, 2026,
  and the Pascha Saturday menu offers Matins. The service Pauline heading and
  numbered body are **1 Corinthians 5:7-13, not 1 Corinthians 1:1-19**. Earlier
  Ephesians 4:1-5 belongs to the morning prayer context. Isaiah 55:2-13, printed
  Psalm 88:4-5; 44:23,26; 126:2-3 and Matthew 27:62-66 are bound as context;
  no additional appointments or coordinate conversion are authorized. This
  document does **not** authenticate Praises, Susanna, Manasseh, Azariah or a
  Jeremiah heading/body repair.

## Guard interface

`pascha_resolution_evidence.authenticate_pascha_evidence(key) -> dict` accepts
only the three exact strings above, with no caller-supplied path or metadata.
It authenticates the hash-pinned manifest, the selected complete document and
all its retained companions on every call. It rejects changed/missing evidence,
manifest rebinding, normalized/escaping paths, symlinks and nonliteral keys.

The fresh return value includes `path`, `sha256`, `locator`, `manifest_path`,
`manifest_sha256`, `service_day`, `service_hour`, `document_title`,
`selected_context`, `navigation`, `readings`, `companions`, and concrete
`qualification_notes`. Paths are repository-relative; reading line numbers are
one-based and body hashes cover newline-joined decoded source lines (the
separate full-capture hash authenticates original bytes). `original_capture_path`
remains a historical provenance label, not a dependency or public portable path.

This helper authenticates evidence, **not arbitrary caller rows**. Consumers must
apply their own exact context/kind/reference allowlist before status resolution
or supplementation and transport these qualifications through provenance and
public disclosure. A correct forward guard does not prove downstream transport;
that integration is outside this helper's scope.
