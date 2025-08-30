import "@testing-library/jest-dom";

// Helpful no-ops for JSDOM environment
// @ts-expect-error JSDOM doesn't implement scrollIntoView
window.HTMLElement.prototype.scrollIntoView = function () {};

