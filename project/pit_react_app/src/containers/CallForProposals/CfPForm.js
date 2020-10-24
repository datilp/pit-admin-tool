import React from 'react';
import './CfPForm.css';
import Datetime from 'react-datetime';
import { connect } from 'react-redux';
import TimeZonePicker from 'react-timezone';
import moment from 'moment';
import "react-datetime/css/react-datetime.css";
import Tooltip from '@atlaskit/tooltip';
import Select, { components } from 'react-select';
import * as actionCreators from "../../store/actions/index";
import Aux from '../../hoc/Aux/Aux';

const DATE_FORMAT="YYYY-MM-DDTHH:mm:ssZ";

function CfPSem(props) {

    // https://react-select.com/components Custom NoOptionsMessage
    // requires
    // npm -i @atlaskit/tooltip styled-components
    const msgStyles = {
        background: 'grey',
        color: 'white',
    };

    const NoOptionsMessage = props => {
        return (
            <Tooltip content="No previous semesters available">
                <components.NoOptionsMessage {...props} />
            </Tooltip>
        );
    };

    //console.log("CfPSem currentSem:", props.currentSem.open, props.currentSem.open === null);
    let header = !props.currentSem.open || props.currentSem.open === null ? `Set ${props.currentSem.semester.year}${props.currentSem.semester.sem} CfP` :
        `Edit ${props.currentSem.semester.year}${props.currentSem.semester.sem} CfP`;
    //console.log("CfPSem header:", header);

    // Does the same thing and makeLabel but on the fly
    /* const formatOptionLabel = data => {
      //console.log("formatOptionLabel:", data);
      return (
        <div>
          <span><b>{`${data.ve.year}${data.ve.sem}`}</b>{` CfP from: ${data.ve.open} to ${data.ve.close} TZ: ${data.ve.tz}`}</span>
        </div>
      )
    };*/

    const makeLabel = (sem) => {
        return (
            <div>
                <span><b>{`${sem.semester.year}${sem.semester.sem}`}</b>{" CfP "} <b>{"from"}</b>{`: ${moment(sem.open).format("dddd, MMMM Do YYYY, h:mm:ss a")}`}
                    <b>{" to "}</b>{`${moment(sem.close).format("dddd, MMMM Do YYYY, h:mm:ss a")} TZ: ${sem.tz}`}</span>
            </div>
        )
        //return `${sem.year}${sem.sem}  CfP from: ${sem.open} to ${sem.close} TZ: ${sem.tz}`;
        //return `<b>${sem.year}${sem.sem}</b> CfP from: ${sem.open} to ${sem.close} TZ: ${sem.tz}`;
    }

    const open_date = props.currentSem.open? 
    moment(props.currentSem.open).format("dddd, MMMM Do YYYY, h:mm:ss a") 
    : "Not Set";
    const close_date = props.currentSem.close? 
    moment(props.currentSem.close).format("dddd, MMMM Do YYYY, h:mm:ss a") 
    : "Not Set";
    const cfp_tz = props.currentSem.tz?
    props.currentSem.tz
    : "Not Set";

    const human_readable_cfp = <div>
    <span><b>{"Open date"}</b>{`: ${open_date}`} <br />
        <b>{"Close date: "}</b>{`${close_date}`} <br />
        <b>{"Time Zone: "}</b>{`${cfp_tz}`}</span>
    </div>
    // sort semesters so the most recent appears first
    // the map each element into a hash
    let options = props.semList.sort(
        (a, b) => {
            const asem = a.semester.year + a.semester.sem;
            const bsem = b.semester.year + b.semester.sem;
            if (asem < bsem) {
                return 1;
            }
            if (asem > bsem) {
                return -1;
            }
            return 0;
        }
    ).map((e, idx) => {
        return {
            value: idx,
            ve: e,
            label: makeLabel(e),
            //color: '#FF5630',
            //isFixed: true,
            // disable semesters that are different from 
            // current one. Say all As or all Bs.
            isDisabled: e.semester.sem !== props.currentSem.semester.sem
        }
    }
    );

    // showSelection and SingleValue are a way
    // to overload components into the react-select
    // component, so once you select your choice
    // only a readable shorthand shows up.
    const showSelection = (data) => {
        return `${data.ve.semester.year}${data.ve.semester.sem}`;
    }

    // Note the capitalization of SingleValue
    // This is because the one of the component
    // properties is SingleValue
    // So instead of having 
    // { SingleValue: singleValue}
    // we can just have
    // { SingleValue } and will magically be 
    //  equivalent to the above key/value pair.
    const SingleValue = props => (
        <components.SingleValue {...props}>
            {showSelection(props.data)}
        </components.SingleValue>
    );

    return (

        <div className="cblock">
            <h2>{header}</h2>
            <div className="Cfp cblock">
                <ul>
                    <li key="1">
                        <Datetime
                            // Is important that "key" is different if the date 
                            // has changed otherwise it will not update the obj.
                            key={props.currentSem.open}
                            closeOnSelect="true"
                            onChange={(e) => {
                                //console.log("Datetime change:", e);
                                props.dateUpdate(e, null);
                            }}
                            //inputProps={{ disabled: false }}
                            initialValue={moment(props.currentSem.open, DATE_FORMAT)}
                            initialViewDate={moment(props.currentSem.open, DATE_FORMAT)}
                        />
                    </li>
                    <li key="2">
                        <Datetime key={props.currentSem.close}
                            closeOnSelect="true"
                            onChange={(e) => {
                                //console.log("Datetime change:", e);
                                props.dateUpdate(null, e);
                            }}
                            initialValue={moment(props.currentSem.close, DATE_FORMAT)}
                            initialViewDate={moment(props.currentSem.close, DATE_FORMAT)}
                        />
                    </li>
                    <li key="3" className="Cfpdiv2">
                        {/* look at react-select for an alternative combobox */}
                        <TimeZonePicker
                            value={props.currentSem.tz}
                            onChange={props.tzOnChange}
                            inputProps={{
                                placeholder: 'Select Timezone ....',
                                name: 'timezone',
                            }}
                        />
                    </li>
                </ul>
            </div>
            <div className="cblock">
                    <p>{human_readable_cfp}</p>
            </div>
            <div className="Cfpdiv3">
                <h3>Or copy from a previous semester</h3>
                <div className="cblock">
                    <Select
                        //value={selectedOption}
                        onChange={props.copySemSelectionChange}
                        options={options}
                        placeholder={'Select from previous CfPs ...'}
                        //options={[]}
                        styles={{ NoOptionsMessage: base => ({ ...base, ...msgStyles }) }}
                        //formatOptionLabel={formatOptionLabel}
                        components={{ SingleValue, NoOptionsMessage }}
                    //getOptionValue={option => option.value}
                    />
                </div>
            </div>

        </div>
    )
}


