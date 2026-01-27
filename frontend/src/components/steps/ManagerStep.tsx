import { useCallback } from 'react';
import { Input, Select, Checkbox, Button } from '../ui';
import { BirthDateInput } from '../BirthDateInput';
import { PREFECTURES } from '../../lib/constants';
import type { FormData, CareerEntry } from '../../types/form';
import { Oaza } from 'jp-zipcode-lookup';

interface ManagerStepProps {
  formData: FormData;
  updateField: (field: keyof FormData, value: string | boolean | CareerEntry[]) => void;
}

export function ManagerStep({ formData, updateField }: ManagerStepProps) {
  // 管理者職歴の操作関数
  const addManagerCareerEntry = () => {
    if (formData.managerCareerHistory.length >= 6) return;
    const newHistory = [...formData.managerCareerHistory, { year: '', month: '', content: '' }];
    updateField('managerCareerHistory', newHistory);
  };

  const removeManagerCareerEntry = (index: number) => {
    const newHistory = formData.managerCareerHistory.filter((_, i) => i !== index);
    updateField('managerCareerHistory', newHistory);
  };

  const updateManagerCareerEntry = (index: number, field: keyof CareerEntry, value: string) => {
    const newHistory = formData.managerCareerHistory.map((entry, i) => {
      if (i === index) {
        return { ...entry, [field]: value };
      }
      return entry;
    });
    updateField('managerCareerHistory', newHistory);
  };

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

          {/* 管理者の職歴 */}
          <div className="mt-6 pt-4 border-t">
            <h3 className="text-lg font-medium mb-4">管理者の職歴</h3>
            <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-4">
              <p className="text-yellow-800 font-medium">
                最近5年間の職歴を入力してください。最大6件まで入力できます。
              </p>
            </div>

            <div className="space-y-4">
              {formData.managerCareerHistory.map((entry, index) => (
                <div key={index} className="border rounded-lg p-4 bg-white">
                  <div className="flex justify-between items-center mb-3">
                    <span className="text-sm font-medium text-gray-700">職歴 {index + 1}</span>
                    <button
                      type="button"
                      onClick={() => removeManagerCareerEntry(index)}
                      className="text-red-500 hover:text-red-700 text-sm"
                    >
                      削除
                    </button>
                  </div>

                  <div className="grid grid-cols-12 gap-2 mb-2">
                    <div className="col-span-3">
                      <Input
                        placeholder="年"
                        value={entry.year}
                        onChange={(e) => updateManagerCareerEntry(index, 'year', e.target.value)}
                      />
                      <span className="text-xs text-gray-500">年（西暦）</span>
                    </div>
                    <div className="col-span-2">
                      <Input
                        placeholder="月"
                        value={entry.month}
                        onChange={(e) => updateManagerCareerEntry(index, 'month', e.target.value)}
                      />
                      <span className="text-xs text-gray-500">月</span>
                    </div>
                    <div className="col-span-7">
                      <Input
                        placeholder="入社・退職等の内容"
                        value={entry.content}
                        onChange={(e) => updateManagerCareerEntry(index, 'content', e.target.value)}
                      />
                      <span className="text-xs text-gray-500">内容</span>
                    </div>
                  </div>
                </div>
              ))}

              {formData.managerCareerHistory.length > 0 && formData.managerCareerHistory.length < 6 && (
                <Button
                  type="button"
                  variant="secondary"
                  onClick={addManagerCareerEntry}
                  className="w-full"
                >
                  + 職歴を追加
                </Button>
              )}

              {formData.managerCareerHistory.length === 0 && (
                <div className="text-center py-8 bg-white rounded-lg border-2 border-dashed border-gray-300">
                  <p className="text-gray-500 mb-4">職歴がまだ登録されていません</p>
                  <Button
                    type="button"
                    variant="secondary"
                    onClick={addManagerCareerEntry}
                  >
                    + 職歴を追加
                  </Button>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
