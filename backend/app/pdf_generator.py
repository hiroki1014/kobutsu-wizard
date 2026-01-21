"""古物商許可申請書 PDF生成モジュール"""

import io
import unicodedata
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
        # TODO: URL描画は後で調整
        # c.drawString(coord.WEBSITE_URL_X, coord.WEBSITE_URL_Y, data.websiteUrl or '')
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
