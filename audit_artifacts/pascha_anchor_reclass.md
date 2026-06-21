# Pascha Anchor Reclassification

Source: `audit_artifacts/pascha_pd_father_layer.md`.
Method: deterministic column logic only. No fetching. No source judgment.

## Bucket counts

| bucket | count |
| --- | ---: |
| A_nt_anchored | 80 |
| B_canon_anchored | 15 |
| C_hour_frame_only | 110 |
| D_typology_unverified | 15 |
| E_psalm_coincidence | 83 |
| total | 303 |

## Input predicate coverage note

The supplied predicates do not cover every non-A/B `pd_relation` value in the source table. To keep A-E exhaustive, non-A/B rows that are not C or E are assigned to D by deterministic residual logic.

| residual_pd_relation_in_D | row_count |
| --- | ---: |
| direct_or_thematic_passion | 5 |
| theme_reading | 5 |
| resurrection_or_praise_theme | 3 |
| nt_fulfillment_theme | 2 |

## Bucket C exact_citation reuse

| exact_citation | row_count |
| --- | ---: |
| Catechetical Lecture XIII, On the Cross | 27 |
| Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 | 27 |
| Homilies on the Gospel of Matthew, Homily LXXXIII, on Matthew 26:36-75 | 22 |
| On the Incarnation of the Word, sections 3-5 and 24-25 | 19 |
| Homilies on the Gospel of Matthew, Homily LXXXIV, on Matthew 27:1-10 | 13 |
| Oration XLV, On Holy Pascha | 2 |

## C_hour_frame_only rows

