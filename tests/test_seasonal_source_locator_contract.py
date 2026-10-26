"""Normalized locator contract; literal printed references remain independent.

The installed/authenticated 1.3.5 third-Wednesday table uses Exod/Isa in the
locator's source_ref component while retaining Exodus/Isaiah in raw evidence.
Fixtures below use tracked retained source text, not ignored HTML caches.
"""
import copy
import json
from pathlib import Path
import unittest

from passage_normalization import parse_passage
from build_lectionary_reference import authenticate_recurring_supplement
import verify_design_deliverables as validator

ROOT = Path(__file__).resolve().parents[1]
POLICY = json.loads((ROOT / 'sources/lectionary_corrections.json').read_text())
PRINTED = ['Exodus 4:19-6:13', 'Joel 2:21-27', 'Isaiah 9:9-10:4', 'Job 12:1-14:22']
NORMALIZED = ['Exod 4:19-6:13', 'Joel 2:21-27', 'Isa 9:9-10:4', 'Job 12:1-14:22']


def fixture(*, precedence=False, qualified_rule=None):
    """Declared serialized schema populated from a separately fixed source list."""
    date = '2026-02-18' if precedence else '2026-03-04'
    source_id_prefix = 'lent:2026-02-18' if precedence else 'lent-week3-wednesday'
    printed_refs = ['Isaiah 2:3-11', 'Joel 2:12-26'] if precedence else PRINTED
    normalized_refs = ['Isa 2:3-11', 'Joel 2:12-26'] if precedence else NORMALIZED
    rule = next(r for r in POLICY['recurring_date_supplements'] if r['source_id'] == source_id_prefix)
    if qualified_rule is not None:
        rule = qualified_rule
        authenticate_recurring_supplement(rule, POLICY)
        date = rule['verified_date']
        source_id_prefix = rule['source_id']
        printed_refs = [r['printed_ref'] for r in rule['readings']]
        normalized_refs = [r['normalized_ref'] for r in rule['readings']]
    primary_text = (ROOT / rule['evidence']).read_text()
    if qualified_rule is None:
        if precedence:
            assert all(ref in primary_text for ref in printed_refs)
        else:
            assert [line.strip() for line in primary_text.splitlines() if line.startswith('\t')] == printed_refs
    sources, consumers = [], []
    for order, (printed, normalized) in enumerate(zip(printed_refs, normalized_refs), 1):
        slot = f'OT{order}'
        source_id = f'{source_id_prefix}:{date}:{slot}'
        sources.append(dict(
            source='Coptic Reader verified recurring supplement', gregorian_date=date,
            day_title=rule['day_title'], service_section='Matins', reading_type='Prophecy',
            matched_ref=normalized, raw_ref=printed, source_slot=slot,
            source_order=str(order), correction_source=rule['evidence'],
            source_ref_status='source_supplement', url='https://copticreader.org/app/',
            normalization_warning=f"verified recurring context; evidence={rule['evidence']}; verified_date={rule['verified_date']}; captured_at={rule['captured_at']}"))
        parsed = parse_passage(normalized)
        assert parsed is not None
        spans = [dict(book=parsed.book_abbrev, chapter_start=p.chapter_start,
                      verse_start=p.verse_start, chapter_end=p.chapter_end,
                      verse_end=p.verse_end) for p in parsed.parts]
        consumers.append(dict(
            occasion=rule['day_title'], service_section='Matins', service_hour='',
            slot=slot, slot_type='prophecy', slot_order=order, display_ref=normalized,
            source_kind='copticchurch_date', source_family='coptic_reader_verified_supplement',
            source_file=rule['evidence'], source_row_id=source_id,
            current_status='current_confirmed_coptic_reader', removed_marker='',
            canonical_mt_ref=normalized, spans_json=json.dumps(spans),
            source_disclosure=json.dumps([dict(source_kind='copticchurch_date',
                source_family='coptic_reader_verified_supplement',
                source_file=rule['evidence'], source_row_id=source_id)]),
            source_locator=f"https://copticreader.org/app/; {rule['evidence']}:row {source_id}; source_ref={normalized if rule.get('legacy_projection_compatible') else printed}"))
    return date, sources, consumers


class SeasonalSourceLocatorContract(unittest.TestCase):
    def test_every_authenticated_rule_uses_only_its_declared_locator_protocol(self):
        for rule in POLICY['recurring_date_supplements']:
            with self.subTest(source_id=rule['source_id']):
                date, source, consumer = fixture(qualified_rule=rule)
                validator.verify_seasonal_daily(source, {date: consumer}, POLICY)
                for index, reading in enumerate(rule['readings']):
                    if reading['printed_ref'] == reading['normalized_ref']:
                        continue
                    damaged = copy.deepcopy(consumer)
                    other = reading['printed_ref'] if rule.get('legacy_projection_compatible') else reading['normalized_ref']
                    prefix = damaged[index]['source_locator'].rsplit('; source_ref=', 1)[0]
                    damaged[index]['source_locator'] = prefix + '; source_ref=' + other
                    with self.assertRaisesRegex(AssertionError, 'Wrong seasonal source locator'):
                        validator.verify_seasonal_daily(source, {date: damaged}, POLICY)

    def test_dated_reader_precedence_requires_its_distinct_printed_locator(self):
        date, source, consumer = fixture(precedence=True)
        self.assertTrue(consumer[0]['source_locator'].endswith('source_ref=Isaiah 2:3-11'))
        validator.verify_seasonal_daily(source, {date: consumer}, POLICY)
        consumer[0]['source_locator'] = consumer[0]['source_locator'].replace('source_ref=Isaiah ', 'source_ref=Isa ')
        with self.assertRaisesRegex(AssertionError, 'Wrong seasonal source locator'):
            validator.verify_seasonal_daily(source, {date: consumer}, POLICY)

    def test_normalized_locator_accepts_unchanged_printed_source(self):
        date, source, consumer = fixture()
        self.assertTrue(consumer[0]['source_locator'].endswith('source_ref=Exod 4:19-6:13'))
        self.assertEqual(source[0]['raw_ref'], 'Exodus 4:19-6:13')
        validator.verify_seasonal_daily(source, {date: consumer}, POLICY)

    def test_locator_endpoint_path_date_and_prefix_corruption_rejected(self):
        date, source, consumer = fixture()
        validator.verify_seasonal_daily(source, {date: consumer}, POLICY)
        locator = consumer[0]['source_locator']
        mutants = [locator.replace('Exod 4:19-6:13', 'Exod 4:19-6:12'),
                   locator.replace('source_ref=Exod ', 'source_ref=Exodus '),
                   locator.replace(':row ', '-unrelated.txt:row '),
                   locator.replace(':2026-03-04:', ':2026-03-05:'),
                   locator.replace('https://copticreader.org/app/', 'https://invalid.example/'),
                   'unqualified ' + locator]
        for mutant in mutants:
            damaged = copy.deepcopy(consumer)
            damaged[0]['source_locator'] = mutant
            with self.subTest(locator=mutant), self.assertRaisesRegex(AssertionError, 'Wrong seasonal source locator'):
                validator.verify_seasonal_daily(source, {date: damaged}, POLICY)

    def test_printed_source_reference_cannot_be_replaced_by_normalized_alias(self):
        date, source, consumer = fixture()
        validator.verify_seasonal_daily(source, {date: consumer}, POLICY)
        source[0]['raw_ref'] = 'Exod 4:19-6:13'
        with self.assertRaisesRegex(AssertionError, 'Wrong printed source reference'):
            validator.verify_seasonal_daily(source, {date: consumer}, POLICY)
