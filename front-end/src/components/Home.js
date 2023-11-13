import { useEffect, useState, useRef } from 'react';
import { collection, getDocs } from 'firebase/firestore';
import { db, auth } from '../firebase';
import { Link } from "react-router-dom";
import React from 'react';
import ReactDOM from 'react-dom';
import { FaMicrophone } from 'react-icons/fa';
import '../styles/Home.css';
import { BsRecordCircleFill } from 'react-icons/bs'; // Assuming this is the red icon


import MicRecorder from 'mic-recorder-to-mp3';

function ToggleButton({ label, isRotated, isPatient }) {
    const [isActive, setIsActive] = useState(false);
    const [audioBlob, setAudioBlob] = useState(null);
    const [isReadyToSend, setIsReadyToSend] = useState(false);
    const recorder = useRef(new MicRecorder({ bitRate: 128 }));

    const handleClick = async () => {
        if (!isActive) {
            try {
                await recorder.current.start();
                setIsActive(true);
            } catch (error) {
                console.error('Error starting recording:', error);
            }
        } else {
            recorder.current.stop().getMp3().then(([buffer, blob]) => {
                const audioURL = URL.createObjectURL(new Blob([blob], { type: 'audio/mp3' }));
                setAudioBlob(new Blob([blob], { type: 'audio/mp3' }));
                setIsActive(false);
                setIsReadyToSend(true);
            }).catch((e) => {
                console.error('Error stopping recording:', e);
            });
        }
    };

    const sendAudioToServer = async () => {
        if (audioBlob && isReadyToSend) {
            try {
                const formData = new FormData();
                formData.append("file", audioBlob, "recording.mp3");

                const endpoint = isPatient
                    ? 'https://medgt-backend.onrender.com/patient-speaks'
                    : 'https://medgt-backend.onrender.com/doctor-speaks';

                const response = await fetch(endpoint, {
                    method: 'POST',
                    body: formData,
                });

                if (response.ok) {
                    const responseBlob = await response.blob();
                    playReceivedAudio(responseBlob);
                    console.log('Audio received successfully');
                } else {
                    console.error('Server error:', response);
                }
            } catch (error) {
                console.error('Error in sending:', error);
            }

            setAudioBlob(null);
            setIsReadyToSend(false);
        }
    };

    const playReceivedAudio = (audioBlob) => {
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        audio.play();
        console.log('Playing the received audio...');
    };

    // Function to test playback of the recorded audio
    const testPlayback = () => {
        if (audioBlob) {
            const audioUrl = URL.createObjectURL(audioBlob);
            const audio = new Audio(audioUrl);
            audio.play();
            console.log('Testing the recorded audio playback...');
        } else {
            console.log('No recorded audio to test.');
        }
    };

    const rotationClass = isRotated ? 'rotate-180' : '';

    return (
        <div className={`flex flex-col items-center mb-4 ${rotationClass} transform`}>
            <button onClick={handleClick} className={`flex items-center justify-center w-48 h-20 bg-white text-gray-700 font-semibold rounded-lg shadow-md hover:shadow-lg transition duration-300 ease-in-out ${isActive ? 'bg-red-100 hover:bg-red-200 text-red-700' : ''}`}>
                {isActive ? <BsRecordCircleFill className="text-red-500" /> : <FaMicrophone className="text-green-500" />}
                <span className="ml-2">{label}</span>
            </button>

            <button
                onClick={sendAudioToServer}
                className="mt-4 w-48 h-10 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-600"
            >
                Translate
            </button>

            <button
                onClick={testPlayback}
                className="mt-4 w-48 h-10 bg-yellow-500 text-white font-semibold rounded-lg shadow-md hover:bg-yellow-600"
            >
                Test Playback
            </button>
        </div>
    );
}

export default function App({ user, language }) {

    console.log(language)

    return (
        <div className="flex flex-col items-center justify-center bg-cover bg-center h-screen space-y-60" style={{ backgroundImage: "url('https://cdn.builder.io/api/v1/image/assets/TEMP/7966c460-a2cd-49b6-8e55-8965ae56e831?apiKey=be43af7b4ce2472eaff8e8a17c078188&')" }}>
            <ToggleButton label="Patient" isRotated={true} isPatient={true} />
            <ToggleButton label="Doctor" isPatient={false} />
            {/* <Link id="signout" className="FormButton" to="/"
                onClick={() => auth.signOut()}>{language}
            </Link> */}
        </div>
    );
}


// backgroundImage: "url('https://cdn.builder.io/api/v1/image/assets/TEMP/7966c460-a2cd-49b6-8e55-8965ae56e831?apiKey=be43af7b4ce2472eaff8e8a17c078188&')"


