"""The canonical Bright Saturday CSV controls its paired JSONL projection."""
import csv
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import build_lectionary_reference as core


class BrightSaturdayProjectionParity(unittest.TestCase):
    def synchronize(self):
        function = getattr(core, 'synchronize_bright_service_order', None)
        self.assertIsNotNone(function, 'Bright Saturday paired-export synchronization is missing')
        function()

    def test_exact_csv_order_and_cells_survive_jsonl_and_repeat(self):
        original = core.DATA / 'bright_saturday_service_order.csv'
        raw = original.read_bytes()
        with original.open(newline='', encoding='utf-8') as handle:
            expected = list(csv.DictReader(handle))
        self.assertEqual(len(expected), 39)
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp)
            (data / original.name).write_bytes(raw)
            target = data / 'bright_saturday_service_order.jsonl'
            target.write_text('{"obsolete":true}\n')
            with patch.object(core, 'DATA', data):
                self.synchronize()
                self.assertEqual([json.loads(line) for line in target.read_text().splitlines()], expected)
                first = target.read_bytes()
                self.synchronize()
                self.assertEqual(target.read_bytes(), first)
            self.assertEqual((data / original.name).read_bytes(), raw)

    def test_missing_canonical_csv_does_not_resurrect_an_old_jsonl(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp)
            target = data / 'bright_saturday_service_order.jsonl'
            target.write_text('{"obsolete":true}\n')
            with patch.object(core, 'DATA', data):
                function = getattr(core, 'synchronize_bright_service_order', None)
                self.assertIsNotNone(function)
                with self.assertRaises(FileNotFoundError):
                    function()
            self.assertEqual(target.read_text(), '{"obsolete":true}\n')


if __name__ == '__main__':
    unittest.main()
