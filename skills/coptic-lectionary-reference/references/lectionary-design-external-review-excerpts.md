# Lectionary design external-review excerpt handoff

Use this when the requester asks for read-only external review content from generated lectionary design artifacts, especially `coptic-lectionary-and-synaxarium.md`.

## Trigger

the requester asks to print sections verbatim for external review, attribution checking, or copy/paste handoff.

## Workflow

1. Treat the request as read-only. Do not edit, regenerate, stage, or commit anything.
2. Read the generated artifact from the repo state, not from memory or prior chat text.
3. Output the requested excerpt verbatim, including the exact Markdown headings as rendered in the file.
4. If the requester asks for source attribution, add a separate attribution checklist after the verbatim excerpt.
5. In the checklist, map each structural claim to the named source cited by the article, using the article's own source wording.
6. If a claim is not directly cited in the same sentence or paragraph, say that plainly instead of inventing an attribution.
7. Keep the response plain-text/copyable. Avoid summaries, paraphrase, or extra commentary.

## Pitfalls

- Do not silently improve wording in a verbatim excerpt.
- Do not omit headings when the requester asks for sections.
- Do not treat source-list entries as proof for uncited body claims unless the body text itself cites them.
- Do not make a file-system change just because the article has an obvious issue. For read-only review, report only what is present.
