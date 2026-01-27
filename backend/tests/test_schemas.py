"""Pydanticスキーマのテスト"""

import pytest
from pydantic import ValidationError

from app.schemas import FormData, CareerEntry


class TestCareerEntry:
    """CareerEntryスキーマのテスト"""

    def test_career_entry_valid(self):
        """正常なデータでCareerEntry作成成功"""
        entry = CareerEntry(
            year="2020",
            month="4",
            content="株式会社テスト 入社"
        )
        assert entry.year == "2020"
        assert entry.month == "4"
        assert entry.content == "株式会社テスト 入社"


class TestFormData:
    """FormDataスキーマのテスト"""

    def test_form_data_valid(self):
        """正常なデータでFormData作成成功"""
        data = FormData(
            applicantType="individual",
            lastNameKanji="山田",
            firstNameKanji="太郎",
            lastNameKana="ヤマダ",
            firstNameKana="タロウ",
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
            submissionPrefecture="東京都",
        )

        assert data.applicantType == "individual"
        assert data.lastNameKana == "ヤマダ"
        assert data.lastNameKanji == "山田"
        assert data.birthEra == "heisei"
        assert data.prefecture == "東京都"
        assert data.officeSameAsAddress is True
        assert data.managerSameAsApplicant is True
        assert data.hasWebsite is False

    def test_form_data_minimal(self):
        """最小限の必須フィールドで作成成功"""
        data = FormData(
            applicantType="individual",
            lastNameKanji="テスト",
            firstNameKanji="太郎",
            lastNameKana="テスト",
            firstNameKana="タロウ",
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
            submissionPrefecture="東京都",
        )

        assert data.applicantType == "individual"
        # デフォルト値のチェック
        assert data.officeSameAsAddress is True
        assert data.managerSameAsApplicant is True
        assert data.hasWebsite is False

    def test_form_data_missing_required(self):
        """必須フィールド欠落でValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            FormData(
                applicantType="individual",
                # lastNameKana is missing
                lastNameKanji="山田",
                firstNameKanji="太郎",
                firstNameKana="タロウ",
                birthEra="heisei",
                birthYear="5",
                birthMonth="3",
                birthDay="15",
            )

        errors = exc_info.value.errors()
        field_names = [e["loc"][0] for e in errors]
        assert "lastNameKana" in field_names

    def test_form_data_optional_fields(self):
        """オプションフィールドがNone許容"""
        data = FormData(
            applicantType="individual",
            corporationType=None,  # optional
            corporationName=None,  # optional
            lastNameKanji="テスト",
            firstNameKanji="太郎",
            lastNameKana="テスト",
            firstNameKana="タロウ",
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
            websiteUrl=None,  # optional
            submissionPrefecture="東京都",
        )

        assert data.corporationType is None
        assert data.corporationName is None
        assert data.postalCode is None
        assert data.websiteUrl is None

    def test_form_data_corporation(self):
        """法人データの作成成功"""
        data = FormData(
            applicantType="corporation",
            corporationType="kabushiki",
            corporationName="株式会社テスト",
            lastNameKanji="山田",
            firstNameKanji="太郎",
            lastNameKana="ヤマダ",
            firstNameKana="タロウ",
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
            submissionPrefecture="東京都",
        )

        assert data.applicantType == "corporation"
        assert data.corporationType == "kabushiki"
        assert data.corporationName == "株式会社テスト"

    def test_form_data_with_website(self):
        """ホームページありのデータ作成成功"""
        data = FormData(
            applicantType="individual",
            lastNameKanji="テスト",
            firstNameKanji="太郎",
            lastNameKana="テスト",
            firstNameKana="タロウ",
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
            submissionPrefecture="東京都",
        )

        assert data.hasWebsite is True
        assert data.websiteUrl == "https://example.com"

    def test_form_data_different_manager(self):
        """管理者が申請者と異なる場合のデータ作成成功"""
        data = FormData(
            applicantType="individual",
            lastNameKanji="山田",
            firstNameKanji="太郎",
            lastNameKana="ヤマダ",
            firstNameKana="タロウ",
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
            managerLastNameKanji="鈴木",
            managerFirstNameKanji="花子",
            managerLastNameKana="スズキ",
            managerFirstNameKana="ハナコ",
            managerBirthEra="showa",
            managerBirthYear="55",
            managerBirthMonth="7",
            managerBirthDay="20",
            managerPrefecture="神奈川県",
            managerCity="横浜市",
            managerStreet="4-5-6",
            managerPhone="045-123-4567",
            submissionPrefecture="東京都",
        )

        assert data.managerSameAsApplicant is False
        assert data.managerLastNameKana == "スズキ"
        assert data.managerLastNameKanji == "鈴木"

    def test_form_data_with_career_history(self):
        """職歴付きのデータ作成成功"""
        career_entries = [
            CareerEntry(year="2020", month="4", content="株式会社テスト 入社"),
            CareerEntry(year="2023", month="3", content="同社 退職"),
        ]
        data = FormData(
            applicantType="individual",
            lastNameKanji="テスト",
            firstNameKanji="太郎",
            lastNameKana="テスト",
            firstNameKana="タロウ",
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
            submissionPrefecture="東京都",
            careerHistory=career_entries,
        )

        assert len(data.careerHistory) == 2
        assert data.careerHistory[0].content == "株式会社テスト 入社"
