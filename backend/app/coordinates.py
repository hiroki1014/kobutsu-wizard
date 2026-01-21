"""PDF座標定義"""

from reportlab.lib.pagesizes import A4

WIDTH, HEIGHT = A4  # 595.27 x 841.89


def convert_y(pdfplumber_y: float) -> float:
    """pdfplumberのy座標をreportlabに変換（上から→下から）"""
    return HEIGHT - pdfplumber_y


# ============================================
# ページ1: その１（基本情報）
# ============================================

# 許可の種類（真円で番号だけ）
PERMIT_TYPE_CIRCLE = (172, convert_y(297) - 6, 190, convert_y(297) + 12)  # 古物商の「1」を囲む

# タイトル部の「古物市場主」に二重線（申請書タイトル）
# 実際の位置: x=170.7-282.3, y=163.2-176.6
TITLE_KOBUTSU_ICHIBONUSHI_DOUBLE_LINE = (170, 283, convert_y(170))  # タイトル部の古物市場主

# 公安委員会（「○○公安委員会 殿」の○○部分）
# 実際の位置: "公安委員会 殿" x=42.5-227.9, y=224.8-234.3
# 都道府県名を公安委員会の前に配置（行の左端から）
PUBLIC_SAFETY_COMMISSION_X = 72
PUBLIC_SAFETY_COMMISSION_Y = convert_y(232)

# 申請者の氏名又は名称及び住所（セクション見出し直下）
# 「住所 氏名」形式で表示（右端揃え）
APPLICANT_INFO_X = 560  # 右端基準
APPLICANT_INFO_Y = convert_y(265)  # 30上

# 氏名
NAME_KANA_X = 202
NAME_KANA_Y = convert_y(315)
NAME_KANJI_X = 195
NAME_KANJI_Y = convert_y(343)  # 1上

# 法人等の種別（真円で番号だけ）
# 実際の位置: 行全体 x=71.6-559.7, y=364.0-373.4、「6.個人」は右端
INDIVIDUAL_CIRCLE = (533, convert_y(375), 548, convert_y(360))  # 個人の「6」を囲む

# 元号の位置（生年月日欄の元号を丸で囲む）
# 実際の位置: 昭和 x=199.6-210.1, 平成 x=217.0-227.6, 令和 x=234.7-245.2, y=380.3-387.0
# 西暦・明治・大正はその左にあると推測
ERA_POSITIONS = {
    'seireki': (143, 161),   # 西暦 (0) - 5左
    'meiji': (166, 182),     # 明治 (1)
    'taisho': (182, 198),    # 大正 (2)
    'showa': (198, 212),     # 昭和 (3)
    'heisei': (215, 229),    # 平成 (4)
    'reiwa': (233, 247),     # 令和 (5)
}
ERA_CIRCLE_Y = (convert_y(387), convert_y(378))  # 1上

# 生年月日
BIRTH_YEAR_X = 253
BIRTH_MONTH_X = 300
BIRTH_DAY_X = 323
BIRTH_Y = convert_y(401)
BIRTH_CHAR_WIDTH = 11  # 文字間隔

# 住所
ADDRESS_PREF_X = 178
ADDRESS_PREF_Y = convert_y(425)
ADDRESS_CITY_X = 263
ADDRESS_CITY_Y = convert_y(425)
ADDRESS_STREET_X = 428
ADDRESS_STREET_Y = convert_y(425)

# 電話番号
PHONE_AREA_X = 202
PHONE_LOCAL_X = 252
PHONE_NUMBER_X = 308
PHONE_Y = convert_y(474)

# 行商（真円で番号だけ）
# 実際の位置: 行全体 x=74.6-414.0, y=485.6-495.1、「2.しない」は「1.する」の後
GYOSHO_SHINAI_CIRCLE = (385, convert_y(496), 400, convert_y(481))  # 「2」を囲む

# 主として取り扱おうとする古物の区分（1ページ目、真円で番号だけ）
MAIN_ITEM_11_CIRCLE = (157, convert_y(541), 172, convert_y(526))  # 「11」を囲む

# 代表者等（法人の場合、真円で番号だけ）
REP_TYPE_POSITIONS = {
    '1': (152, convert_y(557), 167, convert_y(542)),   # 「1」を囲む
    '2': (217, convert_y(557), 232, convert_y(542)),   # 「2」を囲む
    '3': (267, convert_y(557), 282, convert_y(542)),   # 「3」を囲む
}
REP_NAME_KANA_X = 201  # 1右
REP_NAME_KANA_Y = convert_y(569)  # 1下
REP_NAME_KANJI_X = 195  # 上の氏名漢字と同じ
REP_NAME_KANJI_Y = convert_y(593)  # 1下

