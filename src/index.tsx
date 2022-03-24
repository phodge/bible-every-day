import * as React from 'react';
import * as ReactDOM from "react-dom";

import {WelcomeMessage} from './welcome.js';

export const begin = () => {
    ReactDOM.render(
        <WelcomeMessage />,
        document.getElementById('app-root')
    );
};
