"""Candidate Matins integration: independent raw corpus oracle, real BRef APIs."""
import copy
import datetime as dt
import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import build_lectionary_reference as bref
FIXTURE = Path(__file__).resolve().parent
CORPUS = json.loads((FIXTURE / 'accepted-source-corpus.json').read_text())

def context(record):
    return {key: copy.deepcopy(record[key]) for key in (
        'civil_date', 'occasion_key', 'actual_occasion', 'actual_home_line',
        'numeric_coptic_calendar_crosscheck', 'pascha_offset_days', 'weekday', 'service')}

def old_rows(date):
    return [dict(source='copticchurch.net daily scrape', gregorian_date=date,
                 weekday=dt.date.fromisoformat(date).strftime('%A'), day_title='Original day label',
                 service_section=service, reading_type=kind, raw_ref=ref,
                 normalized_ref=ref, parse_status='ok', normalization_warning='', url='original')
            for service, kind, ref in [('Vespers', 'Gospel', 'John 1:1-5'),
                                      ('Matins', 'Prophecy', 'Genesis 1:1-5'),
                                      ('Matins', 'Psalm', 'Psalms 1:1-2'),
                                      ('Matins', 'Gospel', 'Matthew 1:1-5'),
                                      ('Liturgy', 'Gospel', 'John 20:1-8')]]

def pair(date):
    return [x['source_record'] for x in CORPUS['records'] if x['source_record']['civil_date'] == date]

