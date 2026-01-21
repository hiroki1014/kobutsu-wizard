import { Input, Select, RadioGroup } from '../ui';
import { BirthDateInput } from '../BirthDateInput';
import { CORPORATION_TYPES } from '../../lib/constants';
import type { FormData } from '../../types/form';

interface ApplicantStepProps {
  formData: FormData;
  updateField: (field: keyof FormData, value: string | boolean) => void;
}

export function ApplicantStep({ formData, updateField }: ApplicantStepProps) {
  return (
    <div>
      <h2 className="text-xl font-bold mb-6">申請者情報</h2>

      <RadioGroup
        label="申請者の種別"
        name="applicantType"
        options={[
          { value: 'individual', label: '個人' },
          { value: 'corporation', label: '法人' },
        ]}
        value={formData.applicantType}
        onChange={(v) => updateField('applicantType', v)}
      />

      {formData.applicantType === 'corporation' && (
        <>
          <Select
            label="法人種別"
            required
            options={CORPORATION_TYPES}
            value={formData.corporationType}
            onChange={(v) => updateField('corporationType', v)}
          />
          <Input
            label="法人名"
            required
            placeholder="株式会社○○"
            value={formData.corporationName}
            onChange={(e) => updateField('corporationName', e.target.value)}
          />
        </>
      )}

      {/* 氏名（漢字）- 姓・名を分離 */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          氏名（漢字） <span className="text-red-500">*</span>
        </label>
        <div className="grid grid-cols-2 gap-3">
          <Input
            placeholder="山田"
            value={formData.lastNameKanji}
            onChange={(e) => updateField('lastNameKanji', e.target.value)}
          />
          <Input
            placeholder="太郎"
            value={formData.firstNameKanji}
            onChange={(e) => updateField('firstNameKanji', e.target.value)}
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
            placeholder="ヤマダ"
            value={formData.lastNameKana}
            onChange={(e) => updateField('lastNameKana', e.target.value)}
          />
          <Input
            placeholder="タロウ"
            value={formData.firstNameKana}
            onChange={(e) => updateField('firstNameKana', e.target.value)}
          />
        </div>
        <div className="grid grid-cols-2 gap-3 mt-1">
          <span className="text-xs text-gray-500 text-center">セイ</span>
          <span className="text-xs text-gray-500 text-center">メイ</span>
        </div>
        <p className="mt-1 text-xs text-gray-500">全角カタカナで入力</p>
      </div>

      <div className="mt-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          生年月日 <span className="text-red-500">*</span>
        </label>
        <BirthDateInput prefix="birth" formData={formData} updateField={updateField} />
      </div>
    </div>
  );
}
