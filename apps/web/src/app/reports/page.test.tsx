import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import ExportDialog from '../../components/ExportDialog';
import ReportsPage from './page';
import { addExport, __resetExports } from '../../lib/exportStore';
import { vi } from 'vitest';

const push = vi.fn();
vi.mock('next/navigation', () => ({
  useRouter: () => ({ push }),
}));

describe('Reports flow', () => {
  beforeEach(() => {
    __resetExports();
    push.mockReset();
  });

  it('navigates to reports after export and renders history', () => {
    const onClose = vi.fn();
    const onConfirm = () => {
      addExport({
        id: '1',
        name: 'test.txt',
        createdAt: new Date().toISOString(),
      });
      push('/reports');
    };

    const { getByText } = render(
      <ExportDialog isOpen onClose={onClose} onConfirm={onConfirm} />
    );
    fireEvent.click(getByText('Confirm'));
    expect(push).toHaveBeenCalledWith('/reports');

    render(<ReportsPage />);
    expect(screen.getByText('test.txt')).toBeInTheDocument();
  });
});
