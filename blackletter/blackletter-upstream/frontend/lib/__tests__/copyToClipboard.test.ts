import { copyToClipboard } from '../utils';

describe('copyToClipboard', () => {
  beforeEach(() => {
    (navigator as any).clipboard = {
      writeText: jest.fn().mockResolvedValue(undefined),
    };
    (navigator as any).permissions = {
      query: jest.fn().mockResolvedValue({ state: 'granted' }),
    };
  });

  it('copies sanitized text using Clipboard API', async () => {
    const html = '<p>Hello <b>World</b></p>';
    const result = await copyToClipboard(html);
    expect(navigator.clipboard.writeText).toHaveBeenCalledWith('Hello World');
    expect(result).toBe(true);
  });

  it('falls back to execCommand when Clipboard API fails', async () => {
    (navigator as any).clipboard.writeText.mockRejectedValue(new Error('denied'));
    document.execCommand = jest.fn().mockReturnValue(true);

    const result = await copyToClipboard('Fallback test');
    expect(document.execCommand).toHaveBeenCalledWith('copy');
    expect(result).toBe(true);
  });
});
