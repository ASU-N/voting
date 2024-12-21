import React, { useEffect, useState } from 'react';
//import './results.css'; 
import axios from 'axios';

const Results = () => {
    const [results, setResults] = useState([]);

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/get_results/')
            .then(response => {
                setResults(response.data);
            })
            .catch(error => {
                console.error('Error fetching results:', error);
            });
    }, []);

    return (
        <div className="resultsSection">
            <h2>Election Results</h2>
            <div className="resultsList">
                {results.map((result, index) => (
                    <div className="resultCard" key={index}>
                        <p><strong>{result.name}</strong></p>
                        <p>Party: {result.party}</p>
                        <p>Votes: {result.vote_count}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Results;
