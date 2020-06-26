import React from 'react';

import lbtoLogo from '../../assets/images/lbto-logo.png';
import classes from './Logo.module.css';

const logo = (props) => (
    <div className={classes.Logo} style={{height: props.height}}>
        <img src={lbtoLogo} alt="LBTO" />
    </div>
);

export default logo;