import React, { useState } from 'react';
import { signInWithGoogle } from '../firebase';
import { FcGoogle } from "react-icons/fc";
import '../styles/Login.css'
import { signInWithPopup, GoogleAuthProvider } from "firebase/auth";
import { auth } from '../firebase';
import MAITLogo from './MAIT_logo.svg';



const Login = ({ setLanguage }) => {
    const [selectedLanguage, setSelectedLanguage] = useState("English");

    const handleLanguageChange = (e) => {
        setSelectedLanguage(e.target.value); // Use the renamed state setter function
    };

    const signInWithGoogle = async () => {
        const provider = new GoogleAuthProvider();
        try {
            const result = await signInWithPopup(auth, provider);
            // ... (You might want to set the language after successful sign in)
            setLanguage(selectedLanguage); // Now using the prop function to set language
            // handle successful sign in
        } catch (error) {
            // handle errors here, such as displaying a notification to the user
            console.error(error);
        }
    };

    return (
        <div
            className="bg-cover bg-center h-screen flex flex-col justify-center items-center pt-20"
            style={{ backgroundImage: "url('https://cdn.builder.io/api/v1/image/assets/TEMP/7966c460-a2cd-49b6-8e55-8965ae56e831?apiKey=be43af7b4ce2472eaff8e8a17c078188&')" }}>

            <div className="-mt-40">
                <div className="text-center mb-6">
                    <img src={MAITLogo} alt="Medical Grade Translator Logo" className="mx-auto" />
                </div>

                <div className="flex flex-col space-y-4 items-center">

                    <button
                        className="bg-white text-gray-600 border border-gray-300 rounded-2xl px-2 py-2 cursor-pointer transition duration-300 ease-in-out w-full font-medium tracking-wide mx-auto hover:shadow-lg flex items-center justify-center"
                        onClick={signInWithGoogle}
                    >
                        <FcGoogle className="text-xl mr-4" />
                        Sign in with Google
                    </button>

                    <div>
                        <label htmlFor="language-select" className="text-lg font-medium text-blue-500"></label>
                        <select
                            id="language-select"
                            value={selectedLanguage}
                            onChange={handleLanguageChange}
                            className="mt-1 block w-full px-4 py-2 border-gray-300 bg-white rounded-2xl shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                        >
                            <option value="English">English</option>
                            <option value="Mandarin">Mandarin</option>
                            <option value="Korean">Korean</option>
                        </select>
                    </div>
                </div>

            </div>



        </div>
    );
};

export default Login;