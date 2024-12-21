import React, { useState, useEffect } from 'react';
import axios from 'axios';

const VotingPage = () => {
  const [candidates, setCandidates] = useState([]);
  const [selectedCandidate, setSelectedCandidate] = useState('');
  const [votingId, setVotingId] = useState('');

  // Fetch candidates from backend
  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/candidates/')
      .then(response => {
        setCandidates(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching candidates!', error);
      });
  }, []);

  // Handle vote submission
  const handleVoteSubmit = (event) => {
    event.preventDefault();
    const data = {
      voting_id: votingId,
      candidate: selectedCandidate,
    };
    axios.post('http://127.0.0.1:8000/api/votes/', data)
      .then(response => {
        alert('Vote submitted!');
      })
      .catch(error => {
        console.error('There was an error submitting the vote!', error);
      });
  };

  return (
    <div>
      <h1>Voting Page</h1>
      <form onSubmit={handleVoteSubmit}>
        <label>
          Voting ID:
          <input
            type="text"
            value={votingId}
            onChange={(e) => setVotingId(e.target.value)}
            placeholder="Enter your Voting ID"
          />
        </label>
        <div>
          <label>Select Candidate:</label>
          <select
            value={selectedCandidate}
            onChange={(e) => setSelectedCandidate(e.target.value)}
          >
            <option value="">--Choose Candidate--</option>
            {candidates.map((candidate) => (
              <option key={candidate.id} value={candidate.id}>
                {candidate.name}
              </option>
            ))}
          </select>
        </div>
        <button type="submit">Submit Vote</button>
      </form>
    </div>
  );
};

// Only one default export allowed in the file
export default VotingPage;
