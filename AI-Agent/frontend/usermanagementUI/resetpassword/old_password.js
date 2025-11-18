// changePassword.js

import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js';
import { getAuth, onAuthStateChanged, updatePassword, EmailAuthProvider, reauthenticateWithCredential } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js';

// Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyD6ZGFXmcogcggIOGuZvkXXrKjc1GqL8Mo",
    authDomain: "chatbot-b5e2c.firebaseapp.com",
    projectId: "chatbot-b5e2c",
    storageBucket: "chatbot-b5e2c.firebasestorage.app",
    messagingSenderId: "785763711557",
    appId: "1:785763711557:web:bec2b3cccf5e18b174012c",
    measurementId: "G-6K652SG7CY"
};

// Init
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// User input 
const form = document.getElementById('enterOldPasswordForm');
const oldPWInput = document.getElementById('old-password-input');
const msg = document.getElementById('message');
const cancelBtn = document.getElementById('cancelBtn');

if (cancelBtn) {
  cancelBtn.addEventListener('click', () => {
    // Redirect to homepage
    window.location.href = "../homepageUI/nintendoHomePage.html";
  });
}

function show(text, isErr = false) {
  msg.textContent = text;
  msg.className = "message " + (isErr ? "error" : "success");
}

form.addEventListener("submit", async(e) => {
    e.preventDefault();

    const user = auth.currentUser;
    const oldPW = oldPWInput.value.trim();
    const credential = EmailAuthProvider.credential(user.email, oldPW);
    try{
        await reauthenticateWithCredential(user, credential);
        show("Password matched.");
       
      window.location.href = "../resetpassword/reset_password.html";

    } catch (error){
        console.error(error);
        show("Password does not match. Please try again.", true);
    }
});
