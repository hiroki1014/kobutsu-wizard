/**
 * ステップコンポーネントのテスト
 */
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import {
  ApplicantStep,
  AddressStep,
  OfficeStep,
  ManagerStep,
  WebsiteStep,
  ConfirmStep,
} from '../components/steps';
import { initialFormData, FormData } from '../types/form';

describe('ApplicantStep', () => {
  const mockUpdateField = vi.fn();

  it('test_ApplicantStep_renders: 申請者情報フォームが表示される', () => {
    render(
      <ApplicantStep formData={initialFormData} updateField={mockUpdateField} />
    );

    expect(screen.getByText('申請者情報')).toBeInTheDocument();
    expect(screen.getByText('申請者の種別')).toBeInTheDocument();
    expect(screen.getByText('氏名（フリガナ）')).toBeInTheDocument();
    expect(screen.getByText('氏名（漢字）')).toBeInTheDocument();
  });

  it('test_ApplicantStep_individual_selected: 個人選択時に法人フィールド非表示', () => {
    const formData: FormData = {
      ...initialFormData,
      applicantType: 'individual',
    };

    render(<ApplicantStep formData={formData} updateField={mockUpdateField} />);

    // 法人フィールドが表示されていないことを確認
    expect(screen.queryByText('法人種別')).not.toBeInTheDocument();
    expect(screen.queryByText('法人名')).not.toBeInTheDocument();
  });

  it('test_ApplicantStep_corporation_selected: 法人選択時に法人フィールド表示', () => {
    const formData: FormData = {
      ...initialFormData,
      applicantType: 'corporation',
    };

    render(<ApplicantStep formData={formData} updateField={mockUpdateField} />);

    // 法人フィールドが表示されていることを確認
    expect(screen.getByText('法人種別')).toBeInTheDocument();
    expect(screen.getByText('法人名')).toBeInTheDocument();
  });
});

describe('AddressStep', () => {
  const mockUpdateField = vi.fn();

  it('test_AddressStep_renders: 住所フォームが表示される', () => {
    render(
      <AddressStep formData={initialFormData} updateField={mockUpdateField} />
    );

    expect(screen.getByText('住所')).toBeInTheDocument();
    expect(screen.getByText('郵便番号')).toBeInTheDocument();
    expect(screen.getByText('都道府県')).toBeInTheDocument();
    expect(screen.getByText('市区町村')).toBeInTheDocument();
    expect(screen.getByText('番地・建物名')).toBeInTheDocument();
    expect(screen.getByText('電話番号')).toBeInTheDocument();
  });
});

describe('OfficeStep', () => {
  const mockUpdateField = vi.fn();

  it('test_OfficeStep_same_address_checked: "住所と同じ" チェック時に住所入力非表示', () => {
    const formData: FormData = {
      ...initialFormData,
      officeSameAsAddress: true,
    };

    render(<OfficeStep formData={formData} updateField={mockUpdateField} />);

    // 営業所住所の入力フィールドが表示されていないことを確認
    expect(screen.queryByText('営業所所在地')).not.toBeInTheDocument();
  });

  it('"住所と同じ" 未チェック時に営業所住所入力が表示される', () => {
    const formData: FormData = {
      ...initialFormData,
      officeSameAsAddress: false,
    };

    render(<OfficeStep formData={formData} updateField={mockUpdateField} />);

    // 営業所所在地セクションが表示されていることを確認
    expect(screen.getByText('営業所所在地')).toBeInTheDocument();
  });

  it('営業所名称フィールドが表示される', () => {
    render(
      <OfficeStep formData={initialFormData} updateField={mockUpdateField} />
    );

    expect(screen.getByText('営業所名称（フリガナ）')).toBeInTheDocument();
    expect(screen.getByText('営業所名称（漢字）')).toBeInTheDocument();
  });

  it('取扱品目が表示される', () => {
    render(
      <OfficeStep formData={initialFormData} updateField={mockUpdateField} />
    );

    expect(screen.getByText(/衣類、皮革・ゴム製品類/)).toBeInTheDocument();
  });
});

describe('ManagerStep', () => {
  const mockUpdateField = vi.fn();

  it('test_ManagerStep_same_as_applicant_checked: "申請者と同じ" チェック時に管理者入力非表示', () => {
    const formData: FormData = {
      ...initialFormData,
      managerSameAsApplicant: true,
    };

    render(<ManagerStep formData={formData} updateField={mockUpdateField} />);

    // 管理者情報の入力フィールドが表示されていないことを確認
    expect(screen.queryByPlaceholderText('ヤマダ ハナコ')).not.toBeInTheDocument();
  });

  it('"申請者と同じ" 未チェック時に管理者入力が表示される', () => {
    const formData: FormData = {
      ...initialFormData,
      managerSameAsApplicant: false,
    };

    render(<ManagerStep formData={formData} updateField={mockUpdateField} />);

    // 管理者情報の入力フィールドが表示されていることを確認
    expect(screen.getByPlaceholderText('ヤマダ ハナコ')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('山田 花子')).toBeInTheDocument();
  });

  it('管理者情報のタイトルが表示される', () => {
    render(
      <ManagerStep formData={initialFormData} updateField={mockUpdateField} />
    );

    expect(screen.getByText('管理者情報')).toBeInTheDocument();
  });
});

