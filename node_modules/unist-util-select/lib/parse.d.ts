/**
 * @param {string} selector
 * @returns {AstSelector}
 */
export function parse(selector: string): AstSelector;
export type AstSelector = import('css-selector-parser').AstSelector;
