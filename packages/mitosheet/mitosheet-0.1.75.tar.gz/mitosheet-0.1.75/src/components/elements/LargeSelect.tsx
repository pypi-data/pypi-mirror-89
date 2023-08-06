// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React, { Fragment } from 'react';

import '../../../css/large-select.css';

/* 
  A custom select dropdown component created for use in the default taskpane
  The Large Select element is wider than the Small Select element
*/
const LargeSelect = (props: {
    startingValue: string
    optionsArray: string[];
    setValue: (value: string) => void;
  }): JSX.Element => {

    const optionsElements : JSX.Element[] = []
    props.optionsArray.forEach(option => {
      optionsElements.push((<option value={option} key={option}>{option}</option>));
    })

    return (
        <Fragment>
            <select className='large-select' value={props.startingValue} onChange={(e) => props.setValue(e.target.value)}>
                {optionsElements}
            </select>
        </Fragment>
    )
  }

export default LargeSelect