class CfPForm extends React.Component {

    // passed in as props to CfPSem, call on the time picker selection
    // for open and close dates.
    dateUpdate = (open, close) => {

        if (open || close) {
            //console.log("dateUpdate2 idx=", this.props.currentSem.idx);
            //console.log("dateUpdate2 idx=", this.props.currentSem.idx, " open:", open.format("YYYY-MM-DD HH:mm:ss"));
            // if idx not defined use the last element?
            let sem = { ...this.props.cfps.currentSem };
            if (open) {
                sem = { ...sem, open: open.format(DATE_FORMAT) };
            }
            if (close) {
                sem = { ...sem, close: close.format(DATE_FORMAT) };
            }

            // Copy the array. Two ways of doing it
            // with Object.assign or using slice()
            //Object.assign([], semList, {idx: sem});
            const newsemList = this.props.cfps.semList.slice();
            //console.log("dateUpdate3:", newsemList, sem);
            newsemList[sem.idx] = sem;

            this.props.updateState({ semList: newsemList, currentSem: sem });
        }
    }

    // passed in as props to CfPSem, called on the selection dropdown
    // It'll copy the selected semester to the current one
    copySemSelectionChange = (e) => {
        //console.log("copySemSelectionChange select dropdown:", e);
        const sem = e.ve;

        const csem = { ...this.props.cfps.currentSem };
        //console.log("currentSem1:", csem);
        const addYears = Math.abs(csem.semester.year - sem.semester.year);
        //console.log("add years:", addYears);

        csem.open = moment(sem.open, DATE_FORMAT)
            .add(addYears, 'year').format(DATE_FORMAT);
        csem.close = moment(sem.close, DATE_FORMAT)
            .add(addYears, 'year').format(DATE_FORMAT);
        csem.tz = sem.tz;
        //console.log("currentSem2:", csem);

        const newsemList = this.props.cfps.semList.slice();
        newsemList[csem.idx] = csem;
        this.props.updateState({ currentSem: csem, semList: newsemList });
    }

    // passed in as props to CfPSem, called on the TZ selection dropdown
    tzOnChange = (tz) => {
        //console.log('New Timezone selected:', tz);
        this.props.updateState({ currentSem: { ...this.props.cfps.currentSem, tz: tz } });
    };


    render() {
        //console.log("CfPForm render: ", this.props);
        
        // First time around, if semester is null
        // ignore it.
        const saveButton = this.props.cfps.currentSem && this.props.cfps.currentSem.open ?
            <button onClick={() => this.props.saveCfP(this.props.cfps)}>{"Save CfP"}</button> :
            null;

        if (this.props.cfps.currentSem.semester) {
            return (
            <Aux>
                <CfPSem
                    currentSem={{ ...this.props.cfps.currentSem }}
                    semList={this.props.cfps.semList.slice()}
                    dateUpdate={this.dateUpdate}
                    tzOnChange={this.tzOnChange}
                    copySemSelectionChange={this.copySemSelectionChange}
                />
                <div className="cblock save">
                {saveButton}
                </div>
            </Aux>);

        } else {
            return null;
        }
    }
}

const mapStateToProps = (state) => {
    return {
        cfps: state.cfps,
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        updateState: (state) => {
            dispatch(actionCreators.cfpSetState(state))
        },
        saveCfP: (state) => {
            dispatch(actionCreators.cfpSaveToDB(state))
        }
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(CfPForm);
