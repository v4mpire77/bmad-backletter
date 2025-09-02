import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import AdminPage from './page';

describe('AdminPage', () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  it('fetches and displays metrics with sparklines', async () => {
    global.fetch = vi
      .fn()
      .mockResolvedValueOnce({
        json: async () => [
          { name: 'Users', value: 5, slug: 'users' },
        ],
      } as any)
      .mockResolvedValueOnce({
        json: async () => ({ users: [1, 2, 3, 4, 5] }),
      } as any);
    const { container } = render(<AdminPage />);
    await waitFor(() => screen.getByText('Users'));
    expect(screen.getByText('5')).toBeTruthy();
    expect(container.querySelectorAll('svg')).toHaveLength(1);
    expect(global.fetch).toHaveBeenCalledWith('/api/admin/metrics');
    expect(global.fetch).toHaveBeenCalledWith('/api/admin/metrics/timeseries');
  });

  it('renders fallback when timeseries has a single value', async () => {
    global.fetch = vi
      .fn()
      .mockResolvedValueOnce({
        json: async () => [
          { name: 'Users', value: 5, slug: 'users' },
        ],
      } as any)
      .mockResolvedValueOnce({
        json: async () => ({ users: [5] }),
      } as any);
    const { container } = render(<AdminPage />);
    await waitFor(() => screen.getByText('Users'));
    expect(container.querySelector('svg')).toBeNull();
    expect(screen.getByLabelText('sparkline-fallback')).toBeTruthy();
  });

  it('renders fallback when timeseries values are all zero', async () => {
    global.fetch = vi
      .fn()
      .mockResolvedValueOnce({
        json: async () => [
          { name: 'Users', value: 5, slug: 'users' },
        ],
      } as any)
      .mockResolvedValueOnce({
        json: async () => ({ users: [0, 0, 0] }),
      } as any);
    const { container } = render(<AdminPage />);
    await waitFor(() => screen.getByText('Users'));
    expect(container.querySelector('svg')).toBeNull();
    expect(screen.getByLabelText('sparkline-fallback')).toBeTruthy();
  });
});

