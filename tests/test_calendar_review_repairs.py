"""Calendar K1-K6 contracts. Set LECTIONARY_CALENDAR_BASELINE for artifact checks."""
import csv
import json
import os
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASELINE = os.environ.get('LECTIONARY_CALENDAR_BASELINE')


def csv_rows(path):
    with path.open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))


@unittest.skipUnless(BASELINE, 'set LECTIONARY_CALENDAR_BASELINE to authenticated 1.3.6 package')
class CalendarArtifactRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        assert BASELINE is not None
        cls.baseline = Path(BASELINE)
        cls.reverse = [json.loads(line) for line in
                       (cls.baseline / 'data/reverse_lectionary_index.jsonl').read_text().splitlines()]
        cls.presentation = csv_rows(ROOT / 'out/design/reverse_lectionary_presentation.csv')
        cls.raw = csv_rows(ROOT / 'out/data/reverse_lookup_crosswalk.csv')
        cls.cycle = csv_rows(ROOT / 'out/data/katameros_cycle_passage_index.csv')
        cls.synaxarium = json.loads((cls.baseline / 'data/synaxarium/synaxarium.json').read_text())
        cls.projected = os.environ.get('CALENDAR_REVIEW_MODE') != 'baseline'
        if cls.projected:
            import build_design_deliverables as design
            from calendar_review_repairs import CalendarReviewRepairs
            def identity(raw):
                registry = design.source_registry_for_key(design.source_key_for(raw))
                return {
                    **design.identity_for(raw['passage'], raw['source_kind'],
                        design.source_contracts.row_envelope(raw),
                        source_transport=design.consumer_source_transport(raw)),
                    'source_locator': design.source_locator_for(raw, registry),
                    'source_title': registry.get('title', ''),
                    'source_edition': registry.get('edition', ''),
                    'authority_tier': registry.get('authority_tier', 'unclassified'),
                }
            cls.repairs = CalendarReviewRepairs(cls.raw, cls.cycle, cls.synaxarium, identity)
            cls.rows = cls.repairs.apply(cls.presentation)
            from calendar_review_repairs import CalendarRuntimeReview
            cls.runtime = CalendarRuntimeReview(cls.repairs, cls.presentation)
        else:
            cls.rows = cls.reverse

    def test_K1_fixed_month_aliases_have_slug_keys(self):
        rows = [r for r in self.rows if r['source_family'] == 'katameros_cycle'
                and r.get('calendar_key', r.get('calendar_keys')) == 'Kiyahk 23']
        # The Sunday and fixed date paths are qualified by source table in projection.
        fixed = [r for r in rows if 'Sunday' not in r.get('day_title', r.get('day_titles', ''))]
        self.assertTrue(fixed)
        self.assertEqual({r.get('coptic_date_key') for r in fixed}, {'kiahk-23'})

    def test_K2_sunday_and_fixed_Bashans3_are_disjoint(self):
        rows = [r for r in self.rows if r.get('calendar_key', r.get('calendar_keys')) == 'Bashans 3'
                and r['source_family'] == 'katameros_cycle' and r['slot'] == 'liturgy_gospel']
        by_ref = {r['display_ref']: r for r in rows}
        self.assertEqual(by_ref['Lk 10:1-20'].get('coptic_date_key'), 'bashans-3')
        self.assertEqual(by_ref['Lk 10:25-37'].get('annual_sunday'), 'bashans-3')
        self.assertFalse(by_ref['Lk 10:25-37'].get('coptic_date_key'))

    def test_K3_every_fixed_key_exists_without_adding_saints(self):
        rows = [r for r in self.rows if r['source_family'] == 'katameros_cycle'
                and r.get('occasion') == 'Abib 1']
        self.assertTrue(rows)
        self.assertTrue(all(r.get('coptic_date_key') in self.synaxarium for r in rows))
        for row in self.rows:
            if row.get('coptic_date_key'):
                self.assertIn(row['coptic_date_key'], self.synaxarium)

    def test_K4_collision_suffix_is_only_removed_from_display(self):
        rows = [r for r in self.rows if 'and the Feast of Entry into Egypt' in r['occasion']]
        self.assertTrue(rows)
        for row in rows:
            self.assertNotIn('and the Feast of Entry into Egypt', row.get('display_label', row['occasion']))
            if self.projected:
                self.assertEqual(row['source_title'], 'copticchurch.net date-resolved readings cache, 2020 to 2035')
                self.assertIn('and the Feast of Entry into Egypt', row['calendar_key'])
                self.assertFalse(row['coptic_date_key'])

    def test_K5_generic_source_rows_have_dates_or_inactive_hold(self):
        rows = [r for r in self.rows if r['occasion'] in ('Great Lent', "St Mary's Fast")
                and (r['source_family'], r['source_kind']) == ('ordinary_date_resolved', 'copticchurch_date')]
        self.assertTrue(rows)
        for row in rows:
            self.assertTrue(row.get('coptic_date_key') or
                (row.get('calendar_review_status') == 'seasonal_label_unresolved' and row.get('active') is False))

    def test_K6_display_labels_use_Coptic_vocabulary(self):
        rows = [r for r in self.rows if any(token in r['occasion'] for token in ('Epiphany', 'Christmas Fast'))]
        self.assertTrue(rows)
        for row in rows:
            label = row.get('display_label', row['occasion'])
            self.assertNotIn('Epiphany', label)
            self.assertNotIn('Christmas Fast', label)

    def test_projection_preserves_source_and_lifecycle(self):
        if not self.projected:
            self.skipTest('projection-only preservation control')
        for old, new in zip(self.presentation, self.rows, strict=True):
            for key, value in old.items():
                self.assertEqual(new[key], value, (key, old['source_locator']))
            self.assertNotIn('commemorations', new)
            self.assertNotIn('saints', new)
        self.assertEqual(self.repairs.apply(self.rows), self.rows)

    def test_wrong_source_identity_cannot_inherit_normalization(self):
        if not self.projected:
            self.skipTest('projection-only source controls')
        target = next(r for r in self.presentation if r['source_family'] == 'katameros_cycle'
                      and r['calendar_key'] == 'Kiyahk 23')
        for key, value in [('source_kind', 'copticchurch_date'), ('source_family', 'ordinary_date_resolved'),
                           ('source_row_id', '0'), ('calendar_key', 'Kiyahk 24'), ('slot', 'wrong_slot'),
                           ('source_locator', 'forged'), ('source_ref', 'Jn 1:1'),
                           ('identity_key', 'rid_forged'), ('spans_json', '[]')]:
            with self.subTest(key=key):
                bad = dict(target, **{key: value})
                with self.assertRaisesRegex(ValueError, 'calendar source'):
                    self.repairs.apply([bad])

    def test_normalized_grouping_never_collapses_different_dates(self):
        if not self.projected:
            self.skipTest('projection-only grouping controls')
        from calendar_review_repairs import calendar_group_key, calendar_output_fields
        rows = [r for r in self.rows if r['occasion'] == 'Great Lent'
                and r['identity_key'] == 'rid_7c1265d433c5721da0c8']
        self.assertEqual({r['coptic_date_key'] for r in rows}, {'amshir-13', 'amshir-17', 'amshir-25'})
        self.assertEqual(len({calendar_group_key(r) for r in rows}), 3)
        with self.assertRaisesRegex(ValueError, 'distinct calendar contexts'):
            calendar_output_fields(rows)
        for row in rows:
            self.assertEqual(calendar_output_fields([row])['coptic_date_key'], row['coptic_date_key'])

    def test_qualified_Nineveh_cycle_is_not_misclassified_as_fixed(self):
        if not self.projected:
            self.skipTest('projection-only existing-source control')
        rows = [r for r in self.rows if r['occasion'] == 'Fast of Nineveh']
        self.assertTrue(rows)
        self.assertEqual({r['source_family'] for r in rows},
                         {'jonah_fast_source_qualified', 'ordinary_date_resolved_no_service_archive'})
        self.assertTrue(all(not r['coptic_date_key'] for r in rows))


    def test_runtime_reverse_preserves_every_raw_row_and_splits_only_metadata(self):
        if not self.projected:
            self.skipTest('runtime projection control')
        from calendar_review_repairs import FIELDS
        result = self.runtime.apply_reverse_rows(self.reverse)
        self.assertEqual(len(result), 12327)
        added = set(FIELDS) | {'calendar_review_source_locators', 'calendar_review_calendar_keys'}
        serialize = lambda r: json.dumps(r, sort_keys=True)
        self.assertEqual({serialize(r) for r in self.reverse},
                         {serialize({k:v for k,v in r.items() if k not in added}) for r in result})
        self.assertEqual(self.runtime.apply_reverse_rows(result), result)
        self.assertFalse(any('Epiphany' in r['display_label'] or 'Christmas Fast' in r['display_label'] or
                             'and the Feast of Entry into Egypt' in r['display_label'] for r in result))
        self.assertTrue(all(not r['coptic_date_key'] for r in result if r['annual_sunday']))
        self.assertTrue(all(r['coptic_date_key'] in self.synaxarium for r in result if r['coptic_date_key']))

    def test_runtime_daily_complete_years_preserve_order_counts_and_raw_fields(self):
        if not self.projected:
            self.skipTest('runtime projection control')
        for year, expected in [(2026,4097), (2027,4088), (2028,4103)]:
            with self.subTest(year=year):
                days = json.loads((self.baseline / f'data/daily/lectionary-{year}.json').read_text())
                result = self.runtime.apply_daily_year(days)
                self.assertEqual(list(result), list(days))
                self.assertEqual(sum(map(len, result.values())), expected)
                for date, old_rows in days.items():
                    for old, new in zip(old_rows, result[date], strict=True):
                        self.assertEqual({k:new[k] for k in old}, old)
                self.assertEqual(self.runtime.apply_daily_year(result), result)

    def test_runtime_reverse_source_context_and_reading_mutations_fail(self):
        if not self.projected:
            self.skipTest('runtime rejection control')
        row = next(r for r in self.reverse if r['source_family'] == 'katameros_cycle'
                   and r['calendar_keys'] == 'Kiyahk 23')
        for field, value in [('identity_key','rid_forged'), ('display_ref','Jn 1:1'),
                             ('source_locator','forged'), ('slot','wrong'), ('occasion','Invented Feast'),
                             ('calendar_keys','Kiyahk 24'), ('source_title','forged'),
                             ('source_kind','copticchurch_date'), ('source_family','ordinary_date_resolved')]:
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, 'calendar source runtime'):
                    self.runtime.apply_reverse_rows([dict(row, **{field:value})])

        with self.assertRaisesRegex(ValueError, 'calendar source runtime family/kind rebound'):
            self.runtime.apply_reverse_rows([dict(row, source_family='unrelated', source_kind='unrelated')])

    def test_runtime_daily_rejects_wrong_outer_date_and_neighbor_slot(self):
        if not self.projected:
            self.skipTest('runtime rejection control')
        days = json.loads((self.baseline / 'data/daily/lectionary-2026.json').read_text())
        row = next(r for r in days['2026-01-01'] if r['source_family'] == 'ordinary_date_resolved')
        self.runtime.apply_daily_year({'2026-01-01':[row]})
        with self.assertRaisesRegex(ValueError, 'calendar source runtime daily tuple/date mismatch'):
            self.runtime.apply_daily_year({'2026-01-02':[row]})
        with self.assertRaisesRegex(ValueError, 'calendar source runtime daily tuple/date mismatch'):
            self.runtime.apply_daily_year({'2026-01-01':[dict(row, slot='wrong')]})

    def test_runtime_multidate_Generic_Lent_has_no_representative_date_guess(self):
        if not self.projected:
            self.skipTest('runtime multi-source control')
        row = next(r for r in self.reverse if r['occasion'] == 'Great Lent'
                   and r['identity_key'] == 'rid_7c1265d433c5721da0c8')
        result = self.runtime.apply_reverse_rows([row])
        self.assertEqual({r['coptic_date_key'] for r in result}, {'amshir-13','amshir-17','amshir-25'})
        self.assertTrue(all(r['calendar_keys'] == 'Great Lent' for r in result))
        self.assertTrue(all(r['source_locator'] == row['source_locator'] for r in result))
        for item in result:
            self.assertTrue(item['calendar_review_source_locators'])
            bad = dict(item, calendar_review_source_locators=['forged'])
            with self.assertRaisesRegex(ValueError, 'runtime evidence drift'):
                self.runtime.apply_reverse_rows([bad])

    def test_runtime_Kiahk23_does_not_choose_between_R2_witnesses(self):
        if not self.projected:
            self.skipTest('runtime R2 noninterference control')
        result = self.runtime.apply_reverse_rows(self.reverse)
        gospels = {r['canonical_mt_ref'] for r in result if r['coptic_date_key'] == 'kiahk-23'
                   and r['slot'] in ('matins_gospel','Gospel') and r['service_section'] in ('matins_gospel','Matins')}
        self.assertTrue({'Matt 12:1-8','Matt 17:1-9'} <= gospels)


