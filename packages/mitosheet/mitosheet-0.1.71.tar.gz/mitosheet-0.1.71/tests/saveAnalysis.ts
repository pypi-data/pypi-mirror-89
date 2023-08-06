// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for basic, single sheet mito rendering, column additions,
    and column editing.
*/


import {
    addColumnButton,
    getColumnHeaderContainerSelector,
} from './utils/columnHelpers';

import { 
    createNotebookRunCell,
    deleteAllNotebooks,
} from './utils/helpers';

import { saveAnalysis } from './utils/saveAnalysisHelpers';
import { repeatAnalysis } from './utils/repeatAnalysisHelpers';

import { CURRENT_URL } from './config';

const code = 'import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={\'A\': [1, 2, 3]})\nmitosheet.sheet(df1)';

fixture `Test Save and Repeat`
    .page(CURRENT_URL)
    .beforeEach( async t => {
        await createNotebookRunCell(t, true, code);
    })
    .afterEach(async t => {
        // Delete notebook, at the end of the test
        await deleteAllNotebooks(t)
    })

// Generate a random ID to save the test
const randomId = '_' + Math.random().toString(36).substr(2, 9);

test('Save analysis saves, repeat analysis repeats', async t => {
    await t.click(addColumnButton)

    await saveAnalysis(t, randomId)

    // Reset the notebook
    await createNotebookRunCell(t, false, code);
    await t.wait(1000) // wait a bit to avoid weirdness

    // Repeat the analysis on this new blank notebook
    await repeatAnalysis(t, randomId)

    await t.expect(getColumnHeaderContainerSelector('B').exists).ok()
});
   