

/*
    These ENV variables are set in the npm test scripts. To run a test locally, simply
    call npm run test:local. By default, tests run on the remote server.
*/
export const JUPYTER_LAB_LOCAL_TOKEN = process.env.JUPYTER_LAB_LOCAL_TOKEN;
export const LOCAL_TEST = process.env.LOCAL_TEST === 'True';

export const LOCAL_URL = 'http://localhost:8888/lab/tree/examples/tests?token=' + JUPYTER_LAB_LOCAL_TOKEN;
export const REMOTE_URL = 'https://staging.trymito.io'

export const CURRENT_URL = LOCAL_TEST ? LOCAL_URL : REMOTE_URL;