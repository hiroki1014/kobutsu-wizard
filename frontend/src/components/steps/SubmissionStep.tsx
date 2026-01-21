import { useEffect } from 'react';
import { Select } from '../ui';
import { PREFECTURES } from '../../lib/constants';
import type { FormData } from '../../types/form';

interface SubmissionStepProps {
  formData: FormData;
  updateField: (field: keyof FormData, value: string) => void;
}

export function SubmissionStep({ formData, updateField }: SubmissionStepProps) {
  // 住所の都道府県が設定されていて、提出先が未設定なら自動設定
  useEffect(() => {
    if (formData.prefecture && !formData.submissionPrefecture) {
      updateField('submissionPrefecture', formData.prefecture);
    }
  }, [formData.prefecture, formData.submissionPrefecture, updateField]);

  return (
    <div>
      <h2 className="text-xl font-bold mb-6">申請情報</h2>

      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
        <p className="text-sm text-yellow-800">
          <strong>申請日</strong>は申請書提出時に記入してください。
        </p>
      </div>

      <Select
        label="提出先（公安委員会）"
        required
        options={PREFECTURES}
        value={formData.submissionPrefecture}
        onChange={(v) => updateField('submissionPrefecture', v)}
        help="通常は住所の都道府県と同じです"
      />
    </div>
  );
}
