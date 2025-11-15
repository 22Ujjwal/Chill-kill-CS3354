// Import the functions you need from the SDKs you need
import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js';
import { getAuth, createUserWithEmailAndPassword, updateProfile, deleteUser } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";
import { getFirestore, doc, runTransaction, setDoc, serverTimestamp, getDoc } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";
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
const db = getFirestore(app); // added 

// Simple client-side validation for Sign Up form
document.getElementById("signupForm").addEventListener("submit", async function(event) {
  event.preventDefault(); // prevent form from refreshing the page

  const username = document.getElementById("username").value.trim(); // added
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirmPassword").value;

  // Check for empty fields
  if (!username || !email || !password || !confirmPassword) {
    alert("Please fill out all fields!");
    return;
  }

  // Username constraints
  const normalize = (u) => u.trim().toLowerCase(); // Convert username to lowercase
  const isValidUsername = /^[a-zA-Z0-9_]{3,20}$/;

  /*
  Username constraints:
      - Lower case or upper case letters.
      - At lease one number.
      - At least 3 and less that 20 characters. 
  */
  if (!username.match(isValidUsername)){
    alert("Invalid username. ");
    return;
  }

  // Basic email format check
  const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
  if (!email.match(emailPattern)) {
    alert("Please enter a valid email address!");
    return;
  }

  if (email.length > 254) {
    alert("Email is too long. ");
    return;
  }

  const hasNumber = /[0-9]/.test(password);
  const hasSpecialChar = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password);
  const hasCapital = /[A-Z]/.test(password);
  const passHasSpace = /\s/.test(password);

  /*
  Password constraints: 
      - Less than 32 characters.
      - At least 8 characters long.
      - At least 1 number.
      - At least 1 special characters.
      - At least 1 capital letter.
      - No space.
  */
  if (password.length < 8 || password.length > 32) {
    alert("Password requirements not met: Must be between 8 and 32 characters"); 
    return;
  }

  if (!hasNumber) {
    alert("Password requirements not met: Must have at least one number (0-9).");
    return;
  }

  if (!hasSpecialChar) {
    alert("Password requirements not met: Must have at least one special character (e.g., !@#$).");
    return;
  }

  if (!hasCapital) {
    alert("Password requirements not met: Must have at least one capital letter.");
    return;
  }

  if (passHasSpace) {
    alert("Password requirements not met: Must not have space between charaters.");
    return;
  }

  // Check if retyped password matches password
  if (password !== confirmPassword) {
    alert("Passwords do not match!");
    return;
  }

  // Account creation


  const normalizedUsername = normalize(username);
  // Inform the user when a username already exists prior to account creation
  try { 
    const duplicate = await getDoc(doc(db, "user-credentials", normalizedUsername));
    if(duplicate.exists()){
      alert("Username already existed. Choose a different username.");
      return;
    }

    // Create new user
    const credentials = await createUserWithEmailAndPassword(auth, email, password);
    const uid = credentials.user.uid;

    // Check for duplicate username in the database 
    try{ 
      await runTransaction(db, async(tx)=>{
        const ref = doc(db, "user-credentials", normalizedUsername);
        const snap = await tx.get(ref);
        // Print error message if a username already exists
        if (snap.exists()) {
          throw new Error("Username already taken.");
        }
        tx.set(ref, { uid, email, createdAt: serverTimestamp() });
      });
      await setDoc(doc(db, "users", uid),{ // Add user to the database
        username,
        username_lower: normalizedUsername,
        email,
        createdAt: serverTimestamp()
      });

      // Display username on the navigation bar
      await updateProfile(credentials.user, {displayName: username});
      alert("Sign Up successful! Redirecting to Login page.");
      window.location.href = '../loginUI/login.html'; // Redirect to login page
    } catch (e){
      // Rollback if Firestore step fails after Auth user creation
      try { await deleteUser(auth.currentUser); } catch {}
      throw e;
    }
  }  catch (error ){
      alert(error.message || "Signup failed");
    }
});
