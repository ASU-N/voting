import React, { useEffect, useState } from 'react';
import './home.css';
import axios from 'axios';

export default function Home() {
    const [candidates, setCandidates] = useState([]);
    const [timeLeft, setTimeLeft] = useState({ hours: 0, minutes: 0, seconds: 0 });

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/get_candidates/')
            .then(response => {
                setCandidates(response.data);
            })
            .catch(error => {
                console.error('Error fetching candidates:', error);
            });

        // Set the end time for the countdown (e.g., 24 hours from now)
        const endTime = new Date().getTime() + (24 * 60 * 60 * 1000); // 24 hours from now

        const updateTimer = () => {
            const now = new Date().getTime();
            const distance = endTime - now;

            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            setTimeLeft({ hours, minutes, seconds });

            if (distance < 0) {
                clearInterval(timerInterval);
                setTimeLeft({ hours: 0, minutes: 0, seconds: 0 });
                alert('Voting has ended!');
            }
        };

        const timerInterval = setInterval(updateTimer, 1000);

        // Cleanup timer interval on component unmount
        return () => clearInterval(timerInterval);
    }, []);

    const handleVote = (candidateId) => {
        const voterId = sessionStorage.getItem('voterId'); // Retrieve the actual voter ID from session storage or a similar method

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
            <div className="countdown">
                Time left: {timeLeft.hours}h {timeLeft.minutes}m {timeLeft.seconds}s
            </div>
            {candidates.map(candidate => (
                <div className="vote" key={candidate.id}>
                    <div className="info">
                        <div className="text">
                            <p>Name: {candidate.name}</p>
                            <p>Party: {candidate.party}</p>
                        </div>
                        <img src={`http://127.0.0.1:8000${candidate.image}`} alt="Candidate Profile" />
                    </div>
                    <button onClick={() => handleVote(candidate.id)}>Vote Now</button>
                </div>
            ))}
        </div>
    );
}
