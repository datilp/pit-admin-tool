import React from 'react';

import classes from './NavigationItems.module.css';
import NavigationItem from './NavigationItem/NavigationItem';

const navigationItems = ( props ) => (
    <ul className={classes.NavigationItems}>
        <NavigationItem link="/call" exact>Set Call of Proposals</NavigationItem>
        <NavigationItem link="/prep" exact>Prepare Proposals</NavigationItem>
        <NavigationItem link="/send" exact>Send Proposals</NavigationItem>

        {props.isAuthenticated ? <NavigationItem link="/proposals">Proposals</NavigationItem> : null}
        {!props.isAuthenticated
            ? <NavigationItem link="/auth">Sign In</NavigationItem>
            : <NavigationItem link="/logout">Logout</NavigationItem>}
    </ul>
);

export default navigationItems;