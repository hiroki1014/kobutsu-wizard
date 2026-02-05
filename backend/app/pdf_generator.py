"""古物商許可申請書 PDF生成モジュール"""

import io
import unicodedata
from datetime import date
from pathlib import Path

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter

from . import coordinates as coord
from .schemas import FormData


# ============================================
# フォント設定
# ============================================

FONT_PATHS = [
    str(Path(__file__).parent.parent / 'fonts' / 'ipag.ttf'),  # リポジトリ内のフォント
    '/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf',
    '/usr/share/fonts/truetype/ipafont-gothic/ipag.ttf',
    '/usr/share/fonts/ipafont-gothic/ipag.ttf',
    '/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc',
    'C:/Windows/Fonts/msgothic.ttc',
]

FONT_REGISTERED = False


def register_font():
    """日本語フォントを登録"""
    global FONT_REGISTERED
    if FONT_REGISTERED:
        return

    for font_path in FONT_PATHS:
        if Path(font_path).exists():
            try:
                pdfmetrics.registerFont(TTFont('IPAGothic', font_path))
                FONT_REGISTERED = True
                return
            except Exception:
                continue

    raise RuntimeError("日本語フォントが見つかりません。IPAゴシックをインストールしてください。")


# ============================================
# ユーティリティ関数
# ============================================

def separate_dakuten(text: str) -> list[str]:
    """濁点・半濁点を分離して1マスずつにする"""
    result = []
    for char in text:
        decomposed = unicodedata.normalize('NFD', char)
        for c in decomposed:
            result.append(c)
    return result


def katakana_to_hiragana(text: str) -> str:
    """カタカナをひらがなに変換"""
    return ''.join(
        chr(ord(c) - 0x60) if 'ァ' <= c <= 'ン' else c
        for c in text
    )


def to_halfwidth_kana(char: str) -> str:
    """全角カナ・濁点を半角に変換"""
    trans_table = str.maketrans(
        'アイウエオカキクケコサシスセソタチツテトナニヌネノ'
        'ハヒフヘホマミムメモヤユヨラリルレロワヲン'
        'ァィゥェォッャュョー・゛゜\u3099\u309A',
        'ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉ'
        'ﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜｦﾝ'
        'ｧｨｩｪｫｯｬｭｮｰ･ﾞﾟﾞﾟ'
    )
    return char.translate(trans_table)


def draw_kana_in_grid(c: canvas.Canvas, text: str, start_x: float, y: float,
                      char_width: float = 13.5, font_size: float = 9):
    """フリガナをマス目に1文字ずつ配置"""
    c.setFont('IPAGothic', font_size)
    separated = separate_dakuten(text)
    col = 0
    for char in separated:
        if char in (' ', '　'):
            col += 1
            continue
        hw = to_halfwidth_kana(char)
        x = start_x + (col * char_width)
        c.drawString(x, y, hw)
        col += 1


def draw_text_spaced(c: canvas.Canvas, text: str, start_x: float, y: float,
                     char_width: float = 10):
    """文字間隔を指定してテキストを描画"""
    for i, char in enumerate(text):
        x = start_x + (i * char_width)
        c.drawString(x, y, char)


def draw_circle(c: canvas.Canvas, x1: float, y1: float, x2: float, y2: float,
                line_width: float = 1):
    """○で囲む（楕円）"""
    c.setLineWidth(line_width)
    c.ellipse(x1, y1, x2, y2, stroke=1, fill=0)


def draw_double_line(c: canvas.Canvas, x_start: float, x_end: float, y: float,
                     gap: float = 3, line_width: float = 0.8):
    """二重線を引く"""
    c.setLineWidth(line_width)
    c.line(x_start, y, x_end, y)
    c.line(x_start, y - gap, x_end, y - gap)


# ============================================
# URL描画用定数・関数
# ============================================

# フリガナマッピングテーブル
URL_FURIGANA_MAP = {
    # 英小文字
    'a': 'ｴｰ', 'b': 'ﾋﾞｰ', 'c': 'ｼｰ', 'd': 'ﾃﾞｨｰ', 'e': 'ｲｰ',
    'f': 'ｴﾌ', 'g': 'ｼﾞｰ', 'h': 'ｴｲﾁ', 'i': 'ｱｲ', 'j': 'ｼﾞｪｲ',
    'k': 'ｹｲ', 'l': 'ｴﾙ', 'm': 'ｴﾑ', 'n': 'ｴﾇ', 'o': 'ｵｰ',
    'p': 'ﾋﾟｰ', 'q': 'ｷｭｰ', 'r': 'ｱｰﾙ', 's': 'ｴｽ', 't': 'ﾃｨｰ',
    'u': 'ﾕｰ', 'v': 'ﾌﾞｲ', 'w': 'ﾀﾞﾌﾞﾘｭｰ', 'x': 'ｴｯｸｽ', 'y': 'ﾜｲ', 'z': 'ｾﾞｯﾄ',
    # 記号
    ':': 'ｺﾛﾝ', '/': 'ｽﾗｯｼｭ', '.': 'ﾄﾞｯﾄ', '-': 'ﾊｲﾌﾝ',
    '_': 'ｱﾝﾀﾞｰﾊﾞｰ', '~': 'ﾁﾙﾀﾞ', '@': 'ｱｯﾄ', '#': 'ｼｬｰﾌﾟ',
    '?': 'ﾊﾃﾅ', '=': 'ｲｺｰﾙ', '&': 'ｱﾝﾄﾞ', '%': 'ﾊﾟｰｾﾝﾄ',
    # 数字
    '0': 'ｾﾞﾛ', '1': 'ｲﾁ', '2': 'ﾆ', '3': 'ｻﾝ', '4': 'ﾖﾝ',
    '5': 'ｺﾞ', '6': 'ﾛｸ', '7': 'ﾅﾅ', '8': 'ﾊﾁ', '9': 'ｷｭｳ',
}

