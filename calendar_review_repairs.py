"""Source-qualified K1-K6 calendar metadata, without changing source labels.

Run on the complete presentation inventory before reverse grouping and daily
filtering. Supply the ordinary builder's identity resolver, not a second parser.
Raw keys, titles, references, provenance and existing inactive state are retained.
"""
from collections import defaultdict
from functools import lru_cache
import datetime as dt
import re
from urllib.parse import parse_qs, urlparse


MONTH_SLUGS = ('tout', 'baba', 'hatour', 'kiahk', 'toba', 'amshir', 'baramhat',
               'baramouda', 'bashans', 'paona', 'abib', 'mesra', 'nasie')
MONTH_ALIASES = {
    'tout': 1, 'tut': 1, 'thoout': 1,
    'baba': 2, 'babah': 2,
    'hatour': 3, 'hator': 3, 'hatur': 3, 'hatoor': 3,
    'kiahk': 4, 'kiyahk': 4, 'kiak': 4,
    'toba': 5, 'tubah': 5, 'tobe': 5,
    'amshir': 6, 'meshir': 6, 'baramhat': 7,
    'baramouda': 8, 'barmuda': 8, 'baramoudah': 8, 'baramudah': 8,
    'bashans': 9, 'bashons': 9, 'paona': 10, 'baunah': 10,
    'abib': 11, 'mesra': 12, 'misra': 12, 'nasie': 13, 'al-nasi': 13, 'nesi': 13,
}
ORDINALS = ('first', 'second', 'third', 'fourth', 'fifth')
ORDINARY = ('ordinary_date_resolved', 'copticchurch_date')
KATAMEROS = ('katameros_cycle', 'katameros_cycle')
DATED_SOURCES = (ORDINARY,
    ('coptic_reader_verified_supplement', 'copticchurch_date'),
    ('coptic_reader_verified_calendar_boundary', 'copticchurch_date'),
    ('coptic_reader_verified_sunday_policy', 'copticchurch_date'))
GENERIC_SEASONS = {'Great Lent', 'Fast of Nineveh', "St Mary's Fast", "St. Mary's Fast"}
FIELDS = ('coptic_date_key', 'annual_sunday', 'display_label', 'calendar_review_status')
HOLD = 'seasonal_label_unresolved'
COLLISION_SUFFIX = ' and the Feast of Entry into Egypt'
FIXED_FEAST_LABELS = {
    'Annunciation', 'Christmas', 'Christmas Paramoune', 'Circumcision of our Lord',
    'Entrance into the Temple', 'Epiphany Paramoune', 'The Feast of Epiphany',
    'The Second Day of Feast of Epiphany', 'Transfiguration', 'Wedding of Cana',
}


def date_key(month, day):
    """A validated Synaxarium slug, never a Sunday ordinal or pseudo-month."""
    month, day = int(month), int(day)
    if not 1 <= month <= 13 or not 1 <= day <= (6 if month == 13 else 30):
        raise ValueError(f'invalid fixed Coptic date: {month}/{day}')
    return f'{MONTH_SLUGS[month - 1]}-{day}'


def literal_date_key(label):
    """Parse only a literal month/day with an optional source label suffix."""
    label = re.sub(r'^(?:Sunday, |Non-Sunday )', '', label)
    match = re.fullmatch(r'([A-Za-z-]+) (\d{1,2})(?: \(.*\)| of .*)?', label)
    if not match or match[1].casefold() not in MONTH_ALIASES:
        return ''
    return date_key(MONTH_ALIASES[match[1].casefold()], match[2])


