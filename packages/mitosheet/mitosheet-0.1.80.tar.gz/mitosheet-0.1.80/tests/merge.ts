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
    doMerge,
} from './utils/mergeHelpers';

import { CURRENT_URL } from './config';

fixture `Test Merge Functionality`
    .page(CURRENT_URL)
    .beforeEach( async t => {
        await createNotebookRunCell(t, true, 'import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={\'id\': [1, 2, 3], \'values\': [101, 102, 103]})\ndf2 = pd.DataFrame(data={\'id\': [1, 2, 3], \'values\': [201, 202, 203]})\nmitosheet.sheet(df1, df2)');
    })
    .afterEach(async t => {
        // Delete notebook, at the end of the test
        await deleteAllNotebooks(t)
    })

test('Merge opens modal and creates new dataframe multiple times', async t => {
    // Do the merge
    await doMerge(t, 'df1', 'id', 'df2', 'id');

    // Do another merge
    await doMerge(t, 'df1', 'id', 'df2', 'id');

    await checkSheets(t, {
        'df3': {
            'id': ['1', '2', '3'],
            'values_df1': ['101', '102', '103'],
            'values_df2': ['201', '202', '203']
        }, 
        'df4': {
            'id': ['1', '2', '3'],
            'values_df1': ['101', '102', '103'],
            'values_df2': ['201', '202', '203']
        }
    })
});

test('Merge allows you to only take keys from first sheet', async t => {
    // Do the merge
    await doMerge(t, 'df1', 'id', 'df2', 'id', ['values'], []);

    await checkSheets(t, {
        'df3': {
            'id': ['1', '2', '3'],
            'values': ['101', '102', '103']
        }
    })
});
   

test('Merge allows you to only take keys from second sheet', async t => {
    // Do the merge
    await doMerge(t, 'df1', 'id', 'df2', 'id', [], ['values']);

    await checkSheets(t, {
        'df3': {
            'id': ['1', '2', '3'],
            'values': ['201', '202', '203']
        }
    })
});
   
   