def draw_circled_number(c: canvas.Canvas, char: str, x: float, y: float,
                        font_size: float = 10, circle_radius: float = 6):
    """数字を丸で囲んで描画

    Args:
        c: canvas object
        char: 数字文字（'0'-'9'）
        x: X座標
        y: Y座標
        font_size: 数字のフォントサイズ
        circle_radius: 丸の半径
    """
    # 丸を描画（数字の中央に配置、1上0.5左）
    cx = x + font_size * 0.3 - 0.5  # 数字の中央X - 0.5左
    cy = y + font_size * 0.3 + 1  # 数字の中央Y + 1上
    c.circle(cx, cy, circle_radius, stroke=1, fill=0)

    # 数字を描画
    c.setFont('IPAGothic', font_size)
    c.drawString(x, y, char)


def get_url_furigana(char: str) -> str:
    """文字に対応するフリガナを取得"""
    # 小文字に変換して検索
    lower_char = char.lower()
    return URL_FURIGANA_MAP.get(lower_char, '')


def draw_url_with_furigana(c: canvas.Canvas, url: str, start_x: float, start_y: float,
                           char_width: float, furigana_offset_y: float,
                           max_chars_per_line: int, line_height: float,
                           char_font_size: float = 10, furigana_font_size: float = 6):
    """URLを1文字ずつフリガナ付きで描画

    Args:
        c: canvas object
        url: URL文字列
        start_x: 開始X座標
        start_y: 開始Y座標（文字本体の位置）
        char_width: 1文字の幅
        furigana_offset_y: フリガナのY座標オフセット（文字本体からの距離、負の値で下に）
        max_chars_per_line: 1行あたり最大文字数
        line_height: 行間
        char_font_size: URL文字のフォントサイズ
        furigana_font_size: フリガナのフォントサイズ
    """
    col = 0
    row = 0

    for char in url:
        # 改行チェック
        if col >= max_chars_per_line:
            col = 0
            row += 1

        x = start_x + (col * char_width)
        y = start_y - (row * line_height)

        # URL文字を描画
        if char.isdigit():
            # 数字は丸で囲んで描画
            draw_circled_number(c, char, x, y, char_font_size)
        else:
            c.setFont('IPAGothic', char_font_size)
            c.drawString(x, y, char)

        # フリガナを描画（URL文字の中央に揃える）
        furigana = get_url_furigana(char)
        if furigana:
            c.setFont('IPAGothic', furigana_font_size)
            # URL文字の中央を基準に、フリガナ幅の半分だけ左にオフセット
            char_center_x = x + char_font_size * 0.3  # 文字の中央（おおよそ）
            furigana_width = len(furigana) * furigana_font_size * 0.5  # 半角カナの幅
            furigana_x = char_center_x - furigana_width / 2
            c.drawString(furigana_x, y + furigana_offset_y, furigana)

        col += 1


def draw_dot_grid(c: canvas.Canvas, interval: float = 10):
    """全面ドットグリッドを描画（テスト用）"""
    width, height = A4  # 595.276 x 841.890
    c.setFillColorRGB(0.7, 0.7, 0.7)  # 薄いグレー

    x = 0
    while x <= width:
        y = 0
        while y <= height:
            c.circle(x, y, 0.5, stroke=0, fill=1)
            y += interval
        x += interval


def parse_phone(phone: str) -> tuple[str, str, str]:
    """電話番号をパースして3分割"""
    # ハイフンがある場合はそれで分割
    if '-' in phone:
        parts = phone.split('-')
        if len(parts) >= 3:
            return parts[0], parts[1], parts[2]
        elif len(parts) == 2:
            return parts[0], parts[1], ''

    # ハイフンなしの場合は推測
    phone = phone.replace(' ', '').replace('　', '')
    if len(phone) == 10:
        # 固定電話 (03-1234-5678)
        return phone[:2], phone[2:6], phone[6:]
    elif len(phone) == 11:
        # 携帯電話 (090-1234-5678)
        return phone[:3], phone[3:7], phone[7:]
    else:
        return phone, '', ''


# ============================================
# PDF生成メイン関数
# ============================================

