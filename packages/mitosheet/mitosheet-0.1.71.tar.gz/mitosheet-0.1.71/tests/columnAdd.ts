// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/

import {
    addColumnButton
} from './utils/columnHelpers'

import { 
    checkSheet,
    deleteAllNotebooks,
    createNotebookRunCell
} from './utils/helpers';

import { testUser } from './utils/roles';

import { CURRENT_URL } from './config';

fixture `Column Additions`
    .page(CURRENT_URL)
    .beforeEach( async t => {
        await t.useRole(testUser);
        await deleteAllNotebooks(t)
    })
    .afterEach(async t => {
        // Delete notebook, at the end of the test
        await deleteAllNotebooks(t)
    })

test('Can add a column when the new column would overlap with the column name', async t => {
    await createNotebookRunCell(t, false, 'import pandas as pd\nimport mitosheet\ndf = pd.DataFrame(data={\'B\': [1, 2, 3]})\nmitosheet.sheet(df)');
    await t.click(addColumnButton);

    await checkSheet(t, {
        'B': ['1', '2', '3'],
        'C': ['0', '0', '0']
    })
});