def sunday_key(label):
    # The package's documented Kiyahk service-table alias is not a fixed date.
    fast = re.fullmatch(r'(?:the )?(first|second|third|fourth) Sunday of Christmas Fast', label, re.I)
    if fast:
        return f'kiahk-{ORDINALS.index(fast[1].casefold()) + 1}'
    match = re.fullmatch(r'(?:the )?(first|second|third|fourth|fifth) Sunday of '
                         r'([A-Za-z-]+)(?: of Christmas Fast| \(Readings of 29th Baramhat\))?', label, re.I)
    if not match or match[2].casefold() not in MONTH_ALIASES:
        return ''
    return f'{MONTH_SLUGS[MONTH_ALIASES[match[2].casefold()] - 1]}-{ORDINALS.index(match[1].casefold()) + 1}'


def display_label(label):
    if 'holy fifty days' in label.casefold() and label.endswith(COLLISION_SUFFIX):
        label = label[:-len(COLLISION_SUFFIX)]
    # Preserve all raw source fields; vocabulary changes belong only here.
    label = re.sub(r'\bChristmas Fast\b', 'Nativity Fast', label, flags=re.I)
    label = re.sub(r'\bEpiphany Paramoune\b', 'Paramoun of the Theophany', label, flags=re.I)
    label = re.sub(r'\bFeast of Epiphany\b', 'Feast of the Theophany', label, flags=re.I)
    return re.sub(r'\bEpiphany\b', 'Theophany', label, flags=re.I)


def calendar_group_key(row):
    """Append to the ordinary reverse grouping key, before choosing a source."""
    return tuple(row.get(field, '') for field in FIELDS)


def calendar_output_fields(rows):
    """Refuse a lossy scalar projection of distinct normalized contexts."""
    contexts = {calendar_group_key(row) for row in rows}
    if len(contexts) != 1:
        raise ValueError('distinct calendar contexts must be grouped separately')
    return dict(zip(FIELDS, contexts.pop(), strict=True))


def _source_key(row, *, raw=False):
    return tuple(str(row.get(field, '') or '') for field in
        ('source_family', 'source_kind', 'source_file', 'source_row_id',
         'service_section', 'service_hour')) + (
             str((row.get('reading_slot') or row.get('reading_type') or '') if raw else row.get('slot', '')),
             str(row.get('source_ref', '')))


def _numeric_date(value):
    match = re.fullmatch(r'(\d{4})-(\d{2})-(\d{2})', value)
    if not match:
        return ''
    return date_key(match[2], match[3])


def _gregorian_date_key(value):
    # Reuse the repo's qualified calendar, with its explicit supported year range.
    from calendar_resolution import numeric_coptic_date
    _, month, day = numeric_coptic_date(dt.date.fromisoformat(value))
    return date_key(month, day)


def _locator_date(locator):
    url = locator.split(';', 1)[0]
    parsed = urlparse(url)
    if parsed.scheme != 'https' or parsed.netloc != 'copticchurch.net' or parsed.path != '/readings':
        return ''
    query = parse_qs(parsed.query)
    if any(len(query.get(k, [])) != 1 for k in ('g_year', 'g_month', 'g_day')):
        return ''
    return dt.date(*(int(query[k][0]) for k in ('g_year', 'g_month', 'g_day'))).isoformat()