| row_id | day | hour | display_ref | pd_author | exact_citation |
| --- | --- | --- | --- | --- | --- |
| pd-003 | Hosanna Sunday | Ninth Hour | Lam 1:1-4 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-004 | Hosanna Sunday | Ninth Hour | Zeph 3:11-20 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-006 | Hosanna Sunday | Eleventh Hour | Isa 48:12-22 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIV, on Matthew 27:1-10 |
| pd-007 | Hosanna Sunday | Eleventh Hour | Nah 1:2-8 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIV, on Matthew 27:1-10 |
| pd-012 | Monday Eve | First Hour | Zech 1:1-6 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-013 | Monday Eve | First Hour | Zeph 1:2-12 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-017 | Monday Eve | Third Hour | Zeph 1:14-2:2 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIII, on Matthew 26:36-75 |
| pd-020 | Monday Eve | Sixth Hour | Hos 4:15-19 | St Athanasius | On the Incarnation of the Word, sections 3-5 and 24-25 |
| pd-021 | Monday Eve | Sixth Hour | Hos 5:1-7 | St Athanasius | On the Incarnation of the Word, sections 3-5 and 24-25 |
| pd-022 | Monday Eve | Sixth Hour | Joel 1:5-15 | St Athanasius | On the Incarnation of the Word, sections 3-5 and 24-25 |
| pd-025 | Monday Eve | Ninth Hour | Hos 10:12-15 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-027 | Monday Eve | Ninth Hour | Mic 2:3-10 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-030 | Monday Eve | Eleventh Hour | Amos 5:6-14 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIV, on Matthew 27:1-10 |
| pd-031 | Monday Eve | Eleventh Hour | Mic 3:1-4 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIV, on Matthew 27:1-10 |
| pd-043 | Monday | Third Hour | Jer 9:12-19 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIII, on Matthew 26:36-75 |
| pd-052 | Monday | Ninth Hour | Prov 1:1-9 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-059 | Tuesday Eve | First Hour | Zech 1:1-6 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-065 | Tuesday Eve | Sixth Hour | Hos 4:15-19 | St Athanasius | On the Incarnation of the Word, sections 3-5 and 24-25 |
| pd-066 | Tuesday Eve | Sixth Hour | Hos 4:15-5:7 | St Athanasius | On the Incarnation of the Word, sections 3-5 and 24-25 |
| pd-067 | Tuesday Eve | Sixth Hour | Hos 5:1-7 | St Athanasius | On the Incarnation of the Word, sections 3-5 and 24-25 |
| pd-070 | Tuesday Eve | Ninth Hour | Hos 10:12-11:2 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-071 | Tuesday Eve | Ninth Hour | Hos 10:12-15 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-074 | Tuesday Eve | Eleventh Hour | Amos 5:6-14 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIV, on Matthew 27:1-10 |
| pd-076 | Tuesday | First Hour | Exod 19:1-9 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-077 | Tuesday | First Hour | Hos 4:1-8 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-078 | Tuesday | First Hour | Job 23:2-17 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-079 | Tuesday | First Hour | Job 23:2-24:25 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-080 | Tuesday | First Hour | Job 24:1-25 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-082 | Tuesday | Third Hour | 1Kgs 19:9-14 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIII, on Matthew 26:36-75 |
| pd-083 | Tuesday | Third Hour | Deut 8:11-20 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIII, on Matthew 26:36-75 |
| pd-085 | Tuesday | Third Hour | Jer 9:12-19 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIII, on Matthew 26:36-75 |
| pd-086 | Tuesday | Third Hour | Job 27:2-28:2 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIII, on Matthew 26:36-75 |
| pd-090 | Tuesday | Sixth Hour | Ezek 21:3-13 | St Athanasius | On the Incarnation of the Word, sections 3-5 and 24-25 |
| pd-091 | Tuesday | Sixth Hour | Isa 1:1-9 | St Athanasius | On the Incarnation of the Word, sections 3-5 and 24-25 |
| pd-094 | Tuesday | Ninth Hour | Dan 7:9-15 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-095 | Tuesday | Ninth Hour | Gen 6:5-9:7 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-098 | Tuesday | Ninth Hour | Prov 1:1-9 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-099 | Tuesday | Ninth Hour | Prov 8:1-12 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-103 | Tuesday | Eleventh Hour | Isa 30:25-30 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIV, on Matthew 27:1-10 |
| pd-105 | Tuesday | Eleventh Hour | Prov 6:20-7:4 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIV, on Matthew 27:1-10 |
| pd-109 | Wednesday Eve | First Hour | Ezek 22:17-22 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-110 | Wednesday Eve | First Hour | Ezek 22:23-28 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-111 | Wednesday Eve | First Hour | Jer 43:5-11 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-114 | Wednesday Eve | Third Hour | Amos 4:4-13 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIII, on Matthew 26:36-75 |
| pd-115 | Wednesday Eve | Third Hour | Amos 5:18-27 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIII, on Matthew 26:36-75 |
| pd-118 | Wednesday Eve | Sixth Hour | Amos 3:1-11 | St Athanasius | On the Incarnation of the Word, sections 3-5 and 24-25 |
| pd-119 | Wednesday Eve | Sixth Hour | Jer 16:9-13 | St Athanasius | On the Incarnation of the Word, sections 3-5 and 24-25 |
| pd-122 | Wednesday Eve | Ninth Hour | Ezek 20:27-33 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-123 | Wednesday Eve | Ninth Hour | Hos 9:14-10:2 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-129 | Wednesday | First Hour | Hos 5:13-6:3 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-130 | Wednesday | First Hour | Prov 3:5-14 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-136 | Wednesday | Third Hour | Exod 13:17-22 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIII, on Matthew 26:36-75 |
| pd-137 | Wednesday | Third Hour | Job 27:16-28:2 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIII, on Matthew 26:36-75 |
| pd-138 | Wednesday | Third Hour | Prov 4:4-27,5:1-4 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIII, on Matthew 26:36-75 |
| pd-144 | Wednesday | Sixth Hour | Job 27:16-20 | St Athanasius | On the Incarnation of the Word, sections 3-5 and 24-25 |
| pd-145 | Wednesday | Sixth Hour | Job 28:1-2 | St Athanasius | On the Incarnation of the Word, sections 3-5 and 24-25 |
| pd-150 | Wednesday | Ninth Hour | Gen 24:1-9 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-151 | Wednesday | Ninth Hour | Isa 48:1-6 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-152 | Wednesday | Ninth Hour | Isa 59:1-17 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-154 | Wednesday | Ninth Hour | Prov 1:10-33 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-155 | Wednesday | Ninth Hour | Prov 1:11-35 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-159 | Wednesday | Eleventh Hour | Isa 28:16-29 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIV, on Matthew 27:1-10 |
| pd-165 | Great Thursday Eve | First Hour | Ezek 43:5-11 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-166 | Great Thursday Eve | First Hour | Jer 8:17-9:6 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-169 | Great Thursday Eve | Third Hour | Amos 4:4-13 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIII, on Matthew 26:36-75 |
| pd-173 | Great Thursday Eve | Sixth Hour | Amos 3:1-11 | St Athanasius | On the Incarnation of the Word, sections 3-5 and 24-25 |
| pd-174 | Great Thursday Eve | Sixth Hour | Ezek 22:23-28 | St Athanasius | On the Incarnation of the Word, sections 3-5 and 24-25 |
| pd-178 | Great Thursday Eve | Ninth Hour | Ezek 20:27-33 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-179 | Great Thursday Eve | Ninth Hour | Ezek 21:33-37 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-180 | Great Thursday Eve | Ninth Hour | Jer 9:6-10 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-181 | Great Thursday Eve | Ninth Hour | Jer 9:7-11 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-185 | Great Thursday Eve | Eleventh Hour | Isa 27:11-28:15 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIV, on Matthew 27:1-10 |
| pd-186 | Great Thursday Eve | Eleventh Hour | Jer 8:4-9 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIV, on Matthew 27:1-10 |
| pd-192 | Great Thursday | First Hour | Ezek 18:20-32 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-193 | Great Thursday | First Hour | Isa 58:1-11 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-194 | Great Thursday | First Hour | Isa 58:1-9 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-197 | Great Thursday | Third Hour | Prov 30:2-6 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIII, on Matthew 26:36-75 |
| pd-198 | Great Thursday | Third Hour | Prov 4:4-27,5:1-4 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIII, on Matthew 26:36-75 |
| pd-200 | Great Thursday | Third Hour | Zech 10:1-2 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIII, on Matthew 26:36-75 |
| pd-203 | Great Thursday | Sixth Hour | Exod 7:2-15 | St Athanasius | On the Incarnation of the Word, sections 3-5 and 24-25 |
| pd-204 | Great Thursday | Sixth Hour | Ezek 20:39-44 | St Athanasius | On the Incarnation of the Word, sections 3-5 and 24-25 |
| pd-205 | Great Thursday | Sixth Hour | Jer 7:2-15 | St Athanasius | On the Incarnation of the Word, sections 3-5 and 24-25 |
| pd-214 | Great Thursday | Ninth Hour | Job 27:2-28:13 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-217 | Great Thursday | Eleventh Hour | Isa 19:19-25 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIV, on Matthew 27:1-10 |
| pd-227 | Great Thursday | Liturgy of Blessing of the Water | Gen 18:1-23 | St Gregory the Theologian | Oration XLV, On Holy Pascha |
| pd-236 | Good Friday Eve | Ninth Hour | Ezek 21:28-32 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-239 | Good Friday | First Hour | Deut 8:19-9:24 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-240 | Good Friday | First Hour | Isa 1:2-9 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-242 | Good Friday | First Hour | Isa 24:1-13 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-241 | Good Friday | First Hour | Isa 2:10-21 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-243 | Good Friday | First Hour | Jer 22:29-23:6 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-244 | Good Friday | First Hour | Job 12:17-13:1 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-245 | Good Friday | First Hour | Job 12:18-13:1 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-246 | Good Friday | First Hour | Mic 1:16-2:3 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-247 | Good Friday | First Hour | Mic 7:1-8 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-254 | Good Friday | Third Hour | Amos 9:4-5,9:7-10 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIII, on Matthew 26:36-75 |
| pd-255 | Good Friday | Third Hour | Amos 9:4-6 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIII, on Matthew 26:36-75 |
| pd-256 | Good Friday | Third Hour | Amos 9:8-10 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIII, on Matthew 26:36-75 |
| pd-257 | Good Friday | Third Hour | Gen 48:1-19 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIII, on Matthew 26:36-75 |
| pd-258 | Good Friday | Third Hour | Isa 3:9-15 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIII, on Matthew 26:36-75 |
| pd-261 | Good Friday | Third Hour | Job 29:21-25,30:1-10 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIII, on Matthew 26:36-75 |
| pd-262 | Good Friday | Third Hour | Job 29:21-30:10 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIII, on Matthew 26:36-75 |
| pd-265 | Good Friday | Sixth Hour | Amos 8:9-12 | St Athanasius | On the Incarnation of the Word, sections 3-5 and 24-25 |
| pd-266 | Good Friday | Sixth Hour | Isa 12:2-13:10 | St Athanasius | On the Incarnation of the Word, sections 3-5 and 24-25 |
| pd-272 | Good Friday | Ninth Hour | Hos 2:1-3,2:10-11 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-273 | Good Friday | Ninth Hour | Jer 11:18-12:13 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-274 | Good Friday | Ninth Hour | Joel 2:1-3,2:10-11 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-280 | Good Friday | Eleventh Hour | Isa 3:5-12 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIV, on Matthew 27:1-10 |
| pd-281 | Good Friday | Eleventh Hour | Jer 12:1-14 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXXIV, on Matthew 27:1-10 |
| pd-297 | Bright Saturday | unspecified hour | Jer 13:15-22 | St Gregory the Theologian | Oration XLV, On Holy Pascha |