def generate_kobutsu_pdf(data: FormData, template_path: str) -> bytes:
    """古物商許可申請書PDFを生成してバイト列を返す"""

    register_font()

    # オーバーレイPDFをメモリ上に作成
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    # ========================================
    # ページ1: その１（基本情報）
    # ========================================

    c.setFont('IPAGothic', 10)

    # 公安委員会（提出先）
    c.drawString(coord.PUBLIC_SAFETY_COMMISSION_X, coord.PUBLIC_SAFETY_COMMISSION_Y, data.submissionPrefecture)

    # 申請者の氏名又は名称及び住所（セクション見出し直下、右端揃え）
    full_address = f"{data.prefecture}{data.city}{data.street}"
    applicant_info = f"{full_address} {data.nameKanji}"
    c.drawRightString(coord.APPLICANT_INFO_X, coord.APPLICANT_INFO_Y, applicant_info)

    # 許可の種類: 古物商を○で囲む
    draw_circle(c, *coord.PERMIT_TYPE_CIRCLE)

    # タイトル部の「古物市場主」に二重線
    draw_double_line(c, *coord.TITLE_KOBUTSU_ICHIBONUSHI_DOUBLE_LINE)

    # 氏名フリガナ
    draw_kana_in_grid(c, data.nameKana, coord.NAME_KANA_X, coord.NAME_KANA_Y)

    # 氏名漢字
    c.setFont('IPAGothic', 11)
    c.drawString(coord.NAME_KANJI_X, coord.NAME_KANJI_Y, data.nameKanji)

    # 法人等の種別: 個人の場合は6を○で囲む
    if data.applicantType == 'individual':
        draw_circle(c, *coord.INDIVIDUAL_CIRCLE)

    # 生年月日の元号
    era_key = data.birthEra.lower()
    if era_key in coord.ERA_POSITIONS:
        x1, x2 = coord.ERA_POSITIONS[era_key]
        y1, y2 = coord.ERA_CIRCLE_Y
        draw_circle(c, x1, y1, x2, y2)

    # 生年月日（月・日は2桁0埋め）
    c.setFont('IPAGothic', 10)
    draw_text_spaced(c, data.birthYear, coord.BIRTH_YEAR_X, coord.BIRTH_Y, coord.BIRTH_CHAR_WIDTH)
    draw_text_spaced(c, data.birthMonth.zfill(2), coord.BIRTH_MONTH_X, coord.BIRTH_Y, coord.BIRTH_CHAR_WIDTH)
    draw_text_spaced(c, data.birthDay.zfill(2), coord.BIRTH_DAY_X, coord.BIRTH_Y, coord.BIRTH_CHAR_WIDTH)

    # 住所
    c.drawString(coord.ADDRESS_PREF_X, coord.ADDRESS_PREF_Y, data.prefecture)
    c.drawString(coord.ADDRESS_CITY_X, coord.ADDRESS_CITY_Y, data.city)
    c.drawString(coord.ADDRESS_STREET_X, coord.ADDRESS_STREET_Y, data.street)

    # 電話番号
    area, local, number = parse_phone(data.phone)
    c.drawString(coord.PHONE_AREA_X, coord.PHONE_Y, area)
    c.drawString(coord.PHONE_LOCAL_X, coord.PHONE_Y, local)
    c.drawString(coord.PHONE_NUMBER_X, coord.PHONE_Y, number)

    # 行商: しない
    draw_circle(c, *coord.GYOSHO_SHINAI_CIRCLE)

    # 主として取り扱おうとする古物の区分: 11.皮革・ゴム製品類
    draw_circle(c, *coord.MAIN_ITEM_11_CIRCLE)

    # 代表者等（入力がある場合のみ）
    if data.representativeType and data.representativeLastNameKanji:
        # 種別
        if data.representativeType in coord.REP_TYPE_POSITIONS:
            draw_circle(c, *coord.REP_TYPE_POSITIONS[data.representativeType])

        # 氏名フリガナ
        rep_kana = data.representativeNameKana or ''
        draw_kana_in_grid(c, rep_kana, coord.REP_NAME_KANA_X, coord.REP_NAME_KANA_Y)

        # 氏名漢字
        c.setFont('IPAGothic', 11)
        rep_kanji = data.representativeNameKanji or ''
        c.drawString(coord.REP_NAME_KANJI_X, coord.REP_NAME_KANJI_Y, rep_kanji)

        # 生年月日の元号
        c.setFont('IPAGothic', 10)
        rep_era = (data.representativeBirthEra or 'heisei').lower()
        if rep_era in coord.REP_ERA_POSITIONS:
            x1, x2 = coord.REP_ERA_POSITIONS[rep_era]
            y1, y2 = coord.REP_ERA_CIRCLE_Y
            draw_circle(c, x1, y1, x2, y2)

        # 生年月日（月・日は2桁0埋め）
        draw_text_spaced(c, data.representativeBirthYear or '', coord.REP_BIRTH_YEAR_X, coord.REP_BIRTH_Y, coord.REP_BIRTH_CHAR_WIDTH)
        draw_text_spaced(c, (data.representativeBirthMonth or '').zfill(2) if data.representativeBirthMonth else '', coord.REP_BIRTH_MONTH_X, coord.REP_BIRTH_Y, coord.REP_BIRTH_CHAR_WIDTH)
        draw_text_spaced(c, (data.representativeBirthDay or '').zfill(2) if data.representativeBirthDay else '', coord.REP_BIRTH_DAY_X, coord.REP_BIRTH_Y, coord.REP_BIRTH_CHAR_WIDTH)

        # 住所
        c.drawString(coord.REP_PREF_X, coord.REP_PREF_Y, data.representativePrefecture or '')
        c.drawString(coord.REP_CITY_X, coord.REP_CITY_Y, data.representativeCity or '')
        c.drawString(coord.REP_STREET_X, coord.REP_STREET_Y, data.representativeStreet or '')

        # 電話番号
        rep_area, rep_local, rep_number = parse_phone(data.representativePhone or '')
        c.drawString(coord.REP_PHONE_AREA_X, coord.REP_PHONE_Y, rep_area)
        c.drawString(coord.REP_PHONE_LOCAL_X, coord.REP_PHONE_Y, rep_local)
        c.drawString(coord.REP_PHONE_NUMBER_X, coord.REP_PHONE_Y, rep_number)

    c.showPage()

    # ========================================
    # ページ2: その２（主たる営業所）
    # ========================================

    c.setFont('IPAGothic', 10)

    # 営業所あり
    draw_circle(c, *coord.OFFICE_ARI_CIRCLE)

    # 営業所名称
    draw_kana_in_grid(c, data.officeNameKana, coord.OFFICE_NAME_KANA_X, coord.OFFICE_NAME_KANA_Y)
    c.setFont('IPAGothic', 11)
    c.drawString(coord.OFFICE_NAME_KANJI_X, coord.OFFICE_NAME_KANJI_Y, data.officeNameKanji)

    # 営業所所在地
    c.setFont('IPAGothic', 10)
    if data.officeSameAsAddress:
        c.drawString(coord.OFFICE_PREF_X, coord.OFFICE_PREF_Y, data.prefecture)
        c.drawString(coord.OFFICE_CITY_X, coord.OFFICE_CITY_Y, data.city)
        c.drawString(coord.OFFICE_STREET_X, coord.OFFICE_STREET_Y, data.street)
        area, local, number = parse_phone(data.phone)
    else:
        c.drawString(coord.OFFICE_PREF_X, coord.OFFICE_PREF_Y, data.officePrefecture or '')
        c.drawString(coord.OFFICE_CITY_X, coord.OFFICE_CITY_Y, data.officeCity or '')
        c.drawString(coord.OFFICE_STREET_X, coord.OFFICE_STREET_Y, data.officeStreet or '')
        area, local, number = parse_phone(data.officePhone or '')

    c.drawString(coord.OFFICE_PHONE_AREA_X, coord.OFFICE_PHONE_Y, area)
    c.drawString(coord.OFFICE_PHONE_LOCAL_X, coord.OFFICE_PHONE_Y, local)
    c.drawString(coord.OFFICE_PHONE_NUMBER_X, coord.OFFICE_PHONE_Y, number)

    # 取扱品目: 02衣類、11皮革・ゴム製品類
    draw_circle(c, *coord.ITEM_02_CIRCLE)
    draw_circle(c, *coord.ITEM_11_CIRCLE)

    # 管理者情報
    if data.managerSameAsApplicant:
        manager_kana = data.nameKana
        manager_kanji = data.nameKanji
        manager_era = data.birthEra
        manager_year = data.birthYear
        manager_month = data.birthMonth
        manager_day = data.birthDay
        manager_pref = data.prefecture
        manager_city = data.city
        manager_street = data.street
        manager_phone = data.phone
    else:
        manager_kana = data.managerNameKana or ''
        manager_kanji = data.managerNameKanji or ''
        manager_era = data.managerBirthEra or 'heisei'
        manager_year = data.managerBirthYear or ''
        manager_month = data.managerBirthMonth or ''
        manager_day = data.managerBirthDay or ''
        manager_pref = data.managerPrefecture or ''
        manager_city = data.managerCity or ''
        manager_street = data.managerStreet or ''
        manager_phone = data.managerPhone or ''

    draw_kana_in_grid(c, manager_kana, coord.MANAGER_NAME_KANA_X, coord.MANAGER_NAME_KANA_Y)
    c.setFont('IPAGothic', 11)
    c.drawString(coord.MANAGER_NAME_KANJI_X, coord.MANAGER_NAME_KANJI_Y, manager_kanji)

    # 管理者生年月日の元号
    era_key = manager_era.lower()
    if era_key in coord.MANAGER_ERA_POSITIONS:
        x1, x2 = coord.MANAGER_ERA_POSITIONS[era_key]
        y1, y2 = coord.MANAGER_ERA_CIRCLE_Y
        draw_circle(c, x1, y1, x2, y2)

    c.setFont('IPAGothic', 10)
    draw_text_spaced(c, manager_year, coord.MANAGER_BIRTH_YEAR_X, coord.MANAGER_BIRTH_Y, coord.MANAGER_BIRTH_CHAR_WIDTH)
    draw_text_spaced(c, manager_month.zfill(2) if manager_month else '', coord.MANAGER_BIRTH_MONTH_X, coord.MANAGER_BIRTH_Y, coord.MANAGER_BIRTH_CHAR_WIDTH)
    draw_text_spaced(c, manager_day.zfill(2) if manager_day else '', coord.MANAGER_BIRTH_DAY_X, coord.MANAGER_BIRTH_Y, coord.MANAGER_BIRTH_CHAR_WIDTH)

    c.drawString(coord.MANAGER_PREF_X, coord.MANAGER_PREF_Y, manager_pref)
    c.drawString(coord.MANAGER_CITY_X, coord.MANAGER_CITY_Y, manager_city)
    c.drawString(coord.MANAGER_STREET_X, coord.MANAGER_STREET_Y, manager_street)

    area, local, number = parse_phone(manager_phone)
    c.drawString(coord.MANAGER_PHONE_AREA_X, coord.MANAGER_PHONE_Y, area)
    c.drawString(coord.MANAGER_PHONE_LOCAL_X, coord.MANAGER_PHONE_Y, local)
    c.drawString(coord.MANAGER_PHONE_NUMBER_X, coord.MANAGER_PHONE_Y, number)

    c.showPage()

    # ========================================
    # ページ3: その３（その他の営業所）
    # ========================================

    # 使用しないので空ページ
    c.showPage()

    # ========================================
    # ページ4: その４（ホームページ）
    # ========================================

    c.setFont('IPAGothic', 10)

    if data.hasWebsite:
        draw_circle(c, *coord.WEBSITE_USE_CIRCLE)
        # URL描画（1文字ずつフリガナ付き）
        if data.websiteUrl:
            draw_url_with_furigana(
                c,
                url=data.websiteUrl,
                start_x=coord.URL_GRID_START_X,
                start_y=coord.URL_GRID_START_Y,
                char_width=coord.URL_CHAR_WIDTH,
                furigana_offset_y=coord.URL_FURIGANA_OFFSET,
                max_chars_per_line=coord.URL_MAX_CHARS_PER_LINE,
                line_height=coord.URL_LINE_HEIGHT,
                char_font_size=coord.URL_CHAR_FONT_SIZE,
                furigana_font_size=coord.URL_FURIGANA_FONT_SIZE
            )
    else:
        draw_circle(c, *coord.WEBSITE_NOT_USE_CIRCLE)

    c.showPage()

    c.save()

    # ========================================
    # テンプレートとマージ
    # ========================================

    buffer.seek(0)
    overlay_pdf = PdfReader(buffer)
    original_pdf = PdfReader(template_path)

    writer = PdfWriter()

    for i, page in enumerate(original_pdf.pages):
        if i < len(overlay_pdf.pages):
            page.merge_page(overlay_pdf.pages[i])
        writer.add_page(page)

    # 結果をバイト列として返す
    output_buffer = io.BytesIO()
    writer.write(output_buffer)
    output_buffer.seek(0)

    return output_buffer.read()


