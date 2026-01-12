"""
Score Utils Module

This module provides utility functions for working with dart scores.
"""

checkouts = {
    2: ["2x1 The Madhouse"],
    3: ["1x1 2x1"],
    4: ["2x2"],
    5: ["1x1 2x2"],
    6: ["2x3", "1x2 2x2"],
    7: ["1x3 2x2", "1x1 2x3"],
    8: ["2x4"],
    9: ["1x5 2x2", "1x1 2x4"],
    10: ["2x5"],
    11: ["1x3 2x4", "1x7 2x2"],
    12: ["2x6"],
    # 13:

# 41	S1	D20
# 41 (Alternate)	S9	D16
# 42	S2	D20
# 42 (Alternate)	S10	D16
# 43	S3	D20
# 43 (Alternate)	S11	D16
# 44	S4	D20
# 44 (Alternate)	S12	D16
# 45	S5	D20
# 45 (Alternate)	S13	D16
# 46	S6	D20
# 46 (Alternate)	S14	D16
# 47	S7	D20
# 47 (Alternate)	S15	D16
# 48	S8	D20
# 48 (Alternate)	S16	D16
# 49	S9	D20
# 49 (Alternate)	S17	D16
# 50	S10	D20
# 50 (Alternate)	S18	D16
# 51	S11	D20
# 51 (Alternate)	S19	D16
# 52	S12	D20
# 52 (Alternate)	S20	D16
# 53	S13	D20
# 54	S14	D20
# 55	S15	D20
# 56	S16	D20
# 57	S17	D20
# 58	S18	D20
# 59	S19	D20
# 60	S20	D20
# 61	OUTER BULL	D18
# 61 (Alternate)	T7	D20
# 62	T10	D16
# 62 (Backup)	S10	S12	D20
# 63	T9	D18
# 63 (Alternate)	T13	D12
# 64	T16	D8
# 64 (Alternate)	T8	D20
# 64 (Backup)	S16	S16	D16
# 65	OUTER BULL	D20
# 66	T10	D18
# 66 (Backup)	S10	S16	D20
# 67	T17	D8
# 67 (Backup)	S17	S10	D20
# 68	T20	D4
# 68 (Backup)	S20	S16	D16
# 69	T19	D6
# 69 (Alternate)	T15	D12
# 69 (Backup)	S19	S10	D20
# 70	T10	D20
# 70 (Alternate)	T18	D8
# 70 (Backup)	S10	S20	D20
# 71	T13	D16
# 71 (Alternate)	T17	D10
# 71 (Backup)	S13	S18	D20
# 72	T16	D12
# 72 (Alternate)	T12	D18
# 72 (Backup)	S16	S16	D20
# 73	T19	D8
# 73 (Alternate)	T11	D20
# 73 (Backup)	S19	S14	D20
# 74	T14	D16
# 74 (Alternate)	T18	D10
# 74 (Backup)	S15	S20	D20
# 75	T17	D12
# 75 (Alternate)	OUTER BULL	BULL
# 75 (Backup)	S17	S18	D20
# 76	T20	D8
# 76 (Backup)	S20	S16	D20
# 77	T19	D10
# 77 (Backup)	S19	S18	D20
# 78	T18	D12
# 78 (Backup)	S18	S20	D20
# 79	T19	D11
# 79 (Alternate)	T13	D20
# 79 (Backup)	S19	S20	D20
# 80	T20	D10
# 80 (Alternate)	T16	D16
# 80 (Backup)	S20	S20	D20
# 81	T19	D12
# 81 (Alternate)	T15	D18
# 81 (Backup)	S19	T12	D13
# 82	BULL	D16
# 82 (Alternate)	T14	D20
# 82 (Backup)	OUTER BULL	S17	D20
# 83	T17	D16
# 83 (Backup)	S17	T16	D9
# 84	T20	D12
# 84 (Alternate)	T16	D18
# 84 (Backup)	S20	T14	D11
# 85	T15	D20
# 85 (Alternate)	T19	D14
# 85 (Backup)	S15	T20	D5
# 86	T18	D16
# 86 (Backup)	S18	T18	D7
# 87	T17	D18
# 87 (Backup)	S17	T20	D5
# 88	T20	D14
# 88 (Alternate)	T16	D20
# 88 (Backup)	S20	T18	D7
# 89	T19	D16
# 89 (Backup)	S19	T20	D5
# 90	T20	D15
# 90 (Alternate)	T18	D18
# 90 (Backup)	S20	S20	BULL
# 91	T17	D20
# 91 (Backup)	S17	T14	D16
# 92	T20	D16
# 92 (Backup)	S20	D18	D18
# 93	T19	D18
# 93 (Backup)	S19	T14	D16
# 94	T18	D20
# 94 (Backup)	S18	D18	D20
# 95	T19	D19
# 95 (Alternate)	BULL	S5	D20
# 95 (Backup)	OUTER BULL	S20	BULL
# 96	T20	D18
# 96 (Backup)	S20	T20	D8
# 97	T19	D20
# 97 (Backup)	S19	T18	D12
# 98	T20	D19
# 98 (Backup)	S20	T18	D12
# 99	X	X	X
# 100	T20	D20
# 100 (Backup)	S20	T20	D10
#
# 99	T19	S10	D16
# 99 (Backup)	S19	T20	D10
# 101	T20	S9	D16
# 101 (Backup)	S20	T19	D12
# 102	T20	S10	D16
# 103	T20	S11	D16
# 103 (Backup)	S20	T17	D16
# 104	T18	10	D20
# 104 (Backup)	S18	T18	D16
# 105	T20	S5	D20
# 105 (Backup)	S20	T15	D20
# 106	T20	S6	D20
# 106 (Backup)	S20	T18	D16
# 107	T20	S15	D16
# 107 (Backup)	S20	T17	D18
# 108	T19	S19	D16
# 108 (Backup)	S19	T19	D16
# 109	T19	S12	D20
# 109 (Backup)	S19	T19	D18
# 110	T20	S10	D20
# 110 (Backup)	S20	T18	D18
# 111	T20	S11	D20
# 111 (Backup)	S20	T17	D20
# 112	T20	S12	D20
# 112 (Backup)	S20	T20	D16
# 113	T19	S16	D20
# 113 (Backup)	S19	T18	D20
# 114	T20	S14	D20
# 114 (Backup)	S20	T18	D20
# 115	T19	S18	D20
# 115 (Backup)	S19	T20	D18
# 116	T19	S19	D20
# 116 (Backup)	S19	T19	D20
# 117	T20	S17	D20
# 117 (Backup)	S20	T19	D20
# 118	T20	S18	D20
# 118 (Backup)	S20	T20	D19
# 119	T19	12	BULL
# 119 (Backup)	S19	T20	D20
# 120	T20	S20	D20
# 120 (Backup)	S20	T20	D20
# 121	T20	S11	BULL
# 121 (Backup)	S20	T17	BULL
# 122	T18	T18	D7
# 122 (Backup)	S18	T18	BULL
# 123	T19	S16	BULL
# 123 (Backup)	S19	T18	BULL
# 124	T20	S14	BULL
# 124 (Backup)	S20	T18	BULL
# 125	BULL	T17	D12
# 125 (Backup)	OUTER BULL	T20	D20
# 126	T19	T19	D6
# 126 (Backup)	S19	T19	BULL
# 127	T20	T17	D8
# 127 (Backup)	S20	T19	BULL
# 128	T18	T14	D16
# 128 (Backup)	S18	T20	BULL
# 129	T19	T16	D12
# 129 (Backup)	S19	T20	BULL
# 130	T20	T20	D5
# 130 (Backup)	S20	T20	BULL
# 131	T20	T13	D16
# 131 (Alternate)	T17	D20	D20
# 132	BULL	BULL	D16
# 132 (Backup)	OUTER BULL	T19	BULL
# 133	T20	T19	D8
# 133 (Alternate)	T19	D18	D20
# 134	T20	T14	D16
# 134 (Alternate)	T18	D20	D20
# 135	BULL	T15	D20
# 135 (Backup)	OUTER BULL	T20	BULL
# 136	T20	T20	D8
# 137	T20	T19	D10
# 137 (Alternate)	T19	D20	D20
# 138	T20	T18	D12
# 139	T19	T14	D20
# 139 (Alternate)	T20	T19	D11
# 140	T20	T20	D10
# 140 (Alternate)	T20	D20	D20
# 141	T20	T19	D12
# 142	T20	T14	D20
# 143	T20	T17	D16
# 144	T20	T20	D12
# 145	T20	T15	D20
# 146	T20	T18	D16
# 146 (Alternate)	T19	T19	D16
# 147	T20	T17	D18
# 147 (Alternate)	T19	T18	D18
# 148	T20	T20	D14
# 148 (Alternate)	T20	T16	D20
# 149	T20	T19	D16
# 150	T20	T18	D18
# 150 (Alternate)	T19	T19	D18
# 151	T20	T17	D20
# 151 (Alternate)	T19	T18	D20
# 152	T20	T20	D16
# 153	T20	T19	D18
# 154	T20	T18	D20
# 155	T20	T19	D19
# 156	T20	T20	D18
# 157	T20	T19	D20
# 158	T20	T20	D19
# 159	X	X	X
# 160	T20	T20	D20
# 161	T20	T17	BULL
# 162	X	X	X
# 163	X	X	X
# 164	T20	T18	BULL
# 165	X	X	X
# 166	X	X	X
# 167	T20	T19	BULL
# 168	X	X	X
# 169	X	X	X
# 170	T20	T20	BULL
}

def is_valid_score(score: int) -> bool:
    match score:
        case _ if score < 0: return False
        case _ if score > 180: return False
        case 163 | 166 | 169 | 172 | 173 | 175 | 176 | 178 | 179: return False
    return True

def suggested_checkouts(score: int) -> list[str]:
    if score in checkouts:
        return checkouts[score]
    else:
        return []
