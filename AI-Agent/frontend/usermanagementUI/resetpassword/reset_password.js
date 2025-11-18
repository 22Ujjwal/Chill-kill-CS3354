// changePassword.js

import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js';
import { getAuth, onAuthStateChanged, updatePassword} from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js';

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

// DOM
const form = document.getElementById('resetPasswordForm');
const newPwdInput = document.getElementById('new-password');
const retypePwdInput = document.getElementById('retype-password');
const msg = document.getElementById('message');
const cancelBtn = document.getElementById('cancelBtn');

function showMessage(text, isError = false) {
  if (!msg) {
    alert(text);
    return;
  }
  msg.textContent = text;
  msg.style.color = isError ? 'red' : 'limegreen';
}

// Only logged-in users can be here
onAuthStateChanged(auth, (user) => {
  if (!user) {
    showMessage("You must be logged in to change your password.", true);
    window.location.href = "login.html";
  }
});

// Handle cancel
if (cancelBtn) {
  cancelBtn.addEventListener('click', () => {
    window.location.href = "../homepageUI/nintendoHomePage.html";
  });
}

// Handle submit
form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const newPwd = newPwdInput.value.trim();
  const retype = retypePwdInput.value.trim();

  if (!newPwd || !retype) {
    showMessage("Fill out both fields.", true);
    return;
  }

  if (newPwd !== retype) {
    showMessage("Passwords do not match.", true);
    return;
  }

  if (newPwd.length < 8) {
    showMessage("Password must be at least 8 characters.", true);
    return;
  }

  const user = auth.currentUser;
  /*if (!user) {
    showMessage("No user is logged in. Please log in again.", true);
    window.location.href = "../loginUI/login.html";
    return;
  }*/

  try {
    await updatePassword(user, newPwd);
    showMessage("Password updated successfully.");
 
  } catch (error) {
    console.error(error);
    if (error.code === "auth/requires-recent-login") {
      showMessage("Reset password failed. Please log in and try again.", true);
    } else {
      showMessage("Error: " + (error.message || error.code), true);
    }
  }
});
