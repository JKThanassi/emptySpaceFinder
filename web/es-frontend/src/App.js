import React, { Component } from 'react';
import './App.css';
import DataSubmissionForm from './components/dataSubmissionForm'
import EsGraph from './components/graphComponent'

class App extends Component {
  constructor(props){
    super(props);
    this.state = {children:[<DataSubmissionForm key={0} handleSubmit={this.handleSubmit}/>, <EsGraph key={1} data={[{x:1,y:0, size:5}, {x:3, y:4, size:2}]}/>]}
  
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">Empty Space Finder</h1>
        </header>
        {this.state.children}
      </div>
    );
  }
}

export default App;
