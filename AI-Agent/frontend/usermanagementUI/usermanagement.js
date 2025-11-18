// Import firebase modules
import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js';
import { getAuth, onAuthStateChanged, updateProfile, deleteUser, } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";
import { getFirestore, doc, getDoc, updateDoc, setDoc, serverTimestamp, deleteDoc } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";

// Firebase configuration (same as other pages)
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
const db = getFirestore(app);

// Declare global DOM element references
let usernameInput;
let emailInput;
let confirmButton;
let formPersonalInfo;
let deleteAccount;

// ----------------- LOAD USER DATA -----------------
const loadUserData = async (user) => {
    if (!emailInput || !usernameInput) return;

    emailInput.value = user.email || "";

    const userRef = doc(db, "users", user.uid);
    try {
        const snap = await getDoc(userRef);
        if (snap.exists()) {
            usernameInput.value = snap.data().username || "";
        } else {
            usernameInput.value = user.displayName || (user.email?.split('@')[0] ?? "");
        }
    } catch (err) {
        console.error("Error loading user data:", err);
    }
};

// ----------------- UPDATE PROFILE (USERNAME ONLY) -----------------
const handleProfileUpdate = async (e) => {
    e.preventDefault();

    confirmButton.disabled = true;
    confirmButton.textContent = "Saving...";

    const user = auth.currentUser;
    const newUsername = usernameInput.value.trim();

    // Username validation regex: 3–20 chars, letters/numbers/underscore
    const usernameRegex = /^[a-zA-Z0-9_]{3,20}$/;

    console.log("Typed username:", newUsername);
    console.log("Regex passes:", usernameRegex.test(newUsername));

    if (!user) {
        alert("You must be logged in.");
        resetConfirmButton();
        return;
    }

    if (!usernameRegex.test(newUsername)) {
        alert("Invalid username.\n\n• 3–20 characters\n• Letters, numbers, underscore only");
        resetConfirmButton();
        return;
    }

    try {
        // Update Auth displayName
        await updateProfile(user, { displayName: newUsername });
        console.log("Auth displayName updated.");

        const userRef = doc(db, "users", user.uid);

        // Update user doc; fallback to setDoc if it doesn't exist
        await updateDoc(userRef, {
            username: newUsername,
            updatedAt: serverTimestamp()
        }).catch(async () => {
            await setDoc(userRef, {
                username: newUsername,
                updatedAt: serverTimestamp()
            });
        });

        alert("Profile updated!");

    } catch (err) {
        console.error("Profile update error:", err);
        alert("Update failed: " + err.message);
    }

    resetConfirmButton();
};

function resetConfirmButton() {
    if (!confirmButton) return;
    confirmButton.disabled = false;
    confirmButton.textContent = "Confirm";
}

// ******************** DELETE ACCOUNT ************************** 
const handleDeleteAccount = async (e) => {
    e.preventDefault();
    const user = auth.currentUser;

    if (!user) {
        alert("You must be logged in to delete your account.");
        return;
    }

    const confirmDelete = confirm(
        "Are you sure you want to permanently delete your account?\nThis cannot be undone."
    );
    if (!confirmDelete) return;

    deleteAccount.textContent = "Deleting...";
    deleteAccount.disabled = true;

    try {
        // 1. Read current username (normalized)
        const normalizedUsername = usernameInput.value.trim().toLowerCase();

        // 2. Delete the username index IN THE SAME COLLECTION you use in sign-up
        const usernameIndexRef = doc(db, "user-credentials", normalizedUsername);

        await deleteDoc(usernameIndexRef).catch(err => {
            console.warn("Could not delete user-credentials doc:", err);
        });

        // 3. Delete user’s main Firestore doc
        const userDocRef = doc(db, "users", user.uid);
        
        await deleteDoc(userDocRef).catch(err => {
            console.warn("Could not delete users/{uid} doc:", err);
        });

        // 4. Delete Firebase Auth user
        await deleteUser(user);

        alert("Account successfully deleted.");
        window.location.href = "../homepageUI/nintendoHomePage.html";

    } catch (error) {
        console.error("Error deleting account:", error);
        alert(`Account deletion failed: ${error.message}`);
    } finally {
        deleteAccount.textContent = "Delete Account";
        deleteAccount.disabled = false;
    }
};

document.addEventListener("DOMContentLoaded", () => {
    // Grab elements AFTER DOM is ready
    usernameInput   = document.getElementById("username");
    emailInput      = document.getElementById("email");
    confirmButton   = document.querySelector(".confirm-button");
    formPersonalInfo = document.getElementById("personal-info-form");
    deleteAccount   = document.getElementById("delete-account-button");

    // Username/email exist only on the Personal Information tab
    if (formPersonalInfo) {
        formPersonalInfo.addEventListener("submit", handleProfileUpdate);
    }

    if (deleteAccount) {
        deleteAccount.addEventListener("click", handleDeleteAccount);
    }

    // Sidebar navigation
    const navItems = document.querySelectorAll(".nav-item[data-content]");

    const switchContent = (targetId) => {
        document.querySelectorAll(".content-block").forEach(block => {
            block.classList.remove("active-content");
            block.classList.add("hidden-content");
        });

        const targetBlock = document.getElementById(targetId);
        if (targetBlock) {
            targetBlock.classList.remove("hidden-content");
            targetBlock.classList.add("active-content");
        }
    };

    navItems.forEach(item => {
        item.addEventListener("click", () => {
            navItems.forEach(i => i.classList.remove("active"));
            item.classList.add("active");

            const contentId = item.getAttribute("data-content");
            switchContent(contentId);
        });
    });

    // Firebase login check
    onAuthStateChanged(auth, (user) => {
        if (user) {
            loadUserData(user);
        } else {
            console.log("User not logged in.");
        }
    });

    // Back to home button (under Login & Security)
    const backToHome = document.getElementById("backToHome");
    if (backToHome) {
        backToHome.addEventListener("click", () => {
            window.location.href = "../homepageUI/nintendoHomePage.html";
        });
    }
});
