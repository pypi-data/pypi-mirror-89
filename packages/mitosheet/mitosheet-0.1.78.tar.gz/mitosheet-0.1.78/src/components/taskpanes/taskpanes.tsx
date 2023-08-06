// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/* 
    Each Taskpane has a type (included undefined, which is the type of _no taskpane_ (e.g. nothing is displayed)).
*/
export type TaskpaneInfo = 
    | undefined
    | {type: 'Pivot'} 
    | {type: 'Merge'}