# ============================================
# 年齢計算
# ============================================

ERA_TO_SEIREKI = {
    'meiji': 1867,
    'taisho': 1911,
    'showa': 1925,
    'heisei': 1988,
    'reiwa': 2018,
    'seireki': 0,
}


def calculate_age(birth_era: str, birth_year: str, birth_month: str, birth_day: str) -> int:
    """生年月日から年齢を計算"""
    try:
        era_key = birth_era.lower()
        base_year = ERA_TO_SEIREKI.get(era_key, 0)
        birth_year_int = base_year + int(birth_year)
        birth_month_int = int(birth_month)
        birth_day_int = int(birth_day)

        today = date.today()
        age = today.year - birth_year_int

        # 誕生日がまだ来ていない場合は1歳引く
        if (today.month, today.day) < (birth_month_int, birth_day_int):
            age -= 1

        return age
    except (ValueError, TypeError):
        return 0


def era_to_wareki_year(birth_era: str, birth_year: str) -> str:
    """元号と年から和暦の年を返す（西暦の場合は和暦に変換）"""
    try:
        era_key = birth_era.lower()
        if era_key == 'seireki':
            # 西暦から和暦に変換
            seireki_year = int(birth_year)
            if seireki_year >= 2019:
                return str(seireki_year - 2018)  # 令和
            elif seireki_year >= 1989:
                return str(seireki_year - 1988)  # 平成
            elif seireki_year >= 1926:
                return str(seireki_year - 1925)  # 昭和
            elif seireki_year >= 1912:
                return str(seireki_year - 1911)  # 大正
            else:
                return str(seireki_year - 1867)  # 明治
        else:
            return birth_year
    except (ValueError, TypeError):
        return birth_year


