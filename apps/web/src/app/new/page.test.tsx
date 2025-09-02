/// <reference types="vitest" />
import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

import UploadPage from './page';

describe('UploadPage file input accessibility', () => {
  it('focuses input and triggers click via label', async () => {
    const user = userEvent.setup();
    const clickSpy = vi.spyOn(HTMLInputElement.prototype, 'click').mockImplementation(() => {});

    render(<UploadPage />);
    const label = screen.getByRole('button', {
      name: /drag and drop area or click to select a file/i,
    });
    const input = screen.getByTestId('file-input');

    await user.tab();
    expect(label).toHaveFocus();
    await user.tab();
    expect(input).toHaveFocus();

    await user.click(label);
    expect(input).toHaveFocus();
    expect(clickSpy).toHaveBeenCalledTimes(0);

    label.focus();
    await user.keyboard('{Enter}');
    expect(clickSpy).toHaveBeenCalledTimes(1);

    clickSpy.mockRestore();
  });
});
