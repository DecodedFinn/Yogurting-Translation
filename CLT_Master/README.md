# CLT Master Extraction (Translation Source)

A full decode of every CLT table currently packed into the client's
`Models/CLT/CLT.IRD`/`CLT.IRH` archive, pulled straight from a live install.

## What's here

- `clt_decoded/` -- all 64 tables, decrypted, one clean `<TABLE_NAME>.clt.bin`
  file per table. Raw decoded binary, not parsed into rows yet.
- `clt_csv_source/` -- all 64 tables parsed into proper CSVs with real column
  names, one row per table entry. Everything's still in Japanese -- nothing
  has been translated yet.

## Coverage

All 64 tables in the client are here, so this is every entry that can be
translated, not just a handful.

35,522 total data rows across 64 tables. 25 of the 64 tables actually contain
translatable (non-ASCII / Japanese) text in at least one column; the other 39
are pure numeric/config tables (item slot rules, weapon stat curves,
model/sound IDs, etc.) with nothing to translate.

| Table | Columns | Rows | Translatable columns |
|---|---:|---:|---|
| AREA_INFO | 8 | 11 | description,level_range,location,name |
| ATK_WEAPON | 8 | 523 | (none -- numeric/config only) |
| BEITEM_SLOT | 13 | 70 | (none -- numeric/config only) |
| BEITEM_TYPE | 18 | 1713 | desc,name |
| CLI_COMMAND_MOTION | 4 | 4 | (none -- numeric/config only) |
| CLI_MOUSE_CURSOR | 8 | 27 | (none -- numeric/config only) |
| COITEM_TYPE | 9 | 9336 | desc,extra,name |
| ENCHANT_TITLE | 2 | 5 | (none -- numeric/config only) |
| ENITEM_TYPE | 8 | 36 | (none -- numeric/config only) |
| EPISODE | 7 | 153 | t1,t2,t3 |
| EPISODE_DETAIL | 46 | 152 | (none -- numeric/config only) |
| EPISODE_MONSTER | 7 | 728 | name |
| FIELD | 4 | 457 | (none -- numeric/config only) |
| FIELD_MOVE_PRM | 3 | 44 | (none -- numeric/config only) |
| GO_TARGET_PRM | 4 | 103 | (none -- numeric/config only) |
| GUIDE_BOARD | 2 | 2 | (none -- numeric/config only) |
| HUNT_MON | 2 | 187 | (none -- numeric/config only) |
| ITEM_BYUL_BETYPE | 9 | 466 | (none -- numeric/config only) |
| ITEM_BYUL_EFFECT | 2 | 29 | (none -- numeric/config only) |
| ITEM_BYUL_PARAM_ENCHANT | 4 | 152 | (none -- numeric/config only) |
| ITEM_BYUL_TYPE | 15 | 3325 | desc,name |
| ITEM_BYUL_USEDAYICON | 2 | 34 | (none -- numeric/config only) |
| ITEM_CHARGED_TYPE | 8 | 1228 | desc1 |
| LOBBY | 4 | 77 | desc,name |
| MATCHING_BASIC_SKILL | 9 | 17 | (none -- numeric/config only) |
| MATCHING_BGM | 2 | 53 | (none -- numeric/config only) |
| MATCHING_DANCE_MOTION | 2 | 27 | (none -- numeric/config only) |
| MATCHING_EMOTICON | 3 | 240 | text |
| MATCHING_EMOTION | 4 | 50 | (none -- numeric/config only) |
| MATCHING_EN_EFFECT | 5 | 4 | (none -- numeric/config only) |
| MATCHING_FACE | 4 | 90 | (none -- numeric/config only) |
| MATCHING_HAIR | 2 | 56 | (none -- numeric/config only) |
| MATCHING_HELP | 11 | 70 | (none -- numeric/config only) |
| MATCHING_NPCTRADE_MSG | 6 | 324 | (none -- numeric/config only) |
| MATCHING_NPC_CUT_IN | 3 | 159 | (none -- numeric/config only) |
| MATCHING_NPC_EFFECT | 2 | 104 | (none -- numeric/config only) |
| MATCHING_RS_EFFECT | 5 | 12 | (none -- numeric/config only) |
| MATCHING_SKIN_COLOR | 3 | 6 | (none -- numeric/config only) |
| MATCHING_SOUND | 2 | 309 | (none -- numeric/config only) |
| MATCHING_SYS_MSG | 7 | 104 | s2 |
| MATCHING_UNIQUEMON_SPECIAL_EFFECT | 6 | 8 | name |
| MATCHING_WEAPON_EFFECT | 3 | 193 | (none -- numeric/config only) |
| MON | 6 | 238 | name |
| MONSTER_BASIS | 5 | 152 | name |
| NOTIFY_MSG | 2 | 9 | text |
| NPC_EX | 4 | 590 | (none -- numeric/config only) |
| NoOptionField | 2 | 10 | (none -- numeric/config only) |
| PRODUCT_CATEGORY | 3 | 2371 | (none -- numeric/config only) |
| PROMOTE_COND | 5 | 8 | description,requirement,title |
| QUEST_EX | 11 | 285 | notice_text,objective_text,reward_text,title |
| QUEST_ITEM_TYPE | 5 | 423 | description,name |
| QUEST_NPC | 5 | 44 | location,name |
| QUEST_REF_ITEM | 6 | 883 | (none -- numeric/config only) |
| REINFORCE_STONE | 34 | 8448 | (none -- numeric/config only) |
| SCHOOL | 4 | 2 | name |
| SKILL_WEAPON | 11 | 193 | description,name |
| SKL_AREA | 5 | 494 | (none -- numeric/config only) |
| SKL_Desc | 7 | 167 | description,name |
| SKL_Desc2 | 13 | 320 | text |
| SPECIAL_PHONE | 5 | 4 | (none -- numeric/config only) |
| SPECIAL_REWARD | 6 | 30 | name |
| STATE_CHANGE | 4 | 37 | name |
| TITLE | 6 | 56 | condition,description,name |
| TITLE_EFFECT | 4 | 70 | (none -- numeric/config only) |

Largest translation surfaces by row count: COITEM_TYPE (9,336 rows --
consumable/quest/coitem names+descriptions), ITEM_BYUL_TYPE (3,325 rows --
byul pet item names+descriptions), PRODUCT_CATEGORY (2,371 rows, numeric only
despite the size), BEITEM_TYPE (1,713 rows -- equippable item
names+descriptions), ITEM_CHARGED_TYPE (1,228 rows).
