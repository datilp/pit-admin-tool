import React from 'react';

import classes from './NavigationItems.module.css';
import NavigationItem from './NavigationItem/NavigationItem';

const navigationItems = ( props ) => (
    <ul className={classes.NavigationItems}>
        
        {props.isAuthenticated
        ?
        <NavigationItem link="/callForProposals" exact>Call of Proposals</NavigationItem>
        : null}
        {props.isAuthenticated
        ?
        <NavigationItem link="/adminProposals" exact>Admin Proposals</NavigationItem>
        : null}

        {!props.isAuthenticated
            ? <NavigationItem link="/">Sign In</NavigationItem>
            : <NavigationItem link="/logout">Logout</NavigationItem>}
    </ul>
);

export default navigationItems;