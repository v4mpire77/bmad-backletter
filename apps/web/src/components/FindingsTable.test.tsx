import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import FindingsTable from './FindingsTable';
import type { PageFinding } from '@/lib/types';
import { vi } from 'vitest';

describe('FindingsTable', () => {
  const findings: PageFinding[] = [
    {
      id: '1',
      rule_id: 'art28-3-a',
      snippet: 'sample snippet',
      anchors: [],
    },
  ];

    it('renders findings and triggers callback on row click', () => {
      const onRowClick = vi.fn();
      render(<FindingsTable findings={findings} onRowClick={onRowClick} />);
      fireEvent.click(screen.getByText('art28-3-a'));
      expect(onRowClick).toHaveBeenCalled();
    });
  });
