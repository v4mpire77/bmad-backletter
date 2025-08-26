/**
 * TypeScript helper to check if something is indexable (any object is
 * indexable in JavaScript).
 *
 * @param {unknown} value
 *   Thing to check.
 * @returns {asserts value is Record<string, unknown>}
 *   Nothing.
 * @throws {Error}
 *   When `value` is not an object.
 */
export function indexable(value: unknown): asserts value is Record<string, unknown>;
/**
 * @param {Node} node
 * @returns {node is Parent}
 */
export function parent(node: Node): node is import("unist").Parent;
export type Node = import('unist').Node;
export type Parent = import('unist').Parent;
