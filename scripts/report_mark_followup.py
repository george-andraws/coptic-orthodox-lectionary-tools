#!/usr/bin/env python3
"""Render L1-L10 review documents from authenticated predecessor and real output."""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import mark_followup_repairs as m


def table(headers, rows):
    def cell(v):
        return str(v if v is not None else '').replace('|', '&#124;').replace('\n', '<br>')
    return '\n'.join(['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---'] * len(headers)) + ' |'] + ['| ' + ' | '.join(cell(v) for v in row) + ' |' for row in rows]) + '\n'


def witnesses(rows):
    return table(['Identity', 'Source family / kind', 'Raw occasion / calendar', 'Hour / slot', 'Source reference', 'Status / removal', 'Locator'], [
        [r['identity_key'], r['source_family'] + ' / ' + r['source_kind'], r['occasion'] + ' / ' + r.get('calendar_keys', ''), r.get('service_hour', '') + ' / ' + r['slot'], r['display_ref'], r.get('current_status', '') + ' / ' + r.get('removed_marker', ''), r.get('source_locator', '')] for r in rows])


def printed(rows):
    return table(['Raw day', 'Hour', 'Slot', 'Literal printed reference', 'Normalized reference', 'Text line / printed page'], [
        [r['day'], r['hour'], r['reading_type'], r['raw_ref'], r['normalized_ref'], r['source_file'] + ':' + r['source_line'] + ' / ' + r['source_page']] for r in rows])


