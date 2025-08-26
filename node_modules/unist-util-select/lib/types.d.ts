export type AstSelector = import('css-selector-parser').AstSelector;
export type Node = import('unist').Node;
/**
 * Current state.
 */
export type SelectState = {
    /**
     *   Original root selectors.
     */
    rootQuery: AstSelector;
    /**
     *   Matches.
     */
    results: Array<Node>;
    /**
     *   Nodes in scope.
     */
    scopeNodes: Array<Node>;
    /**
     *   Whether we can stop looking after we found one node.
     */
    one: boolean;
    /**
     *   Whether we only allow selectors without nesting.
     */
    shallow: boolean;
    /**
     *   Whether we found at least one match.
     */
    found: boolean;
    /**
     *   Track siblings: this current node has `n` nodes with its type before it.
     */
    typeIndex: number | undefined;
    /**
     *   Track siblings: this current node has `n` nodes before it.
     */
    nodeIndex: number | undefined;
    /**
     *   Track siblings: there are `n` siblings with this node’s type.
     */
    typeCount: number | undefined;
    /**
     *   Track siblings: there are `n` siblings.
     */
    nodeCount: number | undefined;
};
