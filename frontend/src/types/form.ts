export interface CareerEntry {
  year: string;
  month: string;
  content: string;
}

export interface FormData {
  // 申請者種別
  applicantType: 'individual' | 'corporation';
  corporationType: string;

  // 申請者情報（姓・名を分離）
  lastNameKanji: string;
  firstNameKanji: string;
  lastNameKana: string;
  firstNameKana: string;
  corporationName: string;
  birthEra: string;
  birthYear: string;
  birthMonth: string;
  birthDay: string;

  // 住所
  postalCode: string;
  prefecture: string;
  city: string;
  street: string;
  phone: string;

  // 営業所情報
  officeSameAsAddress: boolean;
  officeNameKanji: string;
  officeNameKana: string;
  officePostalCode: string;
  officePrefecture: string;
  officeCity: string;
  officeStreet: string;
  officePhone: string;

  // 管理者情報（姓・名を分離）
  managerSameAsApplicant: boolean;
  managerLastNameKanji: string;
  managerFirstNameKanji: string;
  managerLastNameKana: string;
  managerFirstNameKana: string;
  managerBirthEra: string;
  managerBirthYear: string;
  managerBirthMonth: string;
  managerBirthDay: string;
  managerPostalCode: string;
  managerPrefecture: string;
  managerCity: string;
  managerStreet: string;
  managerPhone: string;

  // 代表者等（法人の場合）
  representativeType: string;  // '1'=代表者, '2'=役員, '3'=法定代理人
  representativeLastNameKanji: string;
  representativeFirstNameKanji: string;
  representativeLastNameKana: string;
  representativeFirstNameKana: string;
  representativeBirthEra: string;
  representativeBirthYear: string;
  representativeBirthMonth: string;
  representativeBirthDay: string;
  representativePostalCode: string;
  representativePrefecture: string;
  representativeCity: string;
  representativeStreet: string;
  representativePhone: string;

  // ホームページ
  hasWebsite: boolean;
  websiteUrl: string;

  // 申請情報（申請日は削除）
  submissionPrefecture: string;

  // 職歴（最近5年間、最大7エントリ）
  careerHistory: CareerEntry[];

  // 管理者の職歴（申請者と異なる場合）
  managerCareerHistory: CareerEntry[];
}

export const initialFormData: FormData = {
  applicantType: 'individual',
  corporationType: '',

  lastNameKanji: '',
  firstNameKanji: '',
  lastNameKana: '',
  firstNameKana: '',
  corporationName: '',
  birthEra: 'seireki',
  birthYear: '',
  birthMonth: '',
  birthDay: '',

  postalCode: '',
  prefecture: '',
  city: '',
  street: '',
  phone: '',

  officeSameAsAddress: true,
  officeNameKanji: '',
  officeNameKana: '',
  officePostalCode: '',
  officePrefecture: '',
  officeCity: '',
  officeStreet: '',
  officePhone: '',

  managerSameAsApplicant: true,
  managerLastNameKanji: '',
  managerFirstNameKanji: '',
  managerLastNameKana: '',
  managerFirstNameKana: '',
  managerBirthEra: 'seireki',
  managerBirthYear: '',
  managerBirthMonth: '',
  managerBirthDay: '',
  managerPostalCode: '',
  managerPrefecture: '',
  managerCity: '',
  managerStreet: '',
  managerPhone: '',

  representativeType: '',
  representativeLastNameKanji: '',
  representativeFirstNameKanji: '',
  representativeLastNameKana: '',
  representativeFirstNameKana: '',
  representativeBirthEra: 'seireki',
  representativeBirthYear: '',
  representativeBirthMonth: '',
  representativeBirthDay: '',
  representativePostalCode: '',
  representativePrefecture: '',
  representativeCity: '',
  representativeStreet: '',
  representativePhone: '',

  hasWebsite: false,
  websiteUrl: '',

  submissionPrefecture: '',

  careerHistory: [],
  managerCareerHistory: [],
};

// テスト用のサンプルデータ（全フィールド入力）
export const testFormData: FormData = {
  applicantType: 'individual',
  corporationType: '',

  lastNameKanji: '山田',
  firstNameKanji: '太郎',
  lastNameKana: 'ヤマダ',
  firstNameKana: 'タロウ',
  corporationName: '',
  birthEra: 'seireki',
  birthYear: '1980',
  birthMonth: '03',
  birthDay: '15',

  postalCode: '545-0053',
  prefecture: '大阪府',
  city: '大阪市阿倍野区松崎町',
  street: '2-3-37-412',
  phone: '090-4906-9060',

  officeSameAsAddress: false,
  officeNameKanji: '山田商店',
  officeNameKana: 'ヤマダショウテン',
  officePostalCode: '530-0001',
  officePrefecture: '大阪府',
  officeCity: '大阪市北区梅田',
  officeStreet: '1-2-3',
  officePhone: '06-1234-5678',

  managerSameAsApplicant: false,
  managerLastNameKanji: '鈴木',
  managerFirstNameKanji: '花子',
  managerLastNameKana: 'スズキ',
  managerFirstNameKana: 'ハナコ',
  managerBirthEra: 'seireki',
  managerBirthYear: '1990',
  managerBirthMonth: '07',
  managerBirthDay: '25',
  managerPostalCode: '550-0002',
  managerPrefecture: '大阪府',
  managerCity: '大阪市西区江戸堀',
  managerStreet: '4-5-6',
  managerPhone: '080-9876-5432',

  representativeType: '1',
  representativeLastNameKanji: '田中',
  representativeFirstNameKanji: '一郎',
  representativeLastNameKana: 'タナカ',
  representativeFirstNameKana: 'イチロウ',
  representativeBirthEra: 'seireki',
  representativeBirthYear: '1965',
  representativeBirthMonth: '11',
  representativeBirthDay: '03',
  representativePostalCode: '542-0081',
  representativePrefecture: '大阪府',
  representativeCity: '大阪市中央区南船場',
  representativeStreet: '7-8-9',
  representativePhone: '06-5555-1234',

  hasWebsite: true,
  websiteUrl: 'https://www.example-shop.co.jp',

  submissionPrefecture: '大阪府',

  careerHistory: [
    { year: '2015', month: '4', content: '○○大学 入学' },
    { year: '2019', month: '3', content: '同大学 卒業' },
    { year: '2019', month: '4', content: '株式会社○○商事 入社' },
    { year: '2021', month: '9', content: '同社 退職' },
    { year: '2021', month: '10', content: '△△株式会社 入社' },
    { year: '2023', month: '3', content: '同社 退職' },
  ],
  managerCareerHistory: [
    { year: '2010', month: '4', content: '□□専門学校 入学' },
    { year: '2012', month: '3', content: '同校 卒業' },
    { year: '2012', month: '4', content: '株式会社××商店 入社' },
    { year: '2016', month: '6', content: '同社 退職' },
    { year: '2016', month: '7', content: '◇◇株式会社 入社' },
    { year: '2020', month: '12', content: '同社 退職' },
  ],
};
