// Import the functions you need from the SDKs you need
import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js';
import { getAuth, createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

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

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Simple client-side validation for Sign Up form
document.getElementById("signupForm").addEventListener("submit", function(event) {
  event.preventDefault(); // prevent form from refreshing the page

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirmPassword").value;

  // Check for empty fields
  if (!email || !password || !confirmPassword) {
    alert("Please fill out all fields!");
    return;
  }

  // Basic email format check
  const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
  if (!email.match(emailPattern)) {
    alert("Please enter a valid email address!");
    return;
  }

  const hasNumber = /[0-9]/.test(password);
  const hasSpecialChar = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password);

  /*
  Password constraints: 
      - At least 8 characters long.
      - At least 1 number.
      - At least 1 special characters.
  */
  if (password.length < 8 || !hasNumber || !hasSpecialChar) {
   alert(`Password requirements not met:
          - Must be at least 8 characters long. 
          - Must have at least one number (0-9).
          - Must have at least one special character (e.g., !@#$).`);
    return;
  }
  // Check if retyped password matches password
  if (password !== confirmPassword) {
    alert("Passwords do not match!");
    return;
  }

  // If all validations pass
  createUserWithEmailAndPassword(auth, email, password)
  .then((userCredential) => {
    // Signed up 
    const user = userCredential.user;
    alert("Sign Up successful! Redirecting to Login page.");
    window.location.href = '../loginUI/login.html'; // Redirect to login page
  })
  .catch((error) => {
    const errorCode = error.code;
    const errorMessage = error.message;
    alert(errorMessage);
    // ..
  });
});