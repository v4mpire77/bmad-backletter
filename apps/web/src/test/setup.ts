import '@testing-library/jest-dom';

// Stub canvas context for axe-core color contrast checks
Object.defineProperty(HTMLCanvasElement.prototype, 'getContext', {
  value: () => ({ getImageData: () => ({ data: [] }) }),
});

// Suppress console errors during tests to avoid noise from intentional error testing
const originalError = console.error;
beforeAll(() => {
  console.error = (...args: any[]) => {
    if (
      typeof args[0] === 'string' && 
      args[0].includes('Upload failed')
    ) {
      return;
    }
    originalError.call(console, ...args);
  };
});

afterAll(() => {
  console.error = originalError;
});
