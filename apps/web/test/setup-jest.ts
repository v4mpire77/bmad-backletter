import '@testing-library/jest-dom';

// Helpful no-ops for JSDOM environment
// @ts-ignore
window.HTMLElement.prototype.scrollIntoView = function () {};