## D_typology_unverified rows

| row_id | day | hour | display_ref | pd_author | exact_citation |
| --- | --- | --- | --- | --- | --- |
| pd-016 | Monday Eve | Third Hour | Mal 1:1-9 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-062 | Tuesday Eve | Third Hour | Mal 1:1-9 | St John Chrysostom | Homilies on the Gospel of Matthew, Homily LXXVIII, on Matthew 25:1-30 |
| pd-170 | Great Thursday Eve | Third Hour | Ezek 36:16-23 | St Augustine | Tractates on the Gospel of John, Tractate LV, on John 13:1-5 |
| pd-222 | Great Thursday | Eleventh Hour | Zech 14:1-4 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-223 | Great Thursday | Eleventh Hour | Zech 14:6-9 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-225 | Great Thursday | Liturgy of Blessing of the Water | Ezek 36:25-29 | St Augustine | Tractates on the Gospel of John, Tractate LV, on John 13:1-5 |
| pd-226 | Great Thursday | Liturgy of Blessing of the Water | Ezek 47:1-9 | St Augustine | Tractates on the Gospel of John, Tractate LV, on John 13:1-5 |
| pd-228 | Great Thursday | Liturgy of Blessing of the Water | Isa 4:2-4 | St Augustine | Tractates on the Gospel of John, Tractate LV, on John 13:1-5 |
| pd-229 | Great Thursday | Liturgy of Blessing of the Water | Isa 55:1-56:1 | St Augustine | Tractates on the Gospel of John, Tractate LV, on John 13:1-5 |
| pd-260 | Good Friday | Third Hour | Isa 63:1-7 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-275 | Good Friday | Ninth Hour | Zech 14:5-11 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-276 | Good Friday | Ninth Hour | Zech 14:6-11 | St Cyril of Jerusalem | Catechetical Lecture XIII, On the Cross |
| pd-288 | Good Friday | Twelfth Hour | Lam 3:1-66 | St Cyril of Jerusalem | Catechetical Lecture XIV, On the Resurrection |
| pd-295 | Bright Saturday | unspecified hour | Isa 45:15-20 | St Cyril of Jerusalem | Catechetical Lecture XIV, On the Resurrection |
| pd-298 | Bright Saturday | unspecified hour | Jer 31:31-34 | St Cyril of Jerusalem | Catechetical Lecture XIV, On the Resurrection |

