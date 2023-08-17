document.addEventListener("DOMContentLoaded", () => {
    const activateButton = document.getElementById("activateButton");
  
    activateButton.addEventListener("click", () => {
      chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
        chrome.scripting.executeScript({
          target: { tabId: tabs[0].id },
          function: () => {
            const port = chrome.runtime.connect({ name: "content-script" });
            port.postMessage({ action: "activateExtension" });
  
            port.onMessage.addListener(message => {
              if (message.action === "showMessage") {
                const h1Element = document.querySelector("h1");
                if (h1Element){
                  h1Element.innerHTML= message.text;
                }
              }
            });
          }
        });
      });
    });
  });
  