def seireki_to_wareki_era(birth_era: str, birth_year: str) -> str:
    """西暦から和暦の元号を返す"""
    try:
        era_key = birth_era.lower()
        if era_key == 'seireki':
            seireki_year = int(birth_year)
            if seireki_year >= 2019:
                return 'reiwa'
            elif seireki_year >= 1989:
                return 'heisei'
            elif seireki_year >= 1926:
                return 'showa'
            elif seireki_year >= 1912:
                return 'taisho'
            else:
                return 'meiji'
        else:
            return era_key
    except (ValueError, TypeError):
        return era_key


# ============================================
# 誓約書PDF生成
# ============================================

def generate_seiyakusho_overlay(data: FormData, is_manager: bool = False) -> io.BytesIO:
    """誓約書のオーバーレイPDFを生成

    Args:
        data: フォームデータ
        is_manager: True=管理者用, False=申請者用
    """
    register_font()

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setFont('IPAGothic', 10)

    # 座標を選択（管理者用は別座標）
    if is_manager:
        pref_y = coord.SEIYAKU_KANRI_PREFECTURE_Y
        addr_y = coord.SEIYAKU_KANRI_ADDRESS_Y
        name_y = coord.SEIYAKU_KANRI_NAME_Y
    else:
        pref_y = coord.SEIYAKU_PREFECTURE_Y
        addr_y = coord.SEIYAKU_ADDRESS_Y
        name_y = coord.SEIYAKU_NAME_Y

    # 公安委員会名（都道府県）- 右揃え
    c.drawRightString(coord.SEIYAKU_PREFECTURE_X, pref_y, data.submissionPrefecture)

    # 署名日は空欄（提出時に記入）

    # 住所・氏名
    if is_manager and not data.managerSameAsApplicant:
        address = f"{data.managerPrefecture or ''}{data.managerCity or ''}{data.managerStreet or ''}"
        name = f"{data.managerLastNameKanji or ''} {data.managerFirstNameKanji or ''}"
    else:
        address = f"{data.prefecture}{data.city}{data.street}"
        name = data.nameKanji

    c.drawString(coord.SEIYAKU_ADDRESS_X, addr_y, address)
    c.drawString(coord.SEIYAKU_NAME_X, name_y, name)

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer


# ============================================
# 略歴書PDF生成
# ============================================