class CalendarReviewRepairs:
    """Qualify complete source tuples, then add presentation-only calendar fields.

    ``identity`` receives an authenticated raw crosswalk row and must return the
    ordinary design builder's identity dictionary. It preserves all existing
    edition and source-transport behavior rather than guessing from references.
    """
    def __init__(self, raw_rows, cycle_rows, synaxarium, identity):
        self.sources = defaultdict(list)
        for row in raw_rows:
            if (row.get('source_family'), row.get('source_kind')) in (*DATED_SOURCES, KATAMEROS):
                self.sources[_source_key(row, raw=True)].append(dict(row))
        self.cycles = {str(i): dict(row) for i, row in enumerate(cycle_rows, 1)}
        self.synaxarium = frozenset(synaxarium)
        self.identity = identity
        self.identity_cache = {}

    def _source(self, row):
        candidates = self.sources.get(_source_key(row), [])
        fields = ('calendar_key', 'gregorian_date', 'coptic_date', 'day_title',
                  'service_day', 'source_ref', 'raw_ref', 'provenance')
        matches = [r for r in candidates if all(str(row.get(f, '') or '') ==
                   str(r.get(f, '') or '') for f in fields)]
        if len(matches) != 1:
            raise ValueError(f'calendar source tuple mismatch: {_source_key(row)!r}')
        raw = matches[0]
        expected_occasion = raw.get('liturgical_place') or raw.get('day_title') or raw.get('calendar_key') or ''
        if row.get('occasion') != expected_occasion:
            raise ValueError('calendar source occasion mismatch')
        # Authenticate the complete public identity, not only its shared rid.
        cache_key = _source_key(raw, raw=True) + tuple(raw.get(f, '') for f in fields)
        if cache_key not in self.identity_cache:
            self.identity_cache[cache_key] = self.identity(raw)
        expected = self.identity_cache[cache_key]
        for field in ('identity_key', 'display_ref', 'canonical_mt_ref', 'canonical_lxx_ref', 'spans_json'):
            if row.get(field, '') != expected.get(field, ''):
                raise ValueError(f'calendar source reading identity mismatch: {field}')
        # The existing builder owns source-specific correction locators too.
        # Do not reconstruct a generic URL for a source-qualified correction.
        for field in ('source_locator', 'source_title', 'source_edition', 'authority_tier'):
            if field not in expected or row.get(field, '') != expected[field]:
                raise ValueError(f'calendar source registry mismatch: {field}')
        return raw

    def _cycle(self, raw):
        cycle = self.cycles.get(str(raw['source_row_id']))
        if cycle is None:
            raise ValueError('calendar source cycle ordinal missing')
        expected = {
            'source_table': raw['source_table'], 'day_key': raw['calendar_key'],
            'reading_slot': raw['reading_slot'], 'raw_ref': raw['raw_ref'],
        }
        if any(cycle.get(k, '') != v for k, v in expected.items()):
            raise ValueError('calendar source cycle context mismatch')
        passage = cycle.get('normalized_segment') or cycle.get('canonical_segment') or cycle.get('normalized_ref') or cycle.get('raw_ref') or ''
        if passage != raw['source_ref']:
            raise ValueError('calendar source cycle reference mismatch')
        return cycle

    def _dated(self, raw, row):
        values = set()
        if raw.get('coptic_date'):
            numeric = _numeric_date(raw['coptic_date'])
            if not numeric:
                raise ValueError('calendar source numeric date malformed')
            values.add(numeric)
        gregorian = raw.get('gregorian_date', '')
        located = _locator_date(row['source_locator'])
        if gregorian and located and gregorian != located:
            raise ValueError('calendar source Gregorian locator mismatch')
        for value in (gregorian, located):
            if value:
                values.add(_gregorian_date_key(value))
        if len(values) > 1:
            raise ValueError('calendar source date evidence disagrees')
        return next(iter(values), '')

    def apply(self, rows):
        result = []
        for row in rows:
            out = dict(row)
            fields = dict.fromkeys(FIELDS, '')
            fields['display_label'] = display_label(row.get('occasion', ''))
            pair = (row.get('source_family'), row.get('source_kind'))
            # A familiar title does not turn a Reader-qualified movable cycle
            # into a fixed-date source. Wrong family/kind combinations fail closed.
            scoped = pair in (*DATED_SOURCES, KATAMEROS)
            if not scoped and (pair[0] in tuple(p[0] for p in (*DATED_SOURCES, KATAMEROS)) or
                               pair[1] == KATAMEROS[1]):
                raise ValueError('calendar source family/kind mismatch')
            if scoped:
                raw = self._source(row)
                if pair == KATAMEROS:
                    cycle = self._cycle(raw)
                    table = cycle['source_table']
                    if table == 'SundayReadings':
                        month, ordinal = int(cycle['month_number']), int(cycle['day'])
                        if not 1 <= ordinal <= 5 or not 1 <= month <= 14:
                            raise ValueError('calendar source annual Sunday dimensions invalid')
                        fields['annual_sunday'] = f'{MONTH_SLUGS[month - 1] if month < 14 else "any-month"}-{ordinal}'
                        fields['display_label'] = display_label(raw['day_title'] or raw['service_day'])
                    elif table == 'AnnualReadings':
                        fields['coptic_date_key'] = date_key(cycle['month_number'], cycle['day'])
                        if literal_date_key(raw['calendar_key']) != fields['coptic_date_key']:
                            raise ValueError('calendar source fixed-date dimensions disagree')
                else:
                    title = raw['calendar_key']
                    fields['annual_sunday'] = sunday_key(title)
                    literal = literal_date_key(title)
                    if not fields['annual_sunday'] and (literal or title in GENERIC_SEASONS or title in FIXED_FEAST_LABELS):
                        dated = self._dated(raw, row)
                        if literal and dated and literal != dated:
                            raise ValueError('calendar source literal and dated context disagree')
                        fields['coptic_date_key'] = dated or literal
                        if title in GENERIC_SEASONS:
                            if dated:
                                month, day = dated.rsplit('-', 1)
                                fields['display_label'] = f'{month.capitalize()} {day}'
                            else:
                                fields['calendar_review_status'] = HOLD
                                # Never overwrite existing lifecycle/provenance.
                                out['active'] = False
                                out['calendar_review_daily_eligible'] = False
            if fields['coptic_date_key'] and fields['coptic_date_key'] not in self.synaxarium:
                raise ValueError(f'calendar source date absent from Synaxarium: {fields["coptic_date_key"]}')
            for field, value in fields.items():
                if field in row and row[field] != value:
                    raise ValueError(f'calendar source normalized metadata drift: {field}')
            out.update(fields)
            result.append(out)
        return result


