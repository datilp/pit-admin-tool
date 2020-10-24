import React, { Component } from 'react';
import Aux from '../../hoc/Aux/Aux';
import { connect } from 'react-redux';
import { cfpQuery } from '../../store/actions/index';
import Modal from '../../components/UI/Modal/Modal';
import CfPForm from './CfPForm';

//import Spinner from '../../components/UI/Spinner/Spinner';
//import withErrorHandler from '../../hoc/withErrorHandler/withErrorHandler';

class CallForProposals extends Component {

    componentDidMount() {
        // only load from server for first time only
        if (this.props.cfps.currentSem.idx === -1) {
            console.log("CallForProposals/componentDidMount");
            this.props.cfpQuery();
        }
    }

    render() {
        var body = (
            <div>
                <div>
                    <h1>Call For Proposals (CfP) Page</h1>
                </div>
                <div>
                    <CfPForm />
                </div>
            </div>
        );
        var close = () => {
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

const mapStateToProps = (state) => {
    return {
        cfps: state.cfps,
    }
};

export default connect(mapStateToProps, { cfpQuery })(CallForProposals);