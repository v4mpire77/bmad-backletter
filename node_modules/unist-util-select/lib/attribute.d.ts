/**
 * @param {AstAttribute} query
 *   Query.
 * @param {Node} node
 *   Node.
 * @returns {boolean}
 *   Whether `node` matches `query`.
 */
export function attribute(query: AstAttribute, node: Node): boolean;
export type AstAttribute = import('css-selector-parser').AstAttribute;
export type AstRule = import('css-selector-parser').AstRule;
export type Node = import('./types.js').Node;
