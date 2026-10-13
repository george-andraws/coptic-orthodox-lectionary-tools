import importlib.util
import json
import os
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('canonical_integrity', os.environ.get('LECTIONARY_VERIFIER_UNDER_TEST', ROOT / 'scripts/verify_package_integrity.py'))
assert spec is not None and spec.loader is not None
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class QualifiedHeldPsalmTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rows = [json.loads(line) for line in (ROOT / 'out/design/reverse_lectionary_index.jsonl').read_text().splitlines()]
        cls.held = next(row for row in rows if row['source_family'] == 'coptic_reader_verified_sunday_policy'
                        and row['occasion'] == 'Third Sunday of Meshir' and row['slot_type'] == 'psalm')
        cls.other = next(row for row in rows if row['source_family'] == 'ordinary_date_resolved'
                         and row['occasion'] == 'The third Sunday of Amshir' and row['canonical_mt_ref'] == 'Ps 89:1')

    def test_authenticated_alignment_hold_is_not_numeric_source_priority_conflict(self):
        ordinary = dict(self.other, occasion='Third Sunday of Meshir', calendar_keys='Third Sunday of Meshir')
        self.assertEqual(verifier.detect_context_passage_conflicts([self.held, ordinary]), [])

    def test_disclosure_loss_coordinate_promotion_and_forged_hold_are_rejected(self):
        for field, value in [('source_disclosure', '[]'), ('canonical_lxx_ref', 'Ps 88:1'), ('source_kind', 'unverified')]:
            with self.subTest(field=field), self.assertRaises(ValueError):
                verifier.detect_context_passage_conflicts([dict(self.held, **{field: value})])
        forged = dict(self.other, source_family='coptic_reader_verified_sunday_policy',
                      spans_json=self.held['spans_json'])
        with self.assertRaises(ValueError):
            verifier.detect_context_passage_conflicts([forged])


if __name__ == '__main__':
    unittest.main()
