import React, { useEffect, useState } from 'react';
import './home.css';
import axios from 'axios';
import Timer from '../components/timer'; // Adjusted import path

export default function Home() {
    const [candidates, setCandidates] = useState([]);
    const [votingEnded, setVotingEnded] = useState(false); // New state to track if voting has ended

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/get_candidates/')
            .then(response => {
                setCandidates(response.data);
            })
            .catch(error => {
                console.error('Error fetching candidates:', error);
            });
    }, []);

    const handleVote = (candidateId) => {
        const voterId = localStorage.getItem('voterId'); // Retrieve the voter ID from local storage

        axios.post('http://127.0.0.1:8000/cast_vote/', { candidate_id: candidateId, voter_id: voterId })
            .then(response => {
                if (response.data.success) {
                    alert('Vote cast successfully!');
                } else {
                    alert('Failed to cast vote: ' + response.data.message);
                }
            })
            .catch(error => {
                console.error('Error casting vote:', error);
                alert('An error occurred while casting vote.');
            });
    };

    return (
        <div className="votingSection">
            <Timer setVotingEnded={setVotingEnded} /> {/* Pass setVotingEnded to Timer component */}
            {candidates.map(candidate => (
                <div className="vote" key={candidate.id}>
                    <div className="info">
                        <div className="text">
                            <p>Name: {candidate.name}</p>
                            <p>Party: {candidate.party}</p>
                        </div>
                        <img src={`http://127.0.0.1:8000${candidate.image}`} alt="Candidate Profile" />
                    </div>
                    <button onClick={() => handleVote(candidate.id)} disabled={votingEnded}>Vote Now</button>
                </div>
            ))}
        </div>
    );
}
