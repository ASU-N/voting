import '../css/styles.css';
// import Navbar from './components/navbar';
import candidates from '../data/candidate';


function Kyc(){   
    return(
        <div>
            {/* <Navbar/> */}
            <main className="content">
                <h2>Manifesto</h2>

                {/* This is array of candidates */}
                {candidates.map((candidate, index) => (
                    <div>
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
                                {candidate.promises.map((promise, index) => (
                                    <li key={index}>
                                        <strong>{promise.title}</strong>
                                        <ul>
                                            {promise.points.map((point, idx) => (
                                                <li key={idx}>{point}</li>
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