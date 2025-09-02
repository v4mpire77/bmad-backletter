'use client';

import { useSyncExternalStore } from 'react';

export interface ReportExport {
  id: string;
  name: string;
  createdAt: string;
}

let exportsStore: ReportExport[] = [];
const listeners = new Set<() => void>();

function subscribe(listener: () => void) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function addExport(report: ReportExport) {
  exportsStore = [report, ...exportsStore];
  listeners.forEach((l) => l());
}

export function useExportStore() {
  return useSyncExternalStore(subscribe, () => exportsStore, () => exportsStore);
}

export function __resetExports() {
  exportsStore = [];
  listeners.forEach((l) => l());
}
