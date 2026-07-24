# Yogurting Translation

Decoded, decrypted client data tables (CLTs) from Yogurting, laid out and
organized for community translation. Everything here starts out in
Japanese; the goal is to get it translated into English and, eventually,
other languages too.

Yogurting's client packs all of its text data (item names, descriptions,
area names, quest text, and so on) into encrypted binary tables called
CLTs. This repo has those tables already decrypted and parsed into plain
CSVs with real column names, so you don't need to touch any of the
extraction/decryption side to help translate -- just open a CSV and start
translating.

## What's in here

- `CLT_Master/clt_decoded/` -- the 64 tables in their raw decrypted binary
  form. You won't need to edit these directly; they're here as the
  canonical source and for anyone who wants to rebuild a patched client
  table later.
- `CLT_Master/clt_csv_source/` -- the same 64 tables, parsed into CSVs with
  real column names. This is what you actually work from. See
  [`CLT_Master/README.md`](CLT_Master/README.md) for the full table-by-table
  breakdown of which columns in which files actually have translatable text
  (a lot of the tables are pure numeric/config data with nothing to
  translate).
- `translations/<lang>/` -- translated CSVs go here, one folder per
  language (e.g. `translations/en/`, `translations/es/`). This is what
  contributions add.

## How to contribute a translation

1. Pick a table from `CLT_Master/clt_csv_source/` that still needs
   translating -- check the coverage table in `CLT_Master/README.md` for
   which columns actually have translatable text.
2. Copy it into `translations/<your-language-code>/<TABLE_NAME>.csv`
   (use a normal short language code -- `en`, `es`, `de`, `fr`, `pt-br`,
   etc.). If the file's already there, just open it and keep going.
3. Translate the text columns in place. Leave everything else exactly as
   it is:
   - Don't touch id/index/numeric columns, or column headers.
   - Don't reorder or remove rows.
   - Keep placeholders and tags exactly as they appear --
     things like `$1`, `%s`, `%d`, `[26]`, `<br>`, `<font ...>` are
     substituted or rendered by the client at runtime and need to stay
     intact for the line to work in-game.
   - If a line doesn't make sense out of context, leave a `# TODO:` note
     as a comment above it (or ask in the PR) rather than guessing.
4. Open a PR. Partial files are fine -- you don't need to finish an entire
   table in one go, and multiple people can split up a big table across
   separate PRs.

If you're starting a language that doesn't have a folder yet, just create
`translations/<code>/` with your first file -- no need to ask first.

## A couple of notes

- Files are plain UTF-8 CSV. Any normal spreadsheet editor (LibreOffice
  Calc, Google Sheets, Excel) or text editor works fine -- just make sure
  whatever you use doesn't change the file's encoding or quoting when you
  save.
- The biggest tables by far are `COITEM_TYPE` (item names/descriptions,
  ~9,300 rows) and `ITEM_BYUL_TYPE` (~3,300 rows) -- good places to look if
  you want to split work across a few people.
- This repo exists for fan translation and preservation. It contains data
  extracted from Yogurting's own client; no ownership over the original
  game or its assets is claimed here.
