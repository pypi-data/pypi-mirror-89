// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains a merging, transforming, and then filtering workflow
*/

import {
    doMerge,
} from './utils/mergeHelpers'

import { 
    applyFiltersToColumn,
    checkColumn,
    createNotebookRunCell,
    deleteAllNotebooks,
} from './utils/helpers';

import {
    addColumnButton,
    renameColumn,
    setFormula
} from './utils/columnHelpers';

import { checkGeneratedCode } from './utils/generatedCodeHelpers';

import { CURRENT_URL } from './config';

fixture `Test Merge Transform Filter Workflow`
    .page(CURRENT_URL)
    .beforeEach( async t => {
        await createNotebookRunCell(t, true, 'import pandas as pd\nimport mitosheet\ndf1 = pd.DataFrame(data={\'id\': [1, 2, 3], \'first_name\': [\'Nate\', \'Aaron\', \'Jake\']})\ndf2 = pd.DataFrame(data={\'id\': [1, 2, 3], \'last_name\': [\'rush\', \'Diamond-Reivich\', \'diamond-reivich\']})\nmitosheet.sheet(df1, df2)');
    })
    .afterEach(async t => {
        // Delete notebook, at the end of the test
        await deleteAllNotebooks(t)
    })

test('Merge Transform Filter', async t => {
    // Do the merge
    await doMerge(t, 'df1', 'id', 'df2', 'id');
    
    // Create a new column
    await t.click(addColumnButton)

    await renameColumn(t, 'D', 'full_name')

    // Set column formula to concat first name and last name
    await setFormula(t, '=CONCAT(first_name, " ", last_name)', 'full_name', '0');

    // then update the last_name column to upper case 
    await setFormula(t, '=UPPER(CONCAT(first_name, " ", last_name))', 'full_name', '0');

    // only keep rows whose full name column contains 'VICH'
    await applyFiltersToColumn(
        t, 
        'full_name', 
        [
            {filterCondition: 'contains', filterValue: 'VICH'},
        ]
    )
    await checkColumn(t, 'full_name', ['AARON DIAMOND-REIVICH', 'JAKE DIAMOND-REIVICH']);

    const expectedDf = {
        'id': ['2', '3'],
        'first_name': ['Aaron', 'Jake'],
        'last_name': ['Diamond-Reivich', 'diamond-reivich'],
        'full_name': ['AARON DIAMOND-REIVICH', 'JAKE DIAMOND-REIVICH']
    }

    await checkGeneratedCode(t, 'df3', expectedDf)
});

