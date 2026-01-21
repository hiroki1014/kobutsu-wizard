"""Pydanticスキーマのテスト"""

import pytest
from pydantic import ValidationError

from app.schemas import FormData


class TestFormData:
    """FormDataスキーマのテスト"""

    def test_form_data_valid(self):
        """正常なデータでFormData作成成功"""
        data = FormData(
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

        assert data.applicantType == "individual"
        assert data.nameKana == "ヤマダ タロウ"
        assert data.nameKanji == "山田 太郎"
        assert data.birthEra == "heisei"
        assert data.prefecture == "東京都"
        assert data.officeSameAsAddress is True
        assert data.managerSameAsApplicant is True
        assert data.hasWebsite is False

    def test_form_data_minimal(self):
        """最小限の必須フィールドで作成成功"""
        data = FormData(
            applicantType="individual",
            nameKana="テスト",
            nameKanji="テスト",
            birthEra="reiwa",
            birthYear="1",
            birthMonth="1",
            birthDay="1",
            prefecture="東京都",
            city="千代田区",
            street="1-1",
            phone="0312345678",
            officeNameKana="テスト",
            officeNameKanji="テスト",
            applicationYear="7",
            applicationMonth="1",
            applicationDay="1",
            submissionPrefecture="東京都",
        )

        assert data.applicantType == "individual"
        # デフォルト値のチェック
        assert data.officeSameAsAddress is True
        assert data.managerSameAsApplicant is True
        assert data.hasWebsite is False
        assert data.applicationEra == "reiwa"

    def test_form_data_missing_required(self):
        """必須フィールド欠落でValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            FormData(
                applicantType="individual",
                # nameKana is missing
                nameKanji="山田 太郎",
                birthEra="heisei",
                birthYear="5",
                birthMonth="3",
                birthDay="15",
            )

        errors = exc_info.value.errors()
        field_names = [e["loc"][0] for e in errors]
        assert "nameKana" in field_names

    def test_form_data_optional_fields(self):
        """オプションフィールドがNone許容"""
        data = FormData(
            applicantType="individual",
            corporationType=None,  # optional
            corporationName=None,  # optional
            nameKana="テスト",
            nameKanji="テスト",
            birthEra="reiwa",
            birthYear="1",
            birthMonth="1",
            birthDay="1",
            postalCode=None,  # optional
            prefecture="東京都",
            city="千代田区",
            street="1-1",
            phone="0312345678",
            officeNameKana="テスト",
            officeNameKanji="テスト",
            officePostalCode=None,  # optional
            officePrefecture=None,  # optional
            officeCity=None,  # optional
            officeStreet=None,  # optional
            officePhone=None,  # optional
            managerNameKana=None,  # optional
            managerNameKanji=None,  # optional
            managerBirthEra=None,  # optional
            managerBirthYear=None,  # optional
            managerBirthMonth=None,  # optional
            managerBirthDay=None,  # optional
            managerPostalCode=None,  # optional
            managerPrefecture=None,  # optional
            managerCity=None,  # optional
            managerStreet=None,  # optional
            managerPhone=None,  # optional
            websiteUrl=None,  # optional
            applicationYear="7",
            applicationMonth="1",
            applicationDay="1",
            submissionPrefecture="東京都",
        )

        assert data.corporationType is None
        assert data.corporationName is None
        assert data.postalCode is None
        assert data.websiteUrl is None
        assert data.managerNameKana is None

    def test_form_data_corporation(self):
        """法人データの作成成功"""
        data = FormData(
            applicantType="corporation",
            corporationType="kabushiki",
            corporationName="株式会社テスト",
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
            officeNameKana="カブシキガイシャテスト",
            officeNameKanji="株式会社テスト",
            applicationYear="7",
            applicationMonth="1",
            applicationDay="1",
            submissionPrefecture="東京都",
        )

        assert data.applicantType == "corporation"
        assert data.corporationType == "kabushiki"
        assert data.corporationName == "株式会社テスト"

    def test_form_data_with_website(self):
        """ホームページありのデータ作成成功"""
        data = FormData(
            applicantType="individual",
            nameKana="テスト",
            nameKanji="テスト",
            birthEra="reiwa",
            birthYear="1",
            birthMonth="1",
            birthDay="1",
            prefecture="東京都",
            city="千代田区",
            street="1-1",
            phone="0312345678",
            officeNameKana="テスト",
            officeNameKanji="テスト",
            hasWebsite=True,
            websiteUrl="https://example.com",
            applicationYear="7",
            applicationMonth="1",
            applicationDay="1",
            submissionPrefecture="東京都",
        )

        assert data.hasWebsite is True
        assert data.websiteUrl == "https://example.com"

    def test_form_data_different_manager(self):
        """管理者が申請者と異なる場合のデータ作成成功"""
        data = FormData(
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
            officeNameKana="ヤマダショウテン",
            officeNameKanji="山田商店",
            managerSameAsApplicant=False,
            managerNameKana="スズキ ハナコ",
            managerNameKanji="鈴木 花子",
            managerBirthEra="showa",
            managerBirthYear="55",
            managerBirthMonth="7",
            managerBirthDay="20",
            managerPrefecture="神奈川県",
            managerCity="横浜市",
            managerStreet="4-5-6",
            managerPhone="045-123-4567",
            applicationYear="7",
            applicationMonth="1",
            applicationDay="1",
            submissionPrefecture="東京都",
        )

        assert data.managerSameAsApplicant is False
        assert data.managerNameKana == "スズキ ハナコ"
        assert data.managerNameKanji == "鈴木 花子"
