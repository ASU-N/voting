import './login.css';
import votingImage from '../assets/login.png';
import {useState,useEffect, act} from 'react';
import axios from 'axios';
import ToggleButton from '../components/toggleButton';

export default function RootLayout(){
    
    const [votingId,setVotingId]=useState('');
    const [action ,setAction]=useState('register');

    const handleToggle=(text)=>{
        setAction(text);
        console.log('Action:'+text);
    }
    

   const handleSubmission=(event)=>{      
    
    event.preventDefault();

    console.log(action);
    alert(
        action
    )
    
    axios.post('https://hello.com',{votingId,action})
    .then(response=>console.log(response))
    .catch(error=>console.log(error))

   }


    return (
        <div className='login-container'>
            <div className="container">
                <div className="image-section">
                    <img src={votingImage} alt="Voting Illustration" />

                </div>

                <form className="form-section" >
                    <div className='toggle-button'>
                    <ToggleButton  onToggle={handleToggle} /> 
                    </div>
                    <div className='form-info'>
                        <h2>Enter Your Voting ID</h2>
                        <input type="text" placeholder="Enter your Voting Id here" value={votingId} onChange={({target})=>{setVotingId(target.value)}} />
                        <div className="button-container">
                            <button onClick={handleSubmission}>Continue</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
      );
}
