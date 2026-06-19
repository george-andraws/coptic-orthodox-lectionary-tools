# Lectionary Note Reconciliation

Scope: read existing coverage artifacts and active study frontmatter only. No vault files were edited.

Method: deterministic phrase scan over occasion, season, service, and hour labels already present in the coverage artifact. The reconciliation is constrained to the 843 study slugs in `out/study_coverage_rollup.csv`.

## Summary

| metric | count |
| --- | ---: |
| Studies represented in rollup artifact | 843 |
| Rollup studies found in active vault scan | 843 |
| Rollup studies with prose lectionary note | 314 |
| Current vault lectionary notes outside rollup scope | 5 |
| Studies with one or more joined occasions | 414 |
| Studies with joined occasions and no lectionary note | 205 |
| bucket: agrees | 114 |
| bucket: extra_in_note | 21 |
| bucket: extra_in_note; missing_from_note | 67 |
| bucket: missing_from_note | 112 |

## Per-study reconciliation

| study_slug | bucket | join_label_count | note_label_count | one_line_diff |
| --- | --- | ---: | ---: | --- |
| 1-maccabees-1-canon-crisis-and-the-abomination-of-desolation | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 1-maccabees-10-jonathan-and-the-dangerous-gift-of-power | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 1-maccabees-11-shifting-kings-and-unstable-promises | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 1-maccabees-12-diplomacy-brotherhood-and-betrayal | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 1-maccabees-13-simon-and-the-restoration-of-the-people | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 1-maccabees-14-peace-until-a-faithful-prophet-should-arise | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 1-maccabees-15-recognition-resistance-and-fragile-freedom | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 1-maccabees-16-an-unfinished-deliverance | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 1-maccabees-2-mattathias-and-holy-refusal | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 1-maccabees-3-judas-the-hammer-and-courage-from-heaven | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 1-maccabees-4-the-cleansing-of-the-temple | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 1-maccabees-5-defending-the-scattered-faithful | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 1-maccabees-6-victory-death-and-the-limits-of-power | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 1-maccabees-7-false-priesthood-and-false-peace | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 1-maccabees-8-rome-and-the-temptation-of-security | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 1-maccabees-9-the-death-of-judas-and-the-burden-of-succession | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 2-maccabees-1-letters-dedication-and-memory-in-trouble | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 2-maccabees-10-cleansing-dedication-and-joy-restored | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 2-maccabees-11-mercy-letters-and-fragile-peace | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 2-maccabees-12-victory-sin-and-prayer-for-the-departed | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 2-maccabees-13-bethsura-prayer-and-deliverance-under-siege | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 2-maccabees-14-alcimus-nicanor-and-razis | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 2-maccabees-15-onias-jeremiah-and-the-defeat-of-nicanor | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 2-maccabees-2-gathering-hidden-fire-and-holy-memory | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 2-maccabees-3-heliodorus-and-the-sanctity-of-the-temple | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 2-maccabees-4-jason-menelaus-and-the-corruption-of-holy-office | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 2-maccabees-5-antiochus-violence-and-the-wounded-holy-city | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 2-maccabees-6-eleazar-and-holy-refusal | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 2-maccabees-7-the-seven-brothers-their-mother-and-resurrection-hope | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 2-maccabees-8-judas-prayer-and-courage-from-god | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 2-maccabees-9-antiochus-humbled-and-the-limits-of-blasphemous-power | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 3-maccabees-1-ptolemy-jerusalem-and-the-holy-place | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 3-maccabees-2-simon-s-prayer-and-god-s-defense-of-the-temple | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 3-maccabees-3-diaspora-faithfulness-under-suspicion | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 3-maccabees-4-gathering-humiliation-and-hidden-providence | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 3-maccabees-5-rage-delayed-by-providence | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 3-maccabees-6-eleazar-s-prayer-and-angelic-deliverance | agrees | 0 | 0 | extra 0: none; missing 0: none |
| 3-maccabees-7-thanksgiving-judgment-and-sacred-memory | agrees | 0 | 0 | extra 0: none; missing 0: none |
| acts-1-1-11-the-ascended-lord-and-the-promise-of-power | extra_in_note; missing_from_note | 17 | 2 | extra 1: liturgy; missing 16: 1.The Dormition of Our Lady, the Virgin Mary, the Theotokos, Fast of Nineveh, first Sunday of Christmas Fast, Holy Fifty Days, Kiak 18 plus 11 more |
| baruch-1-2-confession-in-exile | missing_from_note | 2 | 0 | extra 0: none; missing 2: Pascha / Holy Week, PRAISES OF THE PROPHETS |
| baruch-3-4-wisdom-and-return | agrees | 0 | 0 | extra 0: none; missing 0: none |
| baruch-5-put-on-the-beauty-of-glory | agrees | 0 | 0 | extra 0: none; missing 0: none |
| baruch-overview | missing_from_note | 2 | 0 | extra 0: none; missing 2: Pascha / Holy Week, PRAISES OF THE PROPHETS |
| deuteronomy-16-feasts-justice-and-the-joy-of-worship | agrees | 1 | 1 | extra 0: none; missing 0: none |
| esther-1-2-dream-empire-and-hidden-faithfulness | agrees | 0 | 0 | extra 0: none; missing 0: none |
| esther-5-7-esther-before-the-king-and-haman-s-fall | agrees | 0 | 0 | extra 0: none; missing 0: none |
| esther-8-the-counter-decree-and-shared-deliverance | agrees | 0 | 0 | extra 0: none; missing 0: none |
| esther-9-10-purim-restraint-and-mordecai-s-interpretation | agrees | 0 | 0 | extra 0: none; missing 0: none |
| ezekiel-1-the-vision-of-divine-glory | agrees | 0 | 0 | extra 0: none; missing 0: none |
| ezekiel-2-3-ezekiel-commissioned | agrees | 0 | 0 | extra 0: none; missing 0: none |
| ezekiel-4-5-sign-acts-of-siege-and-judgment | agrees | 0 | 0 | extra 0: none; missing 0: none |
| ezekiel-8-11-temple-abominations-and-departing-glory | agrees | 0 | 0 | extra 0: none; missing 0: none |
| ezra-1-2-cyrus-decree-and-the-first-return | agrees | 0 | 0 | extra 0: none; missing 0: none |
| ezra-10-covenant-correction-and-guarded-interpretation | agrees | 0 | 0 | extra 0: none; missing 0: none |
| ezra-3-altar-worship-and-the-temple-foundation | agrees | 0 | 0 | extra 0: none; missing 0: none |
| ezra-4-opposition-to-rebuilding | agrees | 0 | 0 | extra 0: none; missing 0: none |
| ezra-5-6-prophets-encourage-and-the-temple-is-completed | agrees | 0 | 0 | extra 0: none; missing 0: none |
| ezra-7-ezra-the-priest-and-scribe-arrives | agrees | 0 | 0 | extra 0: none; missing 0: none |
| ezra-8-the-journey-and-the-entrusted-vessels | agrees | 0 | 0 | extra 0: none; missing 0: none |
| ezra-9-intercession-and-corporate-confession | agrees | 0 | 0 | extra 0: none; missing 0: none |
| genesis-1-creation-and-the-image-of-god | agrees | 2 | 2 | extra 0: none; missing 0: none |
| genesis-13-14-separation-lot-war-and-melchizedek | extra_in_note | 2 | 5 | extra 3: Great Thursday Eve, the Covenant Thursday, Thursday; missing 0: none |
| genesis-18-the-lord-visits-abraham-and-intercession-for-sodom | extra_in_note | 3 | 8 | extra 5: Great Thursday Eve, liturgy, prophecy, the Covenant Thursday, Thursday; missing 0: none |
| genesis-2-eden-marriage-and-the-breath-of-life | agrees | 2 | 2 | extra 0: none; missing 0: none |
| genesis-22-the-binding-of-isaac | extra_in_note | 4 | 7 | extra 3: Great Thursday Eve, prophecy, the Covenant Thursday; missing 0: none |
| genesis-23-24-sarah-s-burial-and-isaac-s-bride | extra_in_note; missing_from_note | 5 | 3 | extra 1: Wednesday / Ninth Hour; missing 3: at_burial_site_override, Special service, Wednesday of Holy Pascha |
| genesis-3-the-fall-and-the-first-promise | agrees | 2 | 2 | extra 0: none; missing 0: none |
| genesis-48-jacob-blesses-ephraim-and-manasseh | extra_in_note | 2 | 3 | extra 1: Good Friday Eve; missing 0: none |
| genesis-6-8-noah-the-ark-flood-and-new-beginning | agrees | 2 | 2 | extra 0: none; missing 0: none |
| genesis-9-covenant-with-noah-and-the-bow-in-the-clouds | agrees | 2 | 2 | extra 0: none; missing 0: none |
| jeremiah-1-jeremiah-called | agrees | 0 | 0 | extra 0: none; missing 0: none |
| jeremiah-10-idols-and-the-living-god | agrees | 0 | 0 | extra 0: none; missing 0: none |
| jeremiah-11-12-covenant-betrayal-and-the-innocent-lamb | extra_in_note | 2 | 3 | extra 1: Good Friday Eve; missing 0: none |
| jeremiah-13-the-ruined-linen-girdle-and-bright-saturday-warning | extra_in_note; missing_from_note | 2 | 3 | extra 2: Bright Saturday, prophecy; missing 1: Pascha / Holy Week |
| jeremiah-14-15-drought-intercession-and-prophetic-anguish | agrees | 0 | 0 | extra 0: none; missing 0: none |
| jeremiah-16-life-as-sign-exile-and-the-nations-turning-from-idols | missing_from_note | 2 | 0 | extra 0: none; missing 2: Pascha / Holy Week, Wednesday Eve |
| jeremiah-17-trust-the-deep-heart-and-sabbath-at-the-gates | agrees | 0 | 0 | extra 0: none; missing 0: none |
| jeremiah-2-3-israel-forsakes-the-lord | agrees | 0 | 0 | extra 0: none; missing 0: none |
| jeremiah-4-return-and-the-circumcised-heart | agrees | 0 | 0 | extra 0: none; missing 0: none |
| jeremiah-5-searching-for-faithfulness | agrees | 0 | 0 | extra 0: none; missing 0: none |
| jeremiah-6-false-peace-and-the-old-paths | agrees | 0 | 0 | extra 0: none; missing 0: none |
| jeremiah-7-temple-sermon | extra_in_note; missing_from_note | 2 | 2 | extra 1: Monday; missing 1: Great Thursday |
| jeremiah-8-refused-repentance-and-no-balm-in-gilead | extra_in_note | 2 | 6 | extra 4: Great Thursday, the Covenant Thursday, Thursday, Thursday Eve; missing 0: none |
| jeremiah-9-lament-and-knowing-the-lord | missing_from_note | 4 | 1 | extra 0: none; missing 3: Great Thursday Eve, Monday, Tuesday |
| judith-13-the-fall-of-holofernes | agrees | 0 | 0 | extra 0: none; missing 0: none |
| judith-14-15-achior-s-conversion-and-the-people-s-deliverance | agrees | 0 | 0 | extra 0: none; missing 0: none |
| judith-16-judith-s-song-and-the-fear-of-the-lord | agrees | 0 | 0 | extra 0: none; missing 0: none |
| lamentations-1-lonely-jerusalem | extra_in_note | 2 | 3 | extra 1: Palm Sunday; missing 0: none |
| lamentations-2-the-lord-s-judgment-and-tears | agrees | 0 | 0 | extra 0: none; missing 0: none |
| lamentations-3-mercy-in-the-middle-of-affliction | extra_in_note | 2 | 3 | extra 1: Good Friday Eve; missing 0: none |
| lamentations-4-5-collapse-and-final-prayer | missing_from_note | 2 | 0 | extra 0: none; missing 2: Pascha / Holy Week, PRAISES OF THE PROPHETS |
| letter-of-jeremiah-1-fear-them-not | agrees | 0 | 0 | extra 0: none; missing 0: none |
| leviticus-16-the-day-of-atonement | agrees | 0 | 0 | extra 0: none; missing 0: none |
| luke-1-1-4-certainty-for-theophilus | extra_in_note | 0 | 2 | extra 2: liturgy, The first Sunday of Kiak; missing 0: none |
| malachi-1-polluted-offerings-and-the-great-name-among-the-nations | missing_from_note | 4 | 1 | extra 0: none; missing 3: Monday Eve, Pascha / Holy Week, Tuesday Eve |
| malachi-3-the-messenger-the-lord-in-his-temple-refining-fire-and-the-sun-of-righteousness | agrees | 1 | 1 | extra 0: none; missing 0: none |
| mark-1-1-13-the-beginning-the-forerunner-baptism-and-wilderness | extra_in_note; missing_from_note | 12 | 2 | extra 1: vespers; missing 11: Barmuda 30, Bashons 23, Hator 20, The Commemoration of the Consecration of the Church of St. Mark the Evangelist and the Appearance of His Holy Head, The Departure of St. Anianus, 2nd Pope of Alexandria plus 6 more |
| mark-1-14-20-the-kingdom-proclaimed-and-the-first-call | extra_in_note; missing_from_note | 13 | 2 | extra 1: vespers; missing 12: Hator 27, Hator 5, Kiak 16, Mesra 19, The Appearance of the Head of St. Longinus, the Soldier plus 7 more |
| mark-1-21-34-authority-in-capernaum-teaching-demons-and-healing | extra_in_note; missing_from_note | 17 | 4 | extra 2: Christmas, vespers; missing 15: A Council held in the city of Alexandria, Hator 27, Hator 5, Kiak 16, Mesra 19 plus 10 more |
| mark-1-35-45-prayer-mission-and-the-cleansing-of-the-leper | extra_in_note; missing_from_note | 3 | 4 | extra 2: matins, Tuesday; missing 1: The Martyrdom of St. John the Baptist |
| mark-2-1-12-the-paralytic-forgiveness-and-the-son-of-man | extra_in_note; missing_from_note | 3 | 5 | extra 3: liturgy, Thursday, vespers; missing 1: The Martyrdom of Saint Anastasia |
| mark-2-13-22-levi-mercy-at-the-table-fasting-and-new-wine | extra_in_note; missing_from_note | 5 | 1 | extra 1: matins; missing 5: Feast of El-Nayrouz (Beginning of the Blessed Coptic Year), Feast of Nayrouz - (Readings of the First of Tut), Holy Fifty Days, The Departure of Abba Demetrius I, 12th Pope of Alexandria, The Martyrdom of St. Simon the Zealot, the Apostle who is known by (Simon the Canaanite) |
| mark-2-23-3-6-the-sabbath-mercy-and-the-hardened-heart | extra_in_note | 0 | 3 | extra 3: Hator 24, liturgy, matins; missing 0: none |
| mark-3-7-19-the-crowds-the-mountain-and-the-twelve | extra_in_note; missing_from_note | 18 | 5 | extra 3: matins, Thursday, vespers; missing 16: Barmuda 17, Bashons 26, Hator 18, Kiak 21, Kiak 4 plus 11 more |
| matthew-1-the-genealogy-of-the-king | extra_in_note; missing_from_note | 2 | 3 | extra 2: Christmas, vespers; missing 1: The Martyrdom of 150 Men and 24 Women from Ansena |
| matthew-10-1-42-the-mission-of-the-twelve | extra_in_note; missing_from_note | 145 | 3 | extra 3: liturgy, matins, vespers; missing 145: Abib 8, Barmuda 13, Barmuda 15, Barmuda 17, Barmuda 18 plus 140 more |
| matthew-11-1-30-john-hidden-wisdom-and-the-rest-of-christ | extra_in_note; missing_from_note | 14 | 6 | extra 4: matins, Thursday, vespers, Wednesday; missing 12: Feast of El-Nayrouz (Beginning of the Blessed Coptic Year), Hator 24, The Commemoration of the Appearance of the Bodies of St. John the Baptist and Elisha the Prophet, The Commemoration of the Twenty-Four Priests, The Departure of St. Cyriacus plus 7 more |
| matthew-12-1-21-sabbath-mercy-healing-and-the-servant | extra_in_note; missing_from_note | 19 | 6 | extra 4: liturgy, matins, Paona 8, vespers; missing 17: Barmuda 28, Bashons 25, Entrance into Egypt, Hator 25, Martyrdom of the Sts. Marcian (Marcianus) and Mercurius plus 12 more |
| matthew-12-22-50-spirit-sign-repentance-and-true-kinship | missing_from_note | 29 | 0 | extra 0: none; missing 29: 1.The Dormition of Our Lady, the Virgin Mary, the Theotokos, Barmuda 28, Bashons 25, Entrance into Egypt, Fast of Nineveh plus 24 more |
| matthew-13-1-23-the-parable-of-the-sower | extra_in_note; missing_from_note | 2 | 2 | extra 1: liturgy; missing 1: The Departure of St. Peter the Third 27th Pope of Alexandria |
| matthew-13-24-43-wheat-tares-mustard-seed-and-leaven | extra_in_note; missing_from_note | 3 | 3 | extra 2: liturgy, Paona 12; missing 2: The Commemoration of Archangel Michael, The Commemoration of the Honored Archangel Michael |
| matthew-13-44-52-treasure-pearl-dragnet-and-the-trained-scribe | extra_in_note; missing_from_note | 7 | 3 | extra 2: Paona 12, vespers; missing 6: Feast of El-Nayrouz (Beginning of the Blessed Coptic Year), Feast of Nayrouz - (Readings of the First of Tut), procession_station_04_archangel_michael, Special service, The Commemoration of Archangel Michael plus 1 more |
| matthew-2-emmanuel-the-magi-egypt-and-nazareth | extra_in_note; missing_from_note | 14 | 5 | extra 2: liturgy, matins; missing 11: Amshir 7, Entrance into Egypt, Fast of Nineveh, The Commemoration of the Consecration of the Church of the Virgin Lady known as El-Mahammah, The Commemoration of the Entry of the Lord Christ to Egypt plus 6 more |
| matthew-3-john-repentance-and-the-baptism-of-christ | extra_in_note; missing_from_note | 7 | 3 | extra 2: matins, vespers; missing 6: main_readings, procession_station_10_baptismal_font, Special service, The Commemoration of the Archangel Michael, The Holy Theophany of Our Lord, God and Savior, Jesus Christ (Baptism of the Lord christ) plus 1 more |
| matthew-4-1-11-the-temptation-in-the-wilderness | extra_in_note; missing_from_note | 2 | 2 | extra 1: liturgy; missing 1: Mesra 5 |
| matthew-4-12-25-galilee-and-the-first-call | missing_from_note | 67 | 0 | extra 0: none; missing 67: Amshir 14, Amshir 18, Amshir 27, Amshir 5, Baba 3 plus 62 more |
| matthew-5-1-16-beatitudes-salt-and-light | missing_from_note | 53 | 1 | extra 0: none; missing 52: 6TH HOUR, Agpeya Sixth Hour (Sext), Amshir 14, Amshir 18, Amshir 27 plus 47 more |
| matthew-5-17-26-the-law-fulfilled-and-the-heart-reconciled | extra_in_note | 1 | 3 | extra 2: matins, Wednesday; missing 0: none |
| matthew-5-27-48-purity-truth-mercy-and-enemy-love | extra_in_note; missing_from_note | 3 | 5 | extra 3: liturgy, matins, vespers; missing 1: The Martyrdom of St. Shenousi (Sanusi) |
| matthew-6-1-18-secret-almsgiving-prayer-and-fasting | extra_in_note; missing_from_note | 3 | 3 | extra 1: liturgy; missing 1: Special service |
| matthew-6-19-34-treasure-the-eye-two-masters-and-anxiety | extra_in_note | 1 | 3 | extra 2: liturgy, vespers; missing 0: none |
| matthew-8-1-17-the-king-who-cleanses-and-heals | extra_in_note; missing_from_note | 12 | 3 | extra 2: matins, vespers; missing 11: A Council held in the city of Alexandria, Barmuda 28, Bashons 25, Hator 25, Martyrdom of the Sts. Marcian (Marcianus) and Mercurius plus 6 more |
| matthew-8-18-9-8-following-christ-into-his-authority-over-chaos-demons-and-sin | extra_in_note | 2 | 4 | extra 2: matins, Monday; missing 0: none |
| matthew-9-18-38-faith-touch-sight-speech-and-the-harvest | extra_in_note; missing_from_note | 8 | 6 | extra 4: matins, Tuesday, vespers, Wednesday; missing 6: Abib 7, Amshir 2, Fast of Nineveh, part_5, Special service plus 1 more |
| matthew-9-9-17-the-physician-the-table-and-the-new-wine | extra_in_note; missing_from_note | 4 | 6 | extra 4: matins, Tuesday, vespers, Wednesday; missing 2: The Departure of Abba Demetrius I, 12th Pope of Alexandria, The Martyrdom of St. Simon the Zealot, the Apostle who is known by (Simon the Canaanite) |
| nahum-1-the-lord-is-slow-to-anger-and-great-in-power | extra_in_note; missing_from_note | 2 | 3 | extra 2: Palm Sunday, prophecy; missing 1: Pascha / Holy Week |
| nehemiah-1-prayer-and-holy-grief | agrees | 0 | 0 | extra 0: none; missing 0: none |
| nehemiah-10-covenant-commitments-and-the-house-of-god | agrees | 0 | 0 | extra 0: none; missing 0: none |
| nehemiah-11-resettling-the-holy-city | agrees | 0 | 0 | extra 0: none; missing 0: none |
| nehemiah-12-dedication-procession-and-liturgical-joy | agrees | 0 | 0 | extra 0: none; missing 0: none |
| nehemiah-13-final-reforms | agrees | 0 | 0 | extra 0: none; missing 0: none |
| nehemiah-2-sent-to-jerusalem | agrees | 0 | 0 | extra 0: none; missing 0: none |
| nehemiah-3-the-builders-of-the-wall | agrees | 0 | 0 | extra 0: none; missing 0: none |
| nehemiah-4-opposition-prayer-and-watchfulness | agrees | 0 | 0 | extra 0: none; missing 0: none |
| nehemiah-5-internal-injustice-and-the-fear-of-god | agrees | 0 | 0 | extra 0: none; missing 0: none |
| nehemiah-6-false-prophecy-and-completion-of-the-wall | agrees | 0 | 0 | extra 0: none; missing 0: none |
| nehemiah-7-register-of-the-returned-exiles | agrees | 0 | 0 | extra 0: none; missing 0: none |
| nehemiah-8-the-law-read-to-the-people | agrees | 0 | 0 | extra 0: none; missing 0: none |
| nehemiah-9-confession-through-the-history-of-mercy | agrees | 0 | 0 | extra 0: none; missing 0: none |
| obadiah-1-pride-brotherly-violence-and-the-kingdom-of-the-lord | extra_in_note | 0 | 1 | extra 1: Toba 15; missing 0: none |
| prayer-of-azariah-and-song-of-the-three-holy-children-1-why-this-passage-is-in-our-bible-and-our-hymns | extra_in_note; missing_from_note | 2 | 1 | extra 1: Bright Saturday; missing 2: Pascha / Holy Week, PRAISES OF THE PROPHETS |
| prayer-of-azariah-and-song-of-the-three-holy-children-2-the-prayer-of-azariah | extra_in_note | 0 | 2 | extra 2: Bright Saturday, part_1; missing 0: none |
| prayer-of-azariah-and-song-of-the-three-holy-children-3-the-angel-in-the-furnace | extra_in_note | 0 | 1 | extra 1: Bright Saturday; missing 0: none |
| prayer-of-azariah-and-song-of-the-three-holy-children-4-the-song-and-the-third-hoos | agrees | 0 | 0 | extra 0: none; missing 0: none |
| prayer-of-azariah-and-song-of-the-three-holy-children-5-bright-saturday | extra_in_note; missing_from_note | 2 | 2 | extra 2: Bright Saturday, Special service; missing 2: Pascha / Holy Week, PRAISES OF THE PROPHETS |
| prayer-of-manasseh-1-the-knee-of-the-heart | extra_in_note | 0 | 2 | extra 2: Bright Saturday, PRAISES OF THE PROPHETS; missing 0: none |
| psalm-1-lxx-1-the-blessed-man-and-the-two-ways | missing_from_note | 12 | 1 | extra 0: none; missing 11: Agpeya First Hour (Prime / Morning Prayer), Great Lent, The Commemoration of the Crucifixion of Our Lord Jesus Christ, The Departure of Abba Abraam, Companion of Abba Gawarga, The Departure of St. Agrippinus, 10th Pope of Alexandria plus 6 more |
| psalm-10-lxx-9-22-39-the-hidden-god-and-the-poor | agrees | 0 | 0 | extra 0: none; missing 0: none |
| psalm-100-lxx-99-make-a-joyful-noise-to-the-lord | missing_from_note | 6 | 0 | extra 0: none; missing 6: Agpeya, Agpeya Ninth Hour (None), Great Lent, Holy Fifty Days, The fourth Sunday of Hator plus 1 more |
| psalm-101-lxx-100-i-will-sing-of-mercy-and-judgment | missing_from_note | 5 | 0 | extra 0: none; missing 5: Agpeya, Agpeya Ninth Hour (None), Great Lent, Holy Fifty Days, The Departure of St. Malachi, the Prophet |
| psalm-102-lxx-101-bless-the-lord-o-my-soul | missing_from_note | 20 | 0 | extra 0: none; missing 20: first Sunday of Christmas Fast, Good Friday Eve, Great Lent, Kiak 13, main_readings plus 15 more |
| psalm-103-lxx-102-bless-the-lord-o-my-soul-part-2 | missing_from_note | 6 | 0 | extra 0: none; missing 6: Hator 12, procession_station_04_archangel_michael, Special service, The Commemoration of Archangel Michael, The Commemoration of the Honored Archangel Michael plus 1 more |
| psalm-104-lxx-103-bless-the-lord-o-my-soul | missing_from_note | 17 | 0 | extra 0: none; missing 17: Baba 6, Hator 12, Holy Fifty Days, procession_station_01_main_sanctuary, Special service plus 12 more |
| psalm-105-lxx-104-give-thanks-to-the-lord | missing_from_note | 46 | 0 | extra 0: none; missing 46: Abib 26, Barmuda 30, Barmuda 5, Barmuda 7, Bashons 23 plus 41 more |
| psalm-106-lxx-105-give-thanks-to-the-lord-for-he-is-good | missing_from_note | 5 | 0 | extra 0: none; missing 5: Entrance into Egypt, Holy Fifty Days, The Commemoration of the Consecration of the Church of the Virgin Lady known as El-Mahammah, The Commemoration of the Entry of the Lord Christ to Egypt, The Departure of the Upright St. Joseph, the Carpenter |
| psalm-107-lxx-106-give-thanks-to-the-lord-for-he-is-good | missing_from_note | 47 | 0 | extra 0: none; missing 47: A Council held in the city of Alexandria, Abib 14, Barmuda 12, Barmuda 14, Barmuda 22 plus 42 more |
| psalm-108-lxx-107-o-god-my-heart-is-ready | missing_from_note | 3 | 0 | extra 0: none; missing 3: Great Thursday Eve, Holy Fifty Days, Pascha / Holy Week |
| psalm-109-lxx-108-o-god-pass-not-over-my-praise-in-silence | agrees | 0 | 0 | extra 0: none; missing 0: none |
| psalm-11-lxx-10-the-lord-is-in-his-holy-temple | agrees | 0 | 0 | extra 0: none; missing 0: none |
| psalm-110-lxx-109-the-lord-said-to-my-lord | missing_from_note | 95 | 0 | extra 0: none; missing 95: A Council held in the city of Alexandria, Abib 14, Abib 3, Agpeya, Agpeya Ninth Hour (None) plus 90 more |
| psalm-111-lxx-110-i-will-give-thee-thanks-o-lord-with-my-whole-heart | missing_from_note | 3 | 0 | extra 0: none; missing 3: Agpeya, Agpeya Ninth Hour (None), Holy Fifty Days |
| psalm-112-lxx-111-blessed-is-the-man-that-fears-the-lord | missing_from_note | 34 | 0 | extra 0: none; missing 34: Agpeya, Agpeya Ninth Hour (None), Amshir 15, Assembly of the Holy Council on the island of Bani-Omar, Fast of Nineveh plus 29 more |
| psalm-113-lxx-112-praise-the-lord-ye-servants-of-his | missing_from_note | 31 | 0 | extra 0: none; missing 31: Abib 8, Agpeya, Agpeya First Hour (Prime / Morning Prayer), Agpeya Ninth Hour (None), Amshir 7 plus 26 more |
| psalm-114-lxx-113-1-8-at-the-going-forth-of-israel-from-egypt | missing_from_note | 2 | 0 | extra 0: none; missing 2: main_readings, Special service |
| psalm-115-lxx-113-9-26-not-to-us-o-lord-but-to-thy-name-give-glory | missing_from_note | 5 | 0 | extra 0: none; missing 5: Amshir 7, Fast of Nineveh, Holy Fifty Days, The Commemoration of the Slain Children of Bethlehem by the Order of King Herod, Toba 3 |
| psalm-116-lxx-114-115-the-cup-of-salvation-in-the-land-of-the-living | missing_from_note | 13 | 0 | extra 0: none; missing 13: Agpeya, Agpeya Ninth Hour (None), Agpeya Veil Prayer, Circumcision of our Lord, Entrance into the Temple plus 8 more |
| psalm-117-lxx-116-praise-the-lord-all-ye-nations | missing_from_note | 5 | 0 | extra 0: none; missing 5: Agpeya, Agpeya Eleventh Hour (Vespers), Agpeya Midnight Prayer - First Watch, Great Lent, Holy Fifty Days |
| psalm-118-lxx-117-give-thanks-to-the-lord-for-he-is-good | missing_from_note | 16 | 0 | extra 0: none; missing 16: Agpeya, Agpeya Eleventh Hour (Vespers), Agpeya Midnight Prayer - First Watch, Great Lent, Holy Fifty Days plus 11 more |
| psalm-119-lxx-118-blessed-are-the-undefiled-in-the-way | missing_from_note | 19 | 0 | extra 0: none; missing 19: A Thanksgiving To God, Agpeya, Agpeya Midnight Prayer - First Watch, Agpeya Veil Prayer, Great Lent plus 14 more |
| psalm-12-lxx-11-pure-words-in-a-double-hearted-generation | missing_from_note | 8 | 0 | extra 0: none; missing 8: Agpeya, Agpeya First Hour (Prime / Morning Prayer), Great Lent, Holy Fifty Days, Monday plus 3 more |
| psalm-120-lxx-119-in-my-distress-i-cried-to-the-lord | missing_from_note | 5 | 0 | extra 0: none; missing 5: Agpeya, Agpeya Eleventh Hour (Vespers), Agpeya Midnight Prayer - Second Watch, Pascha / Holy Week, Tuesday |
| psalm-121-lxx-120-i-lift-up-my-eyes-to-the-hills | missing_from_note | 4 | 0 | extra 0: none; missing 4: Agpeya, Agpeya Eleventh Hour (Vespers), Agpeya Midnight Prayer - Second Watch, Agpeya Veil Prayer |
| psalm-122-lxx-121-i-was-glad-when-they-said-to-me | missing_from_note | 12 | 0 | extra 0: none; missing 12: Agpeya, Agpeya Eleventh Hour (Vespers), Agpeya Midnight Prayer - Second Watch, foundation_cornerstone, Great Lent plus 7 more |
| psalm-123-lxx-122-unto-thee-have-i-lifted-up-mine-eyes | missing_from_note | 3 | 0 | extra 0: none; missing 3: Agpeya, Agpeya Eleventh Hour (Vespers), Agpeya Midnight Prayer - Second Watch |
| psalm-124-lxx-123-if-it-had-not-been-the-lord-who-was-on-our-side | missing_from_note | 3 | 0 | extra 0: none; missing 3: Agpeya, Agpeya Eleventh Hour (Vespers), Agpeya Midnight Prayer - Second Watch |
| psalm-125-lxx-124-they-that-trust-in-the-lord-shall-be-as-mount-sion | missing_from_note | 3 | 0 | extra 0: none; missing 3: Agpeya, Agpeya Eleventh Hour (Vespers), Agpeya Midnight Prayer - Second Watch |
| psalm-13-lxx-12-how-long-o-lord | missing_from_note | 15 | 0 | extra 0: none; missing 15: Agpeya, Agpeya First Hour (Prime / Morning Prayer), Agpeya Midnight Prayer - First Watch, Agpeya Veil Prayer, first Sunday of Christmas Fast plus 10 more |
| psalm-132-lxx-131-lord-remember-david-and-all-his-meekness | missing_from_note | 108 | 0 | extra 0: none; missing 108: Agpeya, Agpeya Midnight Prayer - Third Watch, Agpeya Twelfth Hour (Compline / Before Sleep), Agpeya Veil Prayer, Amshir 14 plus 103 more |
| psalm-133-lxx-132-behold-how-good-and-pleasant | missing_from_note | 4 | 0 | extra 0: none; missing 4: Agpeya, Agpeya Midnight Prayer - Third Watch, Agpeya Twelfth Hour (Compline / Before Sleep), Agpeya Veil Prayer |
| psalm-134-lxx-133-bless-ye-the-lord-by-night | missing_from_note | 6 | 0 | extra 0: none; missing 6: Agpeya, Agpeya Midnight Prayer - Third Watch, Agpeya Twelfth Hour (Compline / Before Sleep), Agpeya Veil Prayer, The Departure of St. Kyrillos (Cyril) the First, the Twenty- Fourth Pope of Alexandria plus 1 more |
| psalm-135-lxx-134-praise-the-name-of-the-lord | missing_from_note | 11 | 0 | extra 0: none; missing 11: Hator 27, Hator 5, Holy Fifty Days, Kiak 16, The Appearance of the Head of St. Longinus, the Soldier plus 6 more |
| psalm-136-lxx-135-his-mercy-endures-forever | missing_from_note | 1 | 0 | extra 0: none; missing 1: Holy Fifty Days |
| psalm-137-lxx-136-by-the-rivers-of-babylon | missing_from_note | 4 | 0 | extra 0: none; missing 4: Agpeya, Agpeya Midnight Prayer - Third Watch, Agpeya Twelfth Hour (Compline / Before Sleep), Agpeya Veil Prayer |
| psalm-138-lxx-137-before-the-angels-i-will-sing | missing_from_note | 16 | 0 | extra 0: none; missing 16: Agpeya, Agpeya Midnight Prayer - Third Watch, Agpeya Twelfth Hour (Compline / Before Sleep), Great Lent, Hator 24 plus 11 more |
| psalm-139-lxx-138-whither-shall-i-go-from-thy-spirit | missing_from_note | 9 | 0 | extra 0: none; missing 9: Barmuda 16, Great Lent, Kiak 24, The Commemoration of St. John The Evangelist, The Departure of St. John, of the Golden Gospel plus 4 more |
| psalm-14-lxx-13-the-fool-and-the-salvation-from-zion | missing_from_note | 1 | 0 | extra 0: none; missing 1: The third Sunday of Mesra |
| psalm-140-lxx-139-rescue-me-from-the-evil-man | missing_from_note | 3 | 0 | extra 0: none; missing 3: Pascha / Holy Week, Thursday Eve, Wednesday Eve |
| psalm-141-lxx-140-let-my-prayer-be-set-forth-as-incense | missing_from_note | 4 | 0 | extra 0: none; missing 4: Agpeya, Agpeya Midnight Prayer - Third Watch, Agpeya Twelfth Hour (Compline / Before Sleep), Agpeya Veil Prayer |
| psalm-142-lxx-141-bring-my-soul-out-of-prison | missing_from_note | 6 | 0 | extra 0: none; missing 6: Agpeya, Agpeya Midnight Prayer - Third Watch, Agpeya Twelfth Hour (Compline / Before Sleep), fifth_prayer, Great Lent plus 1 more |
| psalm-143-lxx-142-teach-me-to-do-thy-will | missing_from_note | 14 | 0 | extra 0: none; missing 14: Agpeya, Agpeya First Hour (Prime / Morning Prayer), Good Friday, Great Lent, Pascha / Holy Week plus 9 more |
| psalm-144-lxx-143-blessed-be-the-lord-my-god | missing_from_note | 10 | 0 | extra 0: none; missing 10: Annunciation, second Sunday of Christmas Fast, The Commemoration of the Life giving Annunciation, The Departure of the Saint Abba Hor, the Monk, The fifth Sunday of Abib (Readings of 29th Baramhat) plus 5 more |
| psalm-145-lxx-144-i-will-exalt-thee-my-god-and-king | missing_from_note | 23 | 0 | extra 0: none; missing 23: Barmuda 17, Bashons 26, Great Lent, Hator 18, Holy Fifty Days plus 18 more |
| psalm-146-lxx-145-put-not-your-trust-in-princes | missing_from_note | 15 | 0 | extra 0: none; missing 15: Agpeya, Agpeya Midnight Prayer - Third Watch, Agpeya Twelfth Hour (Compline / Before Sleep), Agpeya Veil Prayer, Hator 27 plus 10 more |
| psalm-147-lxx-146-147-he-heals-the-broken-in-heart | missing_from_note | 4 | 0 | extra 0: none; missing 4: Agpeya, Agpeya Midnight Prayer - Third Watch, Agpeya Twelfth Hour (Compline / Before Sleep), Holy Fifty Days |
| psalm-148-lxx-148-praise-the-lord-from-the-heavens | missing_from_note | 2 | 0 | extra 0: none; missing 2: Hator 12, Paona 12 |
| psalm-149-lxx-149-sing-to-the-lord-a-new-song | missing_from_note | 3 | 0 | extra 0: none; missing 3: The Commemoration of Archangel Michael, The Commemoration of the Honored Archangel Michael, The Martyrdom of St. Moses (Moisees) and his Sister Sarah |
| psalm-15-lxx-14-who-may-dwell-on-the-holy-mountain | missing_from_note | 10 | 0 | extra 0: none; missing 10: Agpeya, Agpeya First Hour (Prime / Morning Prayer), Holy Fifty Days, The fifth Sunday of Baba, The fifth Sunday of Kiak plus 5 more |
| psalm-150-lxx-150-let-everything-that-has-breath-praise-the-lord | agrees | 0 | 0 | extra 0: none; missing 0: none |
| psalm-151-lxx-151-i-was-small-among-my-brethren | agrees | 0 | 0 | extra 0: none; missing 0: none |
| psalm-16-lxx-15-the-holy-one-who-does-not-see-corruption | missing_from_note | 14 | 0 | extra 0: none; missing 14: 3RD HOUR, Agpeya, Agpeya First Hour (Prime / Morning Prayer), Agpeya Veil Prayer, Barmuda 21 plus 9 more |
| psalm-17-lxx-16-keep-me-as-the-apple-of-your-eye | missing_from_note | 3 | 0 | extra 0: none; missing 3: Great Lent, The Departure of St. James, the Ascetic, The third Sunday of Amshir |
| psalm-18-lxx-17-the-lord-my-rock-and-deliverer | missing_from_note | 39 | 0 | extra 0: none; missing 39: A Council held in the city of Alexandria, Abib 20, Abib 25, Amshir 25, Amshir 28 plus 34 more |
| psalm-19-lxx-18-the-heavens-declare-the-glory-of-god | missing_from_note | 40 | 0 | extra 0: none; missing 40: Abib 16, Agpeya, Agpeya First Hour (Prime / Morning Prayer), Amshir 29, Assembly of the Holy Council on the island of Bani-Omar plus 35 more |
| psalm-2-lxx-2-the-son-and-the-nations | missing_from_note | 8 | 0 | extra 0: none; missing 8: Agpeya, Agpeya First Hour (Prime / Morning Prayer), Christmas, Good Friday Eve, Great Lent plus 3 more |
| psalm-20-lxx-19-may-the-lord-hear-you-in-the-day-of-trouble | extra_in_note; missing_from_note | 6 | 4 | extra 2: liturgy, vespers; missing 4: Agpeya Third Hour (Terce), The first Sunday of Abib, The first Sunday of Abib (Apostle's Feast), The Martyrdom of Saint Febronia the Ascetic |
| psalm-21-lxx-20-the-crown-and-joy-of-the-king | extra_in_note; missing_from_note | 20 | 1 | extra 1: liturgy; missing 20: Barmuda 15, Barmuda 29, Bashons 22, Good Friday, Pascha / Holy Week plus 15 more |
| psalm-22-lxx-21-the-suffering-servant-and-the-praise-of-the-resurrection | extra_in_note; missing_from_note | 8 | 9 | extra 4: Good Friday Eve, matins, Palm Sunday, Tuesday; missing 3: The Departure of Abba Demetrius I, 12th Pope of Alexandria, The Martyrdom of St. Simon the Zealot, the Apostle who is known by (Simon the Canaanite), Wednesday Eve |
| psalm-23-lxx-22-the-shepherd-the-table-and-the-house-of-the-lord | extra_in_note; missing_from_note | 12 | 10 | extra 3: Good Friday Eve, Great Thursday Eve, Thursday; missing 5: Agpeya Third Hour (Terce), part_3, Pascha / Holy Week, Special service, vespers |
| psalm-24-lxx-23-the-king-of-glory-enters | extra_in_note; missing_from_note | 15 | 5 | extra 2: liturgy, matins; missing 12: Agpeya Third Hour (Terce), part_3, Special service, The Feast of the Ascension, The fifth Sunday of Baba plus 7 more |
| psalm-25-lxx-24-teach-me-your-paths | missing_from_note | 9 | 5 | extra 0: none; missing 4: Agpeya First Hour (Prime / Morning Prayer), Pascha / Holy Week, Special service, Tuesday |
| psalm-26-lxx-25-i-have-loved-the-beauty-of-thy-house | extra_in_note; missing_from_note | 8 | 3 | extra 1: matins; missing 6: Agpeya Third Hour (Terce), part_3, Special service, The Commemoration of the Consecration of the Sanctuaries of the church of Resurrection in Jerusalem, The Departure of St. Helena, The Empress plus 1 more |
| psalm-27-lxx-26-the-lord-is-my-light-and-my-saviour | extra_in_note; missing_from_note | 13 | 11 | extra 5: Good Friday Eve, Great Thursday, the Covenant Thursday, Thursday, Thursday Eve; missing 7: Agpeya First Hour (Prime / Morning Prayer), Monday Eve, part_3, part_4, Pascha / Holy Week plus 2 more |
| psalm-28-lxx-27-save-thy-people-and-bless-thine-inheritance | extra_in_note; missing_from_note | 11 | 3 | extra 1: Agpeya; missing 9: Good Friday Eve, matins, Monday Eve, Pascha / Holy Week, Special service plus 4 more |
| psalm-29-lxx-28-the-voice-of-the-lord-upon-the-waters | extra_in_note; missing_from_note | 11 | 6 | extra 3: Hosanna Sunday, matins, Palm Sunday; missing 8: Agpeya Third Hour (Terce), Monday Eve, Pascha / Holy Week, procession_station_10_baptismal_font, Special service plus 3 more |
| psalm-3-lxx-3-the-betrayed-king-sleeps-and-rises | missing_from_note | 6 | 0 | extra 0: none; missing 6: Agpeya, Agpeya First Hour (Prime / Morning Prayer), Agpeya Midnight Prayer - First Watch, Bright Saturday, Pascha / Holy Week plus 1 more |
| psalm-30-lxx-29-mourning-turned-into-joy | extra_in_note; missing_from_note | 7 | 5 | extra 1: matins; missing 3: Agpeya Third Hour (Terce), Feast of El-Nayrouz (Beginning of the Blessed Coptic Year), The first Sunday of Tout |
| psalm-31-lxx-30-into-thy-hands-i-commit-my-spirit | extra_in_note; missing_from_note | 13 | 8 | extra 4: Good Friday Eve, Great Thursday Eve, the Covenant Thursday, Thursday; missing 9: Feast of El-Nayrouz (Beginning of the Blessed Coptic Year), matins, Pascha / Holy Week, Special service, The first Sunday of Abib plus 4 more |
| psalm-32-lxx-31-blessed-is-the-forgiven-man | extra_in_note; missing_from_note | 40 | 4 | extra 1: Agpeya; missing 37: Assembly of the Holy Council on the island of Bani-Omar, Barmuda 9, Fast of Nineveh, Hator 3, Hator 9 plus 32 more |
| psalm-33-lxx-32-the-new-song-and-the-counsel-of-the-lord | extra_in_note; missing_from_note | 36 | 9 | extra 2: Monday, Tuesday; missing 29: Barmuda 9, Fast of Nineveh, Hator 8, Kiak 25, Kiak 7 plus 24 more |
| psalm-34-lxx-33-taste-and-see-that-the-lord-is-good | extra_in_note; missing_from_note | 88 | 10 | extra 6: Great Thursday, Hosanna Sunday, Palm Sunday, the Covenant Thursday, Thursday plus 1 more; missing 84: Abib 27, Agpeya Third Hour (Terce), Barmuda 15, Barmuda 23, Barmuda 29 plus 79 more |
| psalm-35-lxx-34-contend-o-lord-with-those-who-contend-with-me | extra_in_note; missing_from_note | 8 | 8 | extra 4: matins, Monday, Tuesday, vespers; missing 4: Pascha / Holy Week, The Commemoration of the Appearance of the Bodies of St. John the Baptist and Elisha the Prophet, The fourth Sunday of Baba, The Martyrdom of St. Bacchus, the Friend of St. Sergius |
| psalm-36-lxx-35-in-thy-light-we-shall-see-light | extra_in_note; missing_from_note | 3 | 4 | extra 2: liturgy, matins; missing 1: The Departure of St. John the Evangelist and Theologian |
| psalm-37-lxx-36-the-meek-shall-inherit-the-earth | extra_in_note; missing_from_note | 35 | 4 | extra 3: Agpeya, liturgy, matins; missing 34: Barmuda 1, Barmuda 10, Bashons 20, Fast of Nineveh, Good Friday plus 29 more |
| psalm-38-lxx-37-wounded-by-sin-and-silent-before-accusers | extra_in_note; missing_from_note | 8 | 5 | extra 3: Agpeya, Good Friday Eve, matins; missing 6: part_6, Pascha / Holy Week, Special service, The Construction of the first church of St. George in the cities of Birma and Beer Maa (Water Well) in the Oases, The third Sunday of Paona plus 1 more |
| psalm-39-lxx-38-a-stranger-before-thee | extra_in_note; missing_from_note | 4 | 8 | extra 5: Agpeya, liturgy, Pascha / Holy Week, Thursday, vespers; missing 1: part_5 |
| psalm-4-lxx-4-peace-in-the-night | missing_from_note | 57 | 0 | extra 0: none; missing 57: Abib 19, Abib 30, Abib 8, Agpeya, Agpeya First Hour (Prime / Morning Prayer) plus 52 more |
| psalm-40-lxx-39-a-body-hast-thou-prepared-me | extra_in_note; missing_from_note | 34 | 6 | extra 2: Agpeya, Special service; missing 30: Barmuda 30, Bashons 21, Bashons 23, Bashons 29, Great Thursday plus 25 more |
| psalm-41-lxx-40-the-betrayed-friend-and-the-poor-man | extra_in_note; missing_from_note | 12 | 6 | extra 1: Bright Saturday; missing 7: 9TH HOUR, Agpeya Third Hour (Terce), the Covenant Thursday, The Departure of St. Eutychus, The Departure of St. Thaddaeus, the Apostle plus 2 more |
| psalm-42-lxx-41-as-the-hart-longs-for-the-living-god | extra_in_note; missing_from_note | 9 | 10 | extra 7: Agpeya, Bright Saturday, matins, Pascha / Holy Week, Special service plus 2 more; missing 6: Paramouni of Holy Theophany (Epiphany), The Commemoration of the Archangel Michael, The Departure of St. Bessarion, the Great, The Feast of Epiphany, The Holy Theophany of Our Lord, God and Savior, Jesus Christ (Baptism of the Lord christ) plus 1 more |
| psalm-43-lxx-42-send-forth-thy-light-and-thy-truth | extra_in_note; missing_from_note | 4 | 8 | extra 5: Bright Saturday, matins, Pascha / Holy Week, Special service, vespers; missing 1: Agpeya Third Hour (Terce) |
| psalm-44-lxx-43-for-thy-sake-we-are-killed-all-the-day | extra_in_note | 1 | 7 | extra 6: Agpeya, Bright Saturday, Pascha / Holy Week, Special service, vespers plus 1 more; missing 0: none |
| psalm-45-lxx-44-the-king-the-bride-and-the-oil-of-gladness | extra_in_note; missing_from_note | 89 | 6 | extra 1: Good Friday Eve; missing 84: 1.The Dormition of Our Lady, the Virgin Mary, the Theotokos, Agpeya Third Hour (Terce), Barmuda 11, Barmuda 16, Barmuda 2 plus 79 more |
| psalm-46-lxx-45-be-still-and-know-that-i-am-god | extra_in_note; missing_from_note | 18 | 6 | extra 4: Bright Saturday, Pascha / Holy Week, Special service, vespers; missing 16: Abib 23, Agpeya Third Hour (Terce), Baba 29, Hator 27, Hator 5 plus 11 more |
| psalm-47-lxx-46-the-king-ascends-with-a-shout | extra_in_note; missing_from_note | 8 | 5 | extra 3: liturgy, matins, vespers; missing 6: Agpeya Third Hour (Terce), Our father Abraham: Who can describe the virtues of he who became father to many nations?, The Departure of Pope John (Youhanna) the First, the Twenty Ninth Patriarch of the See of St. Mark, The first Sunday of Toba, The fourth Sunday of Bashons plus 1 more |
| psalm-48-lxx-47-the-city-of-the-great-king | extra_in_note; missing_from_note | 10 | 10 | extra 7: liturgy, matins, Mesra 16 (St Mary's Feast), Paona 21, Thursday plus 2 more; missing 7: 1.The Dormition of Our Lady, the Virgin Mary, the Theotokos, Fast of Nineveh, Kiak 3, The Assumption of the Body of the Pure Virgin St. Mary, The Commemoration of the First Church for The Virgin Mary in the city of Philippi plus 2 more |
| psalm-49-lxx-48-no-man-can-redeem-his-brother | agrees | 0 | 0 | extra 0: none; missing 0: none |
| psalm-5-lxx-5-morning-prayer-and-the-house-of-mercy | missing_from_note | 47 | 0 | extra 0: none; missing 47: Abib 11, Abib 22, Agpeya, Agpeya First Hour (Prime / Morning Prayer), Amshir 13 plus 42 more |
| psalm-50-lxx-49-the-god-of-gods-calls-for-true-worship | extra_in_note; missing_from_note | 11 | 9 | extra 6: Christmas, Great Thursday Eve, liturgy, the Covenant Thursday, Thursday plus 1 more; missing 8: Circumcision of our Lord, Pascha / Holy Week, The Commemoration of the Circumcision of the Lord Christ, The Departure of St. Malachi, the Prophet, The Feast of Presenting the Lord Christ in the Temple plus 3 more |
| psalm-51-lxx-50-have-mercy-upon-me-o-god | extra_in_note; missing_from_note | 9 | 11 | extra 5: Agpeya, Great Thursday Eve, the Covenant Thursday, Thursday, vespers; missing 3: matins, Special service, The Commemoration of the Appearance of the Bodies of St. John the Baptist and Elisha the Prophet |
| psalm-52-lxx-51-the-deceitful-tongue-and-the-fruitful-olive | extra_in_note; missing_from_note | 7 | 4 | extra 3: Hosanna Sunday, Palm Sunday, vespers; missing 6: Special service, The Departure of St. Kyrillos (Cyril) the First, the Twenty- Fourth Pope of Alexandria, The Martyrdom of St. John the Baptist, The Nativity of St. John, the Baptist, The third Sunday of Abib plus 1 more |
| psalm-53-lxx-52-the-fool-repeated-and-the-salvation-from-zion | agrees | 0 | 0 | extra 0: none; missing 0: none |
| psalm-54-lxx-53-save-me-by-thy-name | extra_in_note; missing_from_note | 3 | 4 | extra 2: liturgy, Tuesday; missing 1: Agpeya Sixth Hour (Sext) |
| psalm-55-lxx-54-betrayed-by-a-familiar-friend | extra_in_note; missing_from_note | 6 | 10 | extra 6: Great Thursday Eve, liturgy, matins, the Covenant Thursday, Thursday plus 1 more; missing 2: Good Friday Eve, Thursday Eve |
| psalm-56-lxx-55-tears-before-god-in-the-land-of-the-living | agrees | 1 | 1 | extra 0: none; missing 0: none |
| psalm-57-lxx-56-under-the-shadow-of-thy-wings | extra_in_note; missing_from_note | 9 | 8 | extra 4: matins, Tuesday, vespers, Wednesday; missing 5: Agpeya Sixth Hour (Sext), Pascha / Holy Week, The Departure of St. Simon II, 51st Pope of the See of St. Mark, The third Sunday of Baba, Wednesday Eve |
| psalm-58-lxx-57-judge-rightly-you-sons-of-men | extra_in_note | 2 | 6 | extra 4: Great Thursday, the Covenant Thursday, Thursday, Thursday Eve; missing 0: none |
| psalm-59-lxx-58-deliver-me-from-bloody-men | extra_in_note; missing_from_note | 5 | 1 | extra 1: vespers; missing 5: Good Friday Eve, Pascha / Holy Week, The Commemoration of the Relocation of the Relics of Sts. Apakir and John, The fourth Sunday of Abib, Wednesday Eve |
| psalm-6-lxx-6-tears-healing-and-the-eighth-day | missing_from_note | 12 | 0 | extra 0: none; missing 12: Agpeya, Agpeya First Hour (Prime / Morning Prayer), Agpeya Midnight Prayer - First Watch, Agpeya Veil Prayer, first_prayer plus 7 more |
| psalm-60-lxx-59-the-banner-given-to-those-who-fear-thee | extra_in_note; missing_from_note | 6 | 1 | extra 1: matins; missing 6: Commemoration Of the Appearance Of The Glorious Cross, Great Lent, The Commemoration of the Honorable Archangel Michael, The Feast of the Consecration of the Church of the Honorable Cross, The fourth Sunday of Paona plus 1 more |
| psalm-61-lxx-60-lead-me-to-the-rock-that-is-higher-than-i | missing_from_note | 20 | 2 | extra 0: none; missing 18: Agpeya Sixth Hour (Sext), Bashons 21, Bashons 29, Kiak 17, The Appearance of the Head of St. John the Baptist plus 13 more |
| psalm-62-lxx-61-my-soul-is-subject-to-god-alone | missing_from_note | 6 | 0 | extra 0: none; missing 6: Monday Eve, Pascha / Holy Week, Sunday, Tout 19 (Feast of the Cross), Thursday Eve, Tout 19 (Feast of the Cross) plus 1 more |
| psalm-63-lxx-62-thirsting-for-thee-in-a-dry-land | missing_from_note | 9 | 0 | extra 0: none; missing 9: Agpeya, Agpeya First Hour (Prime / Morning Prayer), Agpeya Sixth Hour (Sext), Great Lent, Holy Fifty Days plus 4 more |
| psalm-64-lxx-63-hidden-arrows-and-righteous-joy | missing_from_note | 8 | 0 | extra 0: none; missing 8: Barmuda 21, Great Lent, Palm Sunday, Pascha / Holy Week, The Commemoration of the Virgin St. Mary, the Theotokos plus 3 more |
| psalm-65-lxx-64-praise-in-zion-and-the-crown-of-the-year | missing_from_note | 42 | 0 | extra 0: none; missing 42: Barmuda 1, Barmuda 10, Bashons 20, Commemoration Of the Appearance Of The Glorious Cross, Fast of Nineveh plus 37 more |
| psalm-66-lxx-65-through-fire-and-water-into-refreshment | missing_from_note | 33 | 0 | extra 0: none; missing 33: Abib 8, Barmuda 13, Barmuda 4, Circumcision of our Lord, Entrance into the Temple plus 28 more |
| psalm-67-lxx-66-let-the-nations-give-thanks | missing_from_note | 11 | 0 | extra 0: none; missing 11: Agpeya, Agpeya First Hour (Prime / Morning Prayer), Agpeya Sixth Hour (Sext), Agpeya Veil Prayer, Holy Fifty Days plus 6 more |
| psalm-68-lxx-67-let-god-arise-and-scatter-his-enemies | missing_from_note | 129 | 0 | extra 0: none; missing 129: Abib 12, Abib 18, Abib 24, Abib 29, Abib 4 plus 124 more |
| psalm-69-lxx-68-zeal-for-thy-house-and-the-gall-of-reproach | missing_from_note | 12 | 0 | extra 0: none; missing 12: Fast of Nineveh, Good Friday, Good Friday Eve, Great Thursday Eve, Holy Fifty Days plus 7 more |
| psalm-7-lxx-7-the-righteous-judge-and-the-pit-of-the-wicked | missing_from_note | 6 | 0 | extra 0: none; missing 6: Holy Fifty Days, Pascha / Holy Week, The Martyrdom of St. John the Baptist, The second Sunday of Tout, Thursday Eve plus 1 more |
| psalm-70-lxx-69-o-god-make-haste-to-help-me | missing_from_note | 11 | 0 | extra 0: none; missing 11: Agpeya, Agpeya First Hour (Prime / Morning Prayer), Agpeya Midnight Prayer - First Watch, Agpeya Sixth Hour (Sext), Agpeya Veil Prayer plus 6 more |
| psalm-71-lxx-70-forsake-me-not-when-my-strength-fails | missing_from_note | 4 | 0 | extra 0: none; missing 4: Monday, Pascha / Holy Week, The Departure of St. Simon II, 51st Pope of the See of St. Mark, The third Sunday of Baba |
| psalm-72-lxx-71-the-king-of-peace-and-the-poor | missing_from_note | 17 | 0 | extra 0: none; missing 17: Annunciation, Christmas, Holy Fifty Days, Kiak 30, Monday plus 12 more |
| psalm-73-lxx-72-until-i-entered-the-sanctuary-of-god | missing_from_note | 54 | 0 | extra 0: none; missing 54: A Council held in the city of Alexandria, Abib 14, Amshir 18, Barmuda 12, Barmuda 3 plus 49 more |
| psalm-74-lxx-73-arise-o-god-plead-your-cause | missing_from_note | 3 | 0 | extra 0: none; missing 3: Holy Fifty Days, The Commemoration of St. Gregory, Patriarch of the Armenians, The Departure of St. Jason, one of the Seventy disciples |
| psalm-75-lxx-74-the-cup-in-the-hand-of-the-lord | agrees | 0 | 0 | extra 0: none; missing 0: none |
| psalm-76-lxx-75-god-is-known-in-judah | missing_from_note | 2 | 0 | extra 0: none; missing 2: Christmas Paramoune, The Martyrdom of 150 Men and 24 Women from Ansena |
| psalm-77-lxx-76-in-the-night-i-remembered-god | missing_from_note | 6 | 0 | extra 0: none; missing 6: Baba 6, Holy Fifty Days, The Commemoration of the Miracle at Cana of Galilee, The Commemoration of the Slain Children of Bethlehem by the Order of King Herod, The third Sunday of Toba plus 1 more |
| psalm-78-lxx-77-tell-the-coming-generation | missing_from_note | 17 | 0 | extra 0: none; missing 17: Hator 27, Hator 5, Holy Fifty Days, Kiak 16, part_3 plus 12 more |
| psalm-79-lxx-78-help-us-for-the-glory-of-your-name | missing_from_note | 3 | 0 | extra 0: none; missing 3: Great Lent, The Departure of St. Jason, one of the Seventy disciples, The Martyrdom of St. Bacchus, the Friend of St. Sergius |
| psalm-8-lxx-8-the-son-of-man-crowned-with-glory | missing_from_note | 38 | 0 | extra 0: none; missing 38: Agpeya, Agpeya First Hour (Prime / Morning Prayer), Barmuda 11, Barmuda 25, Barmuda 6 plus 33 more |
| psalm-80-lxx-79-shepherd-of-israel-turn-us | missing_from_note | 11 | 0 | extra 0: none; missing 11: fourth Sunday of Christmas Fast, Great Lent, Hator 8, Palm Sunday, Pascha / Holy Week plus 6 more |
| psalm-81-lxx-80-rejoice-in-god-our-helper | missing_from_note | 5 | 0 | extra 0: none; missing 5: Feast of El-Nayrouz (Beginning of the Blessed Coptic Year), Feast of Nayrouz - (Readings of the First of Tut), first_gospel, Holy Fifty Days, Special service |
| psalm-82-lxx-81-god-stands-in-the-assembly-of-gods | missing_from_note | 5 | 0 | extra 0: none; missing 5: Bright Saturday, Holy Fifty Days, On this day of the year 381 A.D., one hundred and fifty fathers assembled upon the order of Emperor Theodosius the Great, in the city of Constantinople, Pascha / Holy Week, The first Sunday of Amshir |
| psalm-83-lxx-82-o-god-who-shall-be-compared-to-thee | missing_from_note | 7 | 0 | extra 0: none; missing 7: Pascha / Holy Week, The Departure of St. Theonas, 16th Pope of Alexandria, The fourth Sunday of Paona, The Martyrdom of St. Shenousi (Sanusi), The second Sunday of Toba plus 2 more |
| psalm-84-lxx-83-how-amiable-are-thy-tabernacles | missing_from_note | 10 | 0 | extra 0: none; missing 10: Agpeya, Agpeya Sixth Hour (Sext), procession_station_09_northern_door, Special service, The Commemoration of the Consecration of the Sanctuaries of the church of Resurrection in Jerusalem plus 5 more |
| psalm-85-lxx-84-o-lord-thou-hast-taken-pleasure-in-thy-land | missing_from_note | 8 | 0 | extra 0: none; missing 8: Agpeya, Agpeya Sixth Hour (Sext), part_3, Special service, The Entrance of Saint Mary into the Temple at Jerusalem plus 3 more |
| psalm-86-lxx-85-incline-thine-ear-o-lord | missing_from_note | 12 | 0 | extra 0: none; missing 12: Agpeya, Agpeya Midnight Prayer - First Watch, Agpeya Sixth Hour (Sext), Agpeya Veil Prayer, Great Lent plus 7 more |
| psalm-87-lxx-86-glorious-things-are-spoken-of-thee | missing_from_note | 20 | 0 | extra 0: none; missing 20: 1.The Dormition of Our Lady, the Virgin Mary, the Theotokos, Agpeya, Agpeya Sixth Hour (Sext), Fast of Nineveh, fourth Sunday of Christmas Fast plus 15 more |
| psalm-88-lxx-87-free-among-the-dead | missing_from_note | 7 | 0 | extra 0: none; missing 7: Good Friday, Great Lent, MATINS / RAISING OF INCENSE, Pascha / Holy Week, The Departure of St. John the Evangelist and Theologian plus 2 more |
| psalm-89-lxx-88-i-will-sing-of-thy-mercies | missing_from_note | 85 | 0 | extra 0: none; missing 85: Barmuda 14, Barmuda 19, Barmuda 22, Bashons 21, Bashons 27 plus 80 more |
| psalm-9-lxx-9-1-21-thanksgiving-at-the-gates-of-death | missing_from_note | 59 | 0 | extra 0: none; missing 59: A Council held in the city of Alexandria, Abib 14, Amshir 16, Barmuda 12, Barmuda 3 plus 54 more |
| psalm-90-lxx-89-lord-thou-hast-been-our-refuge | missing_from_note | 3 | 0 | extra 0: none; missing 3: Holy Fifty Days, The Departure of Hezekiah the King, The first Sunday of Hator |
| psalm-91-lxx-90-he-that-dwelleth-in-the-secret-place | missing_from_note | 20 | 0 | extra 0: none; missing 20: Agpeya, Agpeya Midnight Prayer - First Watch, Agpeya Sixth Hour (Sext), Agpeya Veil Prayer, Barmuda 2 plus 15 more |
| psalm-92-lxx-91-it-is-a-good-thing-to-give-thanks | missing_from_note | 16 | 0 | extra 0: none; missing 16: Fast of Nineveh, Hator 16 of Christmas Fast, Holy Fifty Days, Kiak 11, Kiak 2 plus 11 more |
| psalm-93-lxx-92-the-lord-reigneth | missing_from_note | 12 | 0 | extra 0: none; missing 12: Agpeya, Agpeya Sixth Hour (Sext), part_3, Special service, The Departure of Anba Serapamon, Archpriest of Abba Yehnis (John) monastery plus 7 more |
| psalm-94-lxx-93-o-lord-god-to-whom-vengeance-belongeth | missing_from_note | 2 | 0 | extra 0: none; missing 2: Great Thursday, Pascha / Holy Week |
| psalm-95-lxx-94-o-come-let-us-sing-unto-the-lord | missing_from_note | 3 | 0 | extra 0: none; missing 3: fourth Sunday of Christmas Fast, Great Lent, The fourth Sunday of Kiak |
| psalm-96-lxx-95-o-sing-unto-the-lord-a-new-song | missing_from_note | 34 | 0 | extra 0: none; missing 34: Abib 2, Abib 9, Agpeya, Agpeya Ninth Hour (None), annual Sundays by Coptic month/week plus 29 more |
| psalm-97-lxx-96-the-lord-reigneth-let-the-earth-rejoice | missing_from_note | 62 | 0 | extra 0: none; missing 62: Abib 27, Agpeya, Agpeya Ninth Hour (None), Agpeya Veil Prayer, Barmuda 23 plus 57 more |
| psalm-98-lxx-97-o-sing-unto-the-lord-a-new-song | missing_from_note | 11 | 0 | extra 0: none; missing 11: Agpeya, Agpeya Ninth Hour (None), Feast of El-Nayrouz (Beginning of the Blessed Coptic Year), Feast of Nayrouz - (Readings of the First of Tut), Great Lent plus 6 more |
| psalm-99-lxx-98-the-lord-reigneth-let-the-people-tremble | missing_from_note | 68 | 0 | extra 0: none; missing 68: Abib 26, Agpeya, Agpeya Ninth Hour (None), Barmuda 19, Barmuda 5 plus 63 more |
| sirach-5-7-presumption-speech-and-repentance | extra_in_note; missing_from_note | 3 | 2 | extra 1: prophecy; missing 2: Pascha / Holy Week, Tuesday |
| sirach-8-11-discernment-under-power | extra_in_note | 1 | 2 | extra 1: prophecy; missing 0: none |
| susanna-innocence-vindicated | extra_in_note | 0 | 4 | extra 4: Bright Saturday, liturgy, PRAISES OF THE PROPHETS, Special service; missing 0: none |
| tobit-1-2-righteousness-in-exile-and-the-blindness-of-the-just | agrees | 1 | 1 | extra 0: none; missing 0: none |
| tobit-11-12-sight-restored-and-raphael-revealed | agrees | 1 | 1 | extra 0: none; missing 0: none |
| tobit-13-14-the-new-jerusalem-nineveh-s-fall-and-faithful-death | agrees | 1 | 1 | extra 0: none; missing 0: none |
| tobit-3-two-prayers-heard-before-god | agrees | 1 | 1 | extra 0: none; missing 0: none |
| tobit-4-a-father-s-testament | agrees | 1 | 1 | extra 0: none; missing 0: none |
| tobit-5-6-the-hidden-guide-and-the-fish-by-the-river | agrees | 1 | 1 | extra 0: none; missing 0: none |
| tobit-7-8-marriage-prayer-and-the-defeat-of-the-destroyer | agrees | 1 | 1 | extra 0: none; missing 0: none |
| tobit-9-10-waiting-anxiety-and-mercy-hidden-in-delay | agrees | 1 | 1 | extra 0: none; missing 0: none |
| wisdom-of-solomon-1-love-righteousness-and-seek-god-simply | missing_from_note | 3 | 2 | extra 0: none; missing 1: Wednesday |
| wisdom-of-solomon-10-1-11-14-wisdom-guiding-the-righteous-through-history | agrees | 0 | 0 | extra 0: none; missing 0: none |
| wisdom-of-solomon-11-15-12-27-mercy-measure-and-judgment | missing_from_note | 2 | 0 | extra 0: none; missing 2: Great Thursday, Pascha / Holy Week |
| wisdom-of-solomon-13-15-beauty-creation-and-the-madness-of-idolatry | missing_from_note | 2 | 0 | extra 0: none; missing 2: Great Thursday, Pascha / Holy Week |
| wisdom-of-solomon-16-17-signs-manna-and-darkness | agrees | 0 | 0 | extra 0: none; missing 0: none |
| wisdom-of-solomon-18-19-pascha-the-word-and-new-creation | agrees | 0 | 0 | extra 0: none; missing 0: none |
| wisdom-of-solomon-2-the-righteous-son-condemned | extra_in_note; missing_from_note | 5 | 3 | extra 1: Good Friday Eve; missing 3: Monday, Tuesday, Wednesday |
| wisdom-of-solomon-3-4-the-righteous-in-the-hand-of-god | missing_from_note | 2 | 0 | extra 0: none; missing 2: Pascha / Holy Week, Wednesday |
| wisdom-of-solomon-5-final-vindication-and-the-armor-of-creation | agrees | 0 | 0 | extra 0: none; missing 0: none |
| wisdom-of-solomon-6-1-21-rulers-under-judgment | agrees | 0 | 0 | extra 0: none; missing 0: none |
| wisdom-of-solomon-6-22-8-21-wisdom-brightness-and-friendship-with-god | extra_in_note; missing_from_note | 2 | 2 | extra 1: Wednesday; missing 1: Pascha / Holy Week |
| wisdom-of-solomon-9-solomon-s-prayer-for-wisdom | agrees | 0 | 0 | extra 0: none; missing 0: none |

## Studies with joined occasions and no lectionary note

| study_slug |
| --- |
| 1-chronicles-28-29-davids-final-charge-offering-prayer-and-solomons-accession |
| 1-kings-08-the-dedication-of-the-temple |
| 1-kings-17-elijah-in-hiddenness |
| 1-kings-19-elijah-in-despair-and-the-still-small-voice |
| 1-samuel-1-2-hannah-samuel-and-the-corruption-of-eli-s-house |
| 1-samuel-17-18-david-and-goliath-victory-and-jealousy |
| 1-samuel-23-24-wilderness-discernment-and-mercy-toward-saul |
| 1-samuel-3-speak-lord-your-servant-hears |
| 1-samuel-general-introduction |
| 2-kings-04-elisha-s-miracles-of-life-and-provision |
| 2-kings-05-naaman-the-syrian |
| 2-kings-06-07-spiritual-sight-siege-and-unexpected-deliverance |
| amos-3-4-covenant-accountability |
| amos-5-seek-me-and-live |
| amos-7-8-visions-and-famine-of-the-word |
| amos-9-sifted-people-and-restored-booth-of-david |
| daniel-1-holy-refusal-in-babylon |
| daniel-3-the-fiery-furnace-and-the-three-holy-youths |
| daniel-6-daniel-in-the-lions-den |
| daniel-7-ancient-of-days-and-the-son-of-man |
| daniel-9-confession-and-the-seventy-weeks |
| deuteronomy-11-love-obedience-blessing-and-curse |
| deuteronomy-12-the-place-where-the-lord-chooses-to-dwell |
| deuteronomy-32-the-song-of-moses |
| deuteronomy-5-the-covenant-at-horeb-and-the-ten-words |
| deuteronomy-6-the-shema-and-the-love-of-god |
| deuteronomy-7-a-holy-people-and-a-jealous-love |
| deuteronomy-8-remembering-the-lord-in-the-land-of-plenty |
| deuteronomy-9-10-stubbornness-intercession-and-the-circumcised-heart |
| exodus-11-the-final-plague-announced |
| exodus-12-passover-blood-and-the-exodus |
| exodus-13-consecration-unleavened-bread-and-the-cloud |
| exodus-13-consecration-unleavened-bread-and-the-pillar |
| exodus-14-15-the-red-sea-crossing-and-the-song-of-moses |
| exodus-14-the-red-sea-crossing |
| exodus-15-song-of-moses-and-bitter-waters |
| exodus-16-manna-bread-from-heaven |
| exodus-16-manna-bread-from-heaven-and-sabbath-training |
| exodus-17-18-water-from-the-rock-amalek-and-shared-leadership |
| exodus-17-water-from-the-rock-and-amalek |
| exodus-19-sinai-and-the-priestly-people |
| exodus-2-moses-hidden-drawn-out-and-exiled |
| exodus-3-research-notes |
| exodus-3-the-burning-bush-and-the-name-of-god |
| exodus-32-the-golden-calf |
| exodus-33-presence-glory-and-the-friend-of-god |
| exodus-4-signs-resistance-zipporah-and-return |
| exodus-5-6-pharaoh-resists-and-god-reaffirms-covenant |
| exodus-7-8-the-plagues-begin-and-egypts-gods-are-judged |
| exodus-9-10-plagues-intensify-and-pharaohs-heart-hardens |
| ezekiel-18-the-soul-that-sins-shall-die |
| ezekiel-19-20-lament-and-rebellious-history |
| ezekiel-21-22-sword-and-bloodguilt |
| ezekiel-35-36-edom-judged-and-israel-renewed |
| ezekiel-35-36-edom-judged-and-the-new-heart-promised |
| ezekiel-37-dry-bones-and-one-stick |
| ezekiel-43-44-glory-returns-and-priestly-holiness |
| ezekiel-47-48-river-of-life-and-restored-inheritance |
| ezekiel-47-48-river-of-life-and-the-lord-is-there |
| genesis-19-sodom-judgment-rescue-and-tragic-aftermath |
| genesis-27-jacob-esau-and-the-stolen-blessing |
| genesis-28-jacob-s-ladder-and-bethel |
| genesis-32-jacob-wrestles-and-becomes-israel |
| genesis-49-jacob-blesses-the-twelve-tribes |
| genesis-50-joseph-forgives-and-genesis-ends-in-hope |
| habakkuk-3-prayer-theophany-and-rejoicing-without-visible-deliverance |
| hosea-1-3-covenant-love-and-wounded-marriage |
| hosea-11-out-of-egypt-i-called-my-son |
| hosea-4-5-no-knowledge-of-god |
| hosea-6-on-the-third-day-he-will-raise-us-up |
| hosea-9-10-fruit-for-the-self |
| isaiah-1-vision-of-sinful-judah |
| isaiah-13-14-babylon-and-the-fallen-tyrant |
| isaiah-19-20-egypt-humbled-and-healed |
| isaiah-2-4-zion-judgment-and-the-branch |
| isaiah-24-27-apocalypse-feast-and-resurrection-hope |
| isaiah-28-29-woe-to-pride-and-blind-worship |
| isaiah-30-31-woe-to-egypt-trust |
| isaiah-36-39-hezekiah-assyria-and-babylon |
| isaiah-40-comfort-my-people |
| isaiah-41-42-servant-and-deliverance |
| isaiah-43-44-new-exodus-and-true-god |
| isaiah-45-46-cyrus-and-the-lord-alone |
| isaiah-47-48-babylon-falls-and-israel-called |
| isaiah-49-50-servant-mission-and-obedience |
| isaiah-49-servant-light-to-the-nations-and-zion-remembered |
| isaiah-5-the-vineyard-song |
| isaiah-50-the-obedient-suffering-servant |
| isaiah-51-52-zion-awake-and-good-news |
| isaiah-53-the-suffering-servant |
| isaiah-54-55-covenant-mercy-and-invitation |
| isaiah-55-come-to-the-waters-and-the-everlasting-covenant |
| isaiah-56-57-inclusion-and-false-worship |
| isaiah-58-59-true-fasting-and-intercession |
| isaiah-6-isaiah-call |
| isaiah-60-62-zion-glory-and-anointed-good-news |
| isaiah-63-64-divine-warrior-and-communal-lament |
| isaiah-65-66-new-heavens-new-earth-and-final-worship |
| isaiah-7-8-immanuel-and-assyrian-threat |
| isaiah-9-12-messianic-light-and-thanksgiving |
| jeremiah-16-17-life-as-sign-and-the-heart-examined |
| jeremiah-21-23-kings-shepherds-and-righteous-branch |
| jeremiah-30-31-book-of-consolation-and-new-covenant |
| jeremiah-42-44-flight-to-egypt |
| job-1-2-the-righteous-sufferer-tested |
| job-11-14-zophar-and-job-hope-beyond-death |
| job-15-17-second-cycle-begins |
| job-18-21-wickedness-debate |
| job-22-24-eliphaz-accuses-and-job-seeks-god |
| job-25-28-wisdom-hidden-with-god |
| job-29-31-job-final-defense |
| job-32-34-elihu-begins |
| job-35-37-elihu-on-god-majesty |
| job-38-39-the-lord-answers-from-the-whirlwind |
| job-40-41-behemoth-and-leviathan |
| job-42-repentance-intercession-and-restoration |
| joel-1-locusts-and-lament |
| joel-2-trumpet-fasting-and-the-poured-out-spirit |
| joel-3-spirit-and-judgment |
| jonah-1-flight-storm-and-descent |
| jonah-2-prayer-from-the-belly-of-the-fish |
| joshua-1-2-courage-rahab-and-the-scarlet-cord |
| joshua-6-jericho-and-the-collapse-of-pride |
| judges-10-12-restless-repentance-jephthah-and-tribal-strife |
| leviticus-23-the-feasts-of-the-lord |
| malachi-3-the-messenger-the-lord-in-his-temple-and-refining-fire |
| mark-10-1-16-marriage-hardness-of-heart-and-children |
| mark-10-17-31-the-rich-man-treasure-in-heaven-and-the-impossible-made-possible |
| mark-10-32-45-the-cup-the-ransom-and-servant-greatness |
| mark-10-46-52-blind-bartimaeus-and-the-way-to-jerusalem |
| mark-11-1-11-the-king-enters-jerusalem |
| mark-11-12-26-the-fig-tree-the-temple-prayer-and-forgiveness |
| mark-11-27-12-12-authority-the-vineyard-and-the-rejected-son |
| mark-12-13-34-caesar-resurrection-and-the-great-commandment |
| mark-12-35-44-david-s-lord-the-scribes-and-the-widow-s-offering |
| mark-13-1-23-the-temple-s-fall-deception-and-endurance |
| mark-13-24-37-the-son-of-man-and-the-watchful-servant |
| mark-14-1-11-fragrance-waste-and-betrayal |
| mark-14-12-25-the-mystical-supper-and-the-blood-of-the-covenant |
| mark-14-26-52-gethsemane-watchfulness-betrayal-and-arrest |
| mark-14-53-72-christ-before-the-council-and-peter-s-denial |
| mark-15-1-20-pilate-barabbas-and-the-mocked-king |
| mark-15-21-41-the-cross-the-cry-and-the-centurion-s-confession |
| mark-15-42-47-joseph-of-arimathea-and-the-burial-of-christ |
| mark-16-1-8-the-empty-tomb-and-fearful-joy |
| mark-16-9-20-the-risen-lord-mission-and-signs |
| mark-3-20-35-a-house-divided-and-the-true-family-of-christ |
| mark-4-1-20-the-parable-of-the-sower |
| mark-4-21-34-lamp-measure-hidden-growth-and-mustard-seed |
| mark-4-35-41-lord-of-the-storm |
| mark-5-21-43-jairus-the-woman-with-the-flow-of-blood-and-the-touch-of-faith |
| mark-6-1-13-rejection-at-nazareth-and-the-mission-of-the-twelve |
| mark-6-14-29-herod-herodias-and-the-martyrdom-of-the-forerunner |
| mark-6-30-44-bread-in-the-desert-for-the-shepherdless-sheep |
| mark-6-45-56-walking-on-the-sea-and-healing-at-gennesaret |
| mark-7-1-23-tradition-defilement-and-the-heart |
| mark-8-1-21-the-second-feeding-the-sign-and-the-leaven-of-blindness |
| mark-8-22-30-eyes-opened-and-peter-s-confession |
| mark-8-31-9-1-the-cross-revealed-and-the-disciple-s-cross |
| mark-9-14-29-i-believe-help-my-unbelief |
| mark-9-2-13-the-transfiguration-and-the-glory-before-the-cross |
| mark-9-30-37-the-last-servant-and-the-child-in-the-midst |
| mark-9-38-50-scandal-fire-salt-and-peace |
| micah-1-the-lord-comes-in-judgment |
| micah-2-woe-to-oppressors-and-the-gathered-remnant |
| micah-3-corrupt-rulers-priests-and-prophets |
| micah-7-lament-hope-and-the-god-who-pardons |
| numbers-10-silver-trumpets-and-departure-from-sinai |
| numbers-11-complaining-and-the-seventy-elders |
| numbers-20-meribah-aaron-dies-and-edom-refuses |
| numbers-21-bronze-serpent-and-wilderness-victories |
| proverbs-1-1-7-the-fear-of-the-lord-and-the-beginning-of-wisdom |
| proverbs-1-8-33-the-two-voices-calling-the-soul |
| proverbs-10-the-righteous-tongue-and-the-wise-life |
| proverbs-11-integrity-mercy-and-the-city-that-stands |
| proverbs-12-correction-truth-and-the-way-of-life |
| proverbs-2-wisdom-as-hidden-treasure |
| proverbs-3-trust-in-the-lord-with-all-your-heart |
| proverbs-30-agur-humility-before-mystery |
| proverbs-4-guard-your-heart |
| proverbs-5-the-bitter-end-of-secret-desire |
| proverbs-6-fire-in-the-bosom-and-the-discipline-of-diligence |
| proverbs-7-the-way-to-the-chambers-of-death |
| proverbs-8-wisdom-speaks-and-christ-the-eternal-word |
| proverbs-9-two-banquets-wisdom-and-folly |
| psalm-126-lxx-125-when-the-lord-turned-the-captivity-of-sion |
| psalm-127-lxx-126-except-the-lord-build-the-house |
| psalm-128-lxx-127-blessed-are-all-they-that-fear-the-lord |
| psalm-129-lxx-128-many-a-time-have-they-warred-against-me |
| psalm-130-lxx-129-out-of-the-depths-i-have-cried |
| psalm-131-lxx-130-my-heart-is-not-exalted |
| sirach-1-2-wisdom-fear-and-the-furnace |
| sirach-19-23-the-mouth-and-the-passions |
| sirach-24-wisdom-in-the-congregation |
| sirach-3-4-honor-humility-and-the-poor |
| zechariah-1-return-to-me-and-the-horsemen-among-the-myrtle-trees |
| zechariah-10-11-shepherds-flock-and-thirty-pieces-of-silver |
| zechariah-12-they-shall-look-on-me-whom-they-pierced |
| zechariah-13-the-fountain-opened-and-the-shepherd-struck |
| zechariah-14-the-lord-shall-be-king-over-all-the-earth |
| zechariah-7-8-fasting-truth-mercy-and-the-nations-seeking-god |
| zechariah-9-your-king-comes-humble-and-riding-on-a-donkey |
| zephaniah-1-the-day-of-the-lord-against-false-security |
| zephaniah-2-seek-the-lord-and-the-nations-judged |
| zephaniah-3-the-lord-in-your-midst-and-the-rejoicing-daughter-of-zion |
