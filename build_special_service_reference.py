#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
from pathlib import Path
from typing import List, Dict

from passage_normalization import canonicalize_text_ref, extract_text_ref_tokens, parse_passage
from reading_context_overlays import is_current_source_row

ROOT = Path(__file__).resolve().parent
OUT = Path(os.environ.get('LECTIONARY_SPECIAL_OUTPUT_DIR', str(ROOT / 'out' / 'data')))
VAULT = Path.home() / 'Library/CloudStorage/GoogleDrive-georgeandraws@gmail.com/My Drive/HermesAI/obsidian-vault/Hermes/04-Reference/Coptic Orthodox Lessons/References/Lectionary'


def env_flag(name: str) -> bool:
    return os.environ.get(name, '').strip().lower() in {'1', 'true', 'yes', 'on'}


DISABLE_VAULT_PUBLISH = env_flag('LECTIONARY_DISABLE_VAULT_PUBLISH')

SOURCE_ST_BISHOY_PAGE = 'https://saintbishoy.ca/service-books/'
ROWS: List[Dict[str, str]] = [
    {
        'service_family': 'wedding_crowning',
        'service_variant': 'holy_matrimony_main',
        'section': 'main_readings',
        'reading_type': 'pauline',
        'raw_ref': 'Ephesians 5:22-6:3',
        'source_title': 'The Holy Matrimony Rite',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Wedding_Ceremony.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Main crowning rite Pauline reading.',
    },
    {
        'service_family': 'wedding_crowning',
        'service_variant': 'holy_matrimony_main',
        'section': 'main_readings',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 19:5; Psalm 128:3',
        'source_title': 'The Holy Matrimony Rite',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Wedding_Ceremony.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Printed as Psalm (18) 19:5 and Psalm (127) 128:3 in the rite book.',
    },
    {
        'service_family': 'wedding_crowning',
        'service_variant': 'holy_matrimony_main',
        'section': 'main_readings',
        'reading_type': 'gospel',
        'raw_ref': 'Matthew 19:1-6',
        'source_title': 'The Holy Matrimony Rite',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Wedding_Ceremony.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Main crowning rite Gospel reading.',
    },
    {
        'service_family': 'baptism',
        'service_variant': 'mother_absolution_male_child',
        'section': 'part_1',
        'reading_type': 'pauline',
        'raw_ref': 'Hebrews 1:8-12',
        'source_title': 'Baptism and Chrismation Rite',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Baptism.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Absolution for the woman if she bore a male child.',
    },
    {
        'service_family': 'baptism',
        'service_variant': 'mother_absolution_male_child',
        'section': 'part_1',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 32:1-2',
        'source_title': 'Baptism and Chrismation Rite',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Baptism.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Printed as Psalm 31 in LXX numbering.',
    },
    {
        'service_family': 'baptism',
        'service_variant': 'mother_absolution_male_child',
        'section': 'part_1',
        'reading_type': 'gospel',
        'raw_ref': 'Luke 2:21-35',
        'source_title': 'Baptism and Chrismation Rite',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Baptism.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Absolution for the woman if she bore a male child.',
    },
    {
        'service_family': 'baptism',
        'service_variant': 'mother_absolution_female_child',
        'section': 'part_2',
        'reading_type': 'pauline',
        'raw_ref': '1 Corinthians 7:12-14',
        'source_title': 'Baptism and Chrismation Rite',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Baptism.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Absolution for the woman if she bore a female child.',
    },
    {
        'service_family': 'baptism',
        'service_variant': 'mother_absolution_female_child',
        'section': 'part_2',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 45:9; Psalm 45:13',
        'source_title': 'Baptism and Chrismation Rite',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Baptism.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Printed as Psalm 44:12 in the Arabic line plus 45:9,13 in English/Coptic formatting; preserve the two verse references explicitly.',
    },
    {
        'service_family': 'baptism',
        'service_variant': 'mother_absolution_female_child',
        'section': 'part_2',
        'reading_type': 'gospel',
        'raw_ref': 'Luke 10:38-42',
        'source_title': 'Baptism and Chrismation Rite',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Baptism.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Absolution for the woman if she bore a female child.',
    },
    {
        'service_family': 'baptism',
        'service_variant': 'sanctification_of_baptismal_water',
        'section': 'part_3',
        'reading_type': 'pauline',
        'raw_ref': 'Titus 2:11-3:7',
        'source_title': 'Baptism and Chrismation Rite',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Baptism.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Main baptismal-water sanctification readings.',
    },
    {
        'service_family': 'baptism',
        'service_variant': 'sanctification_of_baptismal_water',
        'section': 'part_3',
        'reading_type': 'catholic',
        'raw_ref': '1 John 5:5-20',
        'source_title': 'Baptism and Chrismation Rite',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Baptism.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Main baptismal-water sanctification readings.',
    },
    {
        'service_family': 'baptism',
        'service_variant': 'sanctification_of_baptismal_water',
        'section': 'part_3',
        'reading_type': 'acts',
        'raw_ref': 'Acts 8:26-39',
        'source_title': 'Baptism and Chrismation Rite',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Baptism.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Main baptismal-water sanctification readings.',
    },
    {
        'service_family': 'baptism',
        'service_variant': 'sanctification_of_baptismal_water',
        'section': 'part_3',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 32:1-2',
        'source_title': 'Baptism and Chrismation Rite',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Baptism.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Printed as Psalm 31 in LXX numbering.',
    },
    {
        'service_family': 'baptism',
        'service_variant': 'sanctification_of_baptismal_water',
        'section': 'part_3',
        'reading_type': 'gospel',
        'raw_ref': 'John 3:1-21',
        'source_title': 'Baptism and Chrismation Rite',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Baptism.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Main baptismal-water sanctification readings.',
    },
    {
        'service_family': 'unction_of_the_sick',
        'service_variant': 'first_prayer',
        'section': 'first_prayer',
        'reading_type': 'catholic',
        'raw_ref': 'James 5:10-20',
        'source_title': 'The Unction of the Sick',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Unction_of_Sick.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'First prayer uses Catholic Epistle rather than Pauline.',
    },
    {
        'service_family': 'unction_of_the_sick',
        'service_variant': 'first_prayer',
        'section': 'first_prayer',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 6:1-2',
        'source_title': 'The Unction of the Sick',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Unction_of_Sick.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'First prayer Psalm.',
    },
    {
        'service_family': 'unction_of_the_sick',
        'service_variant': 'first_prayer',
        'section': 'first_prayer',
        'reading_type': 'gospel',
        'raw_ref': 'John 5:1-17',
        'source_title': 'The Unction of the Sick',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Unction_of_Sick.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'First prayer Gospel.',
    },
    {
        'service_family': 'unction_of_the_sick',
        'service_variant': 'second_prayer',
        'section': 'second_prayer',
        'reading_type': 'pauline',
        'raw_ref': 'Romans 15:1-7',
        'source_title': 'The Unction of the Sick',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Unction_of_Sick.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Second prayer Pauline.',
    },
    {
        'service_family': 'unction_of_the_sick',
        'service_variant': 'second_prayer',
        'section': 'second_prayer',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 102:1-2',
        'source_title': 'The Unction of the Sick',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Unction_of_Sick.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Printed as Psalms (101) 102:1-2.',
    },
    {
        'service_family': 'unction_of_the_sick',
        'service_variant': 'second_prayer',
        'section': 'second_prayer',
        'reading_type': 'gospel',
        'raw_ref': 'Luke 19:1-10',
        'source_title': 'The Unction of the Sick',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Unction_of_Sick.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Second prayer Gospel.',
    },
    {
        'service_family': 'unction_of_the_sick',
        'service_variant': 'third_prayer',
        'section': 'third_prayer',
        'reading_type': 'pauline',
        'raw_ref': '1 Corinthians 12:28-13:8',
        'source_title': 'The Unction of the Sick',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Unction_of_Sick.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Third prayer Pauline.',
    },
    {
        'service_family': 'unction_of_the_sick',
        'service_variant': 'third_prayer',
        'section': 'third_prayer',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 38:1-2',
        'source_title': 'The Unction of the Sick',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Unction_of_Sick.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Printed as Psalm (37) 38:1-2.',
    },
    {
        'service_family': 'unction_of_the_sick',
        'service_variant': 'third_prayer',
        'section': 'third_prayer',
        'reading_type': 'gospel',
        'raw_ref': 'Matthew 10:1-8',
        'source_title': 'The Unction of the Sick',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Unction_of_Sick.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Third prayer Gospel.',
    },
    {
        'service_family': 'unction_of_the_sick',
        'service_variant': 'fourth_prayer',
        'section': 'fourth_prayer',
        'reading_type': 'pauline',
        'raw_ref': 'Romans 8:14-21',
        'source_title': 'The Unction of the Sick',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Unction_of_Sick.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Fourth prayer Pauline.',
    },
    {
        'service_family': 'unction_of_the_sick',
        'service_variant': 'fourth_prayer',
        'section': 'fourth_prayer',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 51:1-2',
        'source_title': 'The Unction of the Sick',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Unction_of_Sick.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Printed as Psalm (50) 51:1-2.',
    },
    {
        'service_family': 'unction_of_the_sick',
        'service_variant': 'fourth_prayer',
        'section': 'fourth_prayer',
        'reading_type': 'gospel',
        'raw_ref': 'Luke 10:1-9',
        'source_title': 'The Unction of the Sick',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Unction_of_Sick.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Fourth prayer Gospel.',
    },
    {
        'service_family': 'unction_of_the_sick',
        'service_variant': 'fifth_prayer',
        'section': 'fifth_prayer',
        'reading_type': 'pauline',
        'raw_ref': 'Galatians 2:16-20',
        'source_title': 'The Unction of the Sick',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Unction_of_Sick.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Fifth prayer Pauline.',
    },
    {
        'service_family': 'unction_of_the_sick',
        'service_variant': 'fifth_prayer',
        'section': 'fifth_prayer',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 142:7',
        'source_title': 'The Unction of the Sick',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Unction_of_Sick.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Printed as Psalm (141) 142:7.',
    },
    {
        'service_family': 'unction_of_the_sick',
        'service_variant': 'fifth_prayer',
        'section': 'fifth_prayer',
        'reading_type': 'gospel',
        'raw_ref': 'John 14:1-19',
        'source_title': 'The Unction of the Sick',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Unction_of_Sick.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Fifth prayer Gospel.',
    },
    {
        'service_family': 'unction_of_the_sick',
        'service_variant': 'sixth_prayer',
        'section': 'sixth_prayer',
        'reading_type': 'pauline',
        'raw_ref': 'Colossians 3:12-17',
        'source_title': 'The Unction of the Sick',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Unction_of_Sick.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Sixth prayer Pauline.',
    },
    {
        'service_family': 'unction_of_the_sick',
        'service_variant': 'sixth_prayer',
        'section': 'sixth_prayer',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 4:1',
        'source_title': 'The Unction of the Sick',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Unction_of_Sick.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Sixth prayer Psalm.',
    },
    {
        'service_family': 'unction_of_the_sick',
        'service_variant': 'sixth_prayer',
        'section': 'sixth_prayer',
        'reading_type': 'gospel',
        'raw_ref': 'Luke 7:36-50',
        'source_title': 'The Unction of the Sick',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Unction_of_Sick.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Sixth prayer Gospel.',
    },
    {
        'service_family': 'unction_of_the_sick',
        'service_variant': 'seventh_prayer',
        'section': 'seventh_prayer',
        'reading_type': 'pauline',
        'raw_ref': 'Ephesians 6:10-18',
        'source_title': 'The Unction of the Sick',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Unction_of_Sick.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Seventh prayer Pauline.',
    },
    {
        'service_family': 'unction_of_the_sick',
        'service_variant': 'seventh_prayer',
        'section': 'seventh_prayer',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 25:18; Psalm 25:20',
        'source_title': 'The Unction of the Sick',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Unction_of_Sick.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Printed as Psalm (24) 25:18,20.',
    },
    {
        'service_family': 'unction_of_the_sick',
        'service_variant': 'seventh_prayer',
        'section': 'seventh_prayer',
        'reading_type': 'gospel',
        'raw_ref': 'Matthew 6:14-18',
        'source_title': 'The Unction of the Sick',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Unction_of_Sick.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Seventh prayer Gospel.',
    },
    {
        'service_family': 'funeral',
        'service_variant': 'men_main',
        'section': 'part_1',
        'reading_type': 'pauline',
        'raw_ref': '1 Corinthians 15:1-23',
        'source_title': 'The Funeral Prayers',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Main funeral service for men.',
    },
    {
        'service_family': 'funeral',
        'service_variant': 'men_main',
        'section': 'part_1',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 65:4',
        'source_title': 'The Funeral Prayers',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Printed as Psalm (64) 65:4.',
    },
    {
        'service_family': 'funeral',
        'service_variant': 'men_main',
        'section': 'part_1',
        'reading_type': 'gospel',
        'raw_ref': 'John 5:19-29',
        'source_title': 'The Funeral Prayers',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Main funeral service for men.',
    },

    # Palm Sunday readings: vespers, procession stations, matins continuation, and Divine Liturgy.
    {
        'service_family': 'palm_sunday',
        'service_variant': 'vespers',
        'section': 'vespers',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 118:26-27',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Vespers Psalm for Palm Sunday; printed as Psalm (117) 118:26-27.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'vespers',
        'section': 'vespers',
        'reading_type': 'gospel',
        'raw_ref': 'John 12:1-11',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Vespers Gospel for Palm Sunday.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'procession',
        'section': 'procession_station_01_main_sanctuary',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 104:4; Psalm 138:1',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday procession station 1: Main Sanctuary; Psalm before the station Gospel.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'procession',
        'section': 'procession_station_01_main_sanctuary',
        'reading_type': 'gospel',
        'raw_ref': 'John 1:43-51',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday procession station 1: Main Sanctuary; station Gospel.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'procession',
        'section': 'procession_station_02_holy_virgin_st_mary',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 87:3,5,7',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday procession station 2: The Holy Virgin St. Mary; Psalm before the station Gospel.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'procession',
        'section': 'procession_station_02_holy_virgin_st_mary',
        'reading_type': 'gospel',
        'raw_ref': 'Luke 1:39-56',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday procession station 2: The Holy Virgin St. Mary; station Gospel.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'procession',
        'section': 'procession_station_03_archangel_gabriel',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 34:7-8',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday procession station 3: The Archangel Gabriel; Psalm before the station Gospel.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'procession',
        'section': 'procession_station_03_archangel_gabriel',
        'reading_type': 'gospel',
        'raw_ref': 'Luke 1:26-38',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday procession station 3: The Archangel Gabriel; station Gospel.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'procession',
        'section': 'procession_station_04_archangel_michael',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 103:20-21',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday procession station 4: The Archangel Michael; Psalm before the station Gospel.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'procession',
        'section': 'procession_station_04_archangel_michael',
        'reading_type': 'gospel',
        'raw_ref': 'Matthew 13:44-53',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday procession station 4: The Archangel Michael; station Gospel.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'procession',
        'section': 'procession_station_05_st_mark_evangelist',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 68:11-12',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday procession station 5: St. Mark the Evangelist; Psalm before the station Gospel.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'procession',
        'section': 'procession_station_05_st_mark_evangelist',
        'reading_type': 'gospel',
        'raw_ref': 'Luke 10:1-12',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday procession station 5: St. Mark the Evangelist; station Gospel.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'procession',
        'section': 'procession_station_06_holy_apostles',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 19:3-4',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday procession station 6: The Holy Apostles; Psalm before the station Gospel.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'procession',
        'section': 'procession_station_06_holy_apostles',
        'reading_type': 'gospel',
        'raw_ref': 'Matthew 10:1-8',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday procession station 6: The Holy Apostles; station Gospel.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'procession',
        'section': 'procession_station_07_st_george',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 97:11-12',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday procession station 7: St. George; Psalm before the station Gospel.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'procession',
        'section': 'procession_station_07_st_george',
        'reading_type': 'gospel',
        'raw_ref': 'Luke 21:12-19',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday procession station 7: St. George; station Gospel.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'procession',
        'section': 'procession_station_08_st_antony',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 68:35; Psalm 68:3',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday procession station 8: St. Antony; Psalm before the station Gospel.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'procession',
        'section': 'procession_station_08_st_antony',
        'reading_type': 'gospel',
        'raw_ref': 'Matthew 16:24-28',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday procession station 8: St. Antony; station Gospel.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'procession',
        'section': 'procession_station_09_northern_door',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 84:1-2',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday procession station 9: Northern Door; Psalm before the station Gospel.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'procession',
        'section': 'procession_station_09_northern_door',
        'reading_type': 'gospel',
        'raw_ref': 'Luke 13:22-30',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday procession station 9: Northern Door; station Gospel.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'procession',
        'section': 'procession_station_10_baptismal_font',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 29:3-4',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday procession station 10: Baptismal Font; Psalm before the station Gospel.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'procession',
        'section': 'procession_station_10_baptismal_font',
        'reading_type': 'gospel',
        'raw_ref': 'Matthew 3:13-17',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday procession station 10: Baptismal Font; station Gospel.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'procession',
        'section': 'procession_station_11_southern_door',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 118:19-20',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday procession station 11: Southern Door; Psalm before the station Gospel.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'procession',
        'section': 'procession_station_11_southern_door',
        'reading_type': 'gospel',
        'raw_ref': 'Matthew 21:1-11',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday procession station 11: Southern Door; station Gospel.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'procession',
        'section': 'procession_station_12_st_john_the_baptist',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 52:8',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday procession station 12: St. John the Baptist; Psalm before the station Gospel.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'procession',
        'section': 'procession_station_12_st_john_the_baptist',
        'reading_type': 'gospel',
        'raw_ref': 'Luke 7:28-35',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday procession station 12: St. John the Baptist; station Gospel.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'matins',
        'section': 'matins',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 68:19; Psalm 68:35',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Matins Psalm after Palm Sunday procession; printed as Psalm (67) 68:19,35.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'matins',
        'section': 'matins',
        'reading_type': 'gospel',
        'raw_ref': 'Luke 19:1-10',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Matins Gospel after Palm Sunday procession, Zacchaeus reading.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'liturgy',
        'section': 'liturgy_readings',
        'reading_type': 'pauline',
        'raw_ref': 'Hebrews 9:11-28',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday Divine Liturgy Pauline reading.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'liturgy',
        'section': 'liturgy_readings',
        'reading_type': 'catholic',
        'raw_ref': '1 Peter 4:1-11',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday Divine Liturgy Catholic Epistle.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'liturgy',
        'section': 'liturgy_readings',
        'reading_type': 'acts',
        'raw_ref': 'Acts 28:11-31',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday Divine Liturgy Praxis / Acts reading.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'liturgy',
        'section': 'first_gospel',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 81:3; Psalm 81:1; Psalm 81:2',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'First Psalm for Palm Sunday before the first Liturgy Gospel; printed as Psalm (80) 81:3,1,2.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'liturgy',
        'section': 'first_gospel',
        'reading_type': 'gospel',
        'raw_ref': 'Matthew 21:1-17',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'First Gospel for Palm Sunday Divine Liturgy.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'liturgy',
        'section': 'second_gospel',
        'reading_type': 'gospel',
        'raw_ref': 'Mark 11:1-11',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Second Gospel for Palm Sunday Divine Liturgy.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'liturgy',
        'section': 'third_gospel',
        'reading_type': 'gospel',
        'raw_ref': 'Luke 19:29-48',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Third Gospel for Palm Sunday Divine Liturgy.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'liturgy',
        'section': 'fourth_gospel',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 65:1-2',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Psalm before the fourth Gospel for Palm Sunday; printed as Psalm (64) 65:1,2.',
    },
    {
        'service_family': 'palm_sunday',
        'service_variant': 'liturgy',
        'section': 'fourth_gospel',
        'reading_type': 'gospel',
        'raw_ref': 'John 12:12-19',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Fourth Gospel for Palm Sunday Divine Liturgy.',
    },
    {
        'service_family': 'general_funeral',
        'service_variant': 'palm_sunday_general_funeral',
        'section': 'prophecy',
        'reading_type': 'old_testament',
        'raw_ref': 'Ezekiel 37:1-14',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'General Funeral prayed after Palm Sunday liturgy before Holy Pascha; prophecy reading in the Palm Sunday book.',
    },
    {
        'service_family': 'general_funeral',
        'service_variant': 'palm_sunday_general_funeral',
        'section': 'main_readings',
        'reading_type': 'pauline',
        'raw_ref': '1 Corinthians 15:1-27',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday General Funeral Pauline from the Palm Sunday book; extends beyond the separate men_main funeral book reading.',
    },
    {
        'service_family': 'general_funeral',
        'service_variant': 'palm_sunday_general_funeral',
        'section': 'main_readings',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 65:4-5',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Printed as Psalm (64) 65:4-5 in the Palm Sunday General Funeral section.',
    },
    {
        'service_family': 'general_funeral',
        'service_variant': 'palm_sunday_general_funeral',
        'section': 'main_readings',
        'reading_type': 'gospel',
        'raw_ref': 'John 5:19-29',
        'source_title': 'Rites and Readings of Palm Sunday, Procession and General Funeral',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Palm_Sunday_And_General_Funeral_Readings_Procession.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Palm Sunday General Funeral Gospel from the Palm Sunday book.',
    },
    {
        'service_family': 'funeral',
        'service_variant': 'men_passion_week',
        'section': 'at_burial_site_override',
        'reading_type': 'old_testament',
        'raw_ref': 'Genesis 50:4-25',
        'source_title': 'The Funeral Prayers',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Passion Week burial-site override. The rite explicitly says the Trisagion, Gospel litany, Psalm, and Gospel are then read as before.',
    },
    {
        'service_family': 'funeral',
        'service_variant': 'women_main',
        'section': 'part_2',
        'reading_type': 'pauline',
        'raw_ref': '1 Corinthians 15:39-49',
        'source_title': 'The Funeral Prayers',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Main funeral service for women.',
    },
    {
        'service_family': 'funeral',
        'service_variant': 'women_main',
        'section': 'part_2',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 116:7-8',
        'source_title': 'The Funeral Prayers',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Printed as Psalm (114) 116:7-8.',
    },
    {
        'service_family': 'funeral',
        'service_variant': 'women_main',
        'section': 'part_2',
        'reading_type': 'gospel',
        'raw_ref': 'Matthew 26:6-13',
        'source_title': 'The Funeral Prayers',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Main funeral service for women.',
    },
    {
        'service_family': 'funeral',
        'service_variant': 'women_passion_week',
        'section': 'at_burial_site_override',
        'reading_type': 'old_testament',
        'raw_ref': 'Genesis 23:1-20',
        'source_title': 'The Funeral Prayers',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Passion Week burial-site override for women; followed by Genesis 24:1-67 and then the Psalm/Gospel as before.',
    },
    {
        'service_family': 'funeral',
        'service_variant': 'women_passion_week',
        'section': 'at_burial_site_override',
        'reading_type': 'old_testament',
        'raw_ref': 'Genesis 24:1-67',
        'source_title': 'The Funeral Prayers',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Second Passion Week burial-site reading for women.',
    },
    {
        'service_family': 'funeral',
        'service_variant': 'women_delivery_main',
        'section': 'part_3',
        'reading_type': 'old_testament',
        'raw_ref': 'Isaiah 26:9-20',
        'source_title': 'The Funeral Prayers',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Funeral for women who depart during delivery.',
    },
    {
        'service_family': 'funeral',
        'service_variant': 'women_delivery_main',
        'section': 'part_3',
        'reading_type': 'pauline',
        'raw_ref': 'Romans 5:1-15',
        'source_title': 'The Funeral Prayers',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Funeral for women who depart during delivery.',
    },
    {
        'service_family': 'funeral',
        'service_variant': 'women_delivery_main',
        'section': 'part_3',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 78:38-39',
        'source_title': 'The Funeral Prayers',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Printed as Psalm (77) 78:38-39.',
    },
    {
        'service_family': 'funeral',
        'service_variant': 'women_delivery_main',
        'section': 'part_3',
        'reading_type': 'gospel',
        'raw_ref': 'John 16:20-23',
        'source_title': 'The Funeral Prayers',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Funeral for women who depart during delivery.',
    },
    {
        'service_family': 'funeral',
        'service_variant': 'women_delivery_passion_week',
        'section': 'at_burial_site_override',
        'reading_type': 'old_testament',
        'raw_ref': 'Genesis 23:1-20',
        'source_title': 'The Funeral Prayers',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Passion Week burial-site override for women who depart during delivery; followed by Genesis 24:1-67 and then the Psalm/Gospel as before.',
    },
    {
        'service_family': 'funeral',
        'service_variant': 'women_delivery_passion_week',
        'section': 'at_burial_site_override',
        'reading_type': 'old_testament',
        'raw_ref': 'Genesis 24:1-67',
        'source_title': 'The Funeral Prayers',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Second Passion Week burial-site reading for women who depart during delivery.',
    },
    {
        'service_family': 'funeral',
        'service_variant': 'male_children_main',
        'section': 'part_4',
        'reading_type': 'pauline',
        'raw_ref': '1 Thessalonians 4:13-18',
        'source_title': 'The Funeral Prayers',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Funeral service for male children.',
    },
    {
        'service_family': 'funeral',
        'service_variant': 'male_children_main',
        'section': 'part_4',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 27:10; Psalm 116:6',
        'source_title': 'The Funeral Prayers',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Printed as Psalms (26) 27:10 and (114) 116:6.',
    },
    {
        'service_family': 'funeral',
        'service_variant': 'male_children_main',
        'section': 'part_4',
        'reading_type': 'gospel',
        'raw_ref': 'Luke 7:11-16',
        'source_title': 'The Funeral Prayers',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Funeral service for male children.',
    },
    {
        'service_family': 'funeral',
        'service_variant': 'male_children_at_burial_site',
        'section': 'at_burial_site',
        'reading_type': 'old_testament',
        'raw_ref': '1 Kings 17:17-24',
        'source_title': 'The Funeral Prayers',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'At the burial site for male children.',
    },
    {
        'service_family': 'funeral',
        'service_variant': 'female_children_main',
        'section': 'part_5',
        'reading_type': 'pauline',
        'raw_ref': '1 Corinthians 15:50-58',
        'source_title': 'The Funeral Prayers',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Funeral service for female children.',
    },
    {
        'service_family': 'funeral',
        'service_variant': 'female_children_main',
        'section': 'part_5',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 39:12-13',
        'source_title': 'The Funeral Prayers',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Printed as Psalm (38) 39:12-13.',
    },
    {
        'service_family': 'funeral',
        'service_variant': 'female_children_main',
        'section': 'part_5',
        'reading_type': 'gospel',
        'raw_ref': 'Matthew 9:18-26',
        'source_title': 'The Funeral Prayers',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Funeral service for female children.',
    },
    {
        'service_family': 'funeral',
        'service_variant': 'female_children_passion_week',
        'section': 'at_burial_site_override',
        'reading_type': 'old_testament',
        'raw_ref': 'Judges 11:30-40',
        'source_title': 'The Funeral Prayers',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Passion Week burial-site override for female children.',
    },
    {
        'service_family': 'funeral',
        'service_variant': 'third_day_and_memorials',
        'section': 'part_6',
        'reading_type': 'pauline',
        'raw_ref': 'Romans 5:6-15',
        'source_title': 'The Funeral Prayers',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Third-day and other memorial prayers.',
    },
    {
        'service_family': 'funeral',
        'service_variant': 'third_day_and_memorials',
        'section': 'part_6',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 38:21-22',
        'source_title': 'The Funeral Prayers',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Printed as Psalm (37) 38:21-22.',
    },
    {
        'service_family': 'funeral',
        'service_variant': 'third_day_and_memorials',
        'section': 'part_6',
        'reading_type': 'gospel',
        'raw_ref': 'John 11:38-45',
        'source_title': 'The Funeral Prayers',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Readings_Funeral_Updated.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Third-day and other memorial prayers.',
    },
    {
        'service_family': 'pentecost_prostration',
        'service_variant': 'first_prostration',
        'section': 'main_readings',
        'reading_type': 'old_testament',
        'raw_ref': 'Deuteronomy 5:23-33; Deuteronomy 6:1-3',
        'source_title': 'Rites of the Prayers of Prostration',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Prostrations.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'First Pentecost prostration prophecy; summary page identifies the exact section.',
    },
    {
        'service_family': 'pentecost_prostration',
        'service_variant': 'first_prostration',
        'section': 'main_readings',
        'reading_type': 'pauline',
        'raw_ref': '1 Corinthians 12:28-31; 1 Corinthians 13:1-12',
        'source_title': 'Rites of the Prayers of Prostration',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Prostrations.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'First Pentecost prostration Pauline from the rite summary.',
    },
    {
        'service_family': 'pentecost_prostration',
        'service_variant': 'first_prostration',
        'section': 'main_readings',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 97:7-8; Psalm 97:1',
        'source_title': 'Rites of the Prayers of Prostration',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Prostrations.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Printed as Psalm 97:7,8,1 in the rite book.',
    },
    {
        'service_family': 'pentecost_prostration',
        'service_variant': 'first_prostration',
        'section': 'main_readings',
        'reading_type': 'gospel',
        'raw_ref': 'John 17:1-26',
        'source_title': 'Rites of the Prayers of Prostration',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Prostrations.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'First Pentecost prostration Gospel.',
    },
    {
        'service_family': 'pentecost_prostration',
        'service_variant': 'second_prostration',
        'section': 'main_readings',
        'reading_type': 'old_testament',
        'raw_ref': 'Deuteronomy 6:17-25',
        'source_title': 'Rites of the Prayers of Prostration',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Prostrations.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Second Pentecost prostration prophecy from the rite summary.',
    },
    {
        'service_family': 'pentecost_prostration',
        'service_variant': 'second_prostration',
        'section': 'main_readings',
        'reading_type': 'pauline',
        'raw_ref': '1 Corinthians 13:13-14:17',
        'source_title': 'Rites of the Prayers of Prostration',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Prostrations.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Second Pentecost prostration Pauline; exact line confirmed in the rite book.',
    },
    {
        'service_family': 'pentecost_prostration',
        'service_variant': 'second_prostration',
        'section': 'main_readings',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 115:12-13',
        'source_title': 'Rites of the Prayers of Prostration',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Prostrations.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Second Pentecost prostration Psalm.',
    },
    {
        'service_family': 'pentecost_prostration',
        'service_variant': 'second_prostration',
        'section': 'main_readings',
        'reading_type': 'gospel',
        'raw_ref': 'Luke 24:36-53',
        'source_title': 'Rites of the Prayers of Prostration',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Prostrations.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Second Pentecost prostration Gospel.',
    },
    {
        'service_family': 'pentecost_prostration',
        'service_variant': 'third_prostration',
        'section': 'main_readings',
        'reading_type': 'old_testament',
        'raw_ref': 'Deuteronomy 16:1-18',
        'source_title': 'Rites of the Prayers of Prostration',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Prostrations.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Third Pentecost prostration prophecy; exact section confirmed in the rite book.',
    },
    {
        'service_family': 'pentecost_prostration',
        'service_variant': 'third_prostration',
        'section': 'main_readings',
        'reading_type': 'pauline',
        'raw_ref': '1 Corinthians 14:18-40',
        'source_title': 'Rites of the Prayers of Prostration',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Prostrations.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Third Pentecost prostration Pauline from the rite summary.',
    },
    {
        'service_family': 'pentecost_prostration',
        'service_variant': 'third_prostration',
        'section': 'main_readings',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 66:4; Psalm 72:11',
        'source_title': 'Rites of the Prayers of Prostration',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Prostrations.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Third Pentecost prostration Psalm; exact line confirmed in the rite book.',
    },
    {
        'service_family': 'pentecost_prostration',
        'service_variant': 'third_prostration',
        'section': 'main_readings',
        'reading_type': 'gospel',
        'raw_ref': 'John 4:1-24',
        'source_title': 'Rites of the Prayers of Prostration',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Prostrations.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Third Pentecost prostration Gospel; exact line confirmed in the rite book.',
    },
    {
        'service_family': 'cornerstone_prayer',
        'service_variant': 'main',
        'section': 'foundation_cornerstone',
        'reading_type': 'old_testament',
        'raw_ref': 'Genesis 28:10-31',
        'source_title': 'Rites of Consecrations',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/consecrations-ar-en-cop.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Foundation cornerstone prophecy for a new church.',
    },
    {
        'service_family': 'cornerstone_prayer',
        'service_variant': 'main',
        'section': 'foundation_cornerstone',
        'reading_type': 'pauline',
        'raw_ref': 'Hebrews 9:1-10',
        'source_title': 'Rites of Consecrations',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/consecrations-ar-en-cop.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Foundation cornerstone Pauline.',
    },
    {
        'service_family': 'cornerstone_prayer',
        'service_variant': 'main',
        'section': 'foundation_cornerstone',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 127:1; Psalm 122:1-2',
        'source_title': 'Rites of Consecrations',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/consecrations-ar-en-cop.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Foundation cornerstone Psalm set printed before the Gospel reading.',
    },
    {
        'service_family': 'cornerstone_prayer',
        'service_variant': 'main',
        'section': 'foundation_cornerstone',
        'reading_type': 'gospel',
        'raw_ref': 'Luke 9:28-35',
        'source_title': 'Rites of Consecrations',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/consecrations-ar-en-cop.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Foundation cornerstone Gospel.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'consecration_day',
        'section': 'vespers',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 23:5-6',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 34-37',
        'notes': 'Printed as Psalm 22:5-6 in source numbering; quote matches Psalm 23:5-6 in modern numbering.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'consecration_day',
        'section': 'vespers',
        'reading_type': 'gospel',
        'raw_ref': 'Luke 23:50-56; Luke 24:1-12',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 34-37',
        'notes': 'Vespers Gospel on the Day of Consecration.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'consecration_day',
        'section': 'matins',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 51:12-13',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 34-37',
        'notes': 'Printed as Psalm 50:12-13 in source numbering; quote matches Psalm 51:12-13 in modern numbering.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'consecration_day',
        'section': 'matins',
        'reading_type': 'gospel',
        'raw_ref': 'Mark 16',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 34-37',
        'notes': 'Matins Gospel printed as Mark chapter 16 whole.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'consecration_day',
        'section': 'liturgy',
        'reading_type': 'pauline',
        'raw_ref': 'Hebrews 9:11-28; Hebrews 10:1-24',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 34-37',
        'notes': 'Pauline for the Day of Consecration.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'consecration_day',
        'section': 'liturgy',
        'reading_type': 'catholic',
        'raw_ref': '1 John 4:7-21; 1 John 5:1-21',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 34-37',
        'notes': 'Catholic Epistle for the Day of Consecration; visual extraction indicates 1 John 5:1-21 despite OCR noise.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'consecration_day',
        'section': 'liturgy',
        'reading_type': 'acts',
        'raw_ref': 'Acts 13:13-49',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 34-37',
        'notes': 'Acts / Praxis for the Day of Consecration.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'consecration_day',
        'section': 'liturgy',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 45:7-8',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 34-37',
        'notes': 'Printed as Psalm 44:10-11 in source numbering; quote matches Psalm 45:7-8 in modern numbering.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'consecration_day',
        'section': 'liturgy',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 89:20-21',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 34-37',
        'notes': 'Printed as Psalm 88:14-15 in source numbering; quote matches Psalm 89:20-21 in modern numbering.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'consecration_day',
        'section': 'liturgy',
        'reading_type': 'gospel',
        'raw_ref': 'John 19:38-42; John 20:1-18',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 34-37',
        'notes': 'Liturgy Gospel for the Day of Consecration.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'first_week_day_1',
        'section': 'matins',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 51:7-8',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 35-37',
        'notes': 'Printed as Psalm 50:7-8 in source numbering; quote matches Psalm 51:7-8.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'first_week_day_1',
        'section': 'matins',
        'reading_type': 'gospel',
        'raw_ref': 'John 1:18-42',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 35-37',
        'notes': 'Morning Gospel for first week day 1.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'first_week_day_1',
        'section': 'liturgy',
        'reading_type': 'pauline',
        'raw_ref': 'Hebrews 7:26-28; Hebrews 8; Hebrews 9:1-10',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 35-37',
        'notes': 'First week day 1 Pauline.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'first_week_day_1',
        'section': 'liturgy',
        'reading_type': 'catholic',
        'raw_ref': '1 Peter 3:8-22; 1 Peter 4:1-11',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 35-37',
        'notes': 'First week day 1 Catholic Epistle.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'first_week_day_1',
        'section': 'liturgy',
        'reading_type': 'acts',
        'raw_ref': 'Acts 18:24-28; Acts 19:1-20',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 35-37',
        'notes': 'First week day 1 Acts / Praxis.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'first_week_day_1',
        'section': 'liturgy',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 132:1',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 35-37',
        'notes': 'First week day 1 liturgy psalm; source numbering preserved as printed.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'first_week_day_1',
        'section': 'liturgy',
        'reading_type': 'gospel',
        'raw_ref': 'Matthew 26:6-13',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 35-37',
        'notes': 'First week day 1 liturgy Gospel.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'first_week_day_2',
        'section': 'matins',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 28:3-4',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 35-37',
        'notes': 'First week day 2 morning psalm; source numbering preserved as printed.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'first_week_day_2',
        'section': 'matins',
        'reading_type': 'gospel',
        'raw_ref': 'John 3:22-36; John 4:1-2',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 35-37',
        'notes': 'First week day 2 morning Gospel.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'first_week_day_2',
        'section': 'liturgy',
        'reading_type': 'pauline',
        'raw_ref': 'Hebrews 1:1-14; Hebrews 2:1-4',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 35-37',
        'notes': 'First week day 2 Pauline.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'first_week_day_2',
        'section': 'liturgy',
        'reading_type': 'catholic',
        'raw_ref': '1 Peter 1:10-25; 1 Peter 2:1-10',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 35-37',
        'notes': 'First week day 2 Catholic Epistle.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'first_week_day_2',
        'section': 'liturgy',
        'reading_type': 'acts',
        'raw_ref': 'Acts 2:22-47; Acts 3:1-10',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 35-37',
        'notes': 'First week day 2 Acts / Praxis.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'first_week_day_2',
        'section': 'liturgy',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 129:2-5',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 35-37',
        'notes': 'First week day 2 liturgy psalm; source numbering preserved as printed.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'first_week_day_2',
        'section': 'liturgy',
        'reading_type': 'gospel',
        'raw_ref': 'Mark 14:3-9',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 35-37',
        'notes': 'First week day 2 liturgy Gospel.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'first_week_day_3',
        'section': 'matins',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 31:1-2',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 35-37',
        'notes': 'First week day 3 morning psalm; source numbering preserved as printed.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'first_week_day_3',
        'section': 'matins',
        'reading_type': 'gospel',
        'raw_ref': 'John 3:1-21',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 35-37',
        'notes': 'First week day 3 morning Gospel.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'first_week_day_3',
        'section': 'liturgy',
        'reading_type': 'pauline',
        'raw_ref': 'Titus 2:11-15; Titus 3:1-7',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 35-37',
        'notes': 'First week day 3 Pauline.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'first_week_day_3',
        'section': 'liturgy',
        'reading_type': 'catholic',
        'raw_ref': '1 John 5:5-13',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 35-37',
        'notes': 'First week day 3 Catholic Epistle.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'first_week_day_3',
        'section': 'liturgy',
        'reading_type': 'acts',
        'raw_ref': 'Acts 8:26-39',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 35-37',
        'notes': 'First week day 3 Acts / Praxis.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'first_week_day_3',
        'section': 'liturgy',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 65:1; Psalm 65:6',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 35-37',
        'notes': 'First week day 3 liturgy psalm.',
    },
    {
        'service_family': 'myron_consecration',
        'service_variant': 'first_week_day_3',
        'section': 'liturgy',
        'reading_type': 'gospel',
        'raw_ref': 'Matthew 28:16-20',
        'source_title': 'Meron and Galileon Rite (Arabic)',
        'source_url': 'https://copticbook.wordpress.com/wp-content/uploads/2023/06/meron-and-galileon-ar.pdf',
        'source_page': 'OCR + visual extraction from pages 35-37',
        'notes': 'First week day 3 liturgy Gospel.',
    },
    {
        'service_family': 'home_blessing',
        'service_variant': 'main',
        'section': 'main_readings',
        'reading_type': 'pauline',
        'raw_ref': 'Romans 8:14-21',
        'source_title': 'Rites of Blessing Houses',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Blessing_Houses.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Main Pauline for house blessing.',
    },
    {
        'service_family': 'home_blessing',
        'service_variant': 'main',
        'section': 'main_readings',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 102:1-2',
        'source_title': 'Rites of Blessing Houses',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Blessing_Houses.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Printed as Psalm 102:1-2.',
    },
    {
        'service_family': 'home_blessing',
        'service_variant': 'main',
        'section': 'main_readings',
        'reading_type': 'gospel',
        'raw_ref': 'Luke 19:1-10',
        'source_title': 'Rites of Blessing Houses',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Blessing_Houses.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Main Gospel for house blessing.',
    },
    {
        'service_family': 'liturgy_of_the_waters',
        'service_variant': 'epiphany_laqan',
        'section': 'prophecies',
        'reading_type': 'old_testament',
        'raw_ref': 'Habakkuk 3:2-19',
        'source_title': 'Coptic Reader: Theophany - Liturgy of the Waters',
        'source_url': 'https://copticreader.org/',
        'source_page': 'sources/coptic-reader/theophany-liturgy-of-the-waters-2026-07-12/readings-09-15.jpg',
        'notes': 'Prophecy shown in the Theophany Laqan service; screenshot supplied by George on 2026-07-12.',
    },
    {
        'service_family': 'liturgy_of_the_waters',
        'service_variant': 'epiphany_laqan',
        'section': 'prophecies',
        'reading_type': 'old_testament',
        'raw_ref': 'Isaiah 35:1-2',
        'source_title': 'Coptic Reader: Theophany - Liturgy of the Waters',
        'source_url': 'https://copticreader.org/',
        'source_page': 'sources/coptic-reader/theophany-liturgy-of-the-waters-2026-07-12/readings-09-15.jpg',
        'notes': 'Prophecy shown in the Theophany Laqan service; screenshot supplied by George on 2026-07-12.',
    },
    {
        'service_family': 'liturgy_of_the_waters',
        'service_variant': 'epiphany_laqan',
        'section': 'prophecies',
        'reading_type': 'old_testament',
        'raw_ref': 'Isaiah 40:1-5',
        'source_title': 'Coptic Reader: Theophany - Liturgy of the Waters',
        'source_url': 'https://copticreader.org/',
        'source_page': 'sources/coptic-reader/theophany-liturgy-of-the-waters-2026-07-12/readings-09-15.jpg',
        'notes': 'Prophecy shown in the Theophany Laqan service; screenshot supplied by George on 2026-07-12.',
    },
    {
        'service_family': 'liturgy_of_the_waters',
        'service_variant': 'epiphany_laqan',
        'section': 'prophecies',
        'reading_type': 'old_testament',
        'raw_ref': 'Isaiah 9:1-2',
        'source_title': 'Coptic Reader: Theophany - Liturgy of the Waters',
        'source_url': 'https://copticreader.org/',
        'source_page': 'sources/coptic-reader/theophany-liturgy-of-the-waters-2026-07-12/readings-09-15.jpg',
        'notes': 'Prophecy shown in the Theophany Laqan service; screenshot supplied by George on 2026-07-12.',
    },
    {
        'service_family': 'liturgy_of_the_waters',
        'service_variant': 'epiphany_laqan',
        'section': 'prophecies',
        'reading_type': 'old_testament',
        'raw_ref': 'Baruch 3:36-4:4',
        'source_title': 'Coptic Reader: Theophany - Liturgy of the Waters',
        'source_url': 'https://copticreader.org/',
        'source_page': 'sources/coptic-reader/theophany-liturgy-of-the-waters-2026-07-12/readings-09-15.jpg',
        'notes': 'Prophecy shown in the Theophany Laqan service; screenshot supplied by George on 2026-07-12.',
    },
    {
        'service_family': 'liturgy_of_the_waters',
        'service_variant': 'epiphany_laqan',
        'section': 'prophecies',
        'reading_type': 'old_testament',
        'raw_ref': 'Ezekiel 36:24-29',
        'source_title': 'Coptic Reader: Theophany - Liturgy of the Waters',
        'source_url': 'https://copticreader.org/',
        'source_page': 'sources/coptic-reader/theophany-liturgy-of-the-waters-2026-07-12/readings-09-15.jpg',
        'notes': 'Prophecy shown in the Theophany Laqan service; screenshot supplied by George on 2026-07-12.',
    },
    {
        'service_family': 'liturgy_of_the_waters',
        'service_variant': 'epiphany_laqan',
        'section': 'prophecies',
        'reading_type': 'old_testament',
        'raw_ref': 'Ezekiel 47:1-9',
        'source_title': 'Coptic Reader: Theophany - Liturgy of the Waters',
        'source_url': 'https://copticreader.org/',
        'source_page': 'sources/coptic-reader/theophany-liturgy-of-the-waters-2026-07-12/readings-09-15.jpg',
        'notes': 'Prophecy shown in the Theophany Laqan service; screenshot supplied by George on 2026-07-12.',
    },
    {
        'service_family': 'liturgy_of_the_waters',
        'service_variant': 'epiphany_laqan',
        'section': 'main_readings',
        'reading_type': 'pauline',
        'raw_ref': '1 Corinthians 10:1-13',
        'source_title': 'Rites of Laqan for the Feast of Theophany (Epiphany)',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Laqan_Epiphany.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Main Pauline for the Epiphany Laqan / waters rite.',
    },
    {
        'service_family': 'liturgy_of_the_waters',
        'service_variant': 'epiphany_laqan',
        'section': 'main_readings',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 114:3; Psalm 114:5',
        'source_title': 'Rites of Laqan for the Feast of Theophany (Epiphany)',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Laqan_Epiphany.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Printed as Psalm 114 (113):3,5.',
    },
    {
        'service_family': 'liturgy_of_the_waters',
        'service_variant': 'epiphany_laqan',
        'section': 'main_readings',
        'reading_type': 'gospel',
        'raw_ref': 'Matthew 3:1-17',
        'source_title': 'Rites of Laqan for the Feast of Theophany (Epiphany)',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Laqan_Epiphany.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Main Gospel for the Epiphany Laqan / waters rite.',
    },
    {
        'service_family': 'liturgy_of_the_waters',
        'service_variant': 'apostles_feast_laqan',
        'section': 'prophecies',
        'reading_type': 'old_testament',
        'raw_ref': 'Exodus 15:22-16:1',
        'source_title': 'Coptic Reader: Apostles Feast - Liturgy of the Waters',
        'source_url': 'https://copticreader.org/',
        'source_page': 'sources/coptic-reader/apostles-feast-liturgy-of-the-waters-2026-07-12/readings-09-15.jpg',
        'notes': 'Prophecy shown in the Apostles Feast Laqan service; screenshot supplied by George on 2026-07-12.',
    },
    {
        'service_family': 'liturgy_of_the_waters',
        'service_variant': 'apostles_feast_laqan',
        'section': 'prophecies',
        'reading_type': 'old_testament',
        'raw_ref': 'Exodus 30:17-30',
        'source_title': 'Coptic Reader: Apostles Feast - Liturgy of the Waters',
        'source_url': 'https://copticreader.org/',
        'source_page': 'sources/coptic-reader/apostles-feast-liturgy-of-the-waters-2026-07-12/readings-09-15.jpg',
        'notes': 'Prophecy shown in the Apostles Feast Laqan service; screenshot supplied by George on 2026-07-12.',
    },
    {
        'service_family': 'liturgy_of_the_waters',
        'service_variant': 'apostles_feast_laqan',
        'section': 'prophecies',
        'reading_type': 'old_testament',
        'raw_ref': 'Isaiah 1:16-26',
        'source_title': 'Coptic Reader: Apostles Feast - Liturgy of the Waters',
        'source_url': 'https://copticreader.org/',
        'source_page': 'sources/coptic-reader/apostles-feast-liturgy-of-the-waters-2026-07-12/readings-09-15.jpg',
        'notes': 'Prophecy shown in the Apostles Feast Laqan service; screenshot supplied by George on 2026-07-12.',
    },
    {
        'service_family': 'liturgy_of_the_waters',
        'service_variant': 'apostles_feast_laqan',
        'section': 'prophecies',
        'reading_type': 'old_testament',
        'raw_ref': 'Isaiah 35:1-10',
        'source_title': 'Coptic Reader: Apostles Feast - Liturgy of the Waters',
        'source_url': 'https://copticreader.org/',
        'source_page': 'sources/coptic-reader/apostles-feast-liturgy-of-the-waters-2026-07-12/readings-09-15.jpg',
        'notes': 'Prophecy shown in the Apostles Feast Laqan service; screenshot supplied by George on 2026-07-12.',
    },
    {
        'service_family': 'liturgy_of_the_waters',
        'service_variant': 'apostles_feast_laqan',
        'section': 'prophecies',
        'reading_type': 'old_testament',
        'raw_ref': 'Isaiah 43:16-44:6',
        'source_title': 'Coptic Reader: Apostles Feast - Liturgy of the Waters',
        'source_url': 'https://copticreader.org/',
        'source_page': 'sources/coptic-reader/apostles-feast-liturgy-of-the-waters-2026-07-12/readings-09-15.jpg',
        'notes': 'Prophecy shown in the Apostles Feast Laqan service; screenshot supplied by George on 2026-07-12.',
    },
    {
        'service_family': 'liturgy_of_the_waters',
        'service_variant': 'apostles_feast_laqan',
        'section': 'prophecies',
        'reading_type': 'old_testament',
        'raw_ref': 'Zechariah 8:7-19',
        'source_title': 'Coptic Reader: Apostles Feast - Liturgy of the Waters',
        'source_url': 'https://copticreader.org/',
        'source_page': 'sources/coptic-reader/apostles-feast-liturgy-of-the-waters-2026-07-12/readings-09-15.jpg',
        'notes': 'Prophecy shown in the Apostles Feast Laqan service; screenshot supplied by George on 2026-07-12.',
    },
    {
        'service_family': 'liturgy_of_the_waters',
        'service_variant': 'apostles_feast_laqan',
        'section': 'prophecies',
        'reading_type': 'old_testament',
        'raw_ref': 'Zechariah 14:8-11',
        'source_title': 'Coptic Reader: Apostles Feast - Liturgy of the Waters',
        'source_url': 'https://copticreader.org/',
        'source_page': 'sources/coptic-reader/apostles-feast-liturgy-of-the-waters-2026-07-12/readings-09-15.jpg',
        'notes': 'Prophecy shown in the Apostles Feast Laqan service; screenshot supplied by George on 2026-07-12.',
    },
    {
        'service_family': 'liturgy_of_the_waters',
        'service_variant': 'apostles_feast_laqan',
        'section': 'main_readings',
        'reading_type': 'pauline',
        'raw_ref': 'Hebrews 10:22-38',
        'source_title': 'Coptic Reader: Apostles Feast - Liturgy of the Waters',
        'source_url': 'https://copticreader.org/',
        'source_page': 'sources/coptic-reader/apostles-feast-liturgy-of-the-waters-2026-07-12/readings-21-32.jpg',
        'notes': 'Pauline reading shown in the Apostles Feast Laqan service; screenshot supplied by George on 2026-07-12.',
    },
    {
        'service_family': 'liturgy_of_the_waters',
        'service_variant': 'apostles_feast_laqan',
        'section': 'main_readings',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 51:7; Psalm 51:10',
        'source_title': 'Coptic Reader: Apostles Feast - Liturgy of the Waters',
        'source_url': 'https://copticreader.org/',
        'source_page': 'sources/coptic-reader/apostles-feast-liturgy-of-the-waters-2026-07-12/readings-27-35.jpg',
        'notes': 'Displayed by Coptic Reader as Psalms 51:7, 10; source numbering preserved.',
    },
    {
        'service_family': 'liturgy_of_the_waters',
        'service_variant': 'apostles_feast_laqan',
        'section': 'main_readings',
        'reading_type': 'gospel',
        'raw_ref': 'John 5:1-18',
        'source_title': 'Coptic Reader: Apostles Feast - Liturgy of the Waters',
        'source_url': 'https://copticreader.org/',
        'source_page': 'sources/coptic-reader/apostles-feast-liturgy-of-the-waters-2026-07-12/readings-27-35.jpg',
        'notes': 'Gospel reading shown in the Apostles Feast Laqan service; screenshot supplied by George on 2026-07-12.',
    },
    {
        'service_family': 'church_consecration',
        'service_variant': 'main',
        'section': 'part_1',
        'reading_type': 'pauline',
        'raw_ref': 'Hebrews 9:1-10',
        'source_title': 'Rites of Consecration of Churches, Altars and Vessels',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Book-2_Consecration.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Main Pauline in church consecration section.',
    },
    {
        'service_family': 'church_consecration',
        'service_variant': 'main',
        'section': 'part_1',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 127:1; Psalm 122:1-2',
        'source_title': 'Rites of Consecration of Churches, Altars and Vessels',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Book-2_Consecration.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Printed as Psalm (126) 127:1 and Psalm (121) 122:1,2.',
    },
    {
        'service_family': 'church_consecration',
        'service_variant': 'main',
        'section': 'part_1',
        'reading_type': 'gospel',
        'raw_ref': 'Luke 9:28-35',
        'source_title': 'Rites of Consecration of Churches, Altars and Vessels',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Book-2_Consecration.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Main Gospel in church consecration section.',
    },
    {
        'service_family': 'altar_consecration',
        'service_variant': 'main',
        'section': 'part_3',
        'reading_type': 'pauline',
        'raw_ref': 'Hebrews 13:10-16',
        'source_title': 'Rites of Consecration of Churches, Altars and Vessels',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Book-2_Consecration.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Main Pauline in altar consecration section.',
    },
    {
        'service_family': 'altar_consecration',
        'service_variant': 'main',
        'section': 'part_3',
        'reading_type': 'psalm',
        'raw_ref': 'Psalm 23; Psalm 24; Psalm 26; Psalm 27; Psalm 85; Psalm 93',
        'source_title': 'Rites of Consecration of Churches, Altars and Vessels',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Book-2_Consecration.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'The altar consecration section explicitly gives a psalm set across the two incense offerings before the Pauline and Gospel.',
    },
    {
        'service_family': 'altar_consecration',
        'service_variant': 'main',
        'section': 'part_3',
        'reading_type': 'gospel',
        'raw_ref': 'Luke 19:1-10',
        'source_title': 'Rites of Consecration of Churches, Altars and Vessels',
        'source_url': 'https://saintbishoy.ca/wp-content/uploads/Rites_Book-2_Consecration.pdf',
        'source_page': SOURCE_ST_BISHOY_PAGE,
        'notes': 'Main Gospel in altar consecration section.',
    },
]


