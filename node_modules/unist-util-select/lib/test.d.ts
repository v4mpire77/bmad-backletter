/**
 * @param {AstRule} query
 * @param {Node} node
 * @param {number | undefined} index
 * @param {Parent | undefined} parent
 * @param {SelectState} state
 * @returns {boolean}
 */
export function test(query: AstRule, node: Node, index: number | undefined, parent: Parent | undefined, state: SelectState): boolean;
export type AstRule = import('css-selector-parser').AstRule;
export type Node = import('unist').Node;
export type Parent = import('unist').Parent;
export type SelectState = import('./types.js').SelectState;
