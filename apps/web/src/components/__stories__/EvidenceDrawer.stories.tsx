import type { Meta, StoryObj } from '@storybook/react';
import EvidenceDrawer from '../EvidenceDrawer';
import type { Finding } from '@/lib/types';

const sample: Finding = {
  id: '1',
  title: 'art28_data_categories',
  verdict: 'weak',
  evidence: 'The Processor shall process personal data...',
  rationale: 'Because <strong>evidence</strong> shows compliance.',
  anchors: [{ text: 'personal data', page: 1, offset: 24 }],
  citations: [{ page: 3, text: 'Sample citation' }],
};

const meta: Meta<typeof EvidenceDrawer> = {
  title: 'EvidenceDrawer',
  component: EvidenceDrawer,
  args: {
    isOpen: true,
    onClose: () => {},
    finding: sample,
  },
};

export default meta;
type Story = StoryObj<typeof EvidenceDrawer>;

export const Default: Story = {};