FIXTURE_DIR = Path(__file__).resolve().parent / 'sources/coptic-reader/special-reconciled-2026-10-07'
FIXTURE_MANIFEST_SHA256 = '44b75adac4ef6b45d3d46ac2f51cf8b1ad356b9ebeb0ab37d7dd5c4ad5f40284'
READER_NOTE_PREFIX = 'Coptic Reader assigned block; evidence='


def load_reader_fixture(directory: Path = FIXTURE_DIR) -> tuple[dict, list[dict]]:
    """Fail closed on changed primary bytes, context inventory or assigned headings."""
    data = (directory / 'manifest.json').read_bytes()
    if hashlib.sha256(data).hexdigest() != FIXTURE_MANIFEST_SHA256:
        raise RuntimeError('special Reader manifest source drift')
    manifest = json.loads(data)
    for name, expected_hash in manifest['files'].items():
        if hashlib.sha256((directory / name).read_bytes()).hexdigest() != expected_hash:
            raise RuntimeError(f'special Reader source drift: {name}')
    oracle = json.loads((directory / 'assigned-scripture-oracle.json').read_text())
    documents = json.loads((directory / 'document-dispositions.json').read_text())
    if len(documents) != manifest['document_count']:
        raise RuntimeError('special Reader document inventory drift')
    doc_by_id = {d['provenance']['captureId']: d for d in documents}
    if len(doc_by_id) != len(documents):
        raise RuntimeError('special Reader duplicate document context')
    texts = {key: (directory / 'raw' / f'{key}.txt').read_text() for key in doc_by_id}
    for block in oracle:
        p = block['provenance']
        doc = doc_by_id[p['captureId']]
        text = texts[p['captureId']]
        if (p['navigation'] != doc['path'] or
                text.splitlines()[block['lineNumber'] - 1] != block['rawHeading'] or
                not text[block['characterOffset']:].startswith(block['rawHeading'])):
            raise RuntimeError('special Reader assigned heading/context drift')
    assigned = [b for b in oracle if b['kind'] == 'assigned_scripture_reading']
    if len(assigned) != manifest['assigned_reading_count']:
        raise RuntimeError('special Reader assigned count drift')
    for context in manifest['contexts']:
        blocks = [b for b in assigned if b['provenance']['navigation'] == context['navigation']]
        if (len(blocks) != context['assigned_count'] or
                any(b['provenance']['captureId'] != context['capture_id'] for b in blocks) or
                [b['lineNumber'] for b in blocks] != sorted(b['lineNumber'] for b in blocks)):
            raise RuntimeError('special Reader assigned order/context inventory drift')
    return manifest, oracle


