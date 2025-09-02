import React from 'react';
import { render, screen } from '@testing-library/react';
import Home from './page';
import '@testing-library/jest-dom';

test('renders home page heading', () => {
  render(<Home />);
  expect(screen.getByText(/GDPR Contract Analyzer/)).toBeInTheDocument();
});