def reader(documents):
    rows = []
    for doc in documents:
        for r in doc['readings']:
            rows.append([doc['document_title'], doc.get('service', ''), doc.get('hour', ''), r['printed_ref'], doc['file'] + ':' + str(r['heading_line']), doc['sha256']])
    return table(['Retained Reader document', 'Service', 'Hour', 'Literal heading reference', 'File / heading line', 'SHA-256'], rows) if rows else 'No retained document is indexed for this group in this source oracle. This is a scoped source observation, not proof of universal absence.\n'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', required=True, type=Path)
    args = parser.parse_args()
    baseline = args.baseline.resolve()
    oracle = m.source_oracle()
    for name, digest in oracle['scope']['baseline_registry_authentication']['files'].items():
        target = baseline / name.removeprefix('package/')
        if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            raise ValueError('Published predecessor member mismatch: ' + name)
    target = ROOT / 'packages/lectionary-data'
    old = {y: json.loads((baseline / f'data/daily/lectionary-{y}.json').read_text()) for y in [2026, 2027, 2028]}
    new = {y: json.loads((target / f'data/daily/lectionary-{y}.json').read_text()) for y in old}
    reverse = [json.loads(l) for l in (target / 'data/reverse_lectionary_index.jsonl').read_text().splitlines()]
    archive = ROOT / 'docs/reviews/mark-followup-1.3.8'
    archive.mkdir(parents=True, exist_ok=True)
    # Full occurrence tables, not only changed readings or selected Gospels.
    pascha = []
    for phase, years in [('1.3.7 before', old), ('1.3.8 candidate after', new)]:
        for date, rows in years[2026].items():
            if '2026-04-05' <= date <= '2026-04-10':
                for r in rows:
                    pascha.append([phase, date, r.get('pascha_service') or r['occasion'], r.get('service_hour') or r['service_section'], r['slot'], r['display_ref'], r['current_status'], r.get('display_label', ''), r['identity_key']])
    (archive / 'pascha-2026-before-after.md').write_text('# Complete 2026 Palm Sunday through Good Friday daily arrays\n\nEvery serialized daily appointment is included in physical service order, including ordinary services alongside Pascha hour blocks. Held rows absent from the after projection remain in the reverse archive. The label is the actual field value, not a reconstructed heading.\n\n' + table(['Projection', 'Civil date', 'Service', 'Hour / section', 'Slot', 'Reading', 'Status', 'display_label', 'Identity'], pascha))
    counts = []
    for year in old:
        before = [r for a in old[year].values() for r in a]
        after = [r for a in new[year].values() for r in a]
        counts.append([year, len(old[year]), len(new[year]), len(before), len(after), len(after)-len(before), sum(r['current_status'].startswith('pending_') for r in before), sum(r['current_status'].startswith('pending_') for r in after)])
    issue_rows = []
    for r in reverse:
        if r.get('mark_followup_note'):
            issue_rows.append({k: r.get(k, '') for k in ('identity_key', 'source_family', 'source_kind', 'occasion', 'calendar_keys', 'service_section', 'service_hour', 'slot', 'display_ref', 'current_status', 'active', 'evidence_status', 'source_locator', 'mark_followup_note')})
    (archive / 'identities-and-dispositions.json').write_text(json.dumps(issue_rows, ensure_ascii=False, indent=2) + '\n')
    # Check sheet includes literal per-source witnesses, not inferred replacements.
    sheet = ['# Coptic Reader check sheet: 1.3.8', '',
        'Current practice is governed by saved Coptic Reader evidence. Printed books and public caches are separate witnesses. A working row, repeated future date or populated hour is not fresh confirmation. Source text, raw calendar keys and locators remain literal. All questions below remain open unless a bounded retained capture is explicitly identified.', '',
        '## Top priority: L3 Eve of Wednesday missing Reader hours', '',
        'Third, Ninth and Eleventh Hours remain outside current daily coverage. Third and Ninth have four explicit inactive candidates alongside their original historical witnesses. The Eleventh printed witness does exist: Wisdom 7:24-30, Psalm 57:1 and John 11:55-57. It does not authorize current activation or a transfer from the differently qualified Eve of Thursday. First Hour Reader Ezekiel 22:23-29 differs from Ottawa 22:23-28. Sixth Hour has retained Reader support.', '',
        printed(oracle['L3']['complete_printed_wednesday_eve_source_rows']),
        '## L2: every Tuesday day hour', '',
        'Six explicitly reported working appointments are held. Sixth Hour and the other companions are preserved. The broader Q-L3 remains unanswered. Saved Reader Third Hour evidence gives a different full table; it is reported here without adding replacements under the explicit hold instruction.', '',
        witnesses(oracle['L2']['all_tuesday_baseline_witnesses']),
        table(['Raw CSV physical line', 'Hour', 'Source', 'Slot', 'Literal refs cell'], [[r['physical_csv_line'], r['hour'], r['source'], r['slot'], r['refs']] for r in oracle['L2']['raw_curated_source_rows']]),
        reader([oracle['L2']['retained_reader_third_hour']]),
        '## L1: Mesra 7 Vespers', '', oracle['L1']['finding'], '', witnesses(oracle['L1']['selectors']),
        'Saved cache heading `Mk 14:-39` is at line 138; its body continues through the whole chapter. Separate cycle Mark 14:3-9 is not a source-backed parsing correction of that cache. Hold the bad dated appointment only.', '',
        '## L6: Hator 11 conflict, Q-L1', '', witnesses(oracle['L6']['conflict_selectors']),
        'Matthew 10:24-33 and Mark 14:3-9 remain conflicting. The catalog has three commemorations, not a reading-to-saint rule. No Gospel is selected by a commemorated name.', '',
        '## L7: service book', '', witnesses(oracle['L7']['package_selectors']),
        'The requested `unverified_service_book` annotation qualifies these service-book claims, not the existence of retained Reader evidence. All six numeric package targets already have saved Reader witnesses. Their statuses, numeric spans and disclosures are preserved.', '',
        table(['Literal Reader heading', 'Navigation', 'Subservice', 'Saved file / line', 'SHA-256'], [[r['printed_ref'], ' > '.join(r['navigation']), r['section'], r['source_file'] + ':' + str(r['line']), r['raw_text_sha256']] for r in oracle['L7']['retained_reader_evidence']]),
        'The separate older inactive Myron lead has `raw_ref=Mark 16`, variant `consecration_day`, section `matins`. The retained page-35 visual receipt transcribes `إنجيل باكر (مرقس أصحاح ١٦ كله)`: Matins Gospel, Mark chapter 16 entirely. This is not an unknown endpoint, a fresh image inspection, an additional active Gospel or permission to reactivate the superseded raw row.', '',
        '## L8: Tout 23, Q-L2', '', witnesses(oracle['L8']['selectors']),
        'The Marian-looking set is preserved exactly. The date-only Synaxarium catalog is not used to choose or replace a reading. Q-L2 remains unanswered.', '',
        '## L9: pending Psalm accounting', '',
        'The public predicate intentionally supports pending Psalm alignment states. Only the three stale legacy Wednesday Pascha appointments per year are excluded with `active: false`; their status is unchanged. The source-only Kiahk/Bright appointments and held Sunday source-coordinate rows remain current under exact source/date/disclosure allowances. Numeric source spans do not certify canonical MT/LXX coordinates.', '',
        table(['Year', 'Civil date', 'Identity', 'Service / slot', 'Printed reference', 'Disposition', 'Canonical MT / LXX'], [[r['year'], r['date'], r['selector']['identity_key'], r['selector']['service_section'] + ' / ' + r['selector']['slot'], r['selector']['display_ref'], r['lane'], r['canonical_mt_ref'] + ' / ' + r['canonical_lxx_ref']] for r in oracle['L9']['pending_occurrence_oracle']]),
        '## L10: all requested service and hour groups', '',
        'The following 21 groups retain each source independently. Saved Reader text below is retained evidence, not a new status promotion or fresh app visit. A missing indexed capture is not replaced from memory. Same-day Great Thursday Third/Ninth Matthew 26:17-19 remains the prior H5 question; all four Friday Gospel appointments remain separate.', '']
    for group in oracle['L10']['service_hour_groups']:
        sheet.extend(['### ' + m.SERVICE_LABELS[group['service']] + ': ' + group['hour'], '', '#### Packaged predecessor witnesses', '', witnesses(group['baseline_package_witnesses']), '#### Printed Ottawa witness', '', printed(group['printed_source_rows']), '#### Retained Reader documents', '', reader(group['retained_reader_documents'])])
    sheet.extend(['## Retained earlier check inventory', '', 'The [1.3.7 detailed inventory](docs/reviews/holy-week-review-2026-10-29/coptic-reader-check-sheet.md) remains historical evidence with 481 declared baseline appointments. H1-H8, R2 Kiahk weekday/Sunday evidence, R5 Amshir 10 identity questions and descriptive R3 seasonal qualifications remain governed by that release and its source contracts. This follow-up does not reopen them or treat the older count as a new current total.', ''])
    (ROOT / 'coptic-reader-check-sheet.md').write_text('\n'.join(sheet))
    summaries = [
        ('L1', 'Yes', 'Hold one reverse witness and its two dated occurrences; malformed source heading does not establish 3-9.'),
        ('L2', 'Yes', 'Hold six exact working Tuesday appointments, not Monday or Tuesday Sixth Hour. No replacement added despite separately retained Third Hour evidence.'),
        ('L3', 'Yes', 'Add four inactive candidates beside four preserved historical witnesses. Third/Ninth/Eleventh remain Reader coverage holds; printed Eleventh exists.'),
        ('L4', 'Yes', 'Every Pascha display label is source-qualified and Coptic-form; Palm/Hosanna and Bright Saturday aliases normalize. Q1 remains unanswered, so the recommended Coptic form is used.'),
        ('L5', 'Yes, count corrected', '30 records carry 60 Kiyank tokens, not 60 records; normalize 30 display labels. Normalize 19 Ninevah display labels. Raw text retained.'),
        ('L6', 'Yes', 'Both Hator 11 Vespers witnesses carry conflict metadata. No selection or saint association; Q-L1 open.'),
        ('L7', 'Rows yes; absent evidence no', 'Six requested annotations, with existing retained Reader evidence and statuses preserved. Old inactive Mark 16 lead means the whole chapter.'),
        ('L8', 'Yes', 'No reading, span, status or catalog change. Q-L2 open.'),
        ('L9', 'Yes, conditional narrowing', 'Exclude exactly three stale legacy Psalms per year without changing status. Preserve supported pending counts 7/22/7, including numeric Sunday source coordinates.'),
        ('L10', 'Requested inventory supplied', 'All 21 service/hour groups, 176 predecessor source witnesses, literal printed tables and indexed retained Reader captures are on the full check sheet. No blanket promotions.')]
    report = ['# Lectionary 1.3.8 follow-up report', '', '## Scope and provenance', '',
        'Local Mark candidate only. No commit, push, npm publication, website change or final clean-source acceptance is performed by this implementation worker. The parent owns the expanded integration and must follow George\'s latest authorization. Concurrent additional source workers make these Mark-only runs diagnostic rather than final whole-candidate acceptance. Candidate `meta.json` truthfully records `source_tree_dirty: true` and the clean predecessor commit, not an invented final source revision.', '',
        'Authenticated predecessor: `@andraws/lectionary-data@1.3.7`, registry `https://registry.npmjs.org`, resolved latest at `' + oracle['scope']['baseline_registry_authentication']['resolved_at'] + '`. Integrity: `' + oracle['scope']['baseline_registry_authentication']['integrity'] + '`. All 11 members were reauthenticated before this report was rendered. Reverse SHA-256: `' + oracle['scope']['baseline_registry_authentication']['files']['package/data/reverse_lectionary_index.jsonl'] + '`.', '',
        'The compressed frozen predecessor subset is `' + m.FIXTURE + '`, SHA-256 `' + m.FIXTURE_SHA256 + '`. The independent pre-candidate source oracle is `' + m.ORACLE + '`, SHA-256 `' + m.ORACLE_SHA256 + '`. It is source acceptance evidence, not candidate approval. No candidate-generated membership ledger or historical fixture-policy renewal is used.', '',
        '## L1-L10 dispositions', '', table(['ID', 'Reproduced', 'Action or hold'], summaries),
        '### Exact affected occurrence identities', '',
        'The following table contains the complete source-qualified metadata/hold target set, including the four new L3 candidates. Identity keys alone are not unique occurrence selectors. The machine-readable companion is [identities-and-dispositions.json](reviews/mark-followup-1.3.8/identities-and-dispositions.json). L4/L5 apply display-only to their complete source cohorts; L8 exact unchanged selectors and all L10 baseline identities are preserved in the check sheet and independent oracle.', '', witnesses([r for r in reverse if r.get('mark_followup_note')]),
        '## Daily counts against the published predecessor', '', table(['Year', 'Dates before', 'Dates after', 'Readings before', 'Readings after', 'Delta', 'Pending before', 'Pending after'], counts),
        'Counting unit: every unfiltered serialized appointment row in every daily date array. All civil dates remain present. L1 removes one row in 2026 and one in 2027; L2 removes six per year; L9 removes three per year. No other reading-count change is authorized. Projection-active and publicly current reverse populations retain their distinct metadata semantics.', '',
        '## Full 2026 Pascha before and after', '',
        '[Complete table: Palm Sunday through Good Friday, every daily row](reviews/mark-followup-1.3.8/pascha-2026-before-after.md). Columns include actual service, hour, slot, reading, status and `display_label` in physical array order. Neither matching totals nor a populated date is presented as complete Reader service verification.', '',
        '## Complete check sheet and open questions', '',
        'The [full check sheet](../coptic-reader-check-sheet.md) contains all L1-L10 follow-up targets, every Tuesday hour, all three missing Reader Eve-of-Wednesday hours with actual printed evidence, service-book witnesses and all 21 L10 service/hour groups. [Q-L1, Q-L2 and Q-L3](../open_questions_for_george.md) remain unanswered. Q1 has no new answer; Coptic eve labels use its recommended default.', '',
        '## Contracts and tests', '',
        'The source-owned runtime overlay runs after the existing H/K/R repairs, without changing the historical design membership gate. Holds have explicit boolean inactivity so unknown-status refusal is not weakened. Raw source title, locator, calendar keys, coordinates, composite spans and source disclosures are retained. New candidates do not remove the old historical rows. Exact emitted-row qualification rejects evidence/context rebinding, coordinate edits, type substitutions and unauthorized reactivation. Whole-date comparison first authenticates the independently projected successor arrays and only then replays the historical cached-source comparator against pinned predecessor rows.', '',
        'The five-hour check accounts separately for 19 current eve hours and six explicitly held Reader gaps across five eves. It does not claim 25 current hours. The duplicate-set check compares complete non-Psalm day-hour Gospel/prophecy sets across distinct days, not an isolated shared Gospel or the same-day H5 repetition. The pending allowance binds all 36 retained occurrences to exact date/source/coordinates and disclosure hash; no arbitrary pending status is admitted.', '',
        'Observed RED: the seven new package tests failed against the published predecessor; retained log [RED-node.txt](reviews/mark-followup-1.3.8/RED-node.txt) records child exit 1. Focused Python tests include complete valid controls and source, context, coordinate, lifecycle, type, omission, addition and order corruptions. Actual builder/test commands and fresh results are recorded in [verification.md](reviews/mark-followup-1.3.8/verification.md). Full final acceptance belongs to the parent after source freeze.', '',
        '## Clean-source finish for the parent', '',
        '1. Review all source/generated diffs and run the complete mixed Python and full Node inventories in the uv Python 3.11 dependency environment. Preserve the historic fixture/policy pairings; do not refresh a ledger from candidate output.',
        '2. Make the one authorized repository commit with the approved source and candidate data. Do not claim the dirty candidate metadata identifies the final source. A second artifact-only commit is not required by this handoff.',
        '3. Clone that committed source into a second fresh release checkout. Verify `git status --short` is empty before running `node scripts/build_npm_package.mjs` through the same uv environment. The generated metadata must naturally record that committed revision and `source_tree_dirty: false`; never force the flag or hash.',
        '4. Compare every packed non-provenance member to the reviewed candidate; only expected clean-provenance `meta.json` differences are permitted. Run strict integrity, cached-source comparison, exact npm pack/install tests and artifact hash checks in the release clone. Parent owns final integrated review and any currently authorized repository, registry or site work. Never pin a nonexistent registry 1.3.8; keep a local candidate isolated until final integrated acceptance and the parent\'s release decision.',
        '5. If adding final receipts changes the source commit, rebuild from that final committed source rather than editing metadata. The release tarball may remain uncommitted as explicitly coordinated by the parent.', '']
    (ROOT / 'docs/LECTIONARY_1_3_8_RELEASE.md').write_text('\n'.join(report))
    print(json.dumps(dict(daily_counts=counts, pascha_table_rows=len(pascha), affected_reverse_rows=len(issue_rows), l10_groups=len(oracle['L10']['service_hour_groups'])), indent=2))


if __name__ == '__main__':
    main()