class CalendarRuntimeReview:
    """Add metadata after npm canonicalization, without touching its input guard.

    A collapsed source row with several fixed dates or Sunday contexts becomes
    one metadata view per authenticated context. Every original field remains
    unchanged. The added locator/key lists disclose the exact selected witnesses.
    """
    def __init__(self, repairs, presentation_rows):
        self.repairs = repairs
        self.by_locator = defaultdict(list)
        self.by_group = defaultdict(list)
        self.source_pairs = defaultdict(set)
        for row in repairs.apply(presentation_rows):
            if (row.get('source_family'), row.get('source_kind')) not in (*DATED_SOURCES, KATAMEROS):
                continue
            self.by_locator[self._locator_key(row)].append(row)
            self.by_group[self._group_key(row)].append(row)
            self.source_pairs[self._locator_key(row)[2:]].add((row['source_family'], row['source_kind']))

    @staticmethod
    def _locator_key(row):
        return tuple(row.get(f, '') for f in ('source_family', 'source_kind', 'source_locator',
                    'service_section', 'service_hour', 'slot', 'identity_key'))

    @staticmethod
    def _group_key(row):
        return tuple(row.get(f, '') for f in ('source_family', 'source_kind', 'occasion',
                    'service_section', 'service_hour', 'slot', 'identity_key'))

    @staticmethod
    def _identity_matches(row, source):
        identity_ok = all(row.get(f, '') == source.get(f, '') for f in
                   ('display_ref', 'canonical_mt_ref', 'canonical_lxx_ref', 'spans_json'))
        registry_ok = all(f not in row or row[f] == source.get(f, '') for f in
                          ('source_title', 'source_edition'))
        return identity_ok and registry_ok

    @staticmethod
    def _canonical_occasion(label):
        # Mirror only the established npm presentation aliases, not recurrence.
        aliases = {'Tout': 'Tut', 'Hator': 'Hatur', 'Hatoor': 'Hatur', 'Kiahk': 'Kiyahk',
            'Kiak': 'Kiyahk', 'Toba': 'Tubah', 'Amshir': 'Meshir', 'Bashans': 'Bashons',
            'Paona': 'Baunah', 'Baba': 'Babah', 'Baramoudah': 'Barmuda', 'Al-Nasi': 'Nesi'}
        for alias, name in aliases.items():
            label = re.sub(r'\b' + re.escape(alias) + r'\b', name, label, flags=re.I)
        label = re.sub(r'^(?:the\s+)?(first|second|third|fourth|fifth) Sunday of ',
                       lambda m: m[1].capitalize() + ' Sunday of ', label, flags=re.I)
        return re.sub(r'^(first|second|third|fourth) Sunday of Christmas Fast$',
                      lambda m: m[1].capitalize() + ' Sunday of Kiyahk', label, flags=re.I)

    def _occasion_matches(self, row, source):
        label = source['occasion']
        allowed_raw = {label}
        if label.endswith('(Feast of the Cross)'):
            allowed_raw.update({'Non-Sunday ' + label, 'Sunday, ' + label})
        allowed_raw |= {re.sub(r'\bBaba\b', 'Babah', re.sub(r'\bKiak\b', 'Kiahk', s)) for s in allowed_raw}
        allowed = allowed_raw | {self._canonical_occasion(s) for s in allowed_raw}
        if row.get('source_occasion') and row['source_occasion'] not in allowed_raw:
            return False
        if row.get('occasion') in allowed:
            return True
        sentinel = {'week 99 day_of_week 0': 'Preparation Sunday',
                    'week 99 day_of_week 6': 'Preparation Saturday'}.get(source['calendar_key'])
        return bool(sentinel and row.get('occasion') == sentinel)

    def _scoped(self, row):
        pair = (row.get('source_family'), row.get('source_kind'))
        known_pairs = self.source_pairs.get(self._locator_key(row)[2:], set())
        if known_pairs and pair not in known_pairs:
            raise ValueError('calendar source runtime family/kind rebound')
        if pair in (*DATED_SOURCES, KATAMEROS):
            return True
        if pair[0] in tuple(p[0] for p in (*DATED_SOURCES, KATAMEROS)) or pair[1] == KATAMEROS[1]:
            raise ValueError('calendar source runtime family/kind mismatch')
        return False

    @staticmethod
    def _unscoped(row):
        return {**row, 'coptic_date_key': row.get('coptic_date_key', ''),
                'annual_sunday': row.get('annual_sunday', ''),
                'calendar_review_status': row.get('calendar_review_status', ''),
                'display_label': display_label(row.get('display_label') or row.get('occasion', ''))}

    def _emit(self, row, sources):
        fields = calendar_output_fields(sources)
        for field, value in fields.items():
            if field in row and row[field] != value:
                raise ValueError(f'calendar source runtime normalized metadata drift: {field}')
        evidence = {
            'calendar_review_source_locators': sorted({s['source_locator'] for s in sources}),
            'calendar_review_calendar_keys': sorted({s['calendar_key'] for s in sources}),
        }
        for field, value in evidence.items():
            if field in row and row[field] != value:
                raise ValueError(f'calendar source runtime evidence drift: {field}')
        output = {**row, **fields, **evidence}
        if fields['calendar_review_status'] == HOLD:
            output['active'] = False
        return output

    def apply_reverse_rows(self, rows):
        """Accept published-like reverse rows after canonicalizeOccurrences."""
        output = []
        for row in rows:
            if not self._scoped(row):
                output.append(self._unscoped(row))
                continue
            representatives = [s for s in self.by_locator[self._locator_key(row)]
                               if self._identity_matches(row, s) and self._occasion_matches(row, s)]
            if not representatives:
                raise ValueError(f'calendar source runtime reverse tuple mismatch: {self._locator_key(row)!r}')
            group_keys = {self._group_key(s) for s in representatives}
            if len(group_keys) != 1:
                raise ValueError('calendar source runtime reverse representative is ambiguous')
            candidates = self.by_group[next(iter(group_keys))]
            keys = set(str(row.get('calendar_keys', '')).split(' || '))
            # The npm transport has two established raw-string aliases. They
            # are not permission to match another date or a Sunday as a date.
            def published_key(value):
                value = re.sub(r'^(?:Non-Sunday |Sunday, )', '', value)
                return re.sub(r'\bBaba\b', 'Babah', re.sub(r'\bKiak\b', 'Kiahk', value))
            def key_matches(source):
                for key in keys:
                    if published_key(source['calendar_key']) != published_key(key):
                        continue
                    if key.startswith(('Non-Sunday ', 'Sunday, ')):
                        date = source.get('gregorian_date')
                        if not date or (dt.date.fromisoformat(date).weekday() == 6) != key.startswith('Sunday, '):
                            continue
                    return True
                return False
            sentinel = {'Preparation Sunday': 'week 99 day_of_week 0',
                        'Preparation Saturday': 'week 99 day_of_week 6'}.get(row.get('occasion'))
            if sentinel and row.get('calendar_keys') == row.get('occasion'):
                if sentinel not in str(row.get('source_calendar_keys', '')).split(' || '):
                    raise ValueError('calendar source runtime preparation context mismatch')
                candidates = [dict(s, display_label=display_label(row['occasion']))
                              for s in candidates if s['calendar_key'] == sentinel]
            else:
                candidates = [s for s in candidates if key_matches(s)]
            if not candidates:
                raise ValueError('calendar source runtime reverse calendar key mismatch')
            contexts = defaultdict(list)
            for source in candidates:
                if self._identity_matches(row, source):
                    contexts[calendar_group_key(source)].append(source)
            # On replay a context-specific view must not expand back to siblings.
            if all(f in row for f in FIELDS):
                contexts = {k: v for k, v in contexts.items() if k == calendar_group_key(row)}
            if not contexts:
                raise ValueError('calendar source runtime reverse context mismatch')
            for context in sorted(contexts):
                output.append(self._emit(row, contexts[context]))
        return output

    def apply_daily_year(self, days):
        """Accept a complete {ISO date: readings[]} year, using its trusted date."""
        output = {}
        for date_value, readings in days.items():
            dt.date.fromisoformat(date_value)
            output[date_value] = []
            for row in readings:
                if not self._scoped(row):
                    output[date_value].append(self._unscoped(row))
                    continue
                sources = [s for s in self.by_locator[self._locator_key(row)]
                           if s['gregorian_date'] == date_value and self._identity_matches(row, s)
                           and self._occasion_matches(row, s)]
                if not sources:
                    raise ValueError(f'calendar source runtime daily tuple/date mismatch: {date_value} {self._locator_key(row)!r}')
                projected = self._emit(row, sources)
                if projected.get('calendar_review_status') != HOLD:
                    output[date_value].append(projected)
        return output


def load_runtime_review(root):
    """Read sources once per process; no per-row SQLite or network access."""
    from pathlib import Path
    return _load_runtime_review(str(Path(root).resolve()))


@lru_cache(maxsize=1)
def _load_runtime_review(root):
    import csv
    import json
    from pathlib import Path
    import build_design_deliverables as design
    root = Path(root)
    if root != design.ROOT:
        raise ValueError('calendar source runtime import root mismatch')
    def read(name):
        with (root / name).open(newline='', encoding='utf-8') as handle:
            return list(csv.DictReader(handle))
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
    repairs = CalendarReviewRepairs(read('out/data/reverse_lookup_crosswalk.csv'),
        read('out/data/katameros_cycle_passage_index.csv'),
        json.loads((root / 'packages/lectionary-data/data/synaxarium/synaxarium.json').read_text()), identity)
    return CalendarRuntimeReview(repairs, read('out/design/reverse_lectionary_presentation.csv'))