READER_MANIFEST, READER_ORACLE = load_reader_fixture()
LEGACY_ROWS = [dict(row) for row in ROWS]
BOUNDARY_CORRECTIONS = {
    (c['service_family'], c['service_variant'], c['reading_type'], c['expected_raw_ref']): c
    for c in READER_MANIFEST['boundary_corrections']
}
for correction_key in BOUNDARY_CORRECTIONS:
    if sum((r['service_family'], r['service_variant'], r['reading_type'], r['raw_ref']) == correction_key
           for r in LEGACY_ROWS) != 1:
        raise RuntimeError('special Reader boundary correction target drift')


def reader_ref_for_index(printed_ref: str) -> str:
    # Expand an omitted book after a semicolon, not a Psalm number or verse.
    # The shared tokenizer otherwise silently loses "122:1-2" in the Cornerstone Psalm.
    book = re.match(r'^((?:[1-4] )?[A-Za-z][A-Za-z ]*?)\s+\d', printed_ref)
    if not book:
        raise RuntimeError(f'special Reader unrecognized printed reference: {printed_ref}')
    return '; '.join(f'{book.group(1)} {part.strip()}'
                     if index > 0 and re.match(r'^\d+(?=[:;,]|$)', part.strip())
                     else part.strip() for index, part in enumerate(printed_ref.split(';')))


