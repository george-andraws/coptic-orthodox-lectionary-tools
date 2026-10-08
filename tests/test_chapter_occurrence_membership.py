import csv
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import verify_lectionary_queries as verify


class ChapterOccurrenceMembershipTests(unittest.TestCase):
    def check(self, occurrences):
        base = {'passage':'Exod 4:19-6:13','source_kind':'copticchurch_date',
                'liturgical_place':'Third Week Wednesday','calendar_key':'2026-03-04',
                'gregorian_date':'2026-03-04','coptic_date':'Meshir25',
                'day_title':'Wednesday of Third Week','service_section':'Matins',
                'reading_type':'Prophecy','source_ref':'Exodus 4:19-6:13','url':'primary'}
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            for name, rows in [('reverse_lookup_crosswalk.csv',[base]),
                               ('bible_chapter_lectionary_occurrences.csv',occurrences(base))]:
                keys = list(rows[0])
                with (folder/name).open('w',newline='') as handle:
                    writer=csv.DictWriter(handle,fieldnames=keys);writer.writeheader();writer.writerows(rows)
            with patch.object(verify,'DATA',folder):
                return verify.assert_chapter_occurrence_row_count()

    @staticmethod
    def valid(base):
        return [dict(base,book_abbrev='Exod',chapter=str(chapter),chapter_ref=f'Exod {chapter}') for chapter in [4,5,6]]

    def test_valid_source_derived_membership_not_historical_fixed_count(self):
        self.assertEqual(self.check(self.valid)['chapter_occurrence_rows'],3)

    def test_omitted_chapter_and_duplicate_occurrence_reject(self):
        for change in [lambda rows:rows[:2],lambda rows:rows+[rows[0]]]:
            with self.subTest(change=change),self.assertRaises(AssertionError):
                self.check(lambda base:change(self.valid(base)))

    def test_same_count_wrong_chapter_and_wrong_context_reject(self):
        for field,value in [('chapter','7'),('gregorian_date','2026-03-05'),('source_ref','Exodus 4:1-6:13'),('url','forged')]:
            def corrupt(base):
                rows=self.valid(base);rows[0][field]=value;return rows
            with self.subTest(field=field),self.assertRaises(AssertionError):self.check(corrupt)


if __name__=='__main__':unittest.main()
