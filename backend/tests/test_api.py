"""APIエンドポイントのテスト"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from pathlib import Path

from app.main import app


@pytest.fixture
def client():
    """テストクライアント"""
    return TestClient(app)


# 有効なフォームデータ（個人申請者）
VALID_INDIVIDUAL_DATA = {
    "applicantType": "individual",
    "lastNameKanji": "山田",
    "firstNameKanji": "太郎",
    "lastNameKana": "ヤマダ",
    "firstNameKana": "タロウ",
    "birthEra": "heisei",
    "birthYear": "5",
    "birthMonth": "3",
    "birthDay": "15",
    "prefecture": "東京都",
    "city": "渋谷区",
    "street": "1-2-3",
    "phone": "03-1234-5678",
    "officeSameAsAddress": True,
    "officeNameKana": "ヤマダショウテン",
    "officeNameKanji": "山田商店",
    "managerSameAsApplicant": True,
    "hasWebsite": False,
    "submissionPrefecture": "東京都",
}

# 有効なフォームデータ（法人申請者）
VALID_CORPORATION_DATA = {
    **VALID_INDIVIDUAL_DATA,
    "applicantType": "corporation",
    "corporationType": "kabushiki",
    "corporationName": "株式会社テスト",
}

# ホームページありのフォームデータ
VALID_DATA_WITH_WEBSITE = {
    **VALID_INDIVIDUAL_DATA,
    "hasWebsite": True,
    "websiteUrl": "https://example.com",
}

# ホームページなしのフォームデータ
VALID_DATA_WITHOUT_WEBSITE = {
    **VALID_INDIVIDUAL_DATA,
    "hasWebsite": False,
    "websiteUrl": None,
}

# 管理者が申請者と異なる場合のフォームデータ
VALID_DATA_DIFFERENT_MANAGER = {
    **VALID_INDIVIDUAL_DATA,
    "managerSameAsApplicant": False,
    "managerLastNameKanji": "鈴木",
    "managerFirstNameKanji": "花子",
    "managerLastNameKana": "スズキ",
    "managerFirstNameKana": "ハナコ",
    "managerBirthEra": "showa",
    "managerBirthYear": "55",
    "managerBirthMonth": "7",
    "managerBirthDay": "20",
    "managerPrefecture": "神奈川県",
    "managerCity": "横浜市",
    "managerStreet": "4-5-6",
    "managerPhone": "045-123-4567",
}

# 営業所住所が申請者住所と異なる場合
VALID_DATA_DIFFERENT_OFFICE = {
    **VALID_INDIVIDUAL_DATA,
    "officeSameAsAddress": False,
    "officePostalCode": "150-0001",
    "officePrefecture": "東京都",
    "officeCity": "渋谷区神宮前",
    "officeStreet": "7-8-9",
    "officePhone": "03-9876-5432",
}


class TestHealthCheck:
    """ヘルスチェックのテスト"""

    def test_health_check(self, client):
        """GET /api/health が {"status": "ok"} を返す"""
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestGeneratePdf:
    """PDF生成エンドポイントのテスト"""

    @pytest.fixture
    def mock_templates_exist(self):
        """テンプレートファイルの存在をモック"""
        mock_path = MagicMock(spec=Path)
        mock_path.exists.return_value = True
        with patch("app.main.TEMPLATE_PATH", mock_path), \
             patch("app.main.SEIYAKU_KOJIN_PATH", mock_path), \
             patch("app.main.SEIYAKU_KANRISHA_PATH", mock_path), \
             patch("app.main.RYAKUREKI_PATH", mock_path):
            yield mock_path

    def test_generate_pdf_success(self, client, mock_templates_exist):
        """POST /api/generate-pdf が正常なデータでPDFを返す"""
        with patch("app.main.generate_full_application_pdf") as mock_generate:
            mock_generate.return_value = b"%PDF-1.4 test pdf content"
            response = client.post("/api/generate-pdf", json=VALID_INDIVIDUAL_DATA)

            assert response.status_code == 200
            assert response.headers["content-type"] == "application/pdf"
            assert "Content-Disposition" in response.headers
            mock_generate.assert_called_once()

    def test_generate_pdf_individual(self, client, mock_templates_exist):
        """個人申請者でPDF生成成功"""
        with patch("app.main.generate_full_application_pdf") as mock_generate:
            mock_generate.return_value = b"%PDF-1.4 test pdf content"
            response = client.post("/api/generate-pdf", json=VALID_INDIVIDUAL_DATA)

            assert response.status_code == 200
            call_args = mock_generate.call_args[0][0]
            assert call_args.applicantType == "individual"

    def test_generate_pdf_corporation(self, client, mock_templates_exist):
        """法人申請者でPDF生成成功"""
        with patch("app.main.generate_full_application_pdf") as mock_generate:
            mock_generate.return_value = b"%PDF-1.4 test pdf content"
            response = client.post("/api/generate-pdf", json=VALID_CORPORATION_DATA)

            assert response.status_code == 200
            call_args = mock_generate.call_args[0][0]
            assert call_args.applicantType == "corporation"
            assert call_args.corporationType == "kabushiki"
            assert call_args.corporationName == "株式会社テスト"

    def test_generate_pdf_with_website(self, client, mock_templates_exist):
        """ホームページありでPDF生成成功"""
        with patch("app.main.generate_full_application_pdf") as mock_generate:
            mock_generate.return_value = b"%PDF-1.4 test pdf content"
            response = client.post("/api/generate-pdf", json=VALID_DATA_WITH_WEBSITE)

            assert response.status_code == 200
            call_args = mock_generate.call_args[0][0]
            assert call_args.hasWebsite is True
            assert call_args.websiteUrl == "https://example.com"

    def test_generate_pdf_without_website(self, client, mock_templates_exist):
        """ホームページなしでPDF生成成功"""
        with patch("app.main.generate_full_application_pdf") as mock_generate:
            mock_generate.return_value = b"%PDF-1.4 test pdf content"
            response = client.post("/api/generate-pdf", json=VALID_DATA_WITHOUT_WEBSITE)

            assert response.status_code == 200
            call_args = mock_generate.call_args[0][0]
            assert call_args.hasWebsite is False

    def test_generate_pdf_different_manager(self, client, mock_templates_exist):
        """管理者が申請者と異なる場合"""
        with patch("app.main.generate_full_application_pdf") as mock_generate:
            mock_generate.return_value = b"%PDF-1.4 test pdf content"
            response = client.post("/api/generate-pdf", json=VALID_DATA_DIFFERENT_MANAGER)

            assert response.status_code == 200
            call_args = mock_generate.call_args[0][0]
            assert call_args.managerSameAsApplicant is False
            assert call_args.managerLastNameKana == "スズキ"
            assert call_args.managerLastNameKanji == "鈴木"

    def test_generate_pdf_different_office_address(self, client, mock_templates_exist):
        """営業所住所が申請者住所と異なる場合"""
        with patch("app.main.generate_full_application_pdf") as mock_generate:
            mock_generate.return_value = b"%PDF-1.4 test pdf content"
            response = client.post("/api/generate-pdf", json=VALID_DATA_DIFFERENT_OFFICE)

            assert response.status_code == 200
            call_args = mock_generate.call_args[0][0]
            assert call_args.officeSameAsAddress is False
            assert call_args.officePrefecture == "東京都"
            assert call_args.officeCity == "渋谷区神宮前"

    def test_generate_pdf_missing_required_field(self, client):
        """必須フィールド欠落で422エラー"""
        invalid_data = {
            "applicantType": "individual",
            # lastNameKana is missing
            "lastNameKanji": "山田",
        }

        response = client.post("/api/generate-pdf", json=invalid_data)

        assert response.status_code == 422

    def test_generate_pdf_invalid_data(self, client):
        """不正なデータ形式で422エラー"""
        invalid_data = {
            "applicantType": 123,  # should be string
            "lastNameKana": "ヤマダ",
            "lastNameKanji": "山田",
        }

        response = client.post("/api/generate-pdf", json=invalid_data)

        assert response.status_code == 422
