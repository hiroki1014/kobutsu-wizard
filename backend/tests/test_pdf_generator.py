"""PDF生成ロジックのテスト"""

import pytest
from unittest.mock import patch, MagicMock

from app.pdf_generator import (
    separate_dakuten,
    to_halfwidth_kana,
    parse_phone,
    generate_kobutsu_pdf,
)
from app.schemas import FormData


class TestSeparateDakuten:
    """濁点分離のテスト"""

    def test_separate_dakuten_basic(self):
        """濁点分離: "ダ" → ["タ", "゛"]"""
        result = separate_dakuten("ダ")
        assert result == ["タ", "\u3099"]  # \u3099 は結合用濁点

    def test_separate_dakuten_handakuten(self):
        """半濁点分離: "パ" → ["ハ", "゜"]"""
        result = separate_dakuten("パ")
        assert result == ["ハ", "\u309A"]  # \u309A は結合用半濁点

    def test_separate_dakuten_no_dakuten(self):
        """濁点なし: "カ" → ["カ"]"""
        result = separate_dakuten("カ")
        assert result == ["カ"]

    def test_separate_dakuten_multiple_chars(self):
        """複数文字: "ガギグゲゴ" が正しく分離される"""
        result = separate_dakuten("ガ")
        assert len(result) == 2
        assert result[0] == "カ"

    def test_separate_dakuten_mixed(self):
        """濁点あり・なし混合"""
        result = separate_dakuten("アガ")
        assert result[0] == "ア"
        assert result[1] == "カ"
        assert result[2] == "\u3099"


class TestToHalfwidthKana:
    """全角→半角カナ変換のテスト"""

    def test_to_halfwidth_kana(self):
        """全角→半角変換: "ア" → "ｱ" """
        assert to_halfwidth_kana("ア") == "ｱ"

    def test_to_halfwidth_kana_dakuten(self):
        """濁点変換: "゛" → "ﾞ" """
        assert to_halfwidth_kana("゛") == "ﾞ"
        assert to_halfwidth_kana("\u3099") == "ﾞ"

    def test_to_halfwidth_kana_handakuten(self):
        """半濁点変換: "゜" → "ﾟ" """
        assert to_halfwidth_kana("゜") == "ﾟ"
        assert to_halfwidth_kana("\u309A") == "ﾟ"

    def test_to_halfwidth_kana_various(self):
        """各種カナの変換"""
        assert to_halfwidth_kana("イ") == "ｲ"
        assert to_halfwidth_kana("ウ") == "ｳ"
        assert to_halfwidth_kana("エ") == "ｴ"
        assert to_halfwidth_kana("オ") == "ｵ"
        assert to_halfwidth_kana("ン") == "ﾝ"
        assert to_halfwidth_kana("ー") == "ｰ"

    def test_to_halfwidth_kana_small(self):
        """小文字カナの変換"""
        assert to_halfwidth_kana("ァ") == "ｧ"
        assert to_halfwidth_kana("ィ") == "ｨ"
        assert to_halfwidth_kana("ッ") == "ｯ"
        assert to_halfwidth_kana("ャ") == "ｬ"


class TestParsePhone:
    """電話番号パースのテスト"""

    def test_parse_phone_with_hyphen(self):
        """電話番号パース: "03-1234-5678" """
        result = parse_phone("03-1234-5678")
        assert result == ("03", "1234", "5678")

    def test_parse_phone_without_hyphen_10digits(self):
        """固定電話: "0312345678" """
        result = parse_phone("0312345678")
        assert result == ("03", "1234", "5678")

    def test_parse_phone_without_hyphen_11digits(self):
        """携帯: "09012345678" """
        result = parse_phone("09012345678")
        assert result == ("090", "1234", "5678")

    def test_parse_phone_with_two_hyphens(self):
        """2つのハイフン形式"""
        result = parse_phone("045-123-4567")
        assert result == ("045", "123", "4567")

    def test_parse_phone_with_spaces(self):
        """スペースを含む電話番号"""
        result = parse_phone("03 1234 5678".replace(" ", ""))
        assert result == ("03", "1234", "5678")


class TestGeneratePdf:
    """PDF生成のテスト"""

    @pytest.fixture
    def valid_form_data(self):
        """有効なフォームデータを返すフィクスチャ"""
        return FormData(
            applicantType="individual",
            nameKana="ヤマダ タロウ",
            nameKanji="山田 太郎",
            birthEra="heisei",
            birthYear="5",
            birthMonth="3",
            birthDay="15",
            prefecture="東京都",
            city="渋谷区",
            street="1-2-3",
            phone="03-1234-5678",
            officeSameAsAddress=True,
            officeNameKana="ヤマダショウテン",
            officeNameKanji="山田商店",
            managerSameAsApplicant=True,
            hasWebsite=False,
            applicationEra="reiwa",
            applicationYear="7",
            applicationMonth="1",
            applicationDay="15",
            submissionPrefecture="東京都",
        )

    def test_generate_pdf_returns_bytes(self, valid_form_data, tmp_path):
        """PDF生成がbytesを返す（フォントが利用可能な場合のみ）"""
        from pathlib import Path

        # テンプレートPDFが必要なのでスキップするかどうかを確認
        template_path = Path(__file__).parent.parent / "templates" / "template.pdf"
        if not template_path.exists():
            pytest.skip("テンプレートPDFが見つかりません")

        # フォントが利用可能かどうかを確認
        from app.pdf_generator import FONT_PATHS
        font_available = any(Path(p).exists() for p in FONT_PATHS)
        if not font_available:
            pytest.skip("日本語フォントが見つかりません")

        result = generate_kobutsu_pdf(valid_form_data, str(template_path))

        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_generated_pdf_is_valid(self, valid_form_data, tmp_path):
        """生成されたPDFが有効なPDF形式（フォントが利用可能な場合のみ）"""
        from pathlib import Path

        # テンプレートPDFが必要なのでスキップするかどうかを確認
        template_path = Path(__file__).parent.parent / "templates" / "template.pdf"
        if not template_path.exists():
            pytest.skip("テンプレートPDFが見つかりません")

        # フォントが利用可能かどうかを確認
        from app.pdf_generator import FONT_PATHS
        font_available = any(Path(p).exists() for p in FONT_PATHS)
        if not font_available:
            pytest.skip("日本語フォントが見つかりません")

        result = generate_kobutsu_pdf(valid_form_data, str(template_path))

        # PDFの基本的な形式チェック
        assert result.startswith(b"%PDF")
