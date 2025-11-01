/**
 * @jest-environment jsdom
 */
let openForm, sendMessage;

beforeEach(() => {
  document.body.innerHTML = `
    <div id="chatOverlay"></div>
    <div id="myForm" style="display:block;"></div>
    <div id="chat-box"></div>
    <input id="user-input" value="">
  `;

  // Import the script AFTER the DOM exists
  ({ openForm, sendMessage } = require("./chatbotScript"));
});

describe("Chatbot Response Tester", () => {
  test("should always generate a bot response for any non-empty input", () => {
    const chatBox = document.getElementById("chat-box");
    const inputBox = document.getElementById("user-input");

    // Example of diverse inputs to test against
    const inputs = [
      "What is Switch 2?",
      "What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2? What is Switch 2?",
      "lsidhfl☀"
    ];


    inputBox.value = inputs[0];
    sendMessage();

    
    expect(chatBox.textContent).toBe("What is Switch 2?");
    

    inputBox.value = inputs[1];
    sendMessage();

    
    expect(chatBox.textContent).toBe("What is Switch 2?");

    inputBox.value = inputs[2];
    sendMessage();

    
    expect(chatBox.textContent).toBe("What is Switch 2?");

  });
});
