from pydantic import BaseModel
from typing import Optional


class FormData(BaseModel):
    """古物商許可申請書のフォームデータ"""

    # 申請者種別
    applicantType: str  # 'individual' or 'corporation'
    corporationType: Optional[str] = None  # 法人種別

    # 申請者情報（姓・名を分離）
    lastNameKanji: str
    firstNameKanji: str
    lastNameKana: str
    firstNameKana: str
    corporationName: Optional[str] = None
    birthEra: str  # 'showa', 'heisei', 'reiwa'
    birthYear: str
    birthMonth: str
    birthDay: str

    # 住所
    postalCode: Optional[str] = None
    prefecture: str
    city: str
    street: str
    phone: str

    # 営業所情報
    officeSameAsAddress: bool = True
    officeNameKanji: str
    officeNameKana: str
    officePostalCode: Optional[str] = None
    officePrefecture: Optional[str] = None
    officeCity: Optional[str] = None
    officeStreet: Optional[str] = None
    officePhone: Optional[str] = None

    # 管理者情報（姓・名を分離）
    managerSameAsApplicant: bool = True
    managerLastNameKanji: Optional[str] = None
    managerFirstNameKanji: Optional[str] = None
    managerLastNameKana: Optional[str] = None
    managerFirstNameKana: Optional[str] = None
    managerBirthEra: Optional[str] = None
    managerBirthYear: Optional[str] = None
    managerBirthMonth: Optional[str] = None
    managerBirthDay: Optional[str] = None
    managerPostalCode: Optional[str] = None
    managerPrefecture: Optional[str] = None
    managerCity: Optional[str] = None
    managerStreet: Optional[str] = None
    managerPhone: Optional[str] = None

    # 代表者等（法人の場合）
    representativeType: Optional[str] = None  # '1'=代表者, '2'=役員, '3'=法定代理人
    representativeLastNameKanji: Optional[str] = None
    representativeFirstNameKanji: Optional[str] = None
    representativeLastNameKana: Optional[str] = None
    representativeFirstNameKana: Optional[str] = None
    representativeBirthEra: Optional[str] = None
    representativeBirthYear: Optional[str] = None
    representativeBirthMonth: Optional[str] = None
    representativeBirthDay: Optional[str] = None
    representativePostalCode: Optional[str] = None
    representativePrefecture: Optional[str] = None
    representativeCity: Optional[str] = None
    representativeStreet: Optional[str] = None
    representativePhone: Optional[str] = None

    # ホームページ
    hasWebsite: bool = False
    websiteUrl: Optional[str] = None

    # 申請情報（申請日は削除）
    submissionPrefecture: str

    @property
    def nameKanji(self) -> str:
        """姓名を結合した漢字氏名"""
        return f"{self.lastNameKanji} {self.firstNameKanji}"

    @property
    def nameKana(self) -> str:
        """姓名を結合したフリガナ氏名"""
        return f"{self.lastNameKana} {self.firstNameKana}"

    @property
    def managerNameKanji(self) -> Optional[str]:
        """管理者の姓名を結合した漢字氏名"""
        if self.managerLastNameKanji and self.managerFirstNameKanji:
            return f"{self.managerLastNameKanji} {self.managerFirstNameKanji}"
        return None

    @property
    def managerNameKana(self) -> Optional[str]:
        """管理者の姓名を結合したフリガナ氏名"""
        if self.managerLastNameKana and self.managerFirstNameKana:
            return f"{self.managerLastNameKana} {self.managerFirstNameKana}"
        return None

    @property
    def representativeNameKanji(self) -> Optional[str]:
        """代表者の姓名を結合した漢字氏名"""
        if self.representativeLastNameKanji and self.representativeFirstNameKanji:
            return f"{self.representativeLastNameKanji} {self.representativeFirstNameKanji}"
        return None

    @property
    def representativeNameKana(self) -> Optional[str]:
        """代表者の姓名を結合したフリガナ氏名"""
        if self.representativeLastNameKana and self.representativeFirstNameKana:
            return f"{self.representativeLastNameKana} {self.representativeFirstNameKana}"
        return None
