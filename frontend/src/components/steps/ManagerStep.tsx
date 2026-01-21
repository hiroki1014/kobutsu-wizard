import { useCallback } from 'react';
import { Input, Select, Checkbox } from '../ui';
import { BirthDateInput } from '../BirthDateInput';
import { PREFECTURES } from '../../lib/constants';
import type { FormData } from '../../types/form';
import { Oaza } from 'jp-zipcode-lookup';

interface ManagerStepProps {
  formData: FormData;
  updateField: (field: keyof FormData, value: string | boolean) => void;
}

export function ManagerStep({ formData, updateField }: ManagerStepProps) {
  const handlePostalCodeChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const value = e.target.value;
      updateField('managerPostalCode', value);

      const cleaned = value.replace(/-/g, '');
      if (cleaned.length === 7 && /^\d{7}$/.test(cleaned)) {
        try {
          const results = Oaza.byZipcode(cleaned);
          if (results && results.length > 0) {
            const result = results[0];
            updateField('managerPrefecture', result.pref?.name || '');
            updateField('managerCity', (result.city?.name || '') + (result.name || ''));
          }
        } catch {
          // 住所が見つからない場合は何もしない
        }
      }
    },
    [updateField]
  );

  return (
    <div>
      <h2 className="text-xl font-bold mb-6">管理者情報</h2>

      <Checkbox
        label="管理者は申請者と同じ"
        checked={formData.managerSameAsApplicant}
        onChange={(v) => updateField('managerSameAsApplicant', v)}
      />

      {!formData.managerSameAsApplicant && (
        <div className="border-l-4 border-blue-500 pl-4 mt-4">
          {/* 氏名（漢字）- 姓・名を分離 */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              氏名（漢字） <span className="text-red-500">*</span>
            </label>
            <div className="grid grid-cols-2 gap-3">
              <Input
                placeholder="鈴木"
                value={formData.managerLastNameKanji}
                onChange={(e) => updateField('managerLastNameKanji', e.target.value)}
              />
              <Input
                placeholder="花子"
                value={formData.managerFirstNameKanji}
                onChange={(e) => updateField('managerFirstNameKanji', e.target.value)}
              />
            </div>
            <div className="grid grid-cols-2 gap-3 mt-1">
              <span className="text-xs text-gray-500 text-center">姓</span>
              <span className="text-xs text-gray-500 text-center">名</span>
            </div>
          </div>

          {/* 氏名（フリガナ）- 姓・名を分離 */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              氏名（フリガナ） <span className="text-red-500">*</span>
            </label>
            <div className="grid grid-cols-2 gap-3">
              <Input
                placeholder="スズキ"
                value={formData.managerLastNameKana}
                onChange={(e) => updateField('managerLastNameKana', e.target.value)}
              />
              <Input
                placeholder="ハナコ"
                value={formData.managerFirstNameKana}
                onChange={(e) => updateField('managerFirstNameKana', e.target.value)}
              />
            </div>
            <div className="grid grid-cols-2 gap-3 mt-1">
              <span className="text-xs text-gray-500 text-center">セイ</span>
              <span className="text-xs text-gray-500 text-center">メイ</span>
            </div>
            <p className="mt-1 text-xs text-gray-500">全角カタカナで入力</p>
          </div>

          <div className="mt-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              生年月日 <span className="text-red-500">*</span>
            </label>
            <BirthDateInput prefix="managerBirth" formData={formData} updateField={updateField} />
          </div>

          <div className="mt-4">
            <Input
              label="郵便番号"
              placeholder="123-4567"
              value={formData.managerPostalCode}
              onChange={handlePostalCodeChange}
              help="入力すると住所が自動入力されます"
            />
            <Select
              label="都道府県"
              required
              options={PREFECTURES}
              value={formData.managerPrefecture}
              onChange={(v) => updateField('managerPrefecture', v)}
            />
            <Input
              label="市区町村"
              required
              placeholder="○○市△△区"
              value={formData.managerCity}
              onChange={(e) => updateField('managerCity', e.target.value)}
            />
            <Input
              label="番地・建物名"
              required
              placeholder="1-2-3 ○○ビル101"
              value={formData.managerStreet}
              onChange={(e) => updateField('managerStreet', e.target.value)}
            />
            <Input
              label="電話番号"
              required
              placeholder="09012345678"
              value={formData.managerPhone}
              onChange={(e) => updateField('managerPhone', e.target.value)}
            />
          </div>
        </div>
      )}
    </div>
  );
}
