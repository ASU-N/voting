import React from 'react';
import Timer from '../components/timer'; // Import the Timer component

const Guidelines = () => {
    return (
        <div className="guidelinesPage">
            <Timer /> {/* Timer component */}
            <h2>Guidelines</h2>
            <p>Welcome to the voting guidelines page. Here you will find all the information you need to cast your vote:</p>
            <ol>
                <li>Register yourself using your unique voter ID.</li>
                <li>Use face recognition to verify your identity.</li>
                <li>Review the list of candidates and their manifestos.</li>
                <li>Cast your vote using the "Vote Now" button under your chosen candidate.</li>
                <li>Remember, voting ends when the countdown reaches zero!</li>
            </ol>
        </div>
    );
};

export default Guidelines;
