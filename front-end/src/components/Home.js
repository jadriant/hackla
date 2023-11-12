import { useEffect, useState, useRef } from 'react';
import { collection, getDocs } from 'firebase/firestore';
import { db, auth } from '../firebase';
import { Link } from "react-router-dom";
import React from 'react';
import ReactDOM from 'react-dom';
import { FaMicrophone } from 'react-icons/fa';
import '../styles/Home.css';
import { BsRecordCircleFill } from 'react-icons/bs'; // Assuming this is the red icon


function ToggleButton({ label, isRotated }) {
    const [isActive, setIsActive] = useState(false);
    const [audioBlob, setAudioBlob] = useState(null);
    const mediaRecorderRef = useRef(null); // Ref to hold the MediaRecorder instance

    // Function to toggle recording on and off
    const handleClick = async () => {
        // If currently not active, start recording
        if (!isActive) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                const recorder = new MediaRecorder(stream);
                mediaRecorderRef.current = recorder;

                recorder.ondataavailable = (event) => {
                    setAudioBlob(event.data);
                };

                recorder.start();
                setIsActive(true); // Set isActive to true to indicate recording has started
            } catch (error) {
                console.error('Error starting recording:', error);
            }
        } else {
            // If currently active, stop recording
            if (mediaRecorderRef.current) {
                mediaRecorderRef.current.stop();
                setIsActive(false); // Set isActive to false to indicate recording has stopped
                // After stopping, send the audio to the server
                sendAudioToServer();
            }
        }
    };

    // Function to send the audio file to the server
    const sendAudioToServer = async () => {
        if (audioBlob) {
            // Convert the Blob to a base64 string
            const reader = new FileReader();
            reader.readAsDataURL(audioBlob);
            reader.onloadend = async () => {
                const base64AudioMessage = reader.result.split(',')[1]; // Split to remove the data URL header

                try {
                    // Send the base64 audio string to the server with the correct key
                    const response = await fetch('/doctor-speaks', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ input_audio: base64AudioMessage }),
                    });
                    if (response.ok) {
                        console.log('Audio sent successfully');
                        // Handle successful response
                    } else {
                        console.error('Server error:', response);
                        // Handle server errors here
                    }
                } catch (error) {
                    console.error('Error sending audio:', error);
                    // Handle network errors here
                }
            };
        }
    };

    const rotationClass = isRotated ? 'rotate-180' : '';

    return (
        <div className={`flex flex-col items-center mb-4 ${rotationClass} transform`}>
            <button onClick={handleClick} className={`flex items-center justify-center w-48 h-20 bg-white text-gray-700 font-semibold rounded-lg shadow-md hover:shadow-lg transition duration-300 ease-in-out ${isActive ? 'bg-red-100 hover:bg-red-200 text-red-700' : ''}`}>
                {isActive ? <BsRecordCircleFill className="text-red-500" /> : <FaMicrophone className="text-green-500" />}
                <span className="ml-2">{label}</span>
            </button>
        </div>
    );
}

export default function App({ user, language }) {



    console.log(language)

    return (
        <div className="flex flex-col items-center justify-center bg-cover bg-center h-screen space-y-80" style={{ backgroundImage: "url('https://cdn.builder.io/api/v1/image/assets/TEMP/7966c460-a2cd-49b6-8e55-8965ae56e831?apiKey=be43af7b4ce2472eaff8e8a17c078188&')" }}>
            <ToggleButton label="Patient" isRotated={true} />
            <ToggleButton label="Doctor" />
            {/* <Link id="signout" className="FormButton" to="/"
                onClick={() => auth.signOut()}>{language}
            </Link> */}
        </div>
    );
}


// backgroundImage: "url('https://cdn.builder.io/api/v1/image/assets/TEMP/7966c460-a2cd-49b6-8e55-8965ae56e831?apiKey=be43af7b4ce2472eaff8e8a17c078188&')"



{/* 




*/}