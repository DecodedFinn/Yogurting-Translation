# Character Limits by Table/Column

Read this before translating anything long. Some of these fields are fixed-size
buffers on the client side -- go over the limit and the text either gets cut
off or (worse) overflows into other data. Others have no real per-field limit
at all. They're not the same, and it matters which one you're editing.

## Quick guidance

- If a column below has a **character limit**, treat it as hard. That number
  comes from the actual buffer size in the client's code, minus 1 character
  for the string terminator. Don't write past it, even if the CSV would
  technically accept more text.
- If a column is marked **unbounded**, there's no per-field buffer capping it
  -- but see "the catch" below, because that doesn't mean unlimited in
  practice.
- If a limit is marked **inferred** or **not confirmed**, it's a best guess,
  not something read directly off a real buffer size. Stay well under it to
  be safe.
- English is usually shorter than Japanese for the same idea, so most fields
  give you *more* headroom once translated, not less. The tight ones to
  actually watch are short fixed fields (names, single-line labels).

## The catch: file size still has a ceiling

Even "unbounded" columns aren't free. Each table is one entry in a packed
archive with a fixed slot size. If you translate a table and the whole file
ends up bigger than its original slot, the rebuild tool refuses to write it:

> `Rebuilt file is too large for fixed slot: Built size: {X} bytes / Original
> slot: {Y} bytes / Over by: {X-Y} bytes -- Shorten the CSV text or use a real
> archive repacker that updates offsets.`

If it's smaller, it just gets padded out -- no problem. So for tables with a
lot of "unbounded" rows (`TITLE`, `QUEST_EX`, `SKILL_WEAPON`, etc.), the real
constraint is "don't make the whole file meaningfully longer than the
original," not "each field can be infinite."

## Per-column limits

| Table | Column | Limit | Notes |
|---|---|---:|---|
| AREA_INFO | name | 32 characters | confirmed client buffer size |
| AREA_INFO | location | 28 characters | confirmed client buffer size |
| AREA_INFO | level_range | 50 characters | confirmed client buffer size |
| AREA_INFO | description | 300 characters | confirmed client buffer size |
| BEITEM_TYPE | name | 32 characters | confirmed client buffer size |
| BEITEM_TYPE | desc | 1024 characters | confirmed client buffer size |
| COITEM_TYPE | name | 64 characters | tool-side cap, not read directly off a client buffer -- stay under it |
| COITEM_TYPE | desc | 1024 characters | tool-side cap, not read directly off a client buffer -- stay under it |
| COITEM_TYPE | extra | 64 characters | tool-side cap, not read directly off a client buffer -- stay under it |
| EPISODE | t1 | 28 characters | confirmed client buffer size |
| EPISODE | t2 | 1024 characters | confirmed client buffer size |
| EPISODE | t3 | 512 characters | confirmed client buffer size |
| EPISODE | t4 | 24 characters | confirmed client buffer size (not in the coverage table since it reads as ASCII, but it exists in this file) |
| EPISODE_MONSTER | name | 32 characters | confirmed client buffer size |
| ITEM_BYUL_TYPE | name | ~32 characters | inferred, not directly confirmed -- be conservative |
| ITEM_BYUL_TYPE | desc | ~1045 characters | inferred, not directly confirmed -- be conservative |
| ITEM_CHARGED_TYPE | desc1 | 1024 characters | confirmed client buffer size |
| ITEM_CHARGED_TYPE | desc2 | 1024 characters | confirmed client buffer size (same file as desc1) |
| LOBBY | name | ~28 characters | confirmed buffer, but slightly ambiguous whether the full 29 is usable -- stay at 28 or under |
| LOBBY | desc | ~128 characters | same ambiguity -- stay at 128 or under |
| MATCHING_EMOTICON | text | 255 characters, less for non-Latin languages | client converts this to a single-byte buffer at load, so multi-byte-per-character languages (CJK, etc.) get meaningfully less than 255 actual characters |
| MATCHING_SYS_MSG | id_code | 32 characters | client buffer size, but overflow here is a soft/display issue rather than a hard parse failure -- still don't rely on going over |
| MATCHING_SYS_MSG | s1 | 128 characters | same as above |
| MATCHING_SYS_MSG | s2 | 1029 characters | same as above |
| MATCHING_UNIQUEMON_SPECIAL_EFFECT | name | unbounded | no confirmed buffer -- see file-size ceiling above |
| MON | name | 32 characters | confirmed client buffer size |
| MONSTER_BASIS | name | 32 characters | confirmed client buffer size |
| NOTIFY_MSG | text | not confirmed | the number in the tooling is an arbitrary safety ceiling, not a real client limit -- nobody's confirmed the actual cap here, so keep this one short and don't push it |
| PROMOTE_COND | title, description, requirement | unbounded | no confirmed buffer -- see file-size ceiling above |
| QUEST_EX | title, objective_text, reward_text, notice_text | unbounded | no confirmed buffer -- see file-size ceiling above |
| QUEST_ITEM_TYPE | name, description | unbounded | no confirmed buffer -- see file-size ceiling above |
| QUEST_NPC | name, location | unbounded | no confirmed buffer -- see file-size ceiling above |
| SCHOOL | name | unbounded | no confirmed buffer -- see file-size ceiling above |
| SKILL_WEAPON | name, description | unbounded | no confirmed buffer -- see file-size ceiling above |
| SKL_Desc | name, description | unbounded | no confirmed buffer -- see file-size ceiling above |
| SKL_Desc2 | text | unbounded | no confirmed buffer -- see file-size ceiling above |
| SPECIAL_REWARD | name | unbounded | no confirmed buffer -- see file-size ceiling above |
| STATE_CHANGE | name | unbounded | no confirmed buffer -- see file-size ceiling above |
| TITLE | name, description, condition | unbounded | no confirmed buffer -- see file-size ceiling above |

Tables not listed here have no translatable text columns at all (pure
numeric/config data) -- see the coverage table in
[`README.md`](README.md) for the full list.
