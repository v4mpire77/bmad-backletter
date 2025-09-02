import '@testing-library/jest-dom';

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
