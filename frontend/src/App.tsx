import { useState } from 'react';
import { ProgressBar } from './components/ProgressBar';
import {
  ApplicantStep,
  AddressStep,
  CareerStep,
  OfficeStep,
  ManagerStep,
  WebsiteStep,
  SubmissionStep,
  ConfirmStep,
} from './components/steps';
import { Button } from './components/ui';
import { STEPS } from './lib/constants';
import { generatePdf } from './lib/api';
import type { FormData, CareerEntry } from './types/form';
import { initialFormData, testFormData } from './types/form';

export default function App() {
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState<FormData>(initialFormData);

  const loadTestData = () => {
    setFormData(testFormData);
    setCurrentStep(7); // 確認画面に移動
  };
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const updateField = (field: keyof FormData, value: string | boolean | CareerEntry[]) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const nextStep = () => {
    if (currentStep < STEPS.length - 1) {
      setCurrentStep((prev) => prev + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep((prev) => prev - 1);
    }
  };

  const handleDownload = async () => {
    setIsGenerating(true);
    setError(null);

    try {
      const blob = await generatePdf(formData);
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const fullName = `${formData.lastNameKanji}${formData.firstNameKanji}` || '申請者';
      a.download = `古物商許可申請書一式_${fullName}.pdf`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'PDF生成に失敗しました');
    } finally {
      setIsGenerating(false);
    }
  };

  const renderStep = () => {
    switch (currentStep) {
      case 0:
        return <ApplicantStep formData={formData} updateField={updateField} />;
      case 1:
        return <AddressStep formData={formData} updateField={updateField} />;
      case 2:
        return <CareerStep formData={formData} updateField={updateField} />;
      case 3:
        return <OfficeStep formData={formData} updateField={updateField} />;
      case 4:
        return <ManagerStep formData={formData} updateField={updateField} />;
      case 5:
        return <WebsiteStep formData={formData} updateField={updateField} />;
      case 6:
        return <SubmissionStep formData={formData} updateField={updateField} />;
      case 7:
        return <ConfirmStep formData={formData} />;
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-2xl mx-auto px-4 py-8">
        <header className="text-center mb-8">
          <h1 className="text-2xl font-bold text-gray-800 mb-2">
            古物商許可申請書 作成ツール
          </h1>
          <p className="text-gray-600 text-sm">
            質問に答えていくだけで申請書が完成します
          </p>
          {import.meta.env.DEV && (
            <button
              onClick={loadTestData}
              className="mt-2 text-xs text-blue-600 hover:text-blue-800 underline"
            >
              [DEV] テストデータを読み込む
            </button>
          )}
        </header>

        <div className="bg-white rounded-2xl shadow-lg p-6 md:p-8">
          <ProgressBar currentStep={currentStep} />

          <div className="min-h-[400px]">{renderStep()}</div>

          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
              {error}
            </div>
          )}

          <div className="flex justify-between mt-8 pt-6 border-t">
            <Button
              variant="secondary"
              onClick={prevStep}
              disabled={currentStep === 0}
              className={currentStep === 0 ? 'opacity-50 cursor-not-allowed' : ''}
            >
              <span className="mr-1">&larr;</span>
              戻る
            </Button>

            {currentStep < STEPS.length - 1 ? (
              <Button onClick={nextStep}>
                次へ
                <span className="ml-1">&rarr;</span>
              </Button>
            ) : (
              <Button
                variant="success"
                onClick={handleDownload}
                disabled={isGenerating}
              >
                {isGenerating ? '生成中...' : '申請書をダウンロード'}
              </Button>
            )}
          </div>
        </div>

        <footer className="text-center mt-6 text-xs text-gray-500">
          ※このツールで生成した申請書は、提出前に必ず内容を確認してください
        </footer>
      </div>
    </div>
  );
}
