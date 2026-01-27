import { ERA_OPTIONS, CORPORATION_TYPES } from '../../lib/constants';
import type { FormData, CareerEntry } from '../../types/form';

interface ConfirmStepProps {
  formData: FormData;
}

export function ConfirmStep({ formData }: ConfirmStepProps) {
  const getEraLabel = (era: string) =>
    ERA_OPTIONS.find((e) => e.value === era)?.label || era;

  const getCorporationTypeLabel = (type: string) =>
    CORPORATION_TYPES.find((t) => t.value === type)?.label || type;

  const formatDate = (prefix: string) => {
    const era = formData[`${prefix}Era` as keyof FormData] as string;
    const year = formData[`${prefix}Year` as keyof FormData] as string;
    const month = formData[`${prefix}Month` as keyof FormData] as string;
    const day = formData[`${prefix}Day` as keyof FormData] as string;
    if (!year || !month || !day) return '未入力';
    return `${getEraLabel(era)}${year}年${month}月${day}日`;
  };

  const formatAddress = (prefix: string = '') => {
    const pref = formData[`${prefix}prefecture` as keyof FormData] || formData[`${prefix}Prefecture` as keyof FormData] || formData.prefecture;
    const city = formData[`${prefix}city` as keyof FormData] || formData[`${prefix}City` as keyof FormData] || formData.city;
    const street = formData[`${prefix}street` as keyof FormData] || formData[`${prefix}Street` as keyof FormData] || formData.street;
    return `${pref}${city}${street}`;
  };

  // 氏名を結合して表示
  const getFullName = (lastNameField: keyof FormData, firstNameField: keyof FormData): string => {
    const lastName = (formData[lastNameField] as string) || '';
    const firstName = (formData[firstNameField] as string) || '';
    return lastName && firstName ? `${lastName} ${firstName}` : lastName || firstName || '未入力';
  };

  // 職歴を表示用にフォーマット
  const formatCareerEntry = (entry: CareerEntry) => {
    const period = entry.year && entry.month ? `${entry.year}年${entry.month}月` : '';
    return period ? `${period} ${entry.content}` : entry.content;
  };

  return (
    <div>
      <h2 className="text-xl font-bold mb-6">入力内容の確認</h2>

      <div className="space-y-6">
        <section className="bg-gray-50 rounded-lg p-4">
          <h3 className="font-bold text-gray-800 mb-3 border-b pb-2">申請者情報</h3>
          <dl className="grid grid-cols-2 gap-2 text-sm">
            <dt className="text-gray-600">種別</dt>
            <dd>{formData.applicantType === 'individual' ? '個人' : '法人'}</dd>
            {formData.applicantType === 'corporation' && (
              <>
                <dt className="text-gray-600">法人種別</dt>
                <dd>{getCorporationTypeLabel(formData.corporationType)}</dd>
                <dt className="text-gray-600">法人名</dt>
                <dd>{formData.corporationName || '未入力'}</dd>
              </>
            )}
            <dt className="text-gray-600">氏名（漢字）</dt>
            <dd>{getFullName('lastNameKanji', 'firstNameKanji')}</dd>
            <dt className="text-gray-600">氏名（フリガナ）</dt>
            <dd>{getFullName('lastNameKana', 'firstNameKana')}</dd>
            <dt className="text-gray-600">生年月日</dt>
            <dd>{formatDate('birth')}</dd>
          </dl>
        </section>

        <section className="bg-gray-50 rounded-lg p-4">
          <h3 className="font-bold text-gray-800 mb-3 border-b pb-2">住所</h3>
          <dl className="grid grid-cols-2 gap-2 text-sm">
            <dt className="text-gray-600">住所</dt>
            <dd className="col-span-1">{formatAddress()}</dd>
            <dt className="text-gray-600">電話</dt>
            <dd>{formData.phone || '未入力'}</dd>
          </dl>
        </section>

        <section className="bg-gray-50 rounded-lg p-4">
          <h3 className="font-bold text-gray-800 mb-3 border-b pb-2">職歴（申請者）</h3>
          {formData.careerHistory.length > 0 ? (
            <ul className="text-sm space-y-1">
              {formData.careerHistory.map((entry, index) => (
                <li key={index}>{formatCareerEntry(entry)}</li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-gray-500">未入力</p>
          )}
        </section>

        <section className="bg-gray-50 rounded-lg p-4">
          <h3 className="font-bold text-gray-800 mb-3 border-b pb-2">主たる営業所</h3>
          <dl className="grid grid-cols-2 gap-2 text-sm">
            <dt className="text-gray-600">名称（漢字）</dt>
            <dd>{formData.officeNameKanji || '未入力'}</dd>
            <dt className="text-gray-600">名称（フリガナ）</dt>
            <dd>{formData.officeNameKana || '未入力'}</dd>
            <dt className="text-gray-600">所在地</dt>
            <dd>{formData.officeSameAsAddress ? '住所と同じ' : formatAddress('office')}</dd>
            <dt className="text-gray-600">取扱品目</dt>
            <dd>衣類、皮革・ゴム製品類</dd>
          </dl>
        </section>

        <section className="bg-gray-50 rounded-lg p-4">
          <h3 className="font-bold text-gray-800 mb-3 border-b pb-2">管理者</h3>
          {formData.managerSameAsApplicant ? (
            <p className="text-sm text-gray-600">申請者と同じ</p>
          ) : (
            <>
              <dl className="grid grid-cols-2 gap-2 text-sm">
                <dt className="text-gray-600">氏名（漢字）</dt>
                <dd>{getFullName('managerLastNameKanji', 'managerFirstNameKanji')}</dd>
                <dt className="text-gray-600">氏名（フリガナ）</dt>
                <dd>{getFullName('managerLastNameKana', 'managerFirstNameKana')}</dd>
                <dt className="text-gray-600">生年月日</dt>
                <dd>{formatDate('managerBirth')}</dd>
              </dl>
              <div className="mt-3 pt-3 border-t">
                <h4 className="text-sm font-medium text-gray-700 mb-2">職歴（管理者）</h4>
                {formData.managerCareerHistory.length > 0 ? (
                  <ul className="text-sm space-y-1">
                    {formData.managerCareerHistory.map((entry, index) => (
                      <li key={index}>{formatCareerEntry(entry)}</li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-sm text-gray-500">未入力</p>
                )}
              </div>
            </>
          )}
        </section>

        <section className="bg-gray-50 rounded-lg p-4">
          <h3 className="font-bold text-gray-800 mb-3 border-b pb-2">ホームページ</h3>
          <p className="text-sm">
            {formData.hasWebsite ? (
              <>用いる: {formData.websiteUrl || '未入力'}</>
            ) : (
              '用いない'
            )}
          </p>
        </section>

        <section className="bg-gray-50 rounded-lg p-4">
          <h3 className="font-bold text-gray-800 mb-3 border-b pb-2">申請情報</h3>
          <dl className="grid grid-cols-2 gap-2 text-sm">
            <dt className="text-gray-600">申請日</dt>
            <dd>（提出時に記入）</dd>
            <dt className="text-gray-600">提出先</dt>
            <dd>{formData.submissionPrefecture || '未入力'}公安委員会</dd>
          </dl>
        </section>

        <section className="bg-blue-50 rounded-lg p-4 border border-blue-200">
          <h3 className="font-bold text-blue-800 mb-3">ダウンロード内容</h3>
          <p className="text-sm text-blue-700 mb-2">
            以下の書類が1つのPDFファイルにまとめて出力されます：
          </p>
          <ul className="text-sm text-blue-700 space-y-1 list-disc list-inside">
            <li>古物商許可申請書 その1〜4（4ページ）</li>
            <li>誓約書（申請者用）</li>
            <li>略歴書（申請者用）</li>
            <li>誓約書（管理者用）</li>
            {!formData.managerSameAsApplicant && (
              <li>略歴書（管理者用）</li>
            )}
          </ul>
          <p className="text-xs text-blue-600 mt-3">
            ※署名日は空欄になっています。提出時に記入してください。
          </p>
        </section>

      </div>
    </div>
  );
}