def reader_section(block: dict) -> str:
    """Keep explicit multi-liturgy stages; do not equate them to legacy day variants."""
    text = (FIXTURE_DIR / 'raw' / f"{block['provenance']['captureId']}.txt").read_text()
    prior = text.splitlines()[:block['lineNumber'] - 1]
    stages = ['First Liturgy', 'Second Liturgy', 'Third Liturgy']
    services = ['Offering of Evening Incense', 'Offering of Morning Incense', 'Liturgy of the Word']
    stage = next((line for line in reversed(prior) if line in stages), '')
    service = next((line for line in reversed(prior) if line in services), '')
    return re.sub(r'[^a-z0-9]+', '_', ' '.join([stage, service]).lower()).strip('_') or 'rendered_document'


def reader_reading_type(block: dict) -> str:
    reference = block['printedRef']
    if reference.startswith(('Psalm ', 'Psalms ')):
        return 'psalm'
    if reference.startswith('Acts '):
        return 'acts'
    if reference.startswith(('James ', '1 Peter ', '2 Peter ', '1 John ', '2 John ', '3 John ', 'Jude ')):
        return 'catholic'
    if reference.startswith(('Matthew ', 'Mark ', 'Luke ', 'John ')):
        # Church consecration includes split Magnificat/Benedictus/Simeon canticles.
        if 'Church' in block['provenance']['navigation'] and reference.startswith(('Luke 1:', 'Luke 2:29')):
            return 'canticle'
        return 'gospel'
    if reference.startswith(('Romans ', '1 Corinthians ', '2 Corinthians ', 'Galatians ', 'Ephesians ',
                             'Philippians ', 'Colossians ', '1 Timothy ', '2 Timothy ', 'Titus ', 'Hebrews ')):
        return 'pauline'
    return 'old_testament' if not reference.startswith('Revelation ') else 'revelation'


