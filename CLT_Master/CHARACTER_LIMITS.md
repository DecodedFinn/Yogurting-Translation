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
- If a column is marked **unbounded**, there's no per-field buffer capping it.
- If a limit is marked **inferred** or **not confirmed**, it's a best guess,
  not something read directly off a real buffer size. Stay well under it to
  be safe.
- English is usually shorter than Japanese for the same idea, so most fields
  give you *more* headroom once translated, not less. The tight ones to
  actually watch are short fixed fields (names, single-line labels).
- These numbers are already **character counts**, not byte counts. The
  client stores this text as UTF-16LE (2 bytes per character), and the
  limits above account for that -- they're not just the raw buffer size in
  bytes. The one exception is `MATCHING_EMOTICON.text`, which the client
  converts to a single-byte buffer instead, which is why it's called out
  separately below. One more edge case worth knowing: the "1 character = 1
  unit of buffer space" math holds for essentially everything you'd
  actually type (Latin, Cyrillic, CJK, Thai, Hangul, etc.), but breaks for
  rare supplementary-plane characters like most emoji, which take up 2
  units instead of 1 -- not something translated flavor text is likely to
  hit, but worth knowing if you ever do.

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
| EPISODE | t1 | 28 characters | confirmed twice over: the record is 0xc87 bytes, t1 sits at +0x04 and t2 at +0x3e, so the field is 29 wchars and 28 characters plus a terminator fits exactly. |
| EPISODE | t2 | 1024 characters | confirmed client buffer size |
| EPISODE | t3 | 512 characters | confirmed client buffer size |
| EPISODE | t4 | 24 characters | confirmed client buffer size (not in the coverage table since it reads as ASCII, but it exists in this file) |
| EPISODE_MONSTER | name | 32 characters | confirmed client buffer size |
| ITEM_BYUL_TYPE | name | ~32 characters | inferred, not directly confirmed -- be conservative |
| ITEM_BYUL_TYPE | desc | ~1045 characters | inferred, not directly confirmed -- be conservative |
| ITEM_CHARGED_TYPE | desc1 | 1024 characters | confirmed client buffer size |
| ITEM_CHARGED_TYPE | desc2 | 1024 characters | confirmed client buffer size (same file as desc1) |
| LOBBY | name | 27 characters | the record is 0x140 bytes and no code path pins the field boundary, so 28 vs 29 wchars stays ambiguous. TITLE showed what filling a field exactly costs, so treat 27 as the limit rather than 28. |
| LOBBY | desc | ~128 characters | same ambiguity -- stay at 128 or under |
| MATCHING_EMOTICON | text | 255 characters, less for non-Latin languages | client converts this to a single-byte buffer at load, so multi-byte-per-character languages (CJK, etc.) get meaningfully less than 255 actual characters |
| MATCHING_SYS_MSG | id_code | 32 characters | client buffer size, but overflow here is a soft/display issue rather than a hard parse failure -- still don't rely on going over |
| MATCHING_SYS_MSG | s1 | 128 characters | same as above |
| MATCHING_SYS_MSG | s2 | 1029 characters | same as above |
| MATCHING_UNIQUEMON_SPECIAL_EFFECT | name | unbounded | no confirmed buffer |
| MON | name | 32 characters | confirmed client buffer size |
| MONSTER_BASIS | name | 32 characters | confirmed client buffer size |
| NOTIFY_MSG | text | not confirmed | the number in the tooling is an arbitrary safety ceiling, not a real client limit -- nobody's confirmed the actual cap here, so keep this one short and don't push it |
| PROMOTE_COND | title, description, requirement | unbounded | no confirmed buffer |
| QUEST_EX | title, objective_text, reward_text, notice_text | unbounded | no confirmed buffer |
| QUEST_ITEM_TYPE | name, description | unbounded | no confirmed buffer |
| QUEST_NPC | name, location | unbounded | no confirmed buffer |
| SCHOOL | name | unbounded | no confirmed buffer |
| SKILL_WEAPON | name, description | unbounded | no confirmed buffer |
| SKL_Desc | name, description | unbounded | no confirmed buffer |
| SKL_Desc2 | text | unbounded | no confirmed buffer |
| SPECIAL_REWARD | name | unbounded | no confirmed buffer |
| STATE_CHANGE | name | unbounded | no confirmed buffer |
| TITLE | name | 10 characters | confirmed: LoadTitle reads a fixed 0x1b2-byte record, the name sits at +0x04, and the nameplate converts it into a 0x15-byte buffer. The field is 11 wchars, so 11 characters fills it and leaves no terminator: the nameplate then runs straight on into the description ("New StudentA title f"). The longest Japanese name is exactly 10. |
| TITLE | description, condition | not confirmed | the client never reads either one in any decompiled path, so nothing displays them and no buffer has been measured. The record leaves 213 wchars for name + description + condition together. |

Tables not listed here have no translatable text columns at all (pure
numeric/config data) -- see the coverage table in
[`README.md`](README.md) for the full list.
