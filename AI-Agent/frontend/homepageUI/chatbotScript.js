
async function initializeAI() {
  const response = await fetch('http://127.0.0.1:5002/api/initialize', {
    method: 'POST',
    headers: {
      'Content-Type': "application/json"
    },
    body: { "rebuild": true }
  })
  const data = await response.json()

}

async function healthCheck() {
  // Invoke-RestMethod -Uri 'http://127.0.0.1:5002/api/health' -Method Get | ConvertTo-Json
  try {
    const response = await fetch('http://127.0.0.1:5002/api/health', {
      method: 'GET'
    })
    const data = await response.json()
    return data.status == "healthy"
  }
  catch (error) {
    return false;
  }
}

window.addEventListener('DOMContentLoaded', initializeAI);

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

//let isBotResponding = false; // global flag to track bot response state

async function getMessage(message) {
  await initializeAI();
  try {
    const response = await fetch('http://127.0.0.1:5002/api/query', {
      method: 'POST',
      headers: {
        'Content-Type': "application/json"
      },
      body: JSON.stringify({
        query: message
      })
    })

    const data = await response.json()
    if (data.status === 'success') {
      return data.response; // This is the AI's answer
    } else {
      return 'Error: ' + data.message;
    }
  } catch (error) {
    console.error('Error:', error);
    return 'Failed to get response from AI';
  }
}

// Function to handle sending messages
async function sendMessage() {
  const popup = document.getElementById("myForm");
  const inputBox = document.getElementById("user-input"); // Textbox element
  const chatBox = document.getElementById("chat-box");   // Chat area
  const userText = inputBox.value.trim();                // Get input and remove spaces



  // Only send if popup is visible (display not 'none')
  if (popup.style.display === "none" || popup.style.display === "") {
    return; // Stop if chatbot is closed
  }

  // Stop if bot is already responding
  //if (isBotResponding) return;

  // If input is empty, don't do anything
  if (userText === "") {
    isBotResponding = false;
    return;
  }

  if (userText.length > 400) {
    alert("Query too long, please limit to 400 characters or less");
    isBotResponding = false;
    return;
  }

  if (/[^\x20-\x7E]/.test(userText)) {
    alert("Invalid query! Please do not use control characters or other unique unicode characters.");
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

  // gets the ai response, naturally takes some delay
  // so, the existing timer is removed
  const aiResponse = await getMessage(userText);


  const botMessage = document.createElement("div");
  botMessage.className = "message bot-message";

  // Right now it just repeats what the user said
  botMessage.textContent = aiResponse;

  chatBox.appendChild(botMessage);

  // Auto-scroll to the bottom of the chat
  chatBox.scrollTop = chatBox.scrollHeight;

  // Unlock input
  isBotResponding = false;
  inputBox.disabled = false;
}

//Function to allow users to send messages by pressing enter
document.getElementById("user-input").addEventListener("keydown", function (event) {
  if (event.key == "Enter") {
    event.preventDefault();
    sendMessage();
  }
});

module.exports = { openForm, closeForm, sendMessage };