describe('WebsiteStep', () => {
  const mockUpdateField = vi.fn();

  it('test_WebsiteStep_no_website: "用いない" 選択時にURL入力非表示', () => {
    const formData: FormData = {
      ...initialFormData,
      hasWebsite: false,
    };

    render(<WebsiteStep formData={formData} updateField={mockUpdateField} />);

    // URL入力フィールドが表示されていないことを確認
    expect(screen.queryByPlaceholderText('https://example.com')).not.toBeInTheDocument();
  });

  it('test_WebsiteStep_has_website: "用いる" 選択時にURL入力表示', () => {
    const formData: FormData = {
      ...initialFormData,
      hasWebsite: true,
    };

    render(<WebsiteStep formData={formData} updateField={mockUpdateField} />);

    // URL入力フィールドが表示されていることを確認
    expect(screen.getByPlaceholderText('https://example.com')).toBeInTheDocument();
  });

  it('ホームページのタイトルが表示される', () => {
    render(
      <WebsiteStep formData={initialFormData} updateField={mockUpdateField} />
    );

    expect(screen.getByText('ホームページ')).toBeInTheDocument();
  });

  it('選択肢が表示される', () => {
    render(
      <WebsiteStep formData={initialFormData} updateField={mockUpdateField} />
    );

    expect(screen.getByText('用いる')).toBeInTheDocument();
    expect(screen.getByText('用いない')).toBeInTheDocument();
  });
});

describe('ConfirmStep', () => {
  it('test_ConfirmStep_displays_data: 入力データが確認画面に表示される', () => {
    const formData: FormData = {
      ...initialFormData,
      applicantType: 'individual',
      nameKana: 'ヤマダ タロウ',
      nameKanji: '山田 太郎',
      birthEra: 'heisei',
      birthYear: '5',
      birthMonth: '3',
      birthDay: '15',
      prefecture: '東京都',
      city: '渋谷区',
      street: '1-2-3',
      phone: '03-1234-5678',
      officeNameKana: 'ヤマダショウテン',
      officeNameKanji: '山田商店',
      officeSameAsAddress: true,
      managerSameAsApplicant: true,
      hasWebsite: false,
      applicationYear: '7',
      applicationMonth: '1',
      applicationDay: '15',
      submissionPrefecture: '東京都',
    };

    render(<ConfirmStep formData={formData} />);

    // 確認画面のタイトル
    expect(screen.getByText('入力内容の確認')).toBeInTheDocument();

    // 申請者情報
    expect(screen.getByText('申請者情報')).toBeInTheDocument();
    expect(screen.getByText('個人')).toBeInTheDocument();
    expect(screen.getByText(/山田 太郎/)).toBeInTheDocument();
    expect(screen.getByText(/ヤマダ タロウ/)).toBeInTheDocument();

    // 住所
    expect(screen.getByText(/東京都渋谷区1-2-3/)).toBeInTheDocument();
    expect(screen.getByText(/03-1234-5678/)).toBeInTheDocument();

    // 営業所
    expect(screen.getByText('主たる営業所')).toBeInTheDocument();
    expect(screen.getByText(/山田商店/)).toBeInTheDocument();
    expect(screen.getByText('住所と同じ')).toBeInTheDocument();

    // 管理者
    expect(screen.getByText('管理者')).toBeInTheDocument();
    expect(screen.getByText('申請者と同じ')).toBeInTheDocument();

    // ホームページ
    expect(screen.getByText('用いない')).toBeInTheDocument();
  });

  it('法人の場合、法人情報が表示される', () => {
    const formData: FormData = {
      ...initialFormData,
      applicantType: 'corporation',
      corporationType: 'kabushiki',
      corporationName: '株式会社テスト',
      nameKana: 'ヤマダ タロウ',
      nameKanji: '山田 太郎',
    };

    render(<ConfirmStep formData={formData} />);

    expect(screen.getByText('法人')).toBeInTheDocument();
    expect(screen.getByText('株式会社')).toBeInTheDocument();
    expect(screen.getByText('株式会社テスト')).toBeInTheDocument();
  });

  it('ホームページありの場合、URLが表示される', () => {
    const formData: FormData = {
      ...initialFormData,
      hasWebsite: true,
      websiteUrl: 'https://example.com',
    };

    render(<ConfirmStep formData={formData} />);

    expect(screen.getByText(/用いる/)).toBeInTheDocument();
    expect(screen.getByText(/https:\/\/example.com/)).toBeInTheDocument();
  });
});
