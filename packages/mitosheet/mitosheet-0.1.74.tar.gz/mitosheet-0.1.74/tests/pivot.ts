// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/

import { 
    checkColumn,
    checkSheet,
    createNotebookRunCell,
    deleteAllNotebooks,
} from './utils/helpers';

import {
    aggFuncSelector,
    doNewPivot,
    updatePivot
} from './utils/pivotHelpers';

const code = `
import pandas as pd
import mitosheet

df1 = pd.DataFrame(data={
    'gender': ['male','male','female', 'female', 'female'], 
    'species': ['human','dog','human', 'human', 'dog'], 
    'size': ['big', 'small', 'small', 'big', 'big'],
    'weight': [160, 20, 110, 175, 95]
})
mitosheet.sheet(df1)
`
import { CURRENT_URL } from './config';
import { addColumnButton, renameColumn, setFormula } from './utils/columnHelpers';
import { getTabSelector, undoButton } from './utils/selectors';

fixture `Test Group`
    .page(CURRENT_URL)
    .beforeEach( async t => {
        await createNotebookRunCell(t, true, code);
    })
    .afterEach(async t => {
        // Delete notebook, at the end of the test
        await deleteAllNotebooks(t)
    })

test('Allows for a basic pivot with a single row', async t => {
    await doNewPivot(t, 'df1', ['gender'], [], {'weight': 'sum'})
    await checkSheet(t, {
        'gender': ['female', 'male'],
        'weight': ['380', '180']
    }, 'df2')
    await updatePivot(t, 'df1', ['gender'], [], {'weight': 'max'})
    await checkSheet(t, {
        'gender': ['female', 'male'],
        'weight': ['175', '160']
    }, 'df2')
});

test('Allows for creating a blank pivot table', async t => {
    await doNewPivot(t, 'df1', [], [], {})
    await checkSheet(t, {}, 'df2')
});

test('Allows for creating a pivot table and then removing all keys', async t => {
    // Create pivot table
    await doNewPivot(t, 'df1', ['gender'], [], {'weight': 'sum'})
    await checkSheet(t, {
        'gender': ['female', 'male'],
        'weight': ['380', '180']
    }, 'df2')

    // Update pivot table
    await updatePivot(t, 'df1', ['gender'], [], {'weight': 'max'})
    await checkSheet(t, {
        'gender': ['female', 'male'],
        'weight': ['175', '160']
    }, 'df2')

    // Remove all values from pivot table
    await updatePivot(t, 'df1', [], [], {})
    await checkSheet(t, {}, 'df2')
});

test('Allows for creating a pivot table and then removing all keys', async t => {
    // Create pivot table
    await doNewPivot(t, 'df1', ['gender'], [], {'weight': 'sum'})
    await checkSheet(t, {
        'gender': ['female', 'male'],
        'weight': ['380', '180']
    }, 'df2')

    // Update pivot table
    await updatePivot(t, 'df1', ['gender'], [], {'weight': 'max'})
    await checkSheet(t, {
        'gender': ['female', 'male'],
        'weight': ['175', '160']
    }, 'df2')

    // Remove all values from pivot table
    await updatePivot(t, 'df1', [], [], {})
    await checkSheet(t, {}, 'df2')
});


test('Pivot Table Taskpane closes when renaming the column', async t => {
    // Create pivot table
    await doNewPivot(t, 'df1', ['gender'], [], {'weight': 'sum'})
    await checkSheet(t, {
        'gender': ['female', 'male'],
        'weight': ['380', '180']
    }, 'df2')

    await renameColumn(t, 'gender', 'full_name')

    // Expect the taskpane to be closed
    t.expect(!aggFuncSelector.exists)
});


test('Pivot Table Taskpane closes when editing', async t => {
    // Create a new column 
    await t.click(addColumnButton);

    // Create pivot table
    await doNewPivot(t, 'df1', ['gender'], [], {'weight': 'sum'})
    await checkSheet(t, {
        'gender': ['female', 'male'],
        'weight': ['380', '180']
    }, 'df2')

    // Switch back to the first sheet
    await t.click(getTabSelector('df1'))

    // Set column formula
    await setFormula(t, '=gender', 'E', '0');
    
    // Expect the taskpane to be closed
    t.expect(!aggFuncSelector.exists)
});


test('Pivot then undo to remove the sheet', async t => {
    // Create pivot table
    await doNewPivot(t, 'df1', ['gender'], [], {'weight': 'sum'})
    await checkSheet(t, {
        'gender': ['female', 'male'],
        'weight': ['380', '180']
    }, 'df2')

    // Undo the edit
    await t.click(undoButton);

    // Expect the pivot table sheet to be gone
    t.expect(!getTabSelector('df2').exists)
});

test('Pivot then add column to pivot table and select formula', async t => {
    // Create pivot table
    await doNewPivot(t, 'df1', ['gender'], [], {'weight': 'sum'})
    await checkSheet(t, {
        'gender': ['female', 'male'],
        'weight': ['380', '180']
    }, 'df2')

    // Create a new column 
    await t.click(addColumnButton);

    // Expect the taskpane to be closed
    t.expect(!aggFuncSelector.exists)

    // Set column formula
    await setFormula(t, '=gender', 'C', '0');

    // Check columns has correct values
    await checkColumn(t, 'C', ['female', 'male'])
});
