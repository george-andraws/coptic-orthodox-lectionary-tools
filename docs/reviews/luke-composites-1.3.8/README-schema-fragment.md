## Provenance and composite evidence (1.3.8 schema fragment)

`provenance` is a reader-facing source name, plain text of at most 300 characters. It is not an authentication envelope. Source authority, current status, coordinate qualifications and literal source locators remain separate fields.

When a former provenance value contains structured evidence or exceeds the display limit, two additive public fields preserve that evidence:

- `provenance_format`: the literal string `lectionary_provenance_v1`.
- `provenance_evidence_json`: a serialized JSON object in exactly one of these two forms:

```json
{
  "schema": "lectionary_provenance_v1",
  "legacy_provenance": "<complete original serialized evidence or source qualification>"
}
```

For an R4 composite, fragment records belong in `composite_fragments_json`, not in `provenance` or duplicated in the evidence envelope:

```json
{
  "schema": "lectionary_provenance_v1",
  "composite_provenance_prefix": "<original source prefix>; R4 composite_fragments="
}
```

The latter form reconstructs the exact predecessor evidence by concatenating its prefix with the complete `composite_fragments_json` cell. It requires that companion cell. Duplicate members, extra envelope fields, missing evidence, unknown schemas and nonstring payloads are invalid.

`composite_fragments_json` is an ordered array of complete source fragment records. Ordered `spans_json` describes one composite appointment. The public key `original_source_row` retains source snapshots formerly held in an internal temporary-key spelling, including nested serialized snapshots. The internal validator adapter restores the prior spelling without dropping evidence. Source titles, locators, raw calendar keys, source identities, lifecycle fields and primary-source qualifications are retained.

The LK5 `composite_review` value `LK5_archived_source_cell_v1` identifies the bounded inactive-appointment projection. These composites stay inactive; their complete original split witnesses remain in their fragment arrays and unchanged in raw source data. They are not additions to current daily readings.

**Consumer migration:** these additive JSON cells transport evidence; they do not grant trust. Decode with `restore_public_row(s)` before existing exact source/disclosure/lifecycle checks. For historical reverse membership or retirement validation, `legacy_validation_rows` also authenticates the bounded LK5 composite and restores its original inactive witness records. Never replace membership/source checks with successful decoding, build new membership oracles from candidate rows, or present historical validator expansions as current daily appointments.
