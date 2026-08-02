#!/usr/bin/env python3
"""Structural validation for translations/<lang>/*.csv against the source
tables in CLT_Master/clt_csv_source/. Run with no arguments; exits non-zero
if any hard error is found. This is what the "Validate translations" GitHub
Actions check runs on every PR.

Checks per file:
  - valid UTF-8
  - header matches the source table's header exactly
  - same row count as the source table
  - no ragged rows (every row has the same column count as the header --
    almost always means an unescaped comma/quote broke the CSV)
  - non-translatable columns (anything not in TRANSLATABLE_COLUMNS for that
    table) are byte-identical to the source, so ids/flags/numeric fields
    can't get edited by accident
  - no U+FFFD replacement characters (encoding corruption)
  - known hard character limits (see CHARACTER_LIMITS.md) aren't exceeded

Soft/inferred limits from CHARACTER_LIMITS.md are reported as warnings, not
failures, since they're not confirmed client buffer sizes.
"""

import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = REPO_ROOT / "CLT_Master" / "clt_csv_source"
TRANSLATIONS_DIR = REPO_ROOT / "translations"

# Which columns are expected to actually be translated per table (matches
# the coverage table in CLT_Master/README.md). Everything else in a table's
# header must stay byte-identical to the source row.
TRANSLATABLE_COLUMNS = {
    "AREA_INFO": {"description", "level_range", "location", "name"},
    "BEITEM_TYPE": {"desc", "name"},
    "COITEM_TYPE": {"desc", "extra", "name"},
    "EPISODE": {"t1", "t2", "t3", "t4"},
    "EPISODE_MONSTER": {"name"},
    "ITEM_BYUL_TYPE": {"desc", "name"},
    "ITEM_CHARGED_TYPE": {"desc1", "desc2"},
    "LOBBY": {"desc", "name"},
    "MATCHING_EMOTICON": {"text"},
    "MATCHING_SYS_MSG": {"id_code", "s1", "s2"},
    "MATCHING_UNIQUEMON_SPECIAL_EFFECT": {"name"},
    "MON": {"name"},
    "MONSTER_BASIS": {"name"},
    "NOTIFY_MSG": {"text"},
    "PROMOTE_COND": {"description", "requirement", "title"},
    "QUEST_EX": {"notice_text", "objective_text", "reward_text", "title"},
    "QUEST_ITEM_TYPE": {"description", "name"},
    "QUEST_NPC": {"location", "name"},
    "SCHOOL": {"name"},
    "SKILL_WEAPON": {"description", "name"},
    "SKL_Desc": {"description", "name"},
    "SKL_Desc2": {"text"},
    "SPECIAL_REWARD": {"name"},
    "STATE_CHANGE": {"name"},
    "TITLE": {"condition", "description", "name"},
}

# Confirmed client buffer sizes (character counts, not bytes -- see
# CHARACTER_LIMITS.md). Exceeding these is a hard failure.
HARD_LIMITS = {
    ("AREA_INFO", "name"): 32,
    ("AREA_INFO", "location"): 28,
    ("AREA_INFO", "level_range"): 50,
    ("AREA_INFO", "description"): 300,
    ("BEITEM_TYPE", "name"): 32,
    ("BEITEM_TYPE", "desc"): 1024,
    ("EPISODE", "t1"): 28,
    ("EPISODE", "t2"): 1024,
    ("EPISODE", "t3"): 512,
    ("EPISODE", "t4"): 24,
    ("EPISODE_MONSTER", "name"): 32,
    ("ITEM_CHARGED_TYPE", "desc1"): 1024,
    ("ITEM_CHARGED_TYPE", "desc2"): 1024,
    ("MATCHING_EMOTICON", "text"): 255,
    ("MON", "name"): 32,
    ("MONSTER_BASIS", "name"): 32,
}

# Inferred/ambiguous limits -- reported as warnings only, never fail CI.
SOFT_LIMITS = {
    ("COITEM_TYPE", "name"): 64,
    ("COITEM_TYPE", "desc"): 1024,
    ("COITEM_TYPE", "extra"): 64,
    ("ITEM_BYUL_TYPE", "name"): 32,
    ("ITEM_BYUL_TYPE", "desc"): 1045,
    ("LOBBY", "name"): 28,
    ("LOBBY", "desc"): 128,
    ("MATCHING_SYS_MSG", "id_code"): 32,
    ("MATCHING_SYS_MSG", "s1"): 128,
    ("MATCHING_SYS_MSG", "s2"): 1029,
}


