/**
 * Walk a tree.
 *
 * @param {SelectState} state
 * @param {Node | undefined} tree
 */
export function walk(state: SelectState, tree: Node | undefined): void;
export type AstRule = import('css-selector-parser').AstRule;
export type Node = import('unist').Node;
export type Parent = import('unist').Parent;
export type SelectState = import('./types.js').SelectState;
/**
 * Rule sets by nesting.
 */
export type Nest = {
    /**
     * `a b`
     */
    descendant: Array<AstRule> | undefined;
    /**
     * `a > b`
     */
    directChild: Array<AstRule> | undefined;
    /**
     * `a + b`
     */
    adjacentSibling: Array<AstRule> | undefined;
    /**
     * `a ~ b`
     */
    generalSibling: Array<AstRule> | undefined;
};
/**
 * Info on nodes in a parent.
 */
export type Counts = {
    /**
     * Number of nodes.
     */
    count: number;
    /**
     * Number of nodes by type.
     */
    types: Map<string, number>;
};
