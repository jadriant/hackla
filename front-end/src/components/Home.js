import { useEffect, useState, useRef } from 'react';
import { collection, getDocs } from 'firebase/firestore';
import { db, auth } from '../firebase';
import { Link } from "react-router-dom";
import React from 'react';
import ReactDOM from 'react-dom';
import { FaMicrophone } from 'react-icons/fa';
import '../styles/Home.css';
import { BsRecordCircleFill } from 'react-icons/bs'; // Assuming this is the red icon


import { FFmpeg } from '@ffmpeg/ffmpeg';
import { fetchFile } from '@ffmpeg/util';


function ToggleButton({ label, isRotated }) {
    const [isActive, setIsActive] = useState(false);
    const [audioBlob, setAudioBlob] = useState(null);
    const mediaRecorderRef = useRef(null);

    const [isReadyToSend, setIsReadyToSend] = useState(false);

    // Function to toggle recording on and off
    const handleClick = async () => {
        if (!isActive) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                const options = { mimeType: 'audio/webm' };
                mediaRecorderRef.current = new MediaRecorder(stream, options);

                mediaRecorderRef.current.onstop = async () => {
                    setIsActive(false);
                    setIsReadyToSend(true); // Ready to send
                };

                mediaRecorderRef.current.ondataavailable = (event) => {
                    setAudioBlob(event.data);
                };

                mediaRecorderRef.current.start();
                setIsActive(true);

            } catch (error) {
                console.error('Error starting recording:', error);
            }
        } else {
            mediaRecorderRef.current.stop();
        }
    };

    

    const sendAudioToServer = async () => {
        if (audioBlob && isReadyToSend) {
            try {
                const formData = new FormData();
                formData.append("file", audioBlob, "recording.webm");

                const response = await fetch('/doctor-speaks', {
                    method: 'POST',
                    body: formData,
                });

                if (response.ok) {
                    console.log('Audio sent successfully');
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

    const playAudio = () => {
        if (audioBlob) {
            const audioUrl = URL.createObjectURL(audioBlob);
            const audio = new Audio(audioUrl);
            audio.play();
            console.log('Playing the recorded audio...');
            setAudioBlob(null);
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
                Send to Server
            </button>


        </div>
    );
}

export default function App({ user, language }) {

    console.log(language)

    return (
        <div className="flex flex-col items-center justify-center bg-cover bg-center h-screen space-y-60" style={{ backgroundImage: "url('https://cdn.builder.io/api/v1/image/assets/TEMP/7966c460-a2cd-49b6-8e55-8965ae56e831?apiKey=be43af7b4ce2472eaff8e8a17c078188&')" }}>
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