def build_reader_rows() -> list[dict]:
    rows = []
    for context in READER_MANIFEST['contexts']:
        for block in READER_ORACLE:
            if (block['kind'] != 'assigned_scripture_reading' or
                    block['provenance']['navigation'] != context['navigation']):
                continue
            p = block['provenance']
            evidence = {
                'navigation': p['navigation'], 'capture_id': p['captureId'],
                'ordinal': block['ordinalWithinDocument'], 'line': block['lineNumber'],
                'raw_heading': block['rawHeading'], 'raw_text_sha256': p['rawTextSha256'],
                'numbering': p['numberingConvention'], 'status': 'source_confirmed_assigned',
                'dedicated_reference_screenshot': block['referenceScreenshotAvailable'],
            }
            rows.append({
                'service_family': context['service_family'], 'service_variant': context['service_variant'],
                'section': reader_section(block), 'reading_type': reader_reading_type(block),
                'raw_ref': block['printedRef'],
                'source_title': 'Coptic Reader: ' + ' / '.join(p['navigation']),
                'source_url': p['sourceUrl'],
                'source_page': f"sources/coptic-reader/special-reconciled-2026-10-07/raw/{p['captureId']}.txt#line={block['lineNumber']}",
                'notes': READER_NOTE_PREFIX + json.dumps(evidence, ensure_ascii=False, sort_keys=True),
            })
    return rows