## E_psalm_coincidence rows

| row_id | day | hour | display_ref | pd_author | exact_citation |
| --- | --- | --- | --- | --- | --- |
| pd-002 | Palm Sunday | Matins | Ps 68:19,68:35 (LXX Ps 67:19; Ps 67:35) | St Augustine | Expositions on the Psalms, Psalm 68 |
| pd-009 | Palm Sunday | Liturgy | Ps 64:1-2 (LXX Ps 63:1-2) | St Augustine | Expositions on the Psalms, Psalm 64 |
| pd-010 | Palm Sunday | Liturgy | Ps 80:1-3 (LXX Ps 79:1-3) | St Augustine | Expositions on the Psalms, Psalm 80 |
| pd-014 | Monday Eve | First Hour | Ps 27:6-7 (LXX Ps 26:6-7) | St Augustine | Expositions on the Psalms, Psalm 27 |
| pd-015 | Monday Eve | First Hour | Ps 62:6-7 (LXX Ps 61:6-7) | St Augustine | Expositions on the Psalms, Psalm 62 |
| pd-018 | Monday Eve | Third Hour | Ps 13:3,13:5 (LXX Ps 12:3; Ps 12:5) | St Augustine | Expositions on the Psalms, Psalm 13 |
| pd-019 | Monday Eve | Third Hour | Ps 28:2,28:9 (LXX Ps 27:2; Ps 27:9) | St Augustine | Expositions on the Psalms, Psalm 28 |
| pd-023 | Monday Eve | Sixth Hour | Ps 29:1-2 (LXX Ps 28:1-2) | St Augustine | Expositions on the Psalms, Psalm 29 |
| pd-024 | Monday Eve | Sixth Hour | Ps 91:2-3 (LXX Ps 90:2-3) | St Augustine | Expositions on the Psalms, Psalm 91 |
| pd-028 | Monday Eve | Ninth Hour | Ps 33:10-11 (LXX Ps 32:10-11) | St Augustine | Expositions on the Psalms, Psalm 33 |
| pd-032 | Monday Eve | Eleventh Hour | Ps 122:4 (LXX Ps 121:4) | St Augustine | Expositions on the Psalms, Psalm 122 |
| pd-033 | Monday Eve | Eleventh Hour | Ps 18:17-18 (LXX Ps 17:17-18) | St Augustine | Expositions on the Psalms, Psalm 18 |
| pd-038 | Monday | First Hour | Ps 72:1-19 (LXX Ps 71:1-19) | St Augustine | Expositions on the Psalms, Psalm 72 |
| pd-040 | Monday | First Hour | Ps 71:18-19 (LXX Ps 70:18-19) | St Augustine | Expositions on the Psalms, Psalm 71 |
| pd-041 | Monday | First Hour | Ps 72:18-19 (LXX Ps 71:18-19) | St Augustine | Expositions on the Psalms, Psalm 72 |
| pd-044 | Monday | Third Hour | Ps 122:1-2 (LXX Ps 121:1-2) | St Augustine | Expositions on the Psalms, Psalm 122 |
| pd-047 | Monday | Sixth Hour | Ps 122:4 (LXX Ps 121:4) | St Augustine | Expositions on the Psalms, Psalm 122 |
| pd-053 | Monday | Ninth Hour | Ps 65:4-5 (LXX Ps 64:4-5) | St Augustine | Expositions on the Psalms, Psalm 65 |
| pd-057 | Monday | Eleventh Hour | Ps 12:3-4 (LXX Ps 11:3-4) | St Augustine | Expositions on the Psalms, Psalm 12 |
| pd-058 | Monday | Eleventh Hour | Ps 13:3-4 (LXX Ps 12:3-4) | St Augustine | Expositions on the Psalms, Psalm 13 |
| pd-060 | Tuesday Eve | First Hour | Ps 62:2,62:7 (LXX Ps 61:2; Ps 61:7) | St Augustine | Expositions on the Psalms, Psalm 62 |
| pd-061 | Tuesday Eve | First Hour | Ps 62:6-7 (LXX Ps 61:6-7) | St Augustine | Expositions on the Psalms, Psalm 62 |
| pd-063 | Tuesday Eve | Third Hour | Ps 13:3,13:5 (LXX Ps 12:3; Ps 12:5) | St Augustine | Expositions on the Psalms, Psalm 13 |
| pd-064 | Tuesday Eve | Third Hour | Ps 28:2,28:9 (LXX Ps 27:2; Ps 27:9) | St Augustine | Expositions on the Psalms, Psalm 28 |
| pd-068 | Tuesday Eve | Sixth Hour | Ps 29:1-2 (LXX Ps 28:1-2) | St Augustine | Expositions on the Psalms, Psalm 29 |
| pd-069 | Tuesday Eve | Sixth Hour | Ps 91:2-3 (LXX Ps 90:2-3) | St Augustine | Expositions on the Psalms, Psalm 91 |
| pd-073 | Tuesday Eve | Ninth Hour | Ps 33:10-11 (LXX Ps 32:10-11) | St Augustine | Expositions on the Psalms, Psalm 33 |
| pd-075 | Tuesday Eve | Eleventh Hour | Ps 122:4 (LXX Ps 121:4) | St Augustine | Expositions on the Psalms, Psalm 122 |
| pd-081 | Tuesday | First Hour | Ps 120:2,120:6-7 (LXX Ps 119:2; Ps 119:6-7) | St Augustine | Expositions on the Psalms, Psalm 120 |
| pd-088 | Tuesday | Third Hour | Ps 119:154-155 (LXX Ps 118:154-155) | St Augustine | Expositions on the Psalms, Psalm 119 |
| pd-089 | Tuesday | Third Hour | Ps 122:1-2 (LXX Ps 121:1-2) | St Augustine | Expositions on the Psalms, Psalm 122 |
| pd-093 | Tuesday | Sixth Hour | Ps 18:17,18:48 (LXX Ps 17:17; Ps 17:48) | St Augustine | Expositions on the Psalms, Psalm 18 |
| pd-101 | Tuesday | Ninth Hour | Ps 25:1-3 (LXX Ps 24:1-3) | St Augustine | Expositions on the Psalms, Psalm 25 |
| pd-102 | Tuesday | Ninth Hour | Ps 65:4-5 (LXX Ps 64:4-5) | St Augustine | Expositions on the Psalms, Psalm 65 |
| pd-107 | Tuesday | Eleventh Hour | Ps 12:3-4 (LXX Ps 11:3-4) | St Augustine | Expositions on the Psalms, Psalm 12 |
| pd-108 | Tuesday | Eleventh Hour | Ps 13:3-4 (LXX Ps 12:3-4) | St Augustine | Expositions on the Psalms, Psalm 13 |
| pd-112 | Wednesday Eve | First Hour | Ps 59:16-17 (LXX Ps 58:16-17) | St Augustine | Expositions on the Psalms, Psalm 59 |
| pd-116 | Wednesday Eve | Third Hour | Ps 55:1,55:21 (LXX Ps 54:1; Ps 54:21) | St Augustine | Expositions on the Psalms, Psalm 55 |
| pd-117 | Wednesday Eve | Third Hour | Ps 65:4 (LXX Ps 64:4) | St Augustine | Expositions on the Psalms, Psalm 65 |
| pd-120 | Wednesday Eve | Sixth Hour | Ps 102:1-2 (LXX Ps 101:1-2) | St Augustine | Expositions on the Psalms, Psalm 102 |
| pd-121 | Wednesday Eve | Sixth Hour | Ps 140:1-2 (LXX Ps 139:1-2) | St Augustine | Expositions on the Psalms, Psalm 140 |
| pd-125 | Wednesday Eve | Ninth Hour | Ps 7:1-2 | St Augustine | Expositions on the Psalms, Psalm 7 |
| pd-127 | Wednesday Eve | Eleventh Hour | Ps 57:1 (LXX Ps 56:1) | St Augustine | Expositions on the Psalms, Psalm 57 |
| pd-134 | Wednesday | First Hour | Ps 33:10 (LXX Ps 32:10) | St Augustine | Expositions on the Psalms, Psalm 33 |
| pd-133 | Wednesday | First Hour | Ps 33:10,51:4 (LXX Ps 32:10; Ps 50:4) | St Augustine | Expositions on the Psalms, Psalm 33 |
| pd-135 | Wednesday | First Hour | Ps 51:4 (LXX Ps 50:6) | St Augustine | Expositions on the Psalms, Psalm 51 |
| pd-142 | Wednesday | Third Hour | Ps 42:5 (LXX Ps 41:6) | St Augustine | Expositions on the Psalms, Psalm 42 |
| pd-147 | Wednesday | Sixth Hour | Ps 83:2,83:5 (LXX Ps 82:2; Ps 82:5) | St Augustine | Expositions on the Psalms, Psalm 83 |
| pd-148 | Wednesday | Sixth Hour | Ps 84:1 (LXX Ps 83:2) | St Augustine | Expositions on the Psalms, Psalm 84 |
| pd-149 | Wednesday | Sixth Hour | Ps 84:4 (LXX Ps 83:5) | St Augustine | Expositions on the Psalms, Psalm 84 |
| pd-160 | Wednesday | Eleventh Hour | Ps 6:1-2 (LXX Ps 6:2-3) | St Augustine | Expositions on the Psalms, Psalm 6 |
| pd-161 | Wednesday | Eleventh Hour | Ps 6:2-3 | St Augustine | Expositions on the Psalms, Psalm 6 |
| pd-162 | Wednesday | Eleventh Hour | Ps 6:2-3,69:17 (LXX Ps 6:2-3,69:17; Ps 68:17) | St Augustine | Expositions on the Psalms, Psalm 6 |
| pd-171 | Great Thursday Eve | Third Hour | Ps 108:1-2 (LXX Ps 107:1-2) | St Augustine | Expositions on the Psalms, Psalm 108 |
| pd-176 | Great Thursday Eve | Sixth Hour | Ps 58:2 (LXX Ps 57:2) | St Augustine | Expositions on the Psalms, Psalm 58 |
| pd-177 | Great Thursday Eve | Sixth Hour | Ps 68:21 (LXX Ps 67:21) | St Augustine | Expositions on the Psalms, Psalm 68 |
| pd-182 | Great Thursday Eve | Ninth Hour | Ps 27:3-4 (LXX Ps 26:3-4) | St Augustine | Expositions on the Psalms, Psalm 27 |
| pd-183 | Great Thursday Eve | Ninth Hour | Ps 34:4-5 (LXX Ps 33:4-5) | St Augustine | Expositions on the Psalms, Psalm 34 |
| pd-172 | Thursday Eve | Third Hour | Ps 55:1,55:21 (LXX Ps 54:1; Ps 54:21) | St Augustine | Expositions on the Psalms, Psalm 55 |
| pd-175 | Thursday Eve | Sixth Hour | Ps 140:1-2 (LXX Ps 139:1-2) | St Augustine | Expositions on the Psalms, Psalm 140 |
| pd-184 | Thursday Eve | Ninth Hour | Ps 7:1-2 | St Augustine | Expositions on the Psalms, Psalm 7 |
| pd-188 | Thursday Eve | Eleventh Hour | Ps 62:6-7 (LXX Ps 61:6-7) | St Augustine | Expositions on the Psalms, Psalm 62 |
| pd-195 | Great Thursday | First Hour | Ps 55:12,55:21 (LXX Ps 54:12; Ps 54:21) | St Augustine | Expositions on the Psalms, Psalm 55 |
| pd-202 | Great Thursday | Third Hour | Ps 94:21,94:23 (LXX Ps 93:21; Ps 93:23) | St Augustine | Expositions on the Psalms, Psalm 94 |
| pd-224 | Great Thursday | Eleventh Hour | Ps 50:17-18 (LXX Ps 49:17-18) | St Augustine | Expositions on the Psalms, Psalm 50 |
| pd-232 | Great Thursday | Liturgy of Blessing of the Water | Ps 51:7,51:10 (LXX Ps 50:7; Ps 50:10) | St Augustine | Expositions on the Psalms, Psalm 51 |
| pd-233 | Good Friday Eve | First Hour | Ps 102:1,102:8 (LXX Ps 101:1; Ps 101:8) | St Augustine | Expositions on the Psalms, Psalm 102 |
| pd-234 | Good Friday Eve | Third Hour | Ps 55:1,55:21 (LXX Ps 54:1; Ps 54:21) | St Augustine | Expositions on the Psalms, Psalm 55 |
| pd-235 | Good Friday Eve | Sixth Hour | Ps 59:1,69:20 (LXX Ps 58:1; Ps 68:20) | St Augustine | Expositions on the Psalms, Psalm 59 |
| pd-237 | Good Friday Eve | Ninth Hour | Ps 28:3-4,35:4 (LXX Ps 27:3-4; Ps 34:4) | St Augustine | Expositions on the Psalms, Psalm 28 |
| pd-252 | Good Friday | First Hour | Ps 27:12 (LXX Ps 26:12) | St Augustine | Expositions on the Psalms, Psalm 27 |
| pd-251 | Good Friday | First Hour | Ps 27:12,35:11-12,35:16 (LXX Ps 26:12; Ps 34:11-12; Ps 34:16) | St Augustine | Expositions on the Psalms, Psalm 27 |
| pd-253 | Good Friday | First Hour | Ps 35:11-12,35:16 (LXX Ps 34:11-12; Ps 34:16) | St Augustine | Expositions on the Psalms, Psalm 35 |
| pd-264 | Good Friday | Third Hour | Ps 38:17 (LXX Ps 37:17) | St Augustine | Expositions on the Psalms, Psalm 38 |
| pd-269 | Good Friday | Sixth Hour | Ps 21:8-9,21:16-17,37:21-22 (LXX Ps 20:8-9; Ps 20:16-17; Ps 36:21-22) | St Augustine | Expositions on the Psalms, Psalm 21 |
| pd-271 | Good Friday | Sixth Hour | Ps 38:21-22 (LXX Ps 37:21-22) | St Augustine | Expositions on the Psalms, Psalm 38 |
| pd-283 | Good Friday | Eleventh Hour | Ps 143:6-7 (LXX Ps 142:6-7) | St Augustine | Expositions on the Psalms, Psalm 143 |
| pd-292 | Good Friday | Twelfth Hour | Ps 88:6 (LXX Ps 87:6) | St Augustine | Expositions on the Psalms, Psalm 88 |
| pd-293 | Bright Saturday | Liturgy | Ps 3:3,3:5 | St Augustine | Expositions on the Psalms, Psalm 3 |
| pd-294 | Bright Saturday | Liturgy | Ps 82:8 (LXX Ps 81:8) | St Augustine | Expositions on the Psalms, Psalm 82 |
| pd-299 | Bright Saturday | unspecified hour | Ps 130:1 (LXX Ps 129:1) | St Augustine | Expositions on the Psalms, Psalm 130 |
| pd-301 | Bright Saturday | unspecified hour | Ps 3:3,3:5 | St Augustine | Expositions on the Psalms, Psalm 3 |
| pd-303 | Bright Saturday | unspecified hour | Ps 88:4-5 (LXX Ps 87:4-5) | St Augustine | Expositions on the Psalms, Psalm 88 |
