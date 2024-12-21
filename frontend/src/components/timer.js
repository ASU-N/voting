import React, { useEffect, useState } from 'react';

const Timer = () => {
    const [timeLeft, setTimeLeft] = useState({ hours: 0, minutes: 0, seconds: 0 });
    const [votingEnded, setVotingEnded] = useState(false);

    useEffect(() => {
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
                setVotingEnded(true);
                alert('Voting has ended!');
            }
        };

        const timerInterval = setInterval(updateTimer, 1000);

        return () => clearInterval(timerInterval);
    }, []);

    return (
        <div className="countdown">
            Time left: {timeLeft.hours}h {timeLeft.minutes}m {timeLeft.seconds}s
        </div>
    );
};

export default Timer;