class UpstreamMatins(unittest.TestCase):
    def api(self):
        self.assertTrue(callable(getattr(bref, 'project_dated_matins_source', None)),
                        'BRef actual dated source projection API is missing')
        return bref.project_dated_matins_source

    def test_59_pairs_complete_raw_order_bodies_history_and_untargeted(self):
        project = self.api()
        ledger=[]
        for target in CORPUS['complete_exact_dated_Matins_pairs']:
            date=target['civil_date']; records=pair(date)
            prophecy=next(r for r in records if r['slot']=='Prophecies')
            pg=next(r for r in records if r['slot']=='Psalm and Gospel')
            with self.subTest(date=date):
                rows=old_rows(date); before=copy.deepcopy(rows)
                result=project(rows, context(pg))
                actual=[r for r in result['active'] if r['service_section']=='Matins']
                oracle=prophecy['ordered_source_blocks']+pg['ordered_source_blocks']
                self.assertEqual([r['raw_ref'] for r in actual], [b['raw_reference_line'].strip() for b in oracle])
                self.assertEqual([r['source_body'] for r in actual], [b['body_envelope_literal'] for b in oracle])
                self.assertEqual([r['source_order'] for r in actual], list(range(1,len(oracle)+1)))
                self.assertEqual(len(actual),len({r['source_slot'] for r in actual}))
                self.assertEqual([r for r in result['active'] if r['service_section']!='Matins'],[rows[0],rows[-1]])
                self.assertEqual(rows,before)
                self.assertEqual([r['raw_ref'] for r in result['history']],[r['raw_ref'] for r in rows[1:-1]])
                self.assertTrue(all(not r['active'] and not r['include_in_current_index'] for r in result['history']))
                for r,b in zip(actual,oracle):
                    self.assertEqual(hashlib.sha256(r['source_body'].encode()).hexdigest(),b['body_envelope_sha256'])
                    self.assertEqual(r['normalized_ref'],'')
                    self.assertEqual(r['canonical_ref'],'')
                    self.assertFalse(r['runtime_activation_approved'])
                    self.assertFalse(r['recurrence_approved'])
                    self.assertTrue(r['source_coordinate_hold'])
                ledger.append({'date':date,'source_rows':len(actual),'history_rows':len(result['history'])})
        self.assertEqual(len(ledger),59)

    def test_optin_parse_helper_and_default_date_index_hold(self):
        self.api(); date='2026-03-04'; c=context(pair(date)[0])
        html='<html><title>Readings</title><body><h1>Readings</h1><h2>Original day label</h2><h2>Vespers</h2><h4>Gospel</h4><h5>John 1:1-5</h5><h2>Matins</h2><h4>Psalm</h4><h5>Psalms 1:1-2</h5><h4>Gospel</h4><h5>Matthew 1:1-5</h5><h2>Liturgy</h2><h4>Gospel</h4><h5>John 20:1-8</h5></body></html>'
        meta,normal=bref.parse_copticchurch_html(html,dt.date.fromisoformat(date))
        meta2,projected=bref.parse_copticchurch_html(html,dt.date.fromisoformat(date),candidate_matins_context=c)
        self.assertEqual([r for r in projected if r['service_section']!='Matins'],[r for r in normal if r['service_section']!='Matins'])
        self.assertEqual(meta2['matins_source_projection']['runtime_activation_approved'],False)
        held=[r for r in projected if r['service_section']=='Matins']
        self.assertFalse(bref.build_date_passage_index(held))
        index=bref.build_date_passage_index(held,include_candidate_matins=True)
        self.assertEqual([r['raw_ref'] for r in index],[r['raw_ref'] for r in held])
        self.assertTrue(all(r['matched_ref']=='' and r['canonical_ref']=='' for r in index))
        self.assertTrue(any(bref.passage_matches('Exodus 4',r['source_parse_input']) for r in index))
        combined=bref.build_date_passage_index(projected,include_candidate_matins=True)
        self.assertEqual(combined[0]['service_section'],'Vespers')
        self.assertEqual(combined[-1]['service_section'],'Liturgy')

    def test_wrong_scope_date_year_neighbor_collision_and_partial_rejected(self):
        project=self.api(); c=context(pair('2026-03-04')[0])
        for key,value in [('civil_date','2027-03-04'),('civil_date','2026-03-05'),
                          ('occasion_key','GreatFast@-40'),('actual_occasion','Annunciation'),
                          ('service','Liturgy'),('pascha_offset_days',-40),
                          ('numeric_coptic_calendar_crosscheck',{'year':1742,'month':7,'day':29}),
                          ('actual_home_line','claimed date only')]:
            forged=copy.deepcopy(c);forged[key]=value
            with self.subTest(key=key,value=value),self.assertRaises(ValueError):project(old_rows('2026-03-04'),forged)
        with self.assertRaises(ValueError):project(old_rows('2026-03-04'),{'civil_date':'2026-03-04'})
        with self.assertRaises(ValueError):project(old_rows('2026-04-03'),context(pair('2026-04-03')[0]))

    def test_removed_duplicate_overlap_and_interleaved_input_rejected(self):
        project=self.api(); c=context(pair('2026-03-04')[0])
        for field,value in [('active',False),('state','removed'),('status','removed'),
                            ('current_status','removed'),('include_in_current_index',False)]:
            rows=old_rows('2026-03-04');rows[1][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):project(rows,c)
        for ref in ['Genesis 1:1-5','Genesis 1:3-8']:
            rows=old_rows('2026-03-04');rows.insert(2,{**rows[1],'raw_ref':ref,'normalized_ref':ref})
            with self.subTest(ref=ref),self.assertRaises(ValueError):project(rows,c)
        rows=old_rows('2026-03-04'); rows.insert(2,copy.deepcopy(rows[-1]))
        with self.assertRaises(ValueError):project(rows,c)

    def test_no_prophecy_removes_only_old_prophecy_not_pg(self):
        project=self.api(); date='2026-02-05'; result=project(old_rows(date),context(pair(date)[0]))
        matins=[r for r in result['active'] if r['service_section']=='Matins']
        self.assertEqual([r['reading_type'] for r in matins],['Psalm','Gospel'])
        self.assertEqual([r['raw_ref'] for r in matins],[b['raw_reference_line'].strip() for b in pair(date)[1]['ordered_source_blocks']])
        self.assertEqual(result['source_context']['prophecy_semantic_state'],'explicit_no_prophecies_rubric')

    def test_partial_and_omitted_verse_qualifications_preserved(self):
        project=self.api()
        expected={
            'Isaiah 1:19-2:2-3':'final label 3 is partial',
            'Isaiah 2:3-11':'last source verse 11 is partial',
            'Isaiah 49:6-10':'first source verse 6 is partial',
            'Isaiah 65:8-16':'last source verse 16 is partial',
            'Zechariah 9:9-15':'verse 15 contains only its first sentence',
            'John 12:26-36':'last source verse 36 is partial',
            'Luke 9:37-43':'last source verse 43 is partial',
            'Mark 9:43-50':'source omits numbered verses 44 and 46',
        }
        found=set()
        for target in CORPUS['complete_exact_dated_Matins_pairs']:
            rs=pair(target['civil_date'])
            if not any(b['raw_reference_line'].strip() in expected for r in rs for b in r['ordered_source_blocks']):
                continue
            result=project(old_rows(target['civil_date']),context(rs[0]))
            for row in result['active']:
                if row['raw_ref'] in expected:
                    found.add(row['raw_ref'])
                    self.assertIn(expected[row['raw_ref']],row['source_body_qualification']['qualification'])
                    self.assertIn(row['source_body'],row['source_document_body'])
                    self.assertEqual(hashlib.sha256(row['source_document_body'].encode()).hexdigest(),row['source_document_sha256'])
                    self.assertEqual(row['canonical_ref'],'')
        self.assertEqual(found,set(expected))

    def test_source_search_omits_unprinted_verses_and_keeps_composite_order(self):
        project=self.api();found={}
        needles={'Isaiah 1:19-2:2-3','Jonah 1:1-2:1','Mark 9:43-50','Psalms 54:1, 26:11'}
        for target in CORPUS['complete_exact_dated_Matins_pairs']:
            rs=pair(target['civil_date'])
            if not any(b['raw_reference_line'].strip() in needles for r in rs for b in r['ordered_source_blocks']):continue
            for row in project(old_rows(target['civil_date']),context(rs[0]))['active']:
                if row['raw_ref'] in needles:found[row['raw_ref']]=row
        self.assertEqual(set(found),needles)
        self.assertFalse(bref.passage_matches('Isaiah 2:1',found['Isaiah 1:19-2:2-3']['source_parse_input']))
        self.assertFalse(bref.passage_matches('Mark 9:44',found['Mark 9:43-50']['source_parse_input']))
        self.assertFalse(bref.passage_matches('Mark 9:46',found['Mark 9:43-50']['source_parse_input']))
        self.assertEqual(found['Jonah 1:1-2:1']['source_parse_input'],'Jonah 1:1-16; Jonah 2:1')
        self.assertEqual(found['Psalms 54:1, 26:11']['source_parse_input'],'Psalms 54:1, 26:11')
        self.assertTrue(all(r['canonical_ref']=='' for r in found.values()))

    def test_unaffected_serialized_context_cell_keeps_default_index_behavior(self):
        rows=[old_rows('2026-03-04')[0]]
        baseline=bref.build_date_passage_index(rows)
        for value in ['', '{"unrelated":true}', None]:
            with self.subTest(value=value):
                self.assertEqual(bref.build_date_passage_index([{**rows[0],'source_context':value}]),baseline)

    def test_authenticated_source_memory_drift_rejected(self):
        from matins_source_projection import load_dated_matins_fixture
        fixture=load_dated_matins_fixture()
        original=context(pair('2026-03-04')[0])
        for field,value in [('text_sha256','0'*64),('semantic_state','explicit_no_prophecies_rubric'),
                            ('actual_occasion','Annunciation')]:
            corrupt=copy.deepcopy(fixture)
            corrupt['corpus']['records'][0]['source_record'][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):
                self.api()(old_rows('2026-03-04'),original,fixture=corrupt)
        corrupt=copy.deepcopy(fixture);corrupt['corpus']['records'][0]['runtime_activation']=True
        with self.assertRaises(ValueError):self.api()(old_rows('2026-03-04'),original,fixture=corrupt)

    def test_projected_table_mutations_rejected_at_real_index_api(self):
        project=self.api(); c=context(pair('2026-03-04')[0])
        rows=[r for r in project(old_rows('2026-03-04'),c)['active'] if r['service_section']=='Matins']
        mutations={
            'omitted':lambda rs:rs.pop(1),
            'reordered':lambda rs:rs.reverse(),
            'truncated':lambda rs:rs[0].update(raw_ref='Exodus 4:19-5:1'),
            'duplicate':lambda rs:rs.insert(1,copy.deepcopy(rs[0])),
            'overlap':lambda rs:rs[1].update(raw_ref='Exodus 4:20-6:13'),
            'bodyhash':lambda rs:rs[0].update(source_body=rs[0]['source_body'][:-1]),
            'removal':lambda rs:rs[0].update(current_status='removed'),
            'rubric':lambda rs:rs[0]['source_context'].update(prophecy_semantic_state='explicit_no_prophecies_rubric'),
            'canonical':lambda rs:rs[0].update(canonical_ref='Exodus 4:19-6:13'),
            'activation':lambda rs:rs[0].update(runtime_activation_approved=True),
            'forged_source':lambda rs:[r.update(source='copticchurch.net daily scrape',parse_status='ok') for r in rs],
            'hold_removed':lambda rs:rs[0].update(source_coordinate_hold=False,normalization_hold=False),
        }
        for name,mutate in mutations.items():
            corrupt=copy.deepcopy(rows);mutate(corrupt)
            with self.subTest(mutation=name),self.assertRaises(ValueError):
                bref.build_date_passage_index(corrupt,include_candidate_matins=True)

if __name__=='__main__':unittest.main(verbosity=2)
