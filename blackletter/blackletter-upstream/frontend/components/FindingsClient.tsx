'use client';

import { useState } from 'react';
import FindingsTable from '@/components/FindingsTable';
import EvidenceDrawer from '@/components/EvidenceDrawer';
import ExportDialog from '@/components/ExportDialog';
import { Finding } from '@/lib/types';

export default function FindingsClient({ findings }: { findings: Finding[] }) {
  const [selectedFinding, setSelectedFinding] = useState<Finding | null>(null);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [isExportDialogOpen, setIsExportDialogOpen] = useState(false);

  const handleRowClick = (finding: Finding) => {
    setSelectedFinding(finding);
    setIsDrawerOpen(true);
  };

  const handleExportClick = () => {
    setIsExportDialogOpen(true);
  };

  const closeDrawer = () => {
    setIsDrawerOpen(false);
    setSelectedFinding(null);
  };

  const closeExportDialog = () => {
    setIsExportDialogOpen(false);
  };

  return (
    <div>
      {/* Header with Export button */}
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold">Findings</h2>
        <button
          onClick={handleExportClick}
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Export
        </button>
      </div>

      {/* Findings Table */}
      <FindingsTable findings={findings} onRowClick={handleRowClick} />

      {/* Evidence Drawer */}
      {selectedFinding && (
        <EvidenceDrawer
          isOpen={isDrawerOpen}
          onClose={closeDrawer}
          finding={selectedFinding}
        />
      )}

      {/* Export Dialog */}
      <ExportDialog
        isOpen={isExportDialogOpen}
        onClose={closeExportDialog}
      />
    </div>
  );
}