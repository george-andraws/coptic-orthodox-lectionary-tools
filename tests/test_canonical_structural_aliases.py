import json
from pathlib import Path
import unittest
from scripts import compare_external_sources as comparator

ROOT = Path(__file__).resolve().parents[1]


class CanonicalStructuralAliasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = json.loads((ROOT / 'scripts/package_baselines/pascha_canonical_aliases_1.3.3.json').read_text())['rows']
        cls.policy = json.loads((ROOT / 'sources/lectionary_corrections.json').read_text())

    def compare(self, row, date='2026-04-08'):
        return comparator.contextual_counters([], {date: [dict(row, reading_order=1)]}, 2026, self.policy)

    def test_only_exact_preserved_wednesday_day_aliases_are_structural(self):
        for row in self.rows:
            with self.subTest(ref=row['display_ref']):
                source, package, skipped, dispositions, issues = self.compare(row)
                self.assertEqual((sum(source.values()), sum(package.values()), skipped, issues), (0, 0, 1, []))

    def test_wrong_context_reference_source_state_and_disclosure_cannot_use_alias(self):
        row = self.rows[0]
        changes = [dict(source_family='unverified_reader'), dict(source_kind='unverified'),
                   dict(occasion='Wednesday Eve'), dict(service_hour='Ninth Hour'),
                   dict(display_ref='Ps 41:1'), dict(active=False), dict(source_disclosure='[]'),
                   dict(spans_json='[]'), dict(source_locator='forged')]
        for change in changes:
            with self.subTest(change=change):
                result = self.compare(dict(row, **change))
                self.assertNotEqual((sum(result[1].values()), result[2], result[4]), (0, 1, []))
        result = self.compare(row, '2026-04-07')
        self.assertNotEqual((sum(result[1].values()), result[2], result[4]), (0, 1, []))


if __name__ == '__main__':
    unittest.main()