def validate_reader_rows(rows: list[dict]) -> None:
    """Independent captured oracle controls count, order, endpoints and source context."""
    actual = [r for r in rows if r['service_variant'].startswith('coptic_reader__')]
    expected = build_reader_rows()
    # All existing schema fields participate, including provenance/status in notes.
    if actual != expected:
        raise RuntimeError('special Reader assigned readings omitted/reordered/truncated/wrong context or status')


ROWS += build_reader_rows()


PROJECTION_DIR = ROOT / 'sources/coptic-reader/special-context-projection-2026-10-07'
PROJECTION_MANIFEST_SHA256 = 'cad392515629f98d3685ba0c1f0f8254d1c3d420c398b82ce3a9bc1a24e03c4d'
PROJECTION_MARKER = '; projection='


def load_projection_fixture(directory: Path = PROJECTION_DIR) -> list[dict]:
    data = (directory / 'manifest.json').read_bytes()
    if hashlib.sha256(data).hexdigest() != PROJECTION_MANIFEST_SHA256:
        raise RuntimeError('special projection manifest source drift')
    manifest = json.loads(data)
    for name, expected in manifest['files'].items():
        if hashlib.sha256((directory / name).read_bytes()).hexdigest() != expected:
            raise RuntimeError(f'special projection source drift: {name}')
    records = json.loads((directory / 'records.json').read_text())
    if len(records) != manifest['records']:
        raise RuntimeError('special projection inventory drift')
    identities = set()
    for record in records:
        identity = (record['capture_id'], record['ordinal'])
        if identity in identities:
            raise RuntimeError('special projection duplicate source identity')
        identities.add(identity)
        text = (directory / 'raw' / (record['capture_id'] + '.txt')).read_text()
        if (text.splitlines()[record['line'] - 1] != record['raw_heading'] or
                not text[record['offset']:].startswith(record['raw_heading'])):
            raise RuntimeError('special projection heading/context drift')
    return records


