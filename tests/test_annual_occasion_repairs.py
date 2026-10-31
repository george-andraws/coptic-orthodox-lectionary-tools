"""Same-occasion annual repairs and the one confirmed Lent Monday Matins table.

Coptic Reader corrections of an annual identity apply to every shipped year of
that occasion except a Sunday or a different feast label. First Monday of
Great Fast Matins is confirmed for 2026-02-16 only. Liturgy, Vespers, other
Lent Mondays, and the 2028-01-08 duplicate Christmas day stay unresolved.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAILY = ROOT / 'packages/lectionary-data/data/daily'
REVERSE = ROOT / 'packages/lectionary-data/data/reverse_lectionary_index.jsonl'


def load_years():
    return {year: json.loads((DAILY / f'lectionary-{year}.json').read_text())
            for year in (2026, 2027, 2028)}


def liturgy(rows, slot):
    found = [row for row in rows if row.get('service_section') == 'Liturgy' and row.get('slot') == slot]
    if len(found) != 1:
        raise AssertionError(slot)
    return found[0].get('display_ref')


def matins(rows, slot):
    return [row.get('display_ref') for row in rows
            if row.get('service_section') == 'Matins' and row.get('slot') == slot]


class AnnualOccasionRepairs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.years = load_years()

    def day(self, date):
        return self.years[int(date[:4])][date]

    def test_annual_identity_corrections_cover_other_non_sunday_years(self):
        self.assertEqual(liturgy(self.day('2027-09-27'), 'Catholic Epistle'), '1Pet 1:25-2:10')
        self.assertEqual(liturgy(self.day('2028-09-26'), 'Catholic Epistle'), '1Pet 1:25-2:10')
        self.assertEqual(liturgy(self.day('2028-09-27'), 'Catholic Epistle'), '1Pet 2:11-25')
        self.assertEqual(liturgy(self.day('2027-09-30'), 'Gospel'), 'Lk 14:25-35')
        self.assertEqual(liturgy(self.day('2028-09-29'), 'Gospel'), 'Lk 14:25-35')
        self.assertEqual(liturgy(self.day('2028-11-06'), 'Gospel'), 'Matt 4:23-5:16')

    def test_sunday_feast_tables_are_not_overwritten_by_the_weekday_repair(self):
        sunday = self.day('2026-09-27')
        self.assertTrue(sunday[0]['occasion'].startswith('Sunday'))
        self.assertEqual(liturgy(sunday, 'Catholic Epistle'), '1Pet 2:1-25')
        baba_sunday = self.day('2027-11-07')
        self.assertEqual(baba_sunday[0]['occasion'], 'The fourth Sunday of Babah')
        self.assertNotEqual(liturgy(baba_sunday, 'Gospel'), 'Matt 4:23-5:16')

    def test_first_monday_matins_uses_the_accepted_reader_table_only_for_2026(self):
        monday = self.day('2026-02-16')
        self.assertEqual(
            [row.get('display_ref') for row in monday if row.get('service_section') == 'Matins'
             and str(row.get('slot', '')).startswith('OT')],
            ['Exod 2:23-3:5', 'Isa 1:2-18'],
        )
        self.assertEqual(matins(monday, 'Psalm'), ['Ps 6:1-2 (LXX Ps 6:2-3)'])
        self.assertEqual(matins(monday, 'Gospel'), ['Matt 12:24-34'])
        self.assertEqual(monday[0]['coptic_date_key'], 'amshir-9')
        # Liturgy was not captured. Do not invent it from the Lent cycle.
        self.assertEqual(liturgy(monday, 'Gospel'), 'Lk 14:25-35')
        self.assertEqual(liturgy(monday, 'Pauline Epistle'), '1Cor 3:1-8')
        later = self.day('2027-03-08')
        self.assertEqual(matins(later, 'Gospel'), ['Jn 1:1-17'])
        self.assertNotIn('Matt 12:24-34', matins(later, 'Gospel'))
        self.assertEqual(later[0]['occasion'], 'Great Lent')

    def test_2028_january_8_christmas_duplicate_remains_unresolved(self):
        seventh = self.day('2028-01-07')
        eighth = self.day('2028-01-08')
        self.assertEqual(seventh[0]['occasion'], 'Christmas')
        self.assertEqual(eighth[0]['occasion'], 'Christmas')
        self.assertEqual(liturgy(eighth, 'Gospel'), 'Matt 2:1-12')

    def test_reverse_index_does_not_keep_the_uncorrected_annual_refs_current(self):
        current = []
        with REVERSE.open() as handle:
            for line in handle:
                row = json.loads(line)
                if row.get('removed_marker'):
                    continue
                if row.get('source_family') != 'ordinary_date_resolved':
                    continue
                key = (row.get('occasion'), row.get('slot'), row.get('display_ref'))
                if key in {
                    ('Tut 16', 'Catholic Epistle', '2Pet 2:1-10'),
                    ('Non-Sunday Tut 17 (Feast of the Cross)', 'Catholic Epistle', '1Pet 2:1-25'),
                    ('Non-Sunday Tut 19 (Feast of the Cross)', 'Gospel', 'Lk 14:25-32'),
                    ('Babah 27', 'Gospel', 'Matt 5:1-16'),
                }:
                    current.append(key)
        self.assertEqual(current, [])

    def test_reader_correction_does_not_rewrite_archived_composite_witness(self):
        try:
            from scripts.apply_review_repairs import _preserve_archived_witnesses
            import composite_followup_repairs as composite
        except ModuleNotFoundError as exc:
            self.skipTest(str(exc))
        groups = composite._witness_groups()
        pair = next(group for group in groups if any(row.get('occasion') == 'Babah 27' and row.get('display_ref') == 'Matt 5:1-16' for row in group))
        before = json.dumps(pair, sort_keys=True)
        projected = _preserve_archived_witnesses(pair, {'2026': {'2026-11-06': []}})
        self.assertEqual(json.dumps(projected, sort_keys=True), before)
        composite.merge_remaining_composites(projected)

    def test_weekday_repair_does_not_clear_authenticated_sunday_occurrence(self):
        try:
            from scripts.apply_review_repairs import _keep_authenticated_occurrence
        except ModuleNotFoundError as exc:
            self.skipTest(str(exc))
        row = None
        with REVERSE.open() as handle:
            for line in handle:
                candidate = json.loads(line)
                if (candidate.get('occasion') == 'Sunday, Tut 19 (Feast of the Cross)'
                        and candidate.get('slot') == 'Gospel'
                        and candidate.get('display_ref') == 'Lk 14:25-32'
                        and not candidate.get('removed_marker')):
                    row = candidate
                    break
        self.assertIsNotNone(row)
        assert row is not None
        restored = _keep_authenticated_occurrence({**row, 'occurs_in_shipped_years': False})
        self.assertIs(restored['occurs_in_shipped_years'], True)
