document.addEventListener("DOMContentLoaded", () => {
    const updateButton = document.getElementById("updateButton");
    const h1Input = document.getElementById("h1Input");
    const statusMessage = document.getElementById("statusMessage");
  
    updateButton.addEventListener("click", () => {
      const text = h1Input.value;
      if (text) {
        chrome.runtime.connect({ name: "h1Updater" }).postMessage({
          type: "updateH1",
          text: text
        });
      }
    });
  
    chrome.runtime.onConnect.addListener(port => {
      if (port.name === "h1Updater") {
        port.onMessage.addListener(message => {
          if (message.success) {
            statusMessage.textContent = "H1 updated successfully.";
          } else {
            statusMessage.textContent = "Error updating H1.";
          }
        });
      }
    });
  });
  