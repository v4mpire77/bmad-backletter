import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import EvidenceDrawer from '../EvidenceDrawer';

describe('EvidenceDrawer copy button', () => {
  beforeEach(() => {
    (navigator as any).clipboard = {
      writeText: jest.fn().mockResolvedValue(undefined),
    };
    (navigator as any).permissions = {
      query: jest.fn().mockResolvedValue({ state: 'granted' }),
    };
  });

  it('copies sanitized evidence text', async () => {
    const finding = {
      id: '1',
      detector: 'detector',
      verdict: 'pass',
      rationale: 'because',
      evidence: 'This is <b>bold</b> evidence',
      anchors: [],
      reviewed: false,
    };

    render(
      <EvidenceDrawer isOpen={true} onClose={() => {}} finding={finding} />
    );

    const button = screen.getByText('Copy to Clipboard');
    fireEvent.click(button);

    await waitFor(() => {
      expect(navigator.clipboard.writeText).toHaveBeenCalledWith('This is bold evidence');
    });
  });
});
