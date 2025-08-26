/** @type {(rule: AstPseudoClass, node: Node, index: number | undefined, parent: Parent | undefined, state: SelectState) => boolean} */
export const pseudo: (rule: AstPseudoClass, node: Node, index: number | undefined, parent: Parent | undefined, state: SelectState) => boolean;
export type AstPseudoClass = import('css-selector-parser').AstPseudoClass;
export type Node = import('unist').Node;
export type Parent = import('unist').Parent;
export type SelectState = import('./types.js').SelectState;
