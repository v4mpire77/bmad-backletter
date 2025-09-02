import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import UploadPage from './page';
import { vi } from 'vitest';

vi.mock('next/navigation', () => ({
  useRouter: () => ({ push: vi.fn() }),
}));

it('opens file dialog when drop zone is clicked', () => {
  const { getByRole, container } = render(<UploadPage />);
  const dropzone = getByRole('button', { name: /drag and drop area or click to select a file/i });
  const input = container.querySelector('input[type="file"]') as HTMLInputElement;
  const clickSpy = vi.spyOn(input, 'click');

  fireEvent.click(dropzone);

  expect(clickSpy).toHaveBeenCalled();
});
