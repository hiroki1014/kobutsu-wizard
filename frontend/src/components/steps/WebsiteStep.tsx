import { Input, RadioGroup } from '../ui';
import type { FormData } from '../../types/form';

interface WebsiteStepProps {
  formData: FormData;
  updateField: (field: keyof FormData, value: string | boolean) => void;
}

export function WebsiteStep({ formData, updateField }: WebsiteStepProps) {
  return (
    <div>
      <h2 className="text-xl font-bold mb-6">ホームページ</h2>

      <RadioGroup
        label="ホームページを用いて古物の取引を行いますか？"
        name="hasWebsite"
        options={[
          { value: 'yes', label: '用いる' },
          { value: 'no', label: '用いない' },
        ]}
        value={formData.hasWebsite ? 'yes' : 'no'}
        onChange={(v) => updateField('hasWebsite', v === 'yes')}
      />

      {formData.hasWebsite && (
        <div className="border-l-4 border-blue-500 pl-4 mt-4">
          <Input
            label="URL"
            required
            placeholder="https://example.com"
            value={formData.websiteUrl}
            onChange={(e) => updateField('websiteUrl', e.target.value)}
            help="メルカリ等のプラットフォームのURLでも可"
          />
        </div>
      )}
    </div>
  );
}
