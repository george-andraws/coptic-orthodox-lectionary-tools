"""Exercise the validator's actual no-service predicate in isolation."""
import ast
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def marker_allowed(section):
    # Compile the exact predicate, not a second implementation of its rules.
    tree = ast.parse((ROOT / 'verify_design_deliverables.py').read_text())
    expression = next(node.value for node in ast.walk(tree)
                      if isinstance(node, ast.Assign)
                      and any(isinstance(target, ast.Name) and target.id == 'is_no_service_marker'
                              for target in node.targets))
    code = compile(ast.Expression(expression), '<actual-no-service-predicate>', 'eval')
    row = {'current_status': 'historical_candidate_removed',
           'source_kind': 'copticchurch_date', 'day_title': 'Fast of Nineveh',
           'service_section': section, 'gregorian_date': '2026-02-02'}
    rules = [{'reason': 'coptic_reader_no_service', 'day_title': 'Fast of Nineveh',
              'service_section': section}]
    return eval(code, {'marker': 'removed_by_coptic_reader_no_service',
                       'row': row, 'suppressed_contexts': rules})


class NoServiceMarkerScope(unittest.TestCase):
    def test_documented_vespers_marker_remains_compatible(self):
        self.assertTrue(marker_allowed('Vespers'))

    def test_matching_matins_policy_cannot_expand_vespers_marker_scope(self):
        self.assertFalse(marker_allowed('Matins'))

    def test_matching_liturgy_policy_cannot_expand_vespers_marker_scope(self):
        self.assertFalse(marker_allowed('Liturgy'))


if __name__ == '__main__':
    unittest.main()
