// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains tests for importing data.
*/


import {
    checkSheets,
    createNotebookRunCell,
    deleteAllNotebooks,
} from './utils/helpers';

import {
    doRawPythonImport,
    doSimpleImport,
    importButton
} from './utils/importHelpers';
import { repeatAnalysis, repeatAnalysisButton, repeatAnalysisChangeImports } from './utils/repeatAnalysisHelpers';
import { saveAnalysis, saveButton } from './utils/saveAnalysisHelpers';

const code = `
import pandas as pd
import mitosheet

df1 = pd.DataFrame(data={'A': [1, 2, 3], 'B': [4, 5, 6]})
df1.to_csv("df1.csv", index=False)

df2 = pd.DataFrame(data={'A': [7, 8, 9], 'B': [10, 11, 12]})
df2.to_csv("df2.csv", index=False)

mitosheet.sheet()
`
import { CURRENT_URL } from './config';
import { deleteColumnButton, documentationButton, downloadSheetButton, undoButton } from './utils/selectors';
import { pivotButton } from './utils/pivotHelpers';
import { mergeButton } from './utils/mergeHelpers';

fixture `Test Sheet Crashing Prevention`
    .page(CURRENT_URL)
    .beforeEach( async t => {
        await createNotebookRunCell(t, true, code);
    })
    .afterEach(async t => {
        // Delete notebook, at the end of the test
        await deleteAllNotebooks(t)
    })

test('Can click modal buttons with an empty sheet then do a simple import', async t => {
    // click the edit button 
    await t.click(undoButton);

    // click the delete button 
    await t.click(deleteColumnButton);

    // click the download button
    await t.click(downloadSheetButton)

    // click the pivot button 
    await t.click(pivotButton);

    // click the pivot button 
    await t.click(mergeButton);

    // click the save analysis button
    await t.click(saveButton);

    // click repeat analysis button
    await t.click(repeatAnalysisButton);

    // click the documentation button 
    await t.click(documentationButton);

    // then do an import 
    await doSimpleImport(t, ['df1.csv', 'df2.csv'])
    await checkSheets(t, {
        'df1_csv': {
            'A': ['1', '2', '3'],
            'B': ['4', '5', '6']
        },
        'df2_csv': {
            'A': ['7', '8', '9'],
            'B': ['10', '11', '12']
        }
    })
});
