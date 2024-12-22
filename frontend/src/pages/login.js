import './login.css';
import votingImage from '../assets/login.png';
import { useState, useRef } from 'react';
import axios from 'axios';
import { useHistory } from 'react-router-dom';
import Webcam from 'react-webcam'; // Using react-webcam for demonstration

export default function Login() {
    const [votingId, setVotingId] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [message, setMessage] = useState('');
    const webcamRef = useRef(null);
    const history = useHistory();

    const handleSubmission = async (event) => {
        event.preventDefault();
        setLoading(true);
        setError('');
        setMessage('');

        // Example of capturing an image using react-webcam
        const imageSrc = webcamRef.current.getScreenshot(); // Using react-webcam for demonstration

        const formData = new FormData();
        formData.append('voter_id', votingId);
        formData.append('image', imageSrc);

        try {
            const response = await axios.post('http://127.0.0.1:8000/face_recognition/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setLoading(false);
            if (response.data.success) {
                setMessage(response.data.message);
                // Save tokens to local storage
                localStorage.setItem('accessToken', response.data.access);
                localStorage.setItem('refreshToken', response.data.refresh);
                history.push('/home'); // Redirect to /home after successful login
            } else {
                setError(response.data.message);
            }
        } catch (error) {
            console.error(error);
            setLoading(false);
            setError('There was an error processing your request. Please try again.');
        }
    };

    return (
        <div className='login-container'>
            <div className="container">
                <div className="image-section">
                    <img src={votingImage} alt="Voting Illustration" />
                </div>

                <form className="form-section" onSubmit={handleSubmission}>
                    <div className='form-info'>
                        <h2>Enter Your Voting ID</h2>
                        <input
                            type="text"
                            placeholder="Enter your Voting ID here"
                            value={votingId}
                            onChange={({ target }) => setVotingId(target.value)}
                            required
                        />
                        <div className="webcam-container">
                            {/* Webcam component from face recognition package or react-webcam */}
                            <Webcam
                                audio={false}
                                ref={webcamRef}
                                screenshotFormat="image/jpeg"
                            />
                        </div>
                        {error && <p style={{ color: 'red' }}>{error}</p>}
                        {message && <p style={{ color: 'green' }}>{message}</p>}
                        <div className="button-container">
                            <button type="submit" disabled={loading}>{loading ? 'Processing...' : 'Continue'}</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    );
}