def read_csv(path):
    with path.open(encoding="utf-8") as f:
        r = csv.reader(f)
        header = next(r)
        rows = list(r)
    return header, rows


def validate_file(pr_path):
    table = pr_path.stem
    src_path = SOURCE_DIR / f"{table}.csv"

    errors = []
    warnings = []

    if not src_path.exists():
        errors.append(f"no matching source table CLT_Master/clt_csv_source/{table}.csv -- "
                       f"translated file must be named after a real table")
        return table, errors, warnings

    try:
        pr_header, pr_rows = read_csv(pr_path)
    except UnicodeDecodeError as e:
        errors.append(f"file is not valid UTF-8: {e}")
        return table, errors, warnings

    src_header, src_rows = read_csv(src_path)

    if pr_header != src_header:
        errors.append(f"header does not match source: got {pr_header}, expected {src_header}")
        return table, errors, warnings

    if len(pr_rows) != len(src_rows):
        errors.append(f"row count mismatch: {len(pr_rows)} rows vs {len(src_rows)} in source "
                       f"(don't add/remove/reorder rows)")

    ragged = [i for i, row in enumerate(pr_rows) if len(row) != len(pr_header)]
    if ragged:
        errors.append(f"ragged rows at 0-indexed data rows {ragged[:15]}"
                       f"{' ...' if len(ragged) > 15 else ''} -- almost always an unescaped "
                       f"comma or quote inside a translated cell; wrap that field in double "
                       f"quotes")

    translatable = TRANSLATABLE_COLUMNS.get(table, set())
    n = min(len(pr_rows), len(src_rows))
    changed_locked_cells = []
    for col_idx, col_name in enumerate(pr_header):
        if col_name in translatable:
            continue
        for i in range(n):
            if col_idx < len(pr_rows[i]) and col_idx < len(src_rows[i]):
                if pr_rows[i][col_idx] != src_rows[i][col_idx]:
                    changed_locked_cells.append((i, col_name))
    if changed_locked_cells:
        errors.append(f"non-translatable column(s) changed at {len(changed_locked_cells)} "
                       f"cell(s), e.g. row {changed_locked_cells[0][0]} column "
                       f"'{changed_locked_cells[0][1]}' -- only columns "
                       f"{sorted(translatable) or '(none)'} should be edited in this table")

    mojibake_rows = [i for i, row in enumerate(pr_rows) for cell in row if "�" in cell]
    if mojibake_rows:
        errors.append(f"replacement character (U+FFFD) found at rows {mojibake_rows[:10]} -- "
                       f"usually a sign of an encoding mismatch when the file was saved")

    for col_idx, col_name in enumerate(pr_header):
        hard_cap = HARD_LIMITS.get((table, col_name))
        soft_cap = SOFT_LIMITS.get((table, col_name))
        for i, row in enumerate(pr_rows):
            if col_idx >= len(row):
                continue
            length = len(row[col_idx])
            if hard_cap is not None and length > hard_cap:
                errors.append(f"row {i} column '{col_name}' is {length} characters, over the "
                               f"confirmed {hard_cap}-character client limit")
            elif soft_cap is not None and length > soft_cap:
                warnings.append(f"row {i} column '{col_name}' is {length} characters, over the "
                                 f"inferred {soft_cap}-character limit (not a confirmed client "
                                 f"buffer size, but worth double-checking)")

    return table, errors, warnings


def main():
    if not TRANSLATIONS_DIR.exists():
        print("No translations/ directory found -- nothing to validate.")
        return 0

    csv_files = sorted(TRANSLATIONS_DIR.glob("*/*.csv"))
    if not csv_files:
        print("No translation CSVs found -- nothing to validate.")
        return 0

    had_errors = False
    for path in csv_files:
        lang = path.parent.name
        table, errors, warnings = validate_file(path)
        label = f"translations/{lang}/{table}.csv"
        if errors:
            had_errors = True
            print(f"::error::{label}: FAILED")
            for e in errors:
                print(f"  - {e}")
        if warnings:
            print(f"::warning::{label}: {len(warnings)} warning(s)")
            for w in warnings:
                print(f"  - {w}")
        if not errors and not warnings:
            print(f"{label}: OK")

    if had_errors:
        print("\nValidation failed -- see errors above.")
        return 1

    print("\nAll translation files passed validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