class CalendarUnitTests(unittest.TestCase):
    def test_all_reported_month_spellings_have_one_slug(self):
        from calendar_review_repairs import literal_date_key, date_key
        aliases = [('Tout', 'Tut', 'tout'), ('Babah', 'Baba', 'baba'),
                   ('Hator', 'Hatur', 'Hatoor', 'hatour'), ('Kiahk', 'Kiyahk', 'Kiak', 'kiahk'),
                   ('Toba', 'Tubah', 'toba'), ('Amshir', 'Meshir', 'amshir'),
                   ('Baramhat', 'baramhat'), ('Barmuda', 'Baramoudah', 'baramouda'),
                   ('Bashons', 'Bashans', 'bashans'), ('Paona', 'Baunah', 'paona'),
                   ('Abib', 'abib'), ('Mesra', 'Misra', 'mesra'), ('Nasie', 'Al-Nasi', 'Nesi', 'nasie')]
        for month, names in enumerate(aliases, 1):
            for name in names:
                with self.subTest(month=name):
                    self.assertEqual(literal_date_key(name + ' 3'), date_key(month, 3))

    def test_invalid_dates_and_pseudo_month_are_rejected(self):
        from calendar_review_repairs import date_key, literal_date_key
        for month, day in [(0, 1), (14, 5), (1, 0), (1, 31), (13, 7)]:
            with self.subTest(month=month, day=day):
                with self.assertRaisesRegex(ValueError, 'invalid fixed Coptic date'):
                    date_key(month, day)
        self.assertEqual(literal_date_key('Third Sunday of Bashans'), '')
        self.assertEqual(literal_date_key('The Fifth Sunday 5'), '')

    def test_display_changes_do_not_remove_real_Entry_feast(self):
        from calendar_review_repairs import display_label
        self.assertEqual(display_label('Feast of Entry into Egypt'), 'Feast of Entry into Egypt')
        self.assertEqual(display_label('The Feast of Epiphany'), 'The Feast of the Theophany')
        self.assertEqual(display_label('Epiphany Paramoune'), 'Paramoun of the Theophany')
        self.assertEqual(display_label('Hator 16 of Christmas Fast'), 'Hator 16 of Nativity Fast')
        self.assertEqual(display_label('Monday of the seventh week of the holy fifty days and the Feast of Entry into Egypt'),
                         'Monday of the seventh week of the holy fifty days')

    def test_sunday_labels_are_not_date_parser_inputs(self):
        from calendar_review_repairs import sunday_key
        self.assertEqual(sunday_key('Third Sunday of Bashans'), 'bashans-3')
        self.assertEqual(sunday_key('The third Sunday of Hator of Christmas Fast'), 'hatour-3')
        self.assertEqual(sunday_key('Sunday of the third week of Great Lent'), '')

    @staticmethod
    def fixture(**changes):
        # Synthetic source-boundary unit fixture. Actual source tests are above.
        from calendar_review_repairs import CalendarReviewRepairs
        raw = dict(source_family='ordinary_date_resolved', source_kind='copticchurch_date',
                   source_file='synthetic-fixture', source_row_id='1', service_section='Liturgy',
                   service_hour='', reading_slot='', reading_type='Gospel', source_ref='Lk 1:39-56',
                   passage='Lk 1:39-56', raw_ref='Lk 1:39-56', calendar_key='Fast of Nineveh',
                   liturgical_place='Fast of Nineveh', gregorian_date='', coptic_date='',
                   day_title='Fast of Nineveh', service_day='Fast of Nineveh', provenance='unit fixture', url='')
        raw.update(changes)
        identity = dict(identity_key='synthetic-not-a-published-rid', display_ref='Lk 1:39-56',
                        canonical_mt_ref='Lk 1:39-56', canonical_lxx_ref='Lk 1:39-56', spans_json='[]',
                        source_title='unit source', source_edition='unit edition', authority_tier='unit',
                        source_locator=raw['url'])
        row = dict(raw, **identity, occasion=raw['liturgical_place'], slot='Gospel',
                   current_status='historical_witness', active=False)
        repair = CalendarReviewRepairs([raw], [], {'toba-21': {}, 'amshir-13': {}}, lambda r: identity)
        return repair, row

    def test_unresolved_generic_label_is_inactive_without_status_promotion(self):
        repair, row = self.fixture()
        result = repair.apply([row])[0]
        self.assertEqual(result['calendar_review_status'], 'seasonal_label_unresolved')
        self.assertFalse(result['active'])
        self.assertEqual(result['current_status'], 'historical_witness')
        self.assertFalse(result['coptic_date_key'])
        self.assertEqual(repair.apply([result]), [result])

    def test_attestation_year_alone_cannot_create_a_date(self):
        repair, row = self.fixture()
        row['attestation_years'] = '2029'
        self.assertEqual(repair.apply([row])[0]['calendar_review_status'], 'seasonal_label_unresolved')

    def test_locator_date_is_source_backed_and_conflicts_are_rejected(self):
        repair, row = self.fixture(url='https://copticchurch.net/readings?g_year=2029&g_month=01&g_day=29',
                                   gregorian_date='2029-01-29', coptic_date='1745-05-21')
        result = repair.apply([row])[0]
        self.assertEqual(result['coptic_date_key'], 'toba-21')
        self.assertEqual(result['display_label'], 'Toba 21')
        self.assertFalse(result['active'])
        # Contradictory evidence must be rejected even when both raw and target
        # contain the same contradiction, not merely caught as a tuple mutation.
        repair, row = self.fixture(url='https://copticchurch.net/readings?g_year=2029&g_month=01&g_day=29',
                                   gregorian_date='2029-01-29', coptic_date='1745-06-13')
        with self.assertRaisesRegex(ValueError, 'calendar source date evidence disagrees'):
            repair.apply([row])

    def test_missing_synaxarium_key_fails_closed(self):
        repair, row = self.fixture(gregorian_date='2029-01-29', coptic_date='1745-05-21')
        repair.synaxarium = frozenset()
        with self.assertRaisesRegex(ValueError, 'date absent from Synaxarium'):
            repair.apply([row])

    def test_normalized_metadata_cannot_be_rebound_on_replay(self):
        repair, row = self.fixture(gregorian_date='2029-01-29', coptic_date='1745-05-21')
        result = repair.apply([row])[0]
        for field, value in [('coptic_date_key', 'amshir-13'), ('annual_sunday', 'toba-3'),
                             ('display_label', 'Invented Feast'), ('calendar_review_status', 'current')]:
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, 'normalized metadata drift'):
                    repair.apply([dict(result, **{field: value})])


if __name__ == '__main__':
    unittest.main()
