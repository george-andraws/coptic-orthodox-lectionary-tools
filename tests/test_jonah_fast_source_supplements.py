"""Bounded Jonah repair: source appointments, not package-derived row counts."""
import copy
import datetime as dt
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import build_lectionary_reference as builder
from calendar_resolution import julian_pascha_gregorian
from reading_context_overlays import is_current_source_row

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'sources/coptic-reader/jonah-qualified-2026-10-25'
import jonah_fast_source_supplements as repair


def apply(date, title, rows):
    return repair.apply_jonah_fast_supplements(date, title, rows)


def parsed(date):
    date = dt.date.fromisoformat(date)
    return builder.parse_copticchurch_html((ROOT / 'cache/copticchurch_html' / f'{date}.html').read_text(), date)


def active(rows):
    return [r for r in rows if is_current_source_row(r)]


def identity(rows):
    return [(r['service_section'], r['reading_type'], r['normalized_ref']) for r in active(rows)]


class JonahRepair(unittest.TestCase):
    def test_three_prophecies_and_monday_complete_table(self):
        expected = [('Matins', 'Prophecy', 'Jonah 1:1-17'),
                    ('Matins', 'Psalm', 'Ps 103:1,8'), ('Matins', 'Gospel', 'Matt 7:6-12'),
                    ('Liturgy', 'Pauline Epistle', 'Rom 6:17-23'),
                    ('Liturgy', 'Catholic Epistle', 'Jude 1:1-13'),
                    ('Liturgy', 'Acts of the Apostles', 'Acts 2:38-47'),
                    ('Liturgy', 'Psalm', 'Ps 130:2,4'), ('Liturgy', 'Gospel', 'Matt 12:35-45')]
        for date, ref in [('2026-02-02', 'Jonah 1:1-17'), ('2026-02-03', 'Jonah 2:1-10'), ('2026-02-04', 'Jonah 3:1-4:11')]:
            with self.subTest(date=date):
                item = next(x for x in json.loads((SOURCE / 'input-contexts.json').read_text()) if x['date'] == date)
                meta, before = {'day_title': item['day_title']}, item['rows']
                snapshot = copy.deepcopy(before)
                rows = apply(dt.date.fromisoformat(date), meta['day_title'], before)
                prophecies = [r for r in active(rows) if r['reading_type'] == 'Prophecy']
                self.assertEqual([r['normalized_ref'] for r in prophecies], [ref])
                self.assertEqual(prophecies[0]['source_slot'], 'OT1')
                self.assertEqual(prophecies[0]['source_order'], 1)
                self.assertEqual(before, snapshot)
                self.assertEqual(len(active(rows)), 8)
                self.assertFalse(any(r['service_section'] == 'Vespers' for r in active(rows)))
                if date == '2026-02-02':
                    self.assertEqual(identity(rows), expected)
                else:
                    retained = [r for r in active(rows) if r['reading_type'] not in ('Prophecy', 'Psalm')]
                    self.assertEqual(identity(retained), identity([r for r in before if r['reading_type'] != 'Psalm']))
                self.assertEqual(apply(dt.date.fromisoformat(date), meta['day_title'], rows), rows)

    def test_clause_aligned_psalm_repairs_preserve_unaffected_companions(self):
        expected = {
            '2026-02-03': {'Matins': 'Ps 103:14-15 & Ps 103:9-10', 'Liturgy': 'Ps 85:2-3'},
            '2026-02-04': {'Matins': 'Ps 103:13 & Ps 103:12', 'Liturgy': 'Psalm 32:1  &  Psalm 32:5'},
        }
        for date, services in expected.items():
            item = next(x for x in json.loads((SOURCE / 'input-contexts.json').read_text()) if x['date'] == date)
            result = apply(dt.date.fromisoformat(date), item['day_title'], item['rows'])
            for service, ref in services.items():
                row = next(r for r in active(result) if r['service_section'] == service and r['reading_type'] == 'Psalm')
                self.assertEqual(row['normalized_ref'], ref)
            for row in item['rows']:
                if row['reading_type'] != 'Psalm':
                    preserved = next(r for r in active(result) if r['service_section'] == row['service_section'] and r['reading_type'] == row['reading_type'])
                    self.assertEqual(preserved['raw_ref'], row['raw_ref'])
                    self.assertEqual(preserved['normalized_ref'], row['normalized_ref'])

    def test_collision_partial_input_adds_only_the_seasonal_child(self):
        item = next(x for x in json.loads((SOURCE / 'input-contexts.json').read_text()) if x['date'] == '2022-02-15')
        subset = [r for r in item['rows'] if r['service_section'] == 'Matins'][:1]
        result = apply(dt.date(2022,2,15), item['day_title'], subset)
        self.assertEqual(identity(result)[1:], identity(subset))
        self.assertEqual(apply(dt.date(2022,2,15), item['day_title'], result), result)

    def test_changed_frozen_lifecycle_and_provenance_are_not_accepted(self):
        item = next(x for x in json.loads((SOURCE / 'input-contexts.json').read_text()) if x['date'] == '2026-02-02')
        rows = copy.deepcopy(item['rows'])
        rows[0].pop('superseded_reason')
        with self.assertRaises(ValueError):
            apply(dt.date(2026,2,2), item['day_title'], rows)
        rows = copy.deepcopy(item['rows'])
        rows[0]['correction_source'] = 'forged'
        with self.assertRaises(ValueError):
            apply(dt.date(2026,2,2), item['day_title'], rows)

    def test_parser_integration_is_not_optional(self):
        for date in ['2026-02-02', '2026-02-03', '2026-02-04']:
            meta, rows = parsed(date)
            self.assertEqual(sum(r['reading_type'] == 'Prophecy' for r in active(rows)), 1)
            self.assertEqual(meta['reading_count'], len(rows))

    def test_all_supported_dates_and_only_two_presentation_hybrids(self):
        captured = json.loads((SOURCE / 'input-contexts.json').read_text())
        self.assertEqual(len(captured), 48)
        for item in captured:
            date = dt.date.fromisoformat(item['date'])
            with self.subTest(date=date):
                rows = apply(date, item['day_title'], item['rows'])
                prophecy = [r for r in active(rows) if r['reading_type'] == 'Prophecy']
                self.assertEqual(len(prophecy), 1)
                self.assertEqual((date - julian_pascha_gregorian(date.year)).days, item['offset'])
                self.assertEqual(prophecy[0]['source_verified_date'], { -69:'2026-02-02', -68:'2026-02-03', -67:'2026-02-04'}[item['offset']])
                if item['date'] in ('2022-02-15', '2033-02-15'):
                    self.assertEqual(identity(rows)[1:], identity([r for r in item['rows'] if r['service_section'] != 'Vespers']))
                    self.assertIn('jonah_collision_witness_json', prophecy[0])
                    witnesses = json.loads(prophecy[0]['jonah_collision_witness_json'])
                    self.assertEqual([w['date'] for w in witnesses], [item['date'], item['date']])
                    self.assertIn('Presentation', witnesses[0]['context'])
                    self.assertEqual([w['slot'] for w in witnesses], ['Prophecies', 'Psalm and Gospel'])
                for wrong_title in ('Jonah Fast', 'Entrance into the Temple', 'Great Lent'):
                    if wrong_title != item['day_title']:
                        self.assertEqual(apply(date, wrong_title, item['rows']), item['rows'])
                neighbor = date + dt.timedelta(days=7)
                self.assertEqual(apply(neighbor, item['day_title'], item['rows']), item['rows'])

    def test_partial_date_supplements_without_duplicate_or_lost_history(self):
        meta, rows = parsed('2026-02-02')
        # Raw baseline comes from the frozen parser input, independent of integration.
        rows = json.loads((SOURCE / 'input-contexts.json').read_text())[18]['rows']
        date = dt.date(2026, 2, 2)
        for subset in ([], rows[:1], rows[2:5], rows):
            result = apply(date, 'Fast of Nineveh', subset)
            self.assertEqual(len(active(result)), 8)
            historical = [r for r in result if not is_current_source_row(r)]
            self.assertEqual([r['raw_ref'] for r in historical], [r['raw_ref'] for r in subset])
            for original, history in zip(subset, historical):
                for key, value in original.items():
                    if key not in {'active', 'state', 'status', 'current_status', 'include_in_current_index', 'superseded_reason'}:
                        self.assertEqual(history[key], value)
                if is_current_source_row(original):
                    self.assertIs(history['active'], False)
                    self.assertIs(history['include_in_current_index'], False)
                else:
                    self.assertEqual(history, original)
            self.assertEqual(apply(date, 'Fast of Nineveh', result), result)

    def test_input_wrong_context_state_overlap_and_replay_tamper_fail_closed(self):
        item = next(x for x in json.loads((SOURCE / 'input-contexts.json').read_text()) if x['date'] == '2026-02-03')
        date = dt.date.fromisoformat(item['date'])
        for changes in ({'source_family':'holy_pascha'}, {'source_kind':'pascha_day_hour'},
                        {'source':'untrusted'}, {'gregorian_date':'2026-02-02'},
                        {'weekday':'Wednesday'}, {'day_title':'Great Lent'},
                        {'service_section':'Vespers'}, {'reading_type':'Prophecy'},
                        {'source_slot':'OT1'}, {'active':False}, {'state':'removed'},
                        {'current_status':'historical_witness'}, {'removed_marker':'retired'},
                        {'include_in_current_index':False}, {'candidate_only':True}):
            rows = copy.deepcopy(item['rows']); rows[0].update(changes)
            with self.subTest(changes=changes), self.assertRaises((ValueError, RuntimeError)):
                apply(date, item['day_title'], rows)
        with self.assertRaises((ValueError, RuntimeError)):
            apply(date, item['day_title'], item['rows'] + [item['rows'][0]])
        repaired = apply(date, item['day_title'], item['rows'])
        for key, value in [('normalized_ref','Jonah 2:2-10'), ('source_order',2),
                           ('source_body_sha256','0'*64), ('source_family','holy_pascha'),
                           ('active',False), ('runtime_activation_approved',False)]:
            altered = copy.deepcopy(repaired); altered[0][key] = value
            with self.subTest(key=key), self.assertRaises((ValueError, RuntimeError)):
                apply(date, item['day_title'], altered)

    def test_repaired_payload_cannot_replay_under_an_out_of_scope_outer_context(self):
        item = next(x for x in json.loads((SOURCE / 'input-contexts.json').read_text()) if x['date'] == '2026-02-03')
        result = apply(dt.date(2026,2,3), item['day_title'], item['rows'])
        for date, title in [(dt.date(2026,2,10), item['day_title']), (dt.date(2026,2,3), 'Great Lent')]:
            with self.subTest(date=date, title=title), self.assertRaises(ValueError):
                apply(date, title, result)

    def test_real_date_index_uses_canonical_prophecy_and_retains_inactive_history(self):
        from matins_source_projection import is_dated_matins_candidate
        for day in repair.load_jonah_contract()['days']:
            item = next(x for x in json.loads((SOURCE / 'input-contexts.json').read_text()) if x['date'] == day['date'])
            rows = apply(dt.date.fromisoformat(day['date']), item['day_title'], item['rows'])
            self.assertFalse(any(is_dated_matins_candidate(r) for r in rows))
            indexed = builder.build_date_passage_index(rows)
            prophecy = [r for r in indexed if r['reading_type'] == 'Prophecy']
            self.assertEqual([r['matched_ref'] for r in prophecy], [day['appointments'][0]['normalized_ref']])
            self.assertEqual(prophecy[0]['raw_ref'], day['appointments'][0]['printed_ref'])
            if day['offset'] == -69:
                self.assertFalse(any(r['matched_ref'].startswith('1Cor 3:') for r in indexed))
                history_index = builder.build_date_passage_index(rows, include_inactive=True)
                self.assertTrue(any(r['matched_ref'].startswith('1Cor 3:') and not is_current_source_row(r) for r in history_index))

    def test_source_numbered_body_sequences_and_bible_boundaries_are_literal(self):
        import re
        import xml.etree.ElementTree as ET
        expected = {'2026-02-02': list(range(1,17))+[1], '2026-02-03': list(range(2,11)), '2026-02-04': list(range(1,11))+list(range(1,12))}
        for date, labels in expected.items():
            text = (SOURCE / date / 'Matins/Prophecies.txt').read_text()
            english = [line for line in text.splitlines() if re.match(r'^\d+ [A-Za-z“]', line)]
            self.assertEqual([int(line.split(' ',1)[0]) for line in english], labels)
            if date == '2026-02-02':
                self.assertIn('three days and three nights', english[-1])
                self.assertFalse(any('Jonah prayed' in line for line in english))
            if date == '2026-02-03':
                self.assertIn('Then Jonah prayed', english[0])
                self.assertIn('I cried out', english[0])
                self.assertIn('clefts of mountains', english[3])
                self.assertIn('dry land', english[-1])
        bible = ET.parse(SOURCE / 'bible/Brenton-Jonah-and-Psalms.xml').getroot()
        labels = [v.get('bcv') for v in bible.find("book[@id='JON']").iter('v')]
        self.assertIn('JON.2.11', labels)
        self.assertNotIn('JON.1.17', labels)
        modern = (SOURCE / 'bible/ch1-4-kjv-jonah1.md').read_text()
        self.assertIn('17 ¶ Now the LORD had prepared a great fish', modern)

    def test_source_body_context_manifest_and_approval_tamper(self):
        self.assertIsNotNone(repair)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'source'; shutil.copytree(SOURCE, root)
            contract = repair.load_jonah_contract(root)
            for relative in ['source-contract.json'] + list(contract['fingerprints'])[:4]:
                target = root / relative; original = target.read_bytes()
                target.write_bytes(original + b'\nTAMPER')
                with self.subTest(relative=relative), self.assertRaises((ValueError, RuntimeError)):
                    repair.load_jonah_contract(root)
                target.write_bytes(original)
            with patch.object(repair, 'SOURCE_ROOT', root):
                target = root / '2026-02-03/Matins/Prophecies.txt'
                original = target.read_bytes(); target.write_bytes(original[:-20])
                with self.assertRaises((ValueError, RuntimeError)):
                    apply(dt.date(2026,2,3), "Tuesday of Ninevah's Fast", [])
                target.write_bytes(original)

    def test_exact_source_tables_printed_separate_from_covering_coordinates(self):
        self.assertIsNotNone(repair)
        contract = repair.load_jonah_contract()
        self.assertEqual([len(d['appointments']) for d in contract['days']], [8,8,8])
        self.assertEqual([d['appointments'][0]['printed_ref'] for d in contract['days']], ['Jonah 1:1-2:1','Jonah 2:2-10','Jonah 3:1-4:11'])
        self.assertEqual([d['appointments'][0]['normalized_ref'] for d in contract['days']], ['Jonah 1:1-17','Jonah 2:1-10','Jonah 3:1-4:11'])
        self.assertFalse(contract['old_receipts_grant_activation'])
        self.assertIn('not exact', contract['days'][1]['appointments'][0]['coordinate_note'])
        for day in contract['days']:
            self.assertEqual([r['order'] for r in day['appointments']], list(range(1,9)))
            item = next(x for x in json.loads((SOURCE / 'input-contexts.json').read_text()) if x['date'] == day['date'])
            rows = active(apply(dt.date.fromisoformat(day['date']), item['day_title'], item['rows']))
            self.assertEqual([(r['service_section'],r['reading_type'],r['printed_ref']) for r in rows], [(r['service_section'],r['reading_type'],r['printed_ref']) for r in day['appointments']])


if __name__ == '__main__':
    unittest.main()
