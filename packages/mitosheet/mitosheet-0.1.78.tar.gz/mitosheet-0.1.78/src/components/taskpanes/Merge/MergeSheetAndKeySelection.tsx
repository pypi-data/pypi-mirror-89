// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';
import LargeSelect from '../../elements/LargeSelect';

// import css
import '../../../../css/merge-sheet-and-key-selection.css'

/* 
  A custom component that allows you to select a sheet and a column header from that sheet
*/
const MergeSheetAndKeySelection = (props: {
    dfNames: string[],
    sheetIndex: number,
    otherSheetIndex: number,
    setNewSheetIndex: (newSheetIndex: number) => void,
    columnHeaders: string[],
    mergeKey: string,
    setNewMergeKey: (newMergeKey: string) => void,
  }): JSX.Element => {

    // We do not let the user select the other sheet index, so we filter
    // it out of the possible options. 
    const optionsArray = [...props.dfNames]
    //optionsArray.splice(props.otherSheetIndex, 1);

    return (
        <div className='merge-sheet-and-key'>
            <div>
                <p className='default-taskpane-body-section-title-text'>
                    Sheet
                </p>
                <LargeSelect
                    startingValue={props.dfNames[props.sheetIndex]}
                    key={props.sheetIndex} // To update the display when you change selections
                    optionsArray={optionsArray}
                    setValue={(value: string) => {
                        const newSheetIndex = props.dfNames.indexOf(value);
                        props.setNewSheetIndex(newSheetIndex);
                    }}
                />
            </div>
            <div>
                <p className='default-taskpane-body-section-title-text'>
                    Key
                </p>
                <LargeSelect
                    startingValue={props.mergeKey}
                    key={props.mergeKey} // To update the display when you change selections
                    optionsArray={props.columnHeaders}
                    setValue={(newMergeKey: string) => {props.setNewMergeKey(newMergeKey)}}
                />
            </div>
        </div>
    )
} 

export default MergeSheetAndKeySelection