# 代表者生年月日の元号
REP_ERA_POSITIONS = {
    'seireki': (144, 162),  # 2左
    'meiji': (166, 182),
    'taisho': (182, 198),
    'showa': (198, 212),
    'heisei': (215, 229),
    'reiwa': (233, 247),
}
REP_ERA_CIRCLE_Y = (convert_y(621), convert_y(612))
REP_BIRTH_YEAR_X = 253
REP_BIRTH_MONTH_X = 300
REP_BIRTH_DAY_X = 323
REP_BIRTH_Y = convert_y(637)  # 1下
REP_BIRTH_CHAR_WIDTH = 11

# 代表者住所（1下）
REP_PREF_X = 178
REP_PREF_Y = convert_y(662)
REP_CITY_X = 263
REP_CITY_Y = convert_y(662)
REP_STREET_X = 428
REP_STREET_Y = convert_y(662)

# 代表者電話番号（3下）
REP_PHONE_AREA_X = 202
REP_PHONE_LOCAL_X = 252
REP_PHONE_NUMBER_X = 308
REP_PHONE_Y = convert_y(711)  # 1下

# ============================================
# ページ2: その２（主たる営業所）
# ============================================

# 営業所形態（42右1下、真円で番号だけ）
OFFICE_ARI_CIRCLE = (154, convert_y(199), 169, convert_y(186))  # 1.営業所あり

# 営業所名称（1上）
OFFICE_NAME_KANA_X = 202
OFFICE_NAME_KANA_Y = convert_y(212)  # 1上
OFFICE_NAME_KANJI_X = 195
OFFICE_NAME_KANJI_Y = convert_y(236)  # 1上

# 営業所所在地（1上、番地10右）
OFFICE_PREF_X = 178
OFFICE_PREF_Y = convert_y(281)  # 1上
OFFICE_CITY_X = 278
OFFICE_CITY_Y = convert_y(281)  # 1上
OFFICE_STREET_X = 438  # 10右
OFFICE_STREET_Y = convert_y(281)  # 市区町村と同じY

# 営業所電話番号（2下）
OFFICE_PHONE_AREA_X = 202
OFFICE_PHONE_LOCAL_X = 252
OFFICE_PHONE_NUMBER_X = 308
OFFICE_PHONE_Y = convert_y(335)  # 2下

# 取扱品目（真円で番号だけ、2下、1個目62右、2個目10右）
ITEM_02_CIRCLE = (238, convert_y(353), 253, convert_y(340))  # 02のみ
ITEM_11_CIRCLE = (157, convert_y(384), 172, convert_y(371))  # 11のみ

# 管理者情報
# 管理者氏名欄（2上）
MANAGER_NAME_KANA_X = 202
MANAGER_NAME_KANA_Y = convert_y(397)  # 2上
MANAGER_NAME_KANJI_X = 195
MANAGER_NAME_KANJI_Y = convert_y(417)  # 2上

# 管理者生年月日の元号（1上）
MANAGER_ERA_POSITIONS = {
    'seireki': (144, 162),
    'showa': (198, 212),
    'heisei': (215, 229),
    'reiwa': (233, 247),
}
MANAGER_ERA_CIRCLE_Y = (convert_y(439), convert_y(429))  # 1上

MANAGER_BIRTH_YEAR_X = 253
MANAGER_BIRTH_MONTH_X = 300
MANAGER_BIRTH_DAY_X = 323
MANAGER_BIRTH_Y = convert_y(454)  # 2下
MANAGER_BIRTH_CHAR_WIDTH = 11

# 管理者住所（2上、番地同じY）
MANAGER_PREF_X = 178
MANAGER_PREF_Y = convert_y(480)  # 2上
MANAGER_CITY_X = 263
MANAGER_CITY_Y = convert_y(480)  # 2上
MANAGER_STREET_X = 428
MANAGER_STREET_Y = convert_y(480)  # 同じY

# 管理者電話番号（1下）
MANAGER_PHONE_AREA_X = 202
MANAGER_PHONE_LOCAL_X = 252
MANAGER_PHONE_NUMBER_X = 308
MANAGER_PHONE_Y = convert_y(531)  # 1下

# ============================================
# ページ4: その４（ホームページ）
# ============================================

# ホームページ利用（真円で番号だけ）
# 実際の位置: "1.用いる 2.用いない" x=275.3-419.8, y=121.0-130.4
WEBSITE_USE_CIRCLE = (273, convert_y(131), 288, convert_y(118))   # 1のみ
WEBSITE_NOT_USE_CIRCLE = (340, convert_y(132), 355, convert_y(119))  # 2のみ

# URL（送信元識別符号の入力欄）
WEBSITE_URL_X = 72
WEBSITE_URL_Y = convert_y(175)
