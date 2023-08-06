// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/*
    Contains initial tests for logging in, whcih also is responsible for
    setting up the kuberenetes pod, so the rest of the tests pass

    NOTE: this file is prefixed with aaa so it runs first.
*/


import { testUser } from './utils/roles';

import { CURRENT_URL } from './config';

fixture `Log In`
    .page(CURRENT_URL)
    
test('Log in', async t => {
    await t.useRole(testUser)
    await t.wait(25000) // wait 25 seconds
});

