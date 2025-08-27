"use client";

import { useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import ExportDialog from "@/components/ExportDialog";
import { addExport } from "@/lib/mockStore";

export default function ExportClient() {
  const [open, setOpen] = useState(false);
  const router = useRouter();
  const pathname = usePathname();

  return (
    <>
      <button className="rounded bg-black text-white px-3 py-2 text-sm" onClick={() => setOpen(true)}>
        Export
      </button>
      <ExportDialog
        open={open}
        onClose={() => setOpen(false)}
        onConfirm={(opts) => {
          const id = pathname?.split("/").pop() || "mock-1";
          const filename = `${id.toUpperCase()}.pdf`;
          addExport({
            id: `${id}-${Date.now()}`,
            analysis_id: id,
            filename,
            created_at: new Date().toISOString(),
            options: opts,
          });
          router.push("/reports");
        }}
      />
    </>
  );
}

