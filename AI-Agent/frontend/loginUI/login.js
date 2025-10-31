// import Firebase modules
import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js';
import { getAuth, signInWithEmailAndPassword } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js';
import { getFirestore, doc, getDoc } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';


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

// initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

// get login form, email, password, and message
const loginForm = document.getElementById('loginForm');
const userInput = document.getElementById('email-or-username');
const passwordInput = document.getElementById('password');
const messageDiv = document.getElementById('message');

// show message function
function showMessage(text, type) {
    messageDiv.textContent = text;
    // display message depending on state (red = error, green = success)
    messageDiv.className = `message ${type}`; 
    messageDiv.style.display = 'block';
    // hide messages after 5 seconds
    setTimeout(() => {
        messageDiv.style.display = 'none';
    }, 5000);
}

// helper
const normalize = (u) => u.trim().toLowerCase();

// username sign in
async function signInFlipFlop(input, password){
    const value = input.trim();
    // direct to sign in with email function if input include @ symbol
    if (input.includes('@')){
        return await signInWithEmailAndPassword(auth, value, password);
    } else { // else the user is signing in with a username. Search database
        const ref_username = doc(db, 'user-credentials', normalize(input));
        const get_data = await getDoc(ref_username);
        if (!get_data.exists()) { // username does not match username in database
            throw new Error('Username not found.');
        }
        const {email} = get_data.data(); // pull email from database
        if (!email) {
            throw new Error('Username mapping missing email');
        }
        return await signInWithEmailAndPassword(auth, email, password);
    }

}

// login form
// for testing purposes:
// email --> abc@fakemail.com 
// password --> abc123
loginForm.addEventListener('submit', async (e) => {
    // prevent browser's default reloading after the user presses "login" button
    e.preventDefault();

    const input = userInput.value;
    const password = passwordInput.value;

    try {
        // login existing user
        const userCredential = await signInFlipFlop(input, password);
        // login successfully
        showMessage('Login successful!', 'success');            // Show message to screen
        console.log('User logged in:', userCredential.user);    // Show message to console
        getDisplayName();                                       // Send username to homepage script
        window.location.href = '../homepageUI/nintendoHomePage.html';   // Take user to homepage
        
    } catch (error) {
        // login unsuccessfully
        console.error('Error:', error);
        showMessage('Invalid username or password.', 'error');
        /*
        PLACEHOLDER FOR NOW, FILL IN WITH PROPER LOCATION WHEN POSSIBLE
        window.location.href = ;
        */
    }
});

// This Function was merged to onAuthStateChanged() in userLoginScript.js to accomodate with FireBase system.
// onAuthStateChanged() use FireBase storage instead of local storage.

// ------------------------------------------------------------------------------------------------------------
// **Note: I commented out getDisplayName() and somehow this caused the login authentication system to crash.
// (When I tried to sign the user in, it threw an error "Invalid username/password")
// Even though the function is empty, do not delete it to avoid crashing.
// ------------------------------------------------------------------------------------------------------------

function getDisplayName() {
    //const email = userEmail.value;
    //const displayName = email.slice(0, email.indexOf("@")); 
    //Send it to local storage to use in other scripts
   // localStorage.setItem('displayName', displayName);
}
