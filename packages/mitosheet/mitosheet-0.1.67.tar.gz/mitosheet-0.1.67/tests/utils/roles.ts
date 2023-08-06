// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains all roles, which are the predefined ways of logging into
    the mito testing infrastructure.
*/

import { Role } from 'testcafe';

function getRandomInt(max: number): number {
    return Math.floor(Math.random() * Math.floor(max));
}

/*
    NOTE: we log in with a random ID to reduce the odds that mulitple tests
    running at once will conflict with eachother!
*/
const id = 'test' + getRandomInt(10);

export const testUser = Role('http://staging.trymito.io', async t => {
    
    await t
        .typeText('#username_input', id)
        .typeText('#password_input', id)
        .click('#login_submit')
});