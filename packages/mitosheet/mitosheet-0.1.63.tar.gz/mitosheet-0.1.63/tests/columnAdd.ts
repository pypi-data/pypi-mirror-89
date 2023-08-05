// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/

import { 
    addColumnButton,
    documentationButton,
    documentationSidebarSelector,
    getCellSelector,
} from './utils/selectors';

import { 
    checkColumn,
    checkSheet,
    createNotebookRunCell,
    deleteAllNotebooks,
    setFormula
} from './utils/helpers';
import { testUser } from './utils/roles';



fixture `Column Additions`
    .page `http://staging.trymito.io`
    .beforeEach( async t => {
        await t.useRole(testUser);
        await deleteAllNotebooks(t)
    })
    .afterEach(async t => {
        // Delete notebook, at the end of the test
        await deleteAllNotebooks(t)
    })

test.only('Can add a column when the new column would overlap with the column name', async t => {
    await createNotebookRunCell(t, 'import pandas as pd\nimport mitosheet\ndf = pd.DataFrame(data={\'B\': [1, 2, 3]})\nmitosheet.sheet(df)');
    await t.click(addColumnButton);

    await checkSheet(t, {
        'B': ['1', '2', '3'],
        'C': ['0', '0', '0']
    })
});

test('Can a new column AA', async t => {
    await createNotebookRunCell(t, 'import pandas as pd\nimport mitosheet\ndf = pd.DataFrame(data={i: [1] for i in range(26)})\nmitosheet.sheet(df)');
    await t.click(addColumnButton);

    await checkColumn(t, 'AA', ['0']);
});

