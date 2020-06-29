import React, { Component } from 'react';
import Aux from '../../hoc/Aux/Aux';
import Modal from '../../components/UI/Modal/Modal';
import Spinner from '../../components/UI/Spinner/Spinner';
import withErrorHandler from '../../hoc/withErrorHandler/withErrorHandler';
class ShowProposals extends Component {

    render() {
        var body = (
            <div>
                <h1>Administrate Proposals Page</h1>
            </div>
        );
        var close=() => {
            console.log("closing");
        }
        return (
            <Aux>
                <Modal show={false} modalClose={close}>

                </Modal>
                {body}
            </Aux>
        )

    }

}

export default ShowProposals;