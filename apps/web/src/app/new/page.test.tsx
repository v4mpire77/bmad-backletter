import React from 'react';
import { render, fireEvent, act } from '@testing-library/react';
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

it('resets to idle on escape key press during upload', () => {
  vi.useFakeTimers();
  const { getByRole, container } = render(<UploadPage />);
  const input = container.querySelector('input[type="file"]') as HTMLInputElement;
  const file = new File(['content'], 'test.txt', { type: 'text/plain' });

  act(() => {
    fireEvent.change(input, { target: { files: [file] } });
    vi.advanceTimersByTime(1000);
  });

  const progressBeforeReset = container.querySelector('.bg-blue-600');
  expect(progressBeforeReset).not.toBeNull();

  act(() => {
    fireEvent.keyDown(window, { key: 'Escape' });
  });

  const dropzoneAfterReset = getByRole('button', { name: /drag and drop area or click to select a file/i });
  expect(dropzoneAfterReset).not.toBeNull();
  expect(container.querySelector('.bg-blue-600')).toBeNull();
  vi.useRealTimers();
});

