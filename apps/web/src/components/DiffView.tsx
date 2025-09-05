import React from 'react';
import { Plus, Minus } from 'lucide-react';

interface DiffPart {
  value: string;
  added?: boolean;
  removed?: boolean;
}

function computeDiff(oldText: string, newText: string): DiffPart[] {
  const oldWords = oldText.split(/\s+/);
  const newWords = newText.split(/\s+/);
  const result: DiffPart[] = [];
  let i = 0;
  let j = 0;
  while (i < oldWords.length || j < newWords.length) {
    const oldWord = oldWords[i];
    const newWord = newWords[j];
    if (oldWord === newWord) {
      result.push({ value: `${newWord}${j < newWords.length - 1 ? ' ' : ''}` });
      i += 1;
      j += 1;
    } else {
      if (newWord !== undefined) {
        result.push({ value: `${newWord} `, added: true });
        j += 1;
      }
      if (oldWord !== undefined) {
        result.push({ value: `${oldWord} `, removed: true });
        i += 1;
      }
    }
  }
  return result;
}

interface DiffViewProps {
  oldText: string;
  newText: string;
}

export default function DiffView({ oldText, newText }: DiffViewProps) {
  const parts = computeDiff(oldText, newText);
  return (
    <div role="region" aria-live="polite" aria-label="Diff results">
      {parts.map((part, idx) => {
        if (part.added) {
          return (
            <span
              key={idx}
              className="diff-added inline-flex items-center"
              aria-label={`Insertion: ${part.value}`}
            >
              <Plus className="mr-1 h-3 w-3" aria-hidden="true" />
              <span aria-hidden="true">{part.value}</span>
            </span>
          );
        }
        if (part.removed) {
          return (
            <span
              key={idx}
              className="diff-removed inline-flex items-center line-through"
              aria-label={`Deletion: ${part.value}`}
            >
              <Minus className="mr-1 h-3 w-3" aria-hidden="true" />
              <span aria-hidden="true">{part.value}</span>
            </span>
          );
        }
        return (
          <span key={idx} aria-hidden="true">{part.value}</span>
        );
      })}
    </div>
  );
}