def generate_ryakurekisyo_overlay(data: FormData, is_manager: bool = False) -> io.BytesIO:
    """略歴書のオーバーレイPDFを生成

    Args:
        data: フォームデータ
        is_manager: True=管理者用, False=申請者用
    """
    register_font()

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.setFont('IPAGothic', 10)

    # 対象者のデータを選択
    if is_manager and not data.managerSameAsApplicant:
        kana = f"{data.managerLastNameKana or ''} {data.managerFirstNameKana or ''}"
        name = f"{data.managerLastNameKanji or ''} {data.managerFirstNameKanji or ''}"
        birth_era = data.managerBirthEra or 'heisei'
        birth_year = data.managerBirthYear or ''
        birth_month = data.managerBirthMonth or ''
        birth_day = data.managerBirthDay or ''
        address = f"{data.managerPrefecture or ''}{data.managerCity or ''}{data.managerStreet or ''}"
        career_history = data.managerCareerHistory or []
    else:
        kana = data.nameKana
        name = data.nameKanji
        birth_era = data.birthEra
        birth_year = data.birthYear
        birth_month = data.birthMonth
        birth_day = data.birthDay
        address = f"{data.prefecture}{data.city}{data.street}"
        career_history = data.careerHistory or []

    # ふりがな（略歴書はひらがな表記）
    kana_hiragana = katakana_to_hiragana(kana)
    c.drawString(coord.RYAKUREKI_KANA_X, coord.RYAKUREKI_KANA_Y, kana_hiragana)

    # 氏名
    c.setFont('IPAGothic', 11)
    c.drawString(coord.RYAKUREKI_NAME_X, coord.RYAKUREKI_NAME_Y, name)
    c.setFont('IPAGothic', 10)

    # 生年月日（西暦）- 略歴書は右揃え、0埋めなし
    c.drawRightString(coord.RYAKUREKI_BIRTH_YEAR_X, coord.RYAKUREKI_BIRTH_Y, birth_year or '')
    c.drawRightString(coord.RYAKUREKI_BIRTH_MONTH_X, coord.RYAKUREKI_BIRTH_Y, birth_month or '')
    c.drawRightString(coord.RYAKUREKI_BIRTH_DAY_X, coord.RYAKUREKI_BIRTH_Y, birth_day or '')

    # 年齢
    age = calculate_age(birth_era, birth_year, birth_month, birth_day)
    c.drawString(coord.RYAKUREKI_AGE_X, coord.RYAKUREKI_AGE_Y, str(age))

    # 住所
    c.drawString(coord.RYAKUREKI_ADDRESS_X, coord.RYAKUREKI_ADDRESS_Y, address)

    # 職歴等（最大6行 + 「現在に至る」）
    for i, entry in enumerate(career_history[:6]):
        y = coord.RYAKUREKI_CAREER_START_Y - (i * coord.RYAKUREKI_CAREER_LINE_HEIGHT)
        # 期間（年・月）- 右揃え
        c.drawRightString(coord.RYAKUREKI_CAREER_YEAR_X, y, entry.year)
        c.drawRightString(coord.RYAKUREKI_CAREER_MONTH_X, y, entry.month)
        # 内容 - 左揃え
        c.drawString(coord.RYAKUREKI_CAREER_CONTENT_X, y, entry.content)

    # 7行目に「現在に至る」を自動追加（5下）
    y = coord.RYAKUREKI_CAREER_START_Y - (6 * coord.RYAKUREKI_CAREER_LINE_HEIGHT) - 5
    c.drawString(coord.RYAKUREKI_CAREER_CONTENT_X, y, '現在に至る')

    # 署名日は空欄（提出時に記入）

    # 署名（氏名）
    c.drawString(coord.RYAKUREKI_SIGN_NAME_X, coord.RYAKUREKI_SIGN_NAME_Y, name)

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer


# ============================================
# 全書類結合PDF生成
# ============================================

def merge_overlay_single_page(template_path: str, overlay_buffer: io.BytesIO) -> any:
    """テンプレートPDFにオーバーレイをマージして1ページを返す"""
    overlay_pdf = PdfReader(overlay_buffer)
    template_pdf = PdfReader(template_path)

    page = template_pdf.pages[0]
    if len(overlay_pdf.pages) > 0:
        page.merge_page(overlay_pdf.pages[0])

    return page


def generate_full_application_pdf(
    data: FormData,
    shinsei_template_path: str,
    seiyaku_kojin_template_path: str,
    seiyaku_kanrisha_template_path: str,
    ryakureki_template_path: str,
    with_grid: bool = False
) -> bytes:
    """全書類を結合した完全版PDFを生成

    構成:
    - 申請者と管理者が同一の場合（7ページ）:
      1-4: 古物商許可申請書その1〜4
      5: 誓約書（申請者用）
      6: 略歴書（申請者用）
      7: 誓約書（管理者用）

    - 申請者と管理者が異なる場合（8ページ）:
      1-4: 古物商許可申請書その1〜4
      5: 誓約書（申請者用）
      6: 略歴書（申請者用）
      7: 誓約書（管理者用）
      8: 略歴書（管理者用）

    Args:
        with_grid: True=ドットグリッド付き（座標調整用）
    """
    register_font()
    writer = PdfWriter()

    def create_grid_page():
        """ドットグリッドのページを生成"""
        grid_buffer = io.BytesIO()
        grid_canvas = canvas.Canvas(grid_buffer, pagesize=A4)
        draw_dot_grid(grid_canvas)
        grid_canvas.showPage()
        grid_canvas.save()
        grid_buffer.seek(0)
        grid_pdf = PdfReader(grid_buffer)
        return grid_pdf.pages[0]

    def add_page_with_optional_grid(page):
        """ページを追加（with_grid=Trueの場合はグリッドもマージ）"""
        if with_grid:
            page.merge_page(create_grid_page())
        writer.add_page(page)

    # 1. 許可申請書（4ページ）
    shinsei_pdf = generate_kobutsu_pdf(data, shinsei_template_path)
    shinsei_reader = PdfReader(io.BytesIO(shinsei_pdf))
    for page in shinsei_reader.pages:
        add_page_with_optional_grid(page)

    # 2. 申請者用誓約書
    seiyaku_applicant_overlay = generate_seiyakusho_overlay(data, is_manager=False)
    seiyaku_applicant_page = merge_overlay_single_page(seiyaku_kojin_template_path, seiyaku_applicant_overlay)
    add_page_with_optional_grid(seiyaku_applicant_page)

    # 3. 申請者用略歴書
    ryakureki_applicant_overlay = generate_ryakurekisyo_overlay(data, is_manager=False)
    ryakureki_applicant_page = merge_overlay_single_page(ryakureki_template_path, ryakureki_applicant_overlay)
    add_page_with_optional_grid(ryakureki_applicant_page)

    # 4. 管理者用誓約書（常に出力）
    seiyaku_manager_overlay = generate_seiyakusho_overlay(data, is_manager=True)
    seiyaku_manager_page = merge_overlay_single_page(seiyaku_kanrisha_template_path, seiyaku_manager_overlay)
    add_page_with_optional_grid(seiyaku_manager_page)

    # 5. 管理者用略歴書（管理者が申請者と異なる場合のみ）
    if not data.managerSameAsApplicant:
        ryakureki_manager_overlay = generate_ryakurekisyo_overlay(data, is_manager=True)
        ryakureki_manager_page = merge_overlay_single_page(ryakureki_template_path, ryakureki_manager_overlay)
        add_page_with_optional_grid(ryakureki_manager_page)

    # 結果をバイト列として返す
    output_buffer = io.BytesIO()
    writer.write(output_buffer)
    output_buffer.seek(0)

    return output_buffer.read()


