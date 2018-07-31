import React, { Component } from 'react';

class DataSubmissionForm extends Component {
    constructor(props){
        super(props);
        this.state = {
            txtValue:"Paste the contents you would like to have calculated in csv format",
            inputValue:4
        };
        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleTxtChange = this.handleTxtChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(event){
        console.log(this.state.txtValue);
        console.log(this.state.inputValue);
    }

    handleTxtChange(event){
        this.setState({txtValue: event.target.value});
    }

    handleInputChange(event){
        this.setState({inputValue: event.target.value});
    }

    render(){
        return (
            <div className="data-entry-wrapper">
                <form>
                    <textarea value={this.state.txtValue} onChange={this.handleTxtChange}/>
                    <input name="max clusters" type="number" value={this.state.inputValue} onChange={this.handleInputChange}/>
                </form>
                <button onClick={this.handleSubmit}>Submit Data</button>
            </div>
        );
    }
}

export default DataSubmissionForm;