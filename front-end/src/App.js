
import { Routes, Route } from "react-router-dom";
import React, { useState, useEffect } from 'react';
import firebase from './firebase.js';
import Login from './components/Login.js'
import Home from './components/Home.js'
import Load from './components/Load.js'

function App() {
    const [user, setUser] = useState(null);
    useEffect(() => {
        firebase.auth().onAuthStateChanged(user => {
            setUser(user);
        })
    }, [])

    const [language, setLanguage] = useState('English'); // Default language


    return (
        <div className="App">
            <Routes>
                <Route path="/" element={user ? <Home user={user} language={language} /> : <Login setLanguage={setLanguage} />} />
                <Route path="/Load" element={<Load user={user} />} />
            </Routes>
        </div>

    );
}

export default App;
