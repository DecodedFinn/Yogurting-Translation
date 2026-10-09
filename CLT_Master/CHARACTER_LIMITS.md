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
| ENITEM_TYPE | name | 32 characters | confirmed client buffer size |
| ENITEM_TYPE | desc | 100 characters | confirmed client buffer size |
| ENITEM_TYPE | extra | 20 characters | confirmed client buffer size. Going over is NOT a cut-off: the buffer sits right below the loader's row counter, so a longer `extra` overwrites it and the client stops reading the table after that row. Every crystal but the first and all six study guides went missing that way until 2026-10-09. |
| ENCHANT_TITLE | title | 11 characters | confirmed client buffer size |
| FIELD | name | 32 characters | confirmed client buffer size |
| GUIDE_BOARD | title | 25 characters | confirmed client buffer size |
| LOBBY | name | 28 characters | confirmed client buffer size |
| LOBBY | desc | 128 characters | confirmed client buffer size |
| MATCHING_UNIQUEMON_SPECIAL_EFFECT | name | 32 characters | confirmed client buffer size |
| NPC_EX | name | 32 characters | confirmed client buffer size |
| PROMOTE_COND | title | 32 characters | confirmed client buffer size |
| PROMOTE_COND | description | 100 characters | confirmed client buffer size |
| PROMOTE_COND | requirement | 51 characters | confirmed client buffer size |
| QUEST_EX | title | 24 characters | confirmed client buffer size |
| QUEST_EX | objective_text | 1024 characters | confirmed client buffer size |
| QUEST_EX | reward_text | 256 characters | confirmed client buffer size |
| QUEST_EX | notice_text | 512 characters | confirmed client buffer size |
| QUEST_ITEM_TYPE | name | 32 characters | confirmed client buffer size |
| QUEST_ITEM_TYPE | description | 1027 characters | confirmed client buffer size |
| QUEST_NPC | name | 32 characters | confirmed client buffer size |
| QUEST_NPC | location | 64 characters | confirmed client buffer size |
| SCHOOL | name | 34 characters | confirmed client buffer size |
| SKL_Desc | name | 32 characters | confirmed client buffer size |
| SKL_Desc | description | 1024 characters | confirmed client buffer size |
| SKL_Desc2 | text | 66 characters | confirmed client buffer size |
| SPECIAL_REWARD | name | 1027 characters | confirmed client buffer size |
| STATE_CHANGE | name | 32 characters | confirmed client buffer size |
| TITLE | description | 100 characters | confirmed client buffer size (LoadTitle; nothing decompiled displays it) |
| TITLE | condition | 100 characters | confirmed client buffer size |
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
| MATCHING_EMOTICON | text | 255 characters, less for non-Latin languages | client converts this to a single-byte buffer at load, so multi-byte-per-character languages (CJK, etc.) get meaningfully less than 255 actual characters |
| MATCHING_SYS_MSG | id_code | 32 characters | client buffer size, but overflow here is a soft/display issue rather than a hard parse failure -- still don't rely on going over |
| MATCHING_SYS_MSG | s1 | 128 characters | same as above |
| MATCHING_SYS_MSG | s2 | 1029 characters | same as above |
| MON | name | 32 characters | confirmed client buffer size |
| MONSTER_BASIS | name | 32 characters | confirmed client buffer size |
| NOTIFY_MSG | text | not confirmed | the number in the tooling is an arbitrary safety ceiling, not a real client limit -- nobody's confirmed the actual cap here, so keep this one short and don't push it |
| SKILL_WEAPON | name, description | unbounded | the SS2 client never loads this table (only the SS1 client reads `_SKILL_WEAPON.clt`) |
| TITLE | name | 10 characters | confirmed: LoadTitle reads a fixed 0x1b2-byte record, the name sits at +0x04, and the nameplate converts it into a 0x15-byte buffer. The field is 11 wchars, so 11 characters fills it and leaves no terminator: the nameplate then runs straight on into the description ("New StudentA title f"). The longest Japanese name is exactly 10. |

Tables not listed here have no translatable text columns at all (pure
numeric/config data) -- see the coverage table in
[`README.md`](README.md) for the full list.

## How the confirmed limits were read (2026-10-09)

Each table's loader in `LuGameEngineDX9.dll` reads a row into stack buffers
(`DecryptManager::GetWordString(manager, buffer)` takes no size, so it writes
whatever the archive holds). The limit is the buffer's declared size in UTF-16
units minus one for the terminator.

What going over does depends on what sits next to the buffer:

- the next field of the same row, read afterwards (most tables): the text loses
  its terminator, so the client shows it running on into that field;
- the loader's own variables (`ENITEM_TYPE.extra`): the row counter is
  overwritten and the client stops reading the table, so every later row is
  unknown to it.

`ITEM_BYUL_EFFECT`, `MATCHING_EMOTICON`, `NOTIFY_MSG` and `SPECIAL_PHONE` keep
the string the reader returns instead of copying it into a buffer, so they have
no per-field limit. `SKILL_WEAPON` is only loaded by the SS1 client.

