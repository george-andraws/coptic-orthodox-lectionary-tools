"""Published daily readings may differ by year only for a named reason.

Coptic Reader is the selection authority. The same Coptic date is not one
universal table: a Sunday, feast, paramoun, or fast can replace it. A
difference with the same occasion label, and no Sunday or feast collision,
is unresolved source drift, not an approved variant.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAILY = ROOT / 'packages/lectionary-data/data/daily'

# Reader corrections of these annual identities now cover every shipped
# non-Sunday year. Do not add a pair here to hide a new disagreement.
UNRESOLVED_SAME_OCCASION = set()


def load_years():
    return {
        year: json.loads((DAILY / f'lectionary-{year}.json').read_text())
        for year in (2026, 2027, 2028)
    }


def refs(rows):
    return tuple(
        (row.get('service_section') or '', row.get('slot') or '',
         row.get('display_ref') or row.get('source_ref') or '')
        for row in rows
    )


def gospel(rows, service):
    found = [row for row in rows if row.get('service_section') == service and row.get('slot') == 'Gospel']
    return found[0].get('display_ref') or found[0].get('source_ref')


class YearSundayFeastContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.years = load_years()

    def day(self, date):
        return self.years[int(date[:4])][date]

    def test_kiahk_23_weekday_table_does_not_replace_its_sunday(self):
        weekday = [self.day(date) for date in ('2026-01-01', '2027-01-01')]
        self.assertEqual({gospel(rows, 'Matins') for rows in weekday}, {'Matt 12:1-8'})
        sunday = self.day('2028-01-02')
        self.assertEqual(sunday[0]['occasion'], 'The fourth Sunday of Kiahk')
        self.assertEqual(sunday[0]['annual_sunday'], 'kiahk-4')
        self.assertFalse(sunday[0].get('coptic_date_key'))
        self.assertEqual(gospel(sunday, 'Matins'), 'Mark 3:28-35')
        self.assertNotEqual(gospel(sunday, 'Liturgy'), gospel(weekday[0], 'Liturgy'))

    def test_paramoun_replaces_the_fixed_day_only_in_the_colliding_year(self):
        ordinary = self.day('2026-01-05')
        colliding = self.day('2028-01-06')
        self.assertEqual(ordinary[0]['coptic_date_key'], 'kiahk-27')
        self.assertEqual(colliding[0]['coptic_date_key'], 'kiahk-27')
        self.assertEqual(ordinary[0]['occasion'], 'Kiahk 27')
        self.assertEqual(colliding[0]['occasion'], 'Christmas Paramoune')
        self.assertNotEqual(gospel(ordinary, 'Liturgy'), gospel(colliding, 'Liturgy'))

    def test_last_friday_annunciation_collision_is_not_the_annunciation_table(self):
        collision = self.day('2028-04-07')
        annunciation = self.day('2027-04-07')
        ordinary_last_friday = self.day('2026-04-03')
        self.assertEqual(collision[0]['occasion'], 'Friday of the seventh week of Great Lent')
        self.assertEqual(annunciation[0]['occasion'], 'Annunciation')
        self.assertEqual(
            [row.get('display_ref') or row.get('source_ref') for row in collision if row.get('slot', '').startswith('OT')],
            ['Gen 49:33-50:26', 'Prov 11:27-12:22', 'Isa 66:10-24', 'Job 42:7-17'],
        )
        self.assertEqual(gospel(collision, 'Matins'), gospel(ordinary_last_friday, 'Matins'))
        self.assertNotEqual(gospel(collision, 'Liturgy'), gospel(annunciation, 'Liturgy'))

    def test_same_occasion_disagreements_are_only_the_named_unresolved_set(self):
        groups = {}
        for year, days in self.years.items():
            for date, rows in days.items():
                key = (rows[0].get('coptic_date_key') or '', rows[0].get('occasion') or '')
                groups.setdefault(key, {})[date] = refs(rows)
        found = set()
        for key, by_date in groups.items():
            if len(by_date) > 1 and len(set(by_date.values())) > 1:
                if key == ('', 'Friday of the seventh week of Great Lent'):
                    continue
                found.add(key)
        self.assertEqual(
            found,
            UNRESOLVED_SAME_OCCASION,
            'A new same-occasion reading difference appeared, or a known one was fixed. '
            'Sunday, feast, paramoun, and fast replacements must change the occasion label. '
            'Do not treat one civil year as the reading for every year.',
        )
