// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/* 
    Each Taskpane has a type (included undefined, which is the type of _no taskpane_ (e.g. nothing is displayed)).

    If you want to be able to open a taskpane in Mito, then you need to add the type of this taskpane, 
    as well as any parameters it has, to this type.

    For example, if you create a new taskpane 'Dork' that takes a columnHeader as input, then you should
    add a new element here that looks like:
        | {type: 'Dork', columnHeader: string}
*/
export type TaskpaneInfo = 
    | {type: 'None'}
    | {type: 'Pivot'} 
    | {type: 'Merge'}

