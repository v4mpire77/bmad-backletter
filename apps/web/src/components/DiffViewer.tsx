'use client';

import React, { useEffect, useState } from 'react';

interface DiffLine {
  number: number;
  content: string;
  context?: boolean;
}

interface Comment {
  id: number;
  line: number;
  text: string;
  resolved: boolean;
}

interface DiffViewerProps {
  prId: string;
}

export default function DiffViewer({ prId }: DiffViewerProps) {
  const [lines, setLines] = useState<DiffLine[]>([]);
  const [comments, setComments] = useState<Record<number, Comment>>({});
  const [expanded, setExpanded] = useState(false);

  useEffect(() => {
    const load = async () => {
      const res = await fetch(`/api/pr/${prId}/diff`);
      const data = await res.json();
      setLines(data.lines);
    };
    load();
  }, [prId]);

  const postComment = async (line: number) => {
    const res = await fetch('/api/comments', {
      method: 'POST',
      body: JSON.stringify({ line, text: 'test comment' }),
    });
    const comment = await res.json();
    setComments((prev) => ({ ...prev, [line]: comment }));
  };

  const editComment = async (line: number) => {
    const existing = comments[line];
    const res = await fetch(`/api/comments/${existing.id}`, {
      method: 'PUT',
      body: JSON.stringify({ text: 'edited comment' }),
    });
    const updated = await res.json();
    setComments((prev) => ({ ...prev, [line]: updated }));
  };

  const resolveComment = async (line: number) => {
    const existing = comments[line];
    const res = await fetch(`/api/comments/${existing.id}/resolve`, {
      method: 'POST',
    });
    const updated = await res.json();
    setComments((prev) => ({ ...prev, [line]: updated }));
  };

  return (
    <div>
      <button onClick={() => setExpanded((e) => !e)}>
        {expanded ? 'Collapse context' : 'Expand context'}
      </button>
      <ul>
        {lines
          .filter((line) => expanded || !line.context)
          .map((line) => (
            <li key={line.number}>
              <span>{line.content}</span>
              {comments[line.number] ? (
                <span data-testid={`comment-${line.number}`}>
                  {comments[line.number].text}
                  {comments[line.number].resolved ? (
                    ' (resolved)'
                  ) : (
                    <>
                      <button onClick={() => editComment(line.number)}>Edit</button>
                      <button onClick={() => resolveComment(line.number)}>Resolve</button>
                    </>
                  )}
                </span>
              ) : (
                <button onClick={() => postComment(line.number)}>Comment</button>
              )}
            </li>
          ))}
      </ul>
    </div>
  );
}

