// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/


import { 
    getCellSelector,
} from './utils/selectors';

import { 
    createNotebookRunCell,
    deleteAllNotebooks,
} from './utils/helpers';

import {
    addColumnButton,
    setFormula
} from './utils/columnHelpers';

import { CURRENT_URL } from './config';

fixture `Test Large Data Set Functionality`
    .page(CURRENT_URL)
    .beforeEach( async t => {
        // Make a dataframe w/ 1M rows
        await createNotebookRunCell(t, true, 'import pandas as pd\nimport mitosheet\ndf = pd.DataFrame({\'A\': [\'A\' * 100] * 1000000})\nmitosheet.sheet(df)');
    })
    .afterEach(async t => {
        // Delete notebook, at the end of the test
        await deleteAllNotebooks(t)
    })

test('Allows you to add a formula to a large dataset', async t => {
    await t.click(addColumnButton)
    await setFormula(t, '=100', 'B', '0')
    await t.expect(getCellSelector('B', '0').innerText).eql('100')
});
   