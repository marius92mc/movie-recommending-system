import React, { Component } from 'react';
import AutoCompleter from 'react-autocompleter';


const styles = {
	root: {
		padding: '5px'
	},
	input: {
		padding: '10px',
		width: '250px',
		fontSize: '12px'
	},
	listContainer: {
		listStyleType: 'none',
		background: '#ffffff',
		padding: '10px',
		margin: 0
	},
	listItems: {
		padding: '10px',
		'.active': {
			fontSize: '20px'
		}
	}
};


class Autocomplete extends Component {

	constructor(props) {
		super(props);
	}

	state = {
		value: ''
	};

	updateValue = (value) => {
		console.log('Value updated', value);
		this.setState({
			value
		});
	}

	render() {
		return (
			<div>
				<AutoCompleter
					data={ this.props.data }
					placeholder={ this.props.placeholder }
					onSelect={ (item) => { console.log('Selected', item); } }
					onFocus={ () => { console.log('Focused'); } }
					onBlur={ () => { console.log('Blurred'); } }
					onChange={ this.updateValue }
					limit={ 5 }
					classes={ {
            root: 'autocomplete',
            input: 'autocomplete-input',
            listContainer: 'autocomplete-container',
            listItems: 'autocomplete-items'
                } }
					styles={ {
						...styles
                	} }
					inputProps={ {
						name: 'url',
						autoComplete: 'off'
					} }
				/>
			</div>
		);
	}
}

export default Autocomplete;