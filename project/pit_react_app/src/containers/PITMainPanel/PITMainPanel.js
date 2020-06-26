import React, { Component } from 'react';
import Aux from '../../hoc/Aux/Aux';
import Modal from '../../components/UI/Modal/Modal';
import Spinner from '../../components/UI/Spinner/Spinner';
import withErrorHandler from '../../hoc/withErrorHandler/withErrorHandler';
class PITMainPanel extends Component {

    render() {
        var login = (
            <div>
                <h1>This is the MAIN Panel</h1>
            </div>
        );
        var close=() => {
            console.log("closing");
        }
        return (
            <Aux>
                <Modal show={false} modalClose={close}>

                </Modal>
                {login}
            </Aux>
        )

    }

}

export default PITMainPanel;