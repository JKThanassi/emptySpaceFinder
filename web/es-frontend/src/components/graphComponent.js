import React, { Component } from 'react';
import { XYPlot, MarkSeries } from 'react-vis';

class EsGraph extends Component {
    render(){
        return(
            <div className="graph">
                <XYPlot height={300} width={300}>
                    <MarkSeries data={this.props.data}/>
                </XYPlot>
            </div>
        )
    }
}

export default EsGraph;