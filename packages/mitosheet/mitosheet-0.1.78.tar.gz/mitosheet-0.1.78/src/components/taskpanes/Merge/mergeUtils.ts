// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import { SheetJSON } from '../../../widget';


/*
    Returns all column headers shared between the sheets at the given indexes.
*/
const getSharedColumnHeaders = (sheetJSONArray: SheetJSON[], sheetOneIndex: number, sheetTwoIndex: number): string[] => {
    // If invalid indexes are passed, return early to avoid errors
    if (sheetJSONArray.length <= sheetOneIndex || sheetJSONArray.length <= sheetOneIndex) {
        return [];
    }

    const sheetOneColumnNames = sheetJSONArray[sheetOneIndex].columns;
    const sheetTwoColumnNames = sheetJSONArray[sheetTwoIndex].columns;

    const sharedKeys = sheetOneColumnNames.filter(columnName => sheetTwoColumnNames.includes(columnName)).map(columnHeader => columnHeader.toString())
    return sharedKeys;
}


type SuggestedKeys = {
    sheetOneMergeKey: string,
    sheetTwoMergeKey: string
}

/*
    Given two sheet indexes, reccomends a key to merge on. If there are x shared keys, then:
    - If x.length >= 1, it returns the first shared key as reccomended.
    - Else, it reccomends the first key

    Returns undefined if no such column headers can exist, normally because the indexs are out of bounds 
    of the sheets.
*/
export const getSuggestedColumnHeaderKeys = (sheetJSONArray: SheetJSON[], sheetOneIndex: number, sheetTwoIndex: number): SuggestedKeys => {
    const sharedKeys = getSharedColumnHeaders(sheetJSONArray, sheetOneIndex, sheetTwoIndex);
    const sheetOneMergeKey = sharedKeys.length >= 1 ? sharedKeys[0] : sheetJSONArray[sheetOneIndex].columns[0];
    const sheetTwoMergeKey = sharedKeys.length >= 1 ? sharedKeys[0] : sheetJSONArray[sheetTwoIndex].columns[0];
    return {
        sheetOneMergeKey: sheetOneMergeKey,
        sheetTwoMergeKey: sheetTwoMergeKey
    }
}