def generate_test_pdf(template_path: str) -> bytes:
    """位置確認用テストPDF（全ての○とサンプルテキストを描画）"""

    register_font()

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    # ========================================
    # ページ1: その１（基本情報）- 全ての○を描画
    # ========================================

    draw_dot_grid(c)  # ドットグリッド
    c.setFont('IPAGothic', 10)

    # 公安委員会
    c.drawString(coord.PUBLIC_SAFETY_COMMISSION_X, coord.PUBLIC_SAFETY_COMMISSION_Y, "大阪府")

    # 申請者の氏名又は名称及び住所
    c.drawRightString(coord.APPLICANT_INFO_X, coord.APPLICANT_INFO_Y, "大阪府大阪市北区梅田1-2-3 山田太郎")

    # 許可の種類: 古物商を○で囲む
    draw_circle(c, *coord.PERMIT_TYPE_CIRCLE)

    # タイトル部の「古物市場主」に二重線
    draw_double_line(c, *coord.TITLE_KOBUTSU_ICHIBONUSHI_DOUBLE_LINE)

    # 氏名フリガナ・漢字
    draw_kana_in_grid(c, "ヤマダ タロウ", coord.NAME_KANA_X, coord.NAME_KANA_Y)
    c.setFont('IPAGothic', 11)
    c.drawString(coord.NAME_KANJI_X, coord.NAME_KANJI_Y, "山田 太郎")

    # 法人等の種別: 全て○
    draw_circle(c, *coord.INDIVIDUAL_CIRCLE)  # 個人

    # 生年月日の元号: 全て○
    c.setFont('IPAGothic', 10)
    for era_key, (x1, x2) in coord.ERA_POSITIONS.items():
        y1, y2 = coord.ERA_CIRCLE_Y
        draw_circle(c, x1, y1, x2, y2)

    # 生年月日
    draw_text_spaced(c, "1980", coord.BIRTH_YEAR_X, coord.BIRTH_Y, coord.BIRTH_CHAR_WIDTH)
    draw_text_spaced(c, "03", coord.BIRTH_MONTH_X, coord.BIRTH_Y, coord.BIRTH_CHAR_WIDTH)
    draw_text_spaced(c, "15", coord.BIRTH_DAY_X, coord.BIRTH_Y, coord.BIRTH_CHAR_WIDTH)

    # 住所
    c.drawString(coord.ADDRESS_PREF_X, coord.ADDRESS_PREF_Y, "大阪府")
    c.drawString(coord.ADDRESS_CITY_X, coord.ADDRESS_CITY_Y, "大阪市北区梅田")
    c.drawString(coord.ADDRESS_STREET_X, coord.ADDRESS_STREET_Y, "1-2-3")

    # 電話番号
    c.drawString(coord.PHONE_AREA_X, coord.PHONE_Y, "06")
    c.drawString(coord.PHONE_LOCAL_X, coord.PHONE_Y, "1234")
    c.drawString(coord.PHONE_NUMBER_X, coord.PHONE_Y, "5678")

    # 行商: 両方○（位置確認用）
    draw_circle(c, *coord.GYOSHO_SHINAI_CIRCLE)

    # 主として取り扱おうとする古物の区分: 11
    draw_circle(c, *coord.MAIN_ITEM_11_CIRCLE)

    # 代表者等: 全て○
    for rep_type, circle_coords in coord.REP_TYPE_POSITIONS.items():
        draw_circle(c, *circle_coords)

    # 代表者氏名
    draw_kana_in_grid(c, "タナカ イチロウ", coord.REP_NAME_KANA_X, coord.REP_NAME_KANA_Y)
    c.setFont('IPAGothic', 11)
    c.drawString(coord.REP_NAME_KANJI_X, coord.REP_NAME_KANJI_Y, "田中 一郎")

    # 代表者生年月日の元号: 全て○
    c.setFont('IPAGothic', 10)
    for era_key, (x1, x2) in coord.REP_ERA_POSITIONS.items():
        y1, y2 = coord.REP_ERA_CIRCLE_Y
        draw_circle(c, x1, y1, x2, y2)

    # 代表者生年月日
    draw_text_spaced(c, "1965", coord.REP_BIRTH_YEAR_X, coord.REP_BIRTH_Y, coord.REP_BIRTH_CHAR_WIDTH)
    draw_text_spaced(c, "11", coord.REP_BIRTH_MONTH_X, coord.REP_BIRTH_Y, coord.REP_BIRTH_CHAR_WIDTH)
    draw_text_spaced(c, "03", coord.REP_BIRTH_DAY_X, coord.REP_BIRTH_Y, coord.REP_BIRTH_CHAR_WIDTH)

    # 代表者住所
    c.drawString(coord.REP_PREF_X, coord.REP_PREF_Y, "大阪府")
    c.drawString(coord.REP_CITY_X, coord.REP_CITY_Y, "大阪市中央区南船場")
    c.drawString(coord.REP_STREET_X, coord.REP_STREET_Y, "7-8-9")

    # 代表者電話番号
    c.drawString(coord.REP_PHONE_AREA_X, coord.REP_PHONE_Y, "06")
    c.drawString(coord.REP_PHONE_LOCAL_X, coord.REP_PHONE_Y, "5555")
    c.drawString(coord.REP_PHONE_NUMBER_X, coord.REP_PHONE_Y, "1234")

    c.showPage()

    # ========================================
    # ページ2: その２（主たる営業所）
    # ========================================

    draw_dot_grid(c)  # ドットグリッド
    c.setFont('IPAGothic', 10)

    # 営業所あり
    draw_circle(c, *coord.OFFICE_ARI_CIRCLE)

    # 営業所名称
    draw_kana_in_grid(c, "ヤマダショウテン", coord.OFFICE_NAME_KANA_X, coord.OFFICE_NAME_KANA_Y)
    c.setFont('IPAGothic', 11)
    c.drawString(coord.OFFICE_NAME_KANJI_X, coord.OFFICE_NAME_KANJI_Y, "山田商店")

    # 営業所所在地
    c.setFont('IPAGothic', 10)
    c.drawString(coord.OFFICE_PREF_X, coord.OFFICE_PREF_Y, "大阪府")
    c.drawString(coord.OFFICE_CITY_X, coord.OFFICE_CITY_Y, "大阪市北区梅田")
    c.drawString(coord.OFFICE_STREET_X, coord.OFFICE_STREET_Y, "1-2-3")

    # 営業所電話番号
    c.drawString(coord.OFFICE_PHONE_AREA_X, coord.OFFICE_PHONE_Y, "06")
    c.drawString(coord.OFFICE_PHONE_LOCAL_X, coord.OFFICE_PHONE_Y, "1234")
    c.drawString(coord.OFFICE_PHONE_NUMBER_X, coord.OFFICE_PHONE_Y, "5678")

    # 取扱品目: 02, 11
    draw_circle(c, *coord.ITEM_02_CIRCLE)
    draw_circle(c, *coord.ITEM_11_CIRCLE)

    # 管理者氏名
    draw_kana_in_grid(c, "スズキ ハナコ", coord.MANAGER_NAME_KANA_X, coord.MANAGER_NAME_KANA_Y)
    c.setFont('IPAGothic', 11)
    c.drawString(coord.MANAGER_NAME_KANJI_X, coord.MANAGER_NAME_KANJI_Y, "鈴木 花子")

    # 管理者生年月日の元号: 全て○
    c.setFont('IPAGothic', 10)
    for era_key, (x1, x2) in coord.MANAGER_ERA_POSITIONS.items():
        y1, y2 = coord.MANAGER_ERA_CIRCLE_Y
        draw_circle(c, x1, y1, x2, y2)

    # 管理者生年月日
    draw_text_spaced(c, "1990", coord.MANAGER_BIRTH_YEAR_X, coord.MANAGER_BIRTH_Y, coord.MANAGER_BIRTH_CHAR_WIDTH)
    draw_text_spaced(c, "07", coord.MANAGER_BIRTH_MONTH_X, coord.MANAGER_BIRTH_Y, coord.MANAGER_BIRTH_CHAR_WIDTH)
    draw_text_spaced(c, "25", coord.MANAGER_BIRTH_DAY_X, coord.MANAGER_BIRTH_Y, coord.MANAGER_BIRTH_CHAR_WIDTH)

    # 管理者住所
    c.drawString(coord.MANAGER_PREF_X, coord.MANAGER_PREF_Y, "大阪府")
    c.drawString(coord.MANAGER_CITY_X, coord.MANAGER_CITY_Y, "大阪市西区江戸堀")
    c.drawString(coord.MANAGER_STREET_X, coord.MANAGER_STREET_Y, "4-5-6")

    # 管理者電話番号
    c.drawString(coord.MANAGER_PHONE_AREA_X, coord.MANAGER_PHONE_Y, "080")
    c.drawString(coord.MANAGER_PHONE_LOCAL_X, coord.MANAGER_PHONE_Y, "9876")
    c.drawString(coord.MANAGER_PHONE_NUMBER_X, coord.MANAGER_PHONE_Y, "5432")

    c.showPage()

    # ========================================
    # ページ3: その３（その他の営業所）
    # ========================================
    draw_dot_grid(c)  # ドットグリッド
    c.showPage()

    # ========================================
    # ページ4: その４（ホームページ）
    # ========================================

    draw_dot_grid(c)  # ドットグリッド
    c.setFont('IPAGothic', 10)

    # ホームページ: 両方○（位置確認用）
    draw_circle(c, *coord.WEBSITE_USE_CIRCLE)
    draw_circle(c, *coord.WEBSITE_NOT_USE_CIRCLE)

    # テスト用URL（全文字網羅）
    test_url = "https://abcdefghijklmnopqrstuvwxyz.jp/0123456789-_~.test"
    draw_url_with_furigana(
        c,
        url=test_url,
        start_x=coord.URL_GRID_START_X,
        start_y=coord.URL_GRID_START_Y,
        char_width=coord.URL_CHAR_WIDTH,
        furigana_offset_y=coord.URL_FURIGANA_OFFSET,
        max_chars_per_line=coord.URL_MAX_CHARS_PER_LINE,
        line_height=coord.URL_LINE_HEIGHT,
        char_font_size=coord.URL_CHAR_FONT_SIZE,
        furigana_font_size=coord.URL_FURIGANA_FONT_SIZE
    )

    c.showPage()

    c.save()

    # テンプレートとマージ
    buffer.seek(0)
    overlay_pdf = PdfReader(buffer)
    original_pdf = PdfReader(template_path)

    writer = PdfWriter()

    for i, page in enumerate(original_pdf.pages):
        if i < len(overlay_pdf.pages):
            page.merge_page(overlay_pdf.pages[i])
        writer.add_page(page)

    output_buffer = io.BytesIO()
    writer.write(output_buffer)
    output_buffer.seek(0)

    return output_buffer.read()
