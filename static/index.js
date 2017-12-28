import React from 'react';
import ReactDOM from 'react-dom'

function Persona(props){
    return <p>Persona name: {props.name}</p>
}

ReactDom.render(
    document.getElementById('root')
);