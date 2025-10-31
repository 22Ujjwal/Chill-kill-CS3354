//Function for opening chatbot
function openForm() {
    const popup = document.getElementById("myForm");
    const overlay = document.getElementById("chatOverlay");

    // Make it visible
    popup.style.display = "block";
    overlay.style.display = "block";

    // Remove any previous animation classes
    popup.classList.remove("animate__bounceOutDown", "animate__animated");

    // Add the animation for opening
    popup.classList.add("animate__animated", "animate__bounceInUp");

    // Disable background scroll
    document.body.classList.add("no-scroll");
}

//Function for closing chatbot
function closeForm() {
    //document.getElementById("myForm").style.display = "none";
    const popup = document.getElementById("myForm");
    const overlay = document.getElementById("chatOverlay");

    // Add exit animation
    popup.classList.remove("animate__bounceInUp", "animate__animated");
    popup.classList.add("animate__animated", "animate__bounceOutDown");

    // Re-enable background scroll
    document.body.classList.remove("no-scroll");

    // Wait for animation to finish, then hide the popup
    setTimeout(() => {
        popup.style.display = "none";
        overlay.style.display = "none";
    }, 800); // duration matches the CSS animation length
}

let isBotResponding = false; // global flag to track bot response state

// Function to handle sending messages
function sendMessage() {
  const popup = document.getElementById("myForm");
  const inputBox = document.getElementById("user-input"); // Textbox element
  const chatBox = document.getElementById("chat-box");   // Chat area
  const userText = inputBox.value.trim();                // Get input and remove spaces

  // Only send if popup is visible (display not 'none')
  if (popup.style.display === "none" || popup.style.display === "") {
    return; // Stop if chatbot is closed
  }

  // Stop if bot is already responding
  if (isBotResponding) return;

  // If input is empty, don't do anything
  if (userText === "") {
    isBotResponding = false;
    return; 
  }

  // Lock input until bot responds
  isBotResponding = true;
  inputBox.disabled = true;

  // User Message
  // Create a new div element for the user's message
  const userMessage = document.createElement("div");
  userMessage.className = "message user-message"; // Add CSS classes
  userMessage.textContent = userText;             // Set the message text
  chatBox.appendChild(userMessage);               // Add to chat box

  // Clear input box after sending
  inputBox.value = "";

  // Bot Response (placeholder for now)
  // Simulate a bot response with a short delay
  setTimeout(() => {
    const botMessage = document.createElement("div");
    botMessage.className = "message bot-message";
    
    // Right now it just repeats what the user said
    botMessage.textContent = "Bot: You said - " + userText;
    
    chatBox.appendChild(botMessage);

    // Auto-scroll to the bottom of the chat
    chatBox.scrollTop = chatBox.scrollHeight;

    // Unlock input
    isBotResponding = false;
    inputBox.disabled = false;
  }, 500); // 500ms delay to feel more natural
}

//Function to allow users to send messages by pressing enter
document.getElementById("user-input").addEventListener("keydown", function(event) {
  if (event.key == "Enter") {
    event.preventDefault();
    sendMessage();
  }
});