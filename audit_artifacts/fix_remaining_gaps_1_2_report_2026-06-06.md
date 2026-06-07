# Fix Remaining Lectionary Gaps 1 and 2 - 2026-06-06
## Status

- Gap 1: fixed. Pascha source-text index now has 277 parsed rows and 0 unparsed rows.
- Gap 2: resolved as verified local absence. `4 Maccabees 1:1-12` parses as `4Macc 1:1-12`, but no local source, crosswalk, or generated occurrence supports a lectionary placement. No row was invented.

## Changed scripts
- `/Users/georgeandraws/workspace/coptic-lectionary-research/passage_normalization.py` — sha256 `755c6f5f6882c055c568b97714878b3fcd36f843be36c1d89e33ab240395d239` size 19634
- `/Users/georgeandraws/workspace/coptic-lectionary-research/verify_lectionary_queries.py` — sha256 `8742c8a0cc68769df9055e6a1b7534c1399ef377469e8b0b8e7c59c584562b4c` size 20112
- `/Users/georgeandraws/workspace/coptic-lectionary-research/out/scripts/passage_normalization.py` — sha256 `755c6f5f6882c055c568b97714878b3fcd36f843be36c1d89e33ab240395d239` size 19634

## Generated artifacts checked/rebuilt
- `/Users/georgeandraws/workspace/coptic-lectionary-research/out/data/pascha_source_text_index.csv` — rows 277 sha256 `6bf91980d448440a7421822fef12852f514f0a74155d1b3b624492902bd9da50`
- `/Users/georgeandraws/workspace/coptic-lectionary-research/out/data/pascha_source_text_index.jsonl` — rows None sha256 `4898269a0634f95e393411d9d875d687be872c3e4c23ee751b7dc5d6e5efcffc`
- `/Users/georgeandraws/workspace/coptic-lectionary-research/out/data/reverse_lookup_crosswalk.csv` — rows 66492 sha256 `1afecd134e2b73e42ed67b932967a15966b8f3b862dbf55185c739e3e50cb8e2`
- `/Users/georgeandraws/workspace/coptic-lectionary-research/out/data/reverse_lookup_summary.csv` — rows 2657 sha256 `5160bfb3308ac9950d3ff8da2c04d477c4bbb69f8174ebf63af2d9ba3eaebcc0`
- `/Users/georgeandraws/workspace/coptic-lectionary-research/out/data/bible_chapter_lectionary_index.csv` — rows 1351 sha256 `ac89f50b9eacda8434e8b2fe1b35f7b038b68a4fafc8eadf12ba209dd6cb8386`
- `/Users/georgeandraws/workspace/coptic-lectionary-research/out/data/bible_chapter_lectionary_occurrences.csv` — rows 71268 sha256 `2d598ef87ab1feb5bc867a825b14396568b6af96ad138140900b2c50474aac54`

## Vault-published artifacts checked
- `/Users/georgeandraws/Library/CloudStorage/GoogleDrive-georgeandraws@gmail.com/My Drive/HermesAI/obsidian-vault/Hermes/04-Reference/Coptic Orthodox Lessons/References/Lectionary/Coptic Orthodox Lectionary Reference/data/pascha_source_text_index.csv` — rows 277 sha256 `6bf91980d448440a7421822fef12852f514f0a74155d1b3b624492902bd9da50`
- `/Users/georgeandraws/Library/CloudStorage/GoogleDrive-georgeandraws@gmail.com/My Drive/HermesAI/obsidian-vault/Hermes/04-Reference/Coptic Orthodox Lessons/References/Lectionary/Coptic Orthodox Lectionary Reference/data/pascha_source_text_index.jsonl` — sha256 `4898269a0634f95e393411d9d875d687be872c3e4c23ee751b7dc5d6e5efcffc`
- `/Users/georgeandraws/Library/CloudStorage/GoogleDrive-georgeandraws@gmail.com/My Drive/HermesAI/obsidian-vault/Hermes/04-Reference/Coptic Orthodox Lessons/References/Lectionary/Coptic Orthodox Lectionary Reference/data/reverse_lookup_crosswalk.csv` — rows 66492 sha256 `1afecd134e2b73e42ed67b932967a15966b8f3b862dbf55185c739e3e50cb8e2`
- `/Users/georgeandraws/Library/CloudStorage/GoogleDrive-georgeandraws@gmail.com/My Drive/HermesAI/obsidian-vault/Hermes/04-Reference/Coptic Orthodox Lessons/References/Lectionary/Coptic Orthodox Lectionary Reference/data/reverse_lookup_summary.csv` — rows 2657 sha256 `5160bfb3308ac9950d3ff8da2c04d477c4bbb69f8174ebf63af2d9ba3eaebcc0`
- `/Users/georgeandraws/Library/CloudStorage/GoogleDrive-georgeandraws@gmail.com/My Drive/HermesAI/obsidian-vault/Hermes/04-Reference/Coptic Orthodox Lessons/References/Lectionary/Coptic Orthodox Lectionary Reference/data/bible_chapter_lectionary_index.csv` — rows 1351 sha256 `ac89f50b9eacda8434e8b2fe1b35f7b038b68a4fafc8eadf12ba209dd6cb8386`
- `/Users/georgeandraws/Library/CloudStorage/GoogleDrive-georgeandraws@gmail.com/My Drive/HermesAI/obsidian-vault/Hermes/04-Reference/Coptic Orthodox Lessons/References/Lectionary/Coptic Orthodox Lectionary Reference/data/bible_chapter_lectionary_occurrences.csv` — rows 71268 sha256 `2d598ef87ab1feb5bc867a825b14396568b6af96ad138140900b2c50474aac54`
- `/Users/georgeandraws/Library/CloudStorage/GoogleDrive-georgeandraws@gmail.com/My Drive/HermesAI/obsidian-vault/Hermes/04-Reference/Coptic Orthodox Lessons/References/Lectionary/Coptic Orthodox Lectionary Reference/scripts/passage_normalization.py` — sha256 `755c6f5f6882c055c568b97714878b3fcd36f843be36c1d89e33ab240395d239`
- `/Users/georgeandraws/Library/CloudStorage/GoogleDrive-georgeandraws@gmail.com/My Drive/HermesAI/obsidian-vault/Hermes/04-Reference/Coptic Orthodox Lessons/References/Lectionary/Coptic Orthodox Lectionary Reference/scripts/query_lectionary.py` — sha256 `d1d2f9893d3f54bc5114d8cd7f404c4739938e176768d36afb82a3004f2c630f`

## Verification evidence
```json
{
  "pascha_source_text_fully_parsed": {
    "rows": 277,
    "parsed_rows": 277,
    "unparsed_rows": 0,
    "cross_chapter_repairs_verified": [
      "Great Thursday | Eleventh Hour | Zech 12:11-14:3,14:6-9",
      "Great Thursday | Liturgy of Blessing of the Water | Isa 55:1-56:1",
      "Monday Eve | Third Hour | Zeph 1:14-2:2",
      "Monday | First Hour | Gen 1:1-2:3"
    ]
  },
  "four_maccabees_local_absence": {
    "parser_canonical": "4Macc 1:1-12",
    "query_rows": 0,
    "source_text_rows": 0,
    "indexed_source_hits": 0,
    "chapter_index_status": {
      "testament": "Deuterocanonical",
      "book": "4 Maccabees",
      "book_abbrev": "4Macc",
      "chapter": "1",
      "chapter_ref": "4Macc 1",
      "is_read": "no",
      "occurrence_count": "0",
      "source_kinds": "",
      "liturgical_places": "",
      "service_sections": "",
      "reading_types": "",
      "sample_occurrences": ""
    },
    "classification": "verified_absent_from_local_lectionary_sources_not_parser_gap"
  }
}
```

## Query evidence

### source_text_genesis_cross_chapter
```text
Monday | First Hour | Prophecy | Gen 1:1-2:3 | raw=Genesis 1:1-2:1-3 | source=out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:2579 page=106

```

### source_text_zephaniah_cross_chapter
```text
Monday Eve | Third Hour | Prophecy | Zeph 1:14-2:2 | raw=Zephaniah 1:14-2:1-2 | source=out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:1967 page=80

```

### source_text_isaiah_cross_chapter
```text
Great Thursday | Liturgy of Blessing of the Water | Prophecy | Isa 55:1-56:1 | raw=Isaiah 55:1-13-56:1 | source=out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:10774 page=426

```

### source_text_zechariah_cross_chapter
```text
Great Thursday | Eleventh Hour | Prophecy | Zech 12:11-14:3,14:6-9 | raw=Zechariah 12:11-14:1-3, 6-9 | source=out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:11882 page=466
Good Friday | Ninth Hour | Prophecy | Zech 14:6-11 | raw=Zechariah 14:6-11 | source=out/sources/St_Mary_Ottawa_Katameros_Holy_Pascha_EN.txt:15745 page=609

```

### four_maccabees_passage
```text
[no rows returned]
```

### four_maccabees_source_text
```text
[no rows returned]
```

## Remaining gaps

- None for requested gaps 1 and 2. 4 Maccabees remains absent from the local lectionary corpus by evidence, not unresolved due to parser failure.
