// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/

import { 
    checkSheets,
    createNotebookRunCell,
    deleteAllNotebooks,
} from './utils/helpers';

import { 
    doNewMerge, mergeButton, updateMerge,
} from './utils/mergeHelpers';

import { CURRENT_URL } from './config';

const mergeCode = `import pandas as pd
import mitosheet
df1 = pd.DataFrame(data={'id': [1, 2, 3], 'values': [101, 102, 103]})
df2 = pd.DataFrame(data={'id': [1, 2, 3], 'values': [201, 202, 203]})
mitosheet.sheet(df1, df2)`

fixture `Test Merge Functionality`
    .page(CURRENT_URL)
    .beforeEach( async t => {
        await createNotebookRunCell(t, true, mergeCode);
    })
    .afterEach(async t => {
        // Delete notebook, at the end of the test
        await deleteAllNotebooks(t)
    })


test('Test merge on an empty sheet', async t => {
    await createNotebookRunCell(t, true, 'import mitosheet\nmitosheet.sheet()');
    await t
        .click(mergeButton)
        // If the sheet crashes, the merge button is no longer there!
        .expect(mergeButton.exists).ok();
});

test('Merge opens modal, can create an edit sheet', async t => {
    await doNewMerge(t, 'df1', 'id', 'df2', 'id');
    await checkSheets(t, {
        'df3': {
            'id': ['1', '2', '3'],
            'values_df1': ['101', '102', '103'],
            'values_df2': ['201', '202', '203']
        }
    })

    await updateMerge(t, 0, 'df1', 'id', 'df2', 'id', {sheetOneColumns: ['values'], sheetTwoColumns: []});
    await checkSheets(t, {
        'df3': {
            'id': ['1', '2', '3'],
            'values': ['101', '102', '103']
        }
    })

    await updateMerge(t, 1, 'df1', 'id', 'df2', 'id', {sheetOneColumns: [], sheetTwoColumns: ['values']});
    await checkSheets(t, {
        'df3': {
            'id': ['1', '2', '3'],
            'values': ['201', '202', '203']
        }
    })
});


test('Test merge a single sheet into itself doesnt crash sheet', async t => {
    await doNewMerge(t, 'df1', 'id', 'df1', 'id');
    await checkSheets(t, {
        'df3': {
            'id': ['1', '2', '3'],
            'values_df1': ['101', '102', '103'],
            'values_df1_2': ['101', '102', '103']
        }
    })
});