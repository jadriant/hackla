// Import the functions you need from the SDKs you need

import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
import firebase from "firebase/compat/app";
import "firebase/compat/auth";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyBNJCuV0TxS5bfqt_vErIFqjRN66y6Rqz4",
    authDomain: "medtranslate-1b404.firebaseapp.com",
    projectId: "medtranslate-1b404",
    storageBucket: "medtranslate-1b404.appspot.com",
    messagingSenderId: "38940060337",
    appId: "1:38940060337:web:f1e0a25a45abe6ad535090"
};

// Initialize Firebase
const app = firebase.initializeApp(firebaseConfig);
export const auth = firebase.auth();
const provider = new firebase.auth.GoogleAuthProvider();
provider.setCustomParameters({ prompt: 'select_account' });
export const signInWithGoogle = () => auth.signInWithPopup(provider);
export default firebase;
export const db = getFirestore(app);