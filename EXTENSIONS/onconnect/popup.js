document.addEventListener("DOMContentLoaded", function() {
    const messageInput = document.getElementById("messageInput");
  
    messageInput.addEventListener("input", function() {
      const message = { h1Text: messageInput.value };
      chrome.runtime.connect({ name: "messageChannel" }).postMessage(message);
    });
  });
  