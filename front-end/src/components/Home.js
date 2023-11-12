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



function ToggleButton({ label, isRotated }) {
    const [isActive, setIsActive] = useState(false);
    const [audioBlob, setAudioBlob] = useState(null);
    const mediaRecorderRef = useRef(null); // Ref to hold the MediaRecorder instance

    const [isReadyToSend, setIsReadyToSend] = useState(false); // New state to track if audio is ready to send


    // Function to toggle recording on and off
    const handleClick = async () => {
        // If currently not active, start recording
        if (!isActive) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                const options = { mimeType: 'audio/webm' }; // Use webm format for wider compatibility
                mediaRecorderRef.current = new MediaRecorder(stream, options);

                // When recording stops, save the blob and prepare to send
                mediaRecorderRef.current.onstop = async () => {
                    setIsActive(false); // Set isActive to false
                    setIsReadyToSend(true); // Ready to convert and send
                };

                // When data is available, save it to state
                mediaRecorderRef.current.ondataavailable = (event) => {
                    setAudioBlob(event.data);
                };


                mediaRecorderRef.current.start();
                setIsActive(true); // Set isActive to true

            } catch (error) {
                console.error('Error starting recording:', error);
            }
        } else {
            // If currently active, stop recording
            mediaRecorderRef.current.stop();
        }
    };

    const convertAndSendAudio = async (audioBlob) => {
        try {
            // Convert audioBlob from webm to wav using ffmpeg.js
            const wavBlob = await convertWebmToWav(audioBlob);

            // Create FormData with the converted wavBlob
            const formData = new FormData();
            formData.append("file", wavBlob, "recording.wav");

            // Send the FormData to the server
            const response = await fetch('/doctor-speaks', {
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
            console.error('Error in conversion or sending:', error);
        }

        // Reset states after sending
        setAudioBlob(null);
        setIsReadyToSend(false);
        playAudio() // Play the audio after sending
    };

    const playReceivedAudio = (audioBlob) => {
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        audio.play();
        console.log('Playing the received audio...');
    };


    async function convertWebmToWav(audioBlob) {
    }

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
                onClick={convertAndSendAudio}
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