import { Input, Button } from '../ui';
import type { FormData, CareerEntry } from '../../types/form';

interface CareerStepProps {
  formData: FormData;
  updateField: (field: keyof FormData, value: string | boolean | CareerEntry[]) => void;
}

export function CareerStep({ formData, updateField }: CareerStepProps) {
  const addCareerEntry = () => {
    if (formData.careerHistory.length >= 6) return;
    const newHistory = [...formData.careerHistory, { year: '', month: '', content: '' }];
    updateField('careerHistory', newHistory);
  };

  const removeCareerEntry = (index: number) => {
    const newHistory = formData.careerHistory.filter((_, i) => i !== index);
    updateField('careerHistory', newHistory);
  };

  const updateCareerEntry = (index: number, field: keyof CareerEntry, value: string) => {
    const newHistory = formData.careerHistory.map((entry, i) => {
      if (i === index) {
        return { ...entry, [field]: value };
      }
      return entry;
    });
    updateField('careerHistory', newHistory);
  };

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">職歴（申請者）</h2>
      <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-4">
        <p className="text-yellow-800 font-medium">
          最近5年間の職歴を入力してください。学生の場合は学歴も可。最大6件まで入力できます。
        </p>
      </div>

      <div className="space-y-4">
        {formData.careerHistory.map((entry, index) => (
          <div key={index} className="border rounded-lg p-4 bg-gray-50">
            <div className="flex justify-between items-center mb-3">
              <span className="text-sm font-medium text-gray-700">職歴 {index + 1}</span>
              <button
                type="button"
                onClick={() => removeCareerEntry(index)}
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
                  onChange={(e) => updateCareerEntry(index, 'year', e.target.value)}
                />
                <span className="text-xs text-gray-500">年（西暦）</span>
              </div>
              <div className="col-span-2">
                <Input
                  placeholder="月"
                  value={entry.month}
                  onChange={(e) => updateCareerEntry(index, 'month', e.target.value)}
                />
                <span className="text-xs text-gray-500">月</span>
              </div>
              <div className="col-span-7">
                <Input
                  placeholder="入社・退職等の内容"
                  value={entry.content}
                  onChange={(e) => updateCareerEntry(index, 'content', e.target.value)}
                />
                <span className="text-xs text-gray-500">内容</span>
              </div>
            </div>
          </div>
        ))}

        {formData.careerHistory.length > 0 && formData.careerHistory.length < 6 && (
          <Button
            type="button"
            variant="secondary"
            onClick={addCareerEntry}
            className="w-full"
          >
            + 職歴を追加
          </Button>
        )}

        {formData.careerHistory.length === 0 && (
          <div className="text-center py-8 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
            <p className="text-gray-500 mb-4">職歴がまだ登録されていません</p>
            <Button
              type="button"
              variant="secondary"
              onClick={addCareerEntry}
            >
              + 職歴を追加
            </Button>
          </div>
        )}
      </div>

      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <h3 className="text-sm font-medium text-blue-800 mb-2">入力例</h3>
        <ul className="text-sm text-blue-700 space-y-1">
          <li>2019年 4月 株式会社○○商事 入社</li>
          <li>2022年 3月 同社 退職</li>
          <li>2022年 4月 個人事業開業</li>
          <li>（空欄） 現在に至る</li>
        </ul>
      </div>
    </div>
  );
}
