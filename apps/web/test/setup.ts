import "@testing-library/jest-dom";

// Helpful no-ops for JSDOM environment
// @ts-expect-error jsdom may not define this in type
window.HTMLElement.prototype.scrollIntoView = function () {};

