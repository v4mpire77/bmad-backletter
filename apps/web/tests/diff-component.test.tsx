import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import DiffViewer from '../src/components/DiffViewer';
import { vi } from 'vitest';

interface Comment {
  id: number;
  line: number;
  text: string;
  resolved: boolean;
}

const diffData = {
  lines: [
    { number: 1, content: 'context line', context: true },
    { number: 2, content: 'changed line' },
  ],
};

let comments: Record<number, Comment>;
let nextId: number;

function mockFetch(url: RequestInfo, init?: RequestInit) {
  const method = init?.method || 'GET';
  const href = typeof url === 'string' ? url : url.toString();

  if (href === '/api/pr/1/diff' && method === 'GET') {
    return Promise.resolve({ ok: true, json: async () => diffData });
  }

  if (href === '/api/comments' && method === 'POST') {
    const body = JSON.parse((init?.body as string) || '{}');
    const comment = { id: nextId++, line: body.line, text: body.text, resolved: false };
    comments[comment.id] = comment;
    return Promise.resolve({ ok: true, json: async () => comment });
  }

  const editMatch = href.match(/\/api\/comments\/(\d+)$/);
  if (editMatch && method === 'PUT') {
    const id = Number(editMatch[1]);
    const body = JSON.parse((init?.body as string) || '{}');
    comments[id].text = body.text;
    return Promise.resolve({ ok: true, json: async () => comments[id] });
  }

  const resolveMatch = href.match(/\/api\/comments\/(\d+)\/resolve$/);
  if (resolveMatch && method === 'POST') {
    const id = Number(resolveMatch[1]);
    comments[id].resolved = true;
    return Promise.resolve({ ok: true, json: async () => comments[id] });
  }

  return Promise.resolve({ ok: false, json: async () => ({}) });
}

beforeEach(() => {
  comments = {};
  nextId = 1;
  global.fetch = vi.fn(mockFetch);
});

afterEach(() => {
  vi.restoreAllMocks();
});

describe('DiffViewer', () => {
  it('fetches and renders diff data for a PR', async () => {
    render(<DiffViewer prId="1" />);
    expect(await screen.findByText('changed line')).toBeInTheDocument();
  });

  it('posting, editing, and resolving comments persists via API', async () => {
    render(<DiffViewer prId="1" />);
    await screen.findByText('changed line');

    fireEvent.click(screen.getByText('Comment'));
    expect(await screen.findByTestId('comment-2')).toHaveTextContent('test comment');

    fireEvent.click(screen.getByText('Edit'));
    expect(await screen.findByTestId('comment-2')).toHaveTextContent('edited comment');

    fireEvent.click(screen.getByText('Resolve'));
    expect(await screen.findByTestId('comment-2')).toHaveTextContent('edited comment (resolved)');
  });

  it('expands and collapses diff context correctly', async () => {
    render(<DiffViewer prId="1" />);
    await screen.findByText('changed line');

    expect(screen.queryByText('context line')).not.toBeInTheDocument();
    fireEvent.click(screen.getByText('Expand context'));
    expect(await screen.findByText('context line')).toBeInTheDocument();
    fireEvent.click(screen.getByText('Collapse context'));
    expect(screen.queryByText('context line')).not.toBeInTheDocument();
  });
});

