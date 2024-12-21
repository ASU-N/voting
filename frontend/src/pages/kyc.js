import React from 'react';
import '../css/styles.css';
import candidates from '../data/candidate';
import Timer from '../components/timer'; // Import the Timer component

function Kyc(){   
    return(
        <div>
            {/* <Navbar/> */}
            <main className="content">
                <h2>Manifesto</h2>

                <Timer /> {/* Timer component */}

                {/* This is array of candidates */}
                {candidates.map((candidate, index) => (
                    <div key={index}> {/* Added key attribute for each candidate */}
                        <div className="manifesto-card">
                            <img src={candidate.imageUrl} alt="Candidate" className="candidate-image" />
                            <div className="candidate-info">
                                <p><strong>{candidate.name}</strong></p>
                                <p>{candidate.party}</p>
                            </div>
                            <blockquote className="manifesto-text">
                                {candidate.manifesto}
                            </blockquote>
                        </div>

                        <section className="promises-section">
                            <h3>My Promises to You</h3>
                            <ol>
                                {candidate.promises.map((promise, promiseIndex) => (
                                    <li key={promiseIndex}>
                                        <strong>{promise.title}</strong>
                                        <ul>
                                            {promise.points.map((point, pointIndex) => (
                                                <li key={pointIndex}>{point}</li>
                                            ))}
                                        </ul>
                                    </li>
                                ))}
                            </ol>
                        </section>
                    </div>
                ))}
            </main>
        </div>
    );
}

export default Kyc;
