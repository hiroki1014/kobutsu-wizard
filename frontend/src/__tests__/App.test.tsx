/**
 * メインアプリのテスト
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import App from '../App';

// APIモック
vi.mock('../lib/api', () => ({
  generatePdf: vi.fn(),
}));

describe('App', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('test_renders_title: タイトル "古物商許可申請書 作成ツール" が表示される', () => {
    render(<App />);
    expect(screen.getByText('古物商許可申請書 作成ツール')).toBeInTheDocument();
  });

  it('test_renders_first_step: 初期表示で "申請者情報" ステップが表示される', () => {
    render(<App />);
    // h2要素のタイトルを確認（プログレスバーのテキストと区別）
    expect(screen.getByRole('heading', { name: '申請者情報', level: 2 })).toBeInTheDocument();
  });

  it('test_next_button_advances_step: "次へ" ボタンで次のステップに進む', () => {
    render(<App />);

    // 初期状態で「申請者情報」のh2見出しが表示されていることを確認
    expect(screen.getByRole('heading', { name: '申請者情報', level: 2 })).toBeInTheDocument();

    // 「次へ」ボタンをクリック
    const nextButton = screen.getByRole('button', { name: /次へ/i });
    fireEvent.click(nextButton);

    // 「住所」ステップのh2見出しが表示されていることを確認
    expect(screen.getByRole('heading', { name: '住所', level: 2 })).toBeInTheDocument();
  });

  it('test_back_button_returns_step: "戻る" ボタンで前のステップに戻る', () => {
    render(<App />);

    // 「次へ」ボタンをクリックして次のステップに進む
    const nextButton = screen.getByRole('button', { name: /次へ/i });
    fireEvent.click(nextButton);

    // 「住所」ステップのh2見出しが表示されていることを確認
    expect(screen.getByRole('heading', { name: '住所', level: 2 })).toBeInTheDocument();

    // 「戻る」ボタンをクリック
    const backButton = screen.getByRole('button', { name: /戻る/i });
    fireEvent.click(backButton);

    // 「申請者情報」ステップのh2見出しに戻ったことを確認
    expect(screen.getByRole('heading', { name: '申請者情報', level: 2 })).toBeInTheDocument();
  });

  it('test_back_button_disabled_on_first_step: 最初のステップで "戻る" が無効', () => {
    render(<App />);

    const backButton = screen.getByRole('button', { name: /戻る/i });
    expect(backButton).toBeDisabled();
  });

  it('test_download_button_on_last_step: 最後のステップで "ダウンロード" ボタン表示', () => {
    render(<App />);

    // 最後のステップまで進む（7ステップ）
    const nextButton = screen.getByRole('button', { name: /次へ/i });
    for (let i = 0; i < 6; i++) {
      fireEvent.click(nextButton);
    }

    // 「申請書をダウンロード」ボタンが表示されていることを確認
    expect(screen.getByRole('button', { name: /申請書をダウンロード/i })).toBeInTheDocument();
  });

  it('test_progress_bar_updates: ステップ進行でプログレスバーが更新される', () => {
    render(<App />);

    // プログレスバーのステップ番号「1」がアクティブ（青色）であることを確認
    const stepOne = screen.getByText('1');
    expect(stepOne).toBeInTheDocument();
    expect(stepOne.className).toContain('bg-blue-600');

    // 「次へ」ボタンをクリック
    const nextButton = screen.getByRole('button', { name: /次へ/i });
    fireEvent.click(nextButton);

    // ステップ2がアクティブになっていることを確認
    const stepTwo = screen.getByText('2');
    expect(stepTwo).toBeInTheDocument();
    expect(stepTwo.className).toContain('bg-blue-600');
  });

  it('説明文が表示される', () => {
    render(<App />);
    expect(screen.getByText('質問に答えていくだけで申請書が完成します')).toBeInTheDocument();
  });

  it('フッターが表示される', () => {
    render(<App />);
    expect(screen.getByText(/このツールで生成した申請書は、提出前に必ず内容を確認してください/i)).toBeInTheDocument();
  });
});