def projection_metadata(row: dict) -> dict | None:
    return json.loads(row['notes'].split(PROJECTION_MARKER, 1)[1]) if PROJECTION_MARKER in row['notes'] else None


def projection_note(meta: dict) -> str:
    meta['projection_status'] = meta['status']
    meta['status'] = 'current' if meta['is_active'] else 'removed'
    meta['active'] = meta['is_active']
    meta['include_in_current_index'] = meta['is_active']
    meta['state'] = 'current' if meta['is_active'] else ('superseded' if meta['projection_status'] in {'superseded', 'coalesced_attestation'} else 'held')
    if not meta['is_active']:
        meta['removal_reason'] = '; '.join(meta['reasons'])
        meta['removal_effective_version'] = 'special-context-projection-2026-10-07'
    return json.dumps(meta, ensure_ascii=False, sort_keys=True)


def _project_special_contexts_base() -> list[dict]:
    """Retain literal history; join by pinned navigation, never passage alone.

    Unclassified rubrics and unaligned Psalm coordinates fail closed in the index.
    """
    records = load_projection_fixture()
    legacy = [dict(row) for row in LEGACY_ROWS]
    history = {}
    projected = []
    for record in records:
        navigation = record['navigation']
        target = record['legacy_context']
        family = target[0] if target else next((c['service_family'] for c in READER_MANIFEST['contexts']
                                               if c['navigation'] == navigation),
                                              'wedding_crowning' if 'Crowning' in navigation else 'special_service')
        variant = target[1] if target else re.sub(r'[^a-z0-9]+', '_', '_'.join(navigation[1:]).lower()).strip('_')
        kind = record['reading_type']
        candidates = [(i, r) for i, r in enumerate(legacy)
                      if target and [r['service_family'], r['service_variant']] == target
                      and r['reading_type'] == kind]
        if len(candidates) > 1:
            # Reference equality only disambiguates inside an already proved
            # rite/navigation + reading-rubric join; never a cross-rite join.
            exact = [(i, r) for i, r in candidates
                     if canonicalize_text_ref(r['raw_ref']) ==
                     canonicalize_text_ref(reader_ref_for_index(record['printed_ref']))]
            if len(exact) == 1:
                candidates = exact
        section = candidates[0][1]['section'] if len(candidates) == 1 else record['section']
        reasons = []
        if not record['selected']:
            reasons.append('older_capture_attestation_not_additional_occurrence')
        if not record['date_verified']:
            reasons.append('date_context_unqualified')
        if record['kind'] != 'assigned_scripture_reading':
            reasons.append(record['kind'])
        if kind == 'unclassified':
            reasons.append('source_rubric_unclassified')
        if kind == 'psalm' and not record['canonical_mt_ref']:
            reasons.append('canonical_psalm_coordinates_held')
        canonical = record['canonical_mt_ref'] if kind == 'psalm' else canonicalize_text_ref(reader_ref_for_index(record['printed_ref']))
        if not is_current_source_row(record):
            reasons.append('parent_source_ineligible')
        meta = dict({key: record[key] for key in PROJECTION_SOURCE_FIELDS if key in record},
                    is_active=not reasons, status='current' if not reasons else 'held',
                    reasons=reasons, canonical_ref=canonical if kind != 'psalm' or record['canonical_mt_ref'] else '',
                    legacy_attestations=[])
        if record['selected'] and record['kind'] == 'assigned_scripture_reading' and len(candidates) == 1:
            i, old = candidates[0]
            same = canonicalize_text_ref(reader_ref_for_index(record['printed_ref'])) == canonicalize_text_ref(old['raw_ref'])
            meta['legacy_attestations'] = [dict(old)]
            history[i] = {'is_active': False, 'status': 'coalesced_attestation' if same else 'superseded',
                          'reasons': ['context_qualified_reader_authority'], 'replacement_capture': record['capture_id'],
                          'replacement_ordinal': record['ordinal'], 'navigation': navigation,
                          'canonical_ref': ''}
        projected.append({'service_family': family, 'service_variant': variant,
                          'section': section, 'reading_type': kind, 'raw_ref': record['printed_ref'],
                          'source_title': 'Coptic Reader: ' + ' / '.join(navigation),
                          'source_url': 'https://copticreader.org/app/#/document',
                          'source_page': f"sources/coptic-reader/special-context-projection-2026-10-07/raw/{record['capture_id']}.txt#line={record['line']}",
                          'notes': 'Source-bound appointment evidence' + PROJECTION_MARKER + projection_note(meta)})
    joined = {tuple(r['legacy_context']) for r in records if r['legacy_context']}
    for i, row in enumerate(legacy):
        meta = history.get(i)
        if meta is None:
            ambiguous = (row['service_family'], row['service_variant']) in joined or row['service_family'] in {'myron_consecration', 'church_consecration', 'altar_consecration'}
            meta = {'is_active': not ambiguous and row['reading_type'] != 'psalm',
                    'status': 'held' if ambiguous or row['reading_type'] == 'psalm' else 'legacy_current',
                    'reasons': ['legacy_stage_join_unproven'] if ambiguous else (['legacy_psalm_coordinates_unqualified'] if row['reading_type'] == 'psalm' else []),
                    'canonical_ref': '' if ambiguous or row['reading_type'] == 'psalm' else canonicalize_text_ref(row['raw_ref'])}
        row['notes'] += PROJECTION_MARKER + projection_note(meta)
    return legacy + projected


# Only source evidence fields may cross the projection boundary. Eligibility is
# evaluated on the original payload before these producer-controlled fields exist.
PROJECTION_SOURCE_FIELDS = (
    'capture_id', 'navigation', 'ordinal', 'line', 'offset', 'raw_heading',
    'printed_ref', 'raw_text_sha256', 'context', 'kind', 'reading_type', 'rubric',
    'section', 'selected', 'legacy_context', 'canonical_mt_ref',
    'normalization_proof', 'date_verified',
)
CLASSIFICATION_DIR = ROOT / 'sources/coptic-reader/special-classification-integration-2026-10-07'
CLASSIFICATION_MANIFEST_SHA256 = 'bf09f32ef23d7feddb6c8ecf08d5b2dcd7034ba9addfb25e8b438443526141d9'


def load_classification_overlay(directory: Path = CLASSIFICATION_DIR) -> dict:
    data = (directory / 'manifest.json').read_bytes()
    if hashlib.sha256(data).hexdigest() != CLASSIFICATION_MANIFEST_SHA256:
        raise RuntimeError('special classification manifest source drift')
    manifest = json.loads(data)
    for name, expected in manifest['files'].items():
        if hashlib.sha256((directory / name).read_bytes()).hexdigest() != expected:
            raise RuntimeError(f'special classification source drift: {name}')
    classifications = json.loads((directory / 'source-classification-verdicts.json').read_text())
    stages = json.loads((directory / 'stage-join-verdicts.json').read_text())
    records = load_projection_fixture()
    by_identity = {(r['capture_id'], r['ordinal']): r for r in records}

    def verify_evidence(proof: dict, lines: list[dict]) -> dict:
        record = by_identity[(proof['capture_id'], proof['ordinal'])]
        if (record['navigation'] != proof['navigation'] or record['section'] != proof['section'] or
                record['printed_ref'] != proof['printed_ref'] or record['raw_text_sha256'] != proof['sha256']):
            raise RuntimeError('special classification stage/context drift')
        # Resolve source locally rather than trusting a personal absolute pointer.
        raw = PROJECTION_DIR / 'raw' / (proof['capture_id'] + '.txt')
        if hashlib.sha256(raw.read_bytes()).hexdigest() != proof['sha256']:
            raise RuntimeError('special classification primary source drift')
        text = raw.read_text().splitlines()
        if any(text[line['line'] - 1] != line['text'] for line in lines):
            raise RuntimeError('special classification rubric drift')
        return record

    if len(classifications) != manifest['classifications'] or len({(p['capture_id'], p['ordinal']) for p in classifications}) != len(classifications):
        raise RuntimeError('special classification inventory drift')
    for proof in classifications:
        record = verify_evidence(proof, proof['evidence'] + proof['governing_rubric'])
        if (record['kind'] != 'assigned_scripture_reading' or record['reading_type'] != 'unclassified' or
                proof['classification'] != 'assigned_reading' or proof['confidence'] != 'confirmed'):
            raise RuntimeError('special classification assignment drift')
    if sum(p['verdict'] == 'proven_stage_assigned_reading' for p in stages) != manifest['stage_joins']:
        raise RuntimeError('special stage join inventory drift')
    for proof in stages:
        old = LEGACY_ROWS[proof['legacy_row']]  # review row identifiers are zero-based
        if ([old['service_family'], old['service_variant'], old['section']] != proof['legacy_context'] or
                old['raw_ref'] != proof['legacy_raw_ref'] or old['reading_type'] != proof['reading_type']):
            raise RuntimeError('special legacy stage source drift')
        for evidence in proof['reader_evidence']:
            verify_evidence(evidence, evidence['lines'])
    return {'manifest': manifest, 'classifications': classifications, 'stages': stages}


