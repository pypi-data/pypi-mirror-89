// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains all useful selectors and helpers for interacting with the merge modal.
*/

import { Selector } from 'testcafe';
import { modalAdvanceButtonSelector } from './allModals';

export const mergeButton = Selector('div')
    .withExactText('Merge')
    .parent()


export const mergeModalSheetOneSelector = Selector('select.merge-modal-sheet-dropdown').nth(0)
export const mergeModalSheetOneOptionSelector = mergeModalSheetOneSelector.find('option')
export const mergeModalKeyOneSelector = Selector('select.merge-modal-key-dropdown').nth(0)
export const mergeModalKeyOneOptionSelector = mergeModalKeyOneSelector.find('option')

export const mergeModalSheetTwoSelector = Selector('select.merge-modal-sheet-dropdown').nth(1)
export const mergeModalSheetTwoOptionSelector = mergeModalSheetTwoSelector.find('option')
export const mergeModalKeyTwoSelector = Selector('select.merge-modal-key-dropdown').nth(1)
export const mergeModalKeyTwoOptionSelector = mergeModalKeyTwoSelector.find('option')

export const getMergeModalColumnSelector = (sheet: 1 | 2, columnHeader: string): Selector => {
    return Selector('div.merge-modal-column-selection')
        .nth(sheet - 1)
        .child('div')
        .withExactText(columnHeader)
        .child('input');
}


/*
    If repeating an analysis with imports, this changes the files
    that are imported, as well as the pythonCode 
*/
export async function doMerge(t: TestController, sheetOneName: string, sheetOneKey: string, sheetTwoName: string, sheetTwoKey: string, sheetOneColumns?: string[], sheetTwoColumns?: string[]): Promise<void> {
    
    await t
        .click(mergeButton)
        .click(mergeModalSheetOneSelector)
        .click(mergeModalSheetOneOptionSelector.withExactText(sheetOneName))
        .click(mergeModalKeyOneSelector)
        .click(mergeModalKeyOneOptionSelector.withExactText(sheetOneKey))
        .click(mergeModalSheetTwoSelector)
        .click(mergeModalSheetTwoOptionSelector.withExactText(sheetTwoName))
        .click(mergeModalKeyTwoSelector)
        .click(mergeModalKeyTwoOptionSelector.withExactText(sheetTwoKey))

    // Since they are all toggled by default, we toggle them all off, then we go through and turn on the ones we want
    if (sheetOneColumns !== undefined) {
        await t.click(getMergeModalColumnSelector(1, 'Select all'))
        for (let i = 0; i < sheetOneColumns.length; i++) {
            const columnHeader = sheetOneColumns[i];
            await t.click(getMergeModalColumnSelector(1, columnHeader))
        }
    }   
    if (sheetTwoColumns !== undefined) {
        await t.click(getMergeModalColumnSelector(2, 'Select all'))
        for (let i = 0; i < sheetTwoColumns.length; i++) {
            const columnHeader = sheetTwoColumns[i];
            await t.click(getMergeModalColumnSelector(2, columnHeader))
        }
    }

    await t.click(modalAdvanceButtonSelector)
}