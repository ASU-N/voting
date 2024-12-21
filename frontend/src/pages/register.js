import React, { useState } from 'react';
import axios from 'axios';
import { useHistory } from 'react-router-dom';
import './register.css';

const Register = () => {
    const [voterId, setVoterId] = useState('');
    const [image, setImage] = useState(null);
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const history = useHistory();

    const handleImageChange = (e) => {
        setImage(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        const formData = new FormData();
        formData.append('voter_id', voterId);
        formData.append('image_path', image);

        try {
            const response = await axios.post('http://127.0.0.1:8000/api/register/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setLoading(false);
            setMessage(response.data.message);
            setError('');
            // Redirect to /home after successful registration
            if (response.data.success) {
                history.push('/home');
            }
        } catch (error) {
            setError('There was an error processing your request. Please try again.');
            setMessage('');
            setLoading(false);
        }
    };

    return (
        <div className="register-container">
            <h1>Register</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Voter ID</label>
                    <input
                        type="text"
                        value={voterId}
                        onChange={(e) => setVoterId(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Image</label>
                    <input type="file" onChange={handleImageChange} required />
                </div>
                <button type="submit" disabled={loading}>
                    {loading ? 'Registering...' : 'Register'}
                </button>
            </form>
            {message && <p style={{ color: 'green' }}>{message}</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
    );
};

export default Register;