def _replace_projection_metadata(row: dict, meta: dict) -> None:
    # Drop only producer state; retained primary metadata and literal notes survive.
    for key in ('active', 'include_in_current_index', 'state', 'removal_reason', 'removal_effective_version', 'projection_status'):
        meta.pop(key, None)
    row['notes'] = row['notes'].split(PROJECTION_MARKER)[0] + PROJECTION_MARKER + projection_note(meta)


def _required_projection_metadata(row: dict) -> dict:
    meta = projection_metadata(row)
    if meta is None:
        raise RuntimeError('missing special projection metadata')
    return meta


def project_special_contexts() -> list[dict]:
    rows = _project_special_contexts_base()
    overlay = load_classification_overlay()
    sources = {(_required_projection_metadata(r)['capture_id'], _required_projection_metadata(r)['ordinal']): r for r in rows[len(LEGACY_ROWS):]}
    for proof in overlay['classifications']:
        row = sources[(proof['capture_id'], proof['ordinal'])]
        meta = _required_projection_metadata(row)
        row['reading_type'] = meta['reading_type'] = proof['proposed_reading_type']
        meta['assignment_proof'] = {key: proof[key] for key in ('capture_id', 'ordinal', 'navigation', 'printed_ref', 'section', 'sha256', 'classification', 'proposed_reading_type', 'evidence', 'governing_rubric', 'confidence')}
        meta['reasons'].remove('source_rubric_unclassified')
        # Assignment approval does not supply an edition/coordinate crosswalk.
        if row['raw_ref'].startswith('Sirach '):
            meta['source_edition'] = 'unverified_source_edition'
            meta['reasons'].append('deuterocanonical_edition_coordinates_held')
            meta['canonical_ref'] = ''
        meta['is_active'] = not meta['reasons'] and is_current_source_row(row)
        meta['status'] = 'current' if meta['is_active'] else 'held'
        _replace_projection_metadata(row, meta)

    for proof in overlay['stages']:
        index = proof['legacy_row']
        old = rows[index]
        old_meta = _required_projection_metadata(old)
        stage_proof = {key: proof[key] for key in ('legacy_row', 'legacy_context', 'legacy_raw_ref', 'reading_type', 'verdict', 'confidence', 'canonical_psalm_coordinates_approved', 'note', 'reader_evidence', 'official_book_pages', 'official_book_evidence_file') if key in proof}
        old_meta.update(is_active=False, canonical_ref='', stage_join_proof=stage_proof)
        if proof['verdict'] == 'unresolved_reader_join':
            old_meta.update(status='held', reasons=['unresolved_reader_join'])
        elif proof['verdict'] == 'proven_prescribed_psalm_prayers_not_assigned_lessons':
            old_meta.update(status='prescribed_prayer', kind='prescribed_psalm_prayer', reasons=['prescribed_psalm_prayer_not_assigned_reading'])
        else:
            evidence, = proof['reader_evidence']
            target = sources[(evidence['capture_id'], evidence['ordinal'])]
            target_meta = _required_projection_metadata(target)
            # The exact capture+ordinal+stage proof controls, not book/ref similarity.
            if (not target_meta['selected'] or target_meta['kind'] != 'assigned_scripture_reading' or
                    target['reading_type'] != proof['reading_type']):
                raise RuntimeError('special stage target is not selected assigned evidence')
            if LEGACY_ROWS[index] in target_meta['legacy_attestations']:
                raise RuntimeError('special duplicate legacy stage attestation')
            target_meta['legacy_attestations'].append(dict(LEGACY_ROWS[index]))
            same = canonicalize_text_ref(old['raw_ref']) == canonicalize_text_ref(reader_ref_for_index(evidence['printed_ref']))
            conflict = 'source_book_conflict' if index == 144 else ('same_reference' if same else 'source_qualified_literal_reference_difference')
            old_meta.update(status='coalesced_attestation' if same else 'superseded', reasons=['context_qualified_reader_authority'],
                            replacement_capture=evidence['capture_id'], replacement_ordinal=evidence['ordinal'],
                            navigation=evidence['navigation'], conflict_type=conflict, authoritative_printed_ref=evidence['printed_ref'])
            target_meta.setdefault('stage_join_proofs', []).append(stage_proof)
            if index == 144:
                target_meta.setdefault('source_conflicts', []).append({'legacy_row': index, 'legacy_raw_ref': old['raw_ref'],
                    'authoritative_printed_ref': evidence['printed_ref'], 'conflict_type': conflict,
                    'authority': 'Coptic Reader', 'body_proof': 'independent-timothy-proof.json'})
            target_meta['status'] = target_meta['projection_status']
            _replace_projection_metadata(target, target_meta)
        _replace_projection_metadata(old, old_meta)
    return rows


def validate_projection_rows(rows: list[dict]) -> None:
    if rows != project_special_contexts():
        raise RuntimeError('special projection omitted/reordered/changed context, canonical reference or active state')


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if not DISABLE_VAULT_PUBLISH:
        VAULT.mkdir(parents=True, exist_ok=True)


def ordered_reader_ref(printed_ref: str) -> str:
    """Keep ordered components, not the canonical verse-set serialization."""
    expanded = reader_ref_for_index(printed_ref)
    if ';' not in expanded:
        return canonicalize_text_ref(expanded)
    components = [part.strip() for part in expanded.split(';')]
    parsed = [parse_passage(part) for part in components]
    # Keep the historically supported multi-book tokenizer lane separate.
    if all(part and part.parts for part in parsed) and len({part.book_abbrev for part in parsed if part is not None}) > 1:
        return canonicalize_text_ref(expanded)
    if parse_passage(expanded) is None:
        raise ValueError('Malformed complete Reader reference: ' + printed_ref)
    return '; '.join(dict.fromkeys(canonicalize_text_ref(part) for part in components))


def canonicalize_row_refs(row: Dict[str, str]) -> Dict[str, str]:
    row = dict(row)
    if not is_current_source_row(row):
        row['canonical_ref'] = ''
        return row
    projection = projection_metadata(row)
    if projection is not None:
        row['canonical_ref'] = projection['canonical_ref'] if projection['is_active'] and is_current_source_row(projection) else ''
        return row
    key = (row['service_family'], row['service_variant'], row['reading_type'], row['raw_ref'])
    correction = BOUNDARY_CORRECTIONS.get(key)
    effective_ref = correction['corrected_ref'] if correction else row['raw_ref']
    if row['service_variant'].startswith('coptic_reader__'):
        row['canonical_ref'] = ordered_reader_ref(effective_ref)
    else:
        row['canonical_ref'] = canonicalize_text_ref(effective_ref)
    if correction:
        # Preserve raw source and the old provenance; disclose the bound supersession.
        note = '; Reader boundary supersession=' + json.dumps(correction, ensure_ascii=False, sort_keys=True)
        if note not in row['notes']:
            row['notes'] += note
    return row


def build_passage_index(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    out: List[Dict[str, str]] = []
    for row in rows:
        if not is_current_source_row(row):
            continue
        projection = projection_metadata(row)
        if projection is not None and (not projection['is_active'] or not is_current_source_row(projection)):
            continue
        base = canonicalize_row_refs(row)
        seen = set()
        key = (base['service_family'], base['service_variant'], base['reading_type'], base['raw_ref'])
        indexed_ref = (base['canonical_ref'] if projection is not None or key in BOUNDARY_CORRECTIONS or
                       base['service_variant'].startswith('coptic_reader__') else base['raw_ref'])
        for seg in extract_text_ref_tokens(indexed_ref):
            normalized = canonicalize_text_ref(seg)
            if not normalized:
                continue
            key = (base['service_family'], base['service_variant'], base['section'], base['reading_type'], normalized)
            if key in seen:
                continue
            seen.add(key)
            out.append({
                'service_family': base['service_family'],
                'service_variant': base['service_variant'],
                'section': base['section'],
                'reading_type': base['reading_type'],
                'raw_ref': base['raw_ref'],
                'canonical_ref': base['canonical_ref'],
                'matched_ref': normalized,
                'source_title': base['source_title'],
                'source_url': base['source_url'],
                'source_page': base['source_page'],
                'notes': base['notes'],
                'source_kind': 'special_service',
            })
    return out


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    if not rows:
        path.write_text('', encoding='utf-8')
        return
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def write_jsonl(path: Path, rows: List[Dict[str, str]]) -> None:
    with path.open('w', encoding='utf-8') as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')


def main() -> None:
    load_reader_fixture()
    validate_reader_rows(ROWS)
    projected = project_special_contexts()
    validate_projection_rows(projected)
    ensure_dirs()
    curated = [canonicalize_row_refs(r) for r in projected]
    pidx = build_passage_index(projected)
    write_csv(OUT / 'special_service_readings_curated.csv', curated)
    write_jsonl(OUT / 'special_service_readings_curated.jsonl', curated)
    write_csv(OUT / 'special_service_passage_index.csv', pidx)
    write_jsonl(OUT / 'special_service_passage_index.jsonl', pidx)
    if not DISABLE_VAULT_PUBLISH:
        write_csv(VAULT / 'special_service_readings_curated.csv', curated)
        write_csv(VAULT / 'special_service_passage_index.csv', pidx)
    print(json.dumps({'curated_rows': len(curated), 'passage_rows': len(pidx)}, indent=2))


if __name__ == '__main__':
    main()
