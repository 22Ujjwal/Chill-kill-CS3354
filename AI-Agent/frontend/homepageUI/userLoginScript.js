
//Script needs to check if user is actually logged in AND needs to know the user's name.
//The back-end for the authorization could return a boolean to let this script know if user is logged in.
//Could also return the first name of the user along with it, so that it can be plugged into the
//dashboard.

// Firebase initialization
import { initializeApp, getApps } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js';
import { getAuth, onAuthStateChanged, signOut } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js';

// -- Use the SAME config as login.js --
const firebaseConfig = {
  apiKey: "AIzaSyD6ZGFXmcogcggIOGuZvkXXrKjc1GqL8Mo",
  authDomain: "chatbot-b5e2c.firebaseapp.com",
  projectId: "chatbot-b5e2c",
  storageBucket: "chatbot-b5e2c.firebasestorage.app",
  messagingSenderId: "785763711557",
  appId: "1:785763711557:web:bec2b3cccf5e18b174012c",
  measurementId: "G-6K652SG7CY"
};

// Avoid double-initialization if another script initializes Firebase
if (getApps().length === 0) initializeApp(firebaseConfig);

const auth = getAuth();
const navbarDisplayUser = document.getElementById('navbarDisplayUser');
const navbarLoginButton = document.getElementById('navbarLoginButton');
const navbarSignUpButton = document.getElementById('navbarSignUpButton');
const ACCOUNT_MANAGEMENT_PATH = '../usermanagementUI/usermanagement.html';

// **** Keeping old version for future reference ******//
//----------------------------------------------------------------------
/*//Function for displaying username in dashboard when user logs in
window.addEventListener('DOMContentLoaded', () => {
    const navbarDisplayUser = document.getElementById('navbarDisplayUser');
    const navbarLoginButton = document.getElementById('navbarLoginButton');
    const displayName = localStorage.getItem('displayName');
    console.log("Loaded display name:", displayName);
    if (displayName) {
        navbarDisplayUser.textContent = 'Welcome ' + displayName + '!';
        navbarLoginButton.textContent = 'Logout';
    } else {
        navbarDisplayUser.textContent = '';
        navbarLoginButton.textContent = 'Login';
    }
});*/
//--------------------------------------------------------------------------
// Preparing to export user email.
let currentUserEmail = null;

// Function for displaying contents of navigation bar depends on log in/log out state
onAuthStateChanged(auth, (user) =>{
    if (user) { // logged in state
        const name = user.displayName || (user.email ? user.email.split('@')[0] : 'User'); // display username before @ symbol from email
        currentUserEmail = user.email; // save current user's email for export
        if (navbarDisplayUser) {
            navbarDisplayUser.textContent = 'Welcome ' + name + '!';
        }
        if (navbarLoginButton) { // change login button to logout
            navbarLoginButton.textContent = 'Logout';
        }
        if (navbarSignUpButton) {
            navbarSignUpButton.textContent = 'Account Management';
            navbarSignUpButton.href = ACCOUNT_MANAGEMENT_PATH;
        }
    } else { // logged out state
        currentUserEmail = null;
        if (navbarDisplayUser) {
            navbarDisplayUser.textContent = 'Hello!'; // replace "Welcome, username" with "Hello"
        }
        if (navbarLoginButton) { // change logout button -> login
            navbarLoginButton.textContent = 'Login';
        }
    }
});
// export currentUserEmail to getSummary in chatbotScript
export {currentUserEmail};

// Logging out using Firebase authentication system when the user clicks the logout button/
if (navbarLoginButton){
    navbarLoginButton.addEventListener('click', async () => {
        if (auth.currentUser){ // user is currently logging in
            try { // log user out
                await signOut(auth);
                localStorage.removeItem('displayName');
                // redirect user to homepage after logging out
                window.location.href = '../homepageUI/nintendoHomePage.html';
            } catch (err) {// logout failed
                console.error('Log out failed:', err);
                alert('Failed to log out. Try again.');
            }
        } else { // user is not currently loggin in
            window.location.href = '../loginUI/login.html'; // direct to login UI
        }
    })
}
