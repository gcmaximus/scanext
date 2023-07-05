chrome.runtime.onConnect.addListener(port => {
    if (port.name === "h1Updater") {
      port.onMessage.addListener(message => {
        if (message.type === "updateH1") {
          chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
            if (tabs && tabs.length > 0) {
              const tabId = tabs[0].id;
              chrome.scripting.executeScript({
                target: { tabId },
                files: ["content.js"]
              })
              .then(() => {
                chrome.tabs.sendMessage(tabId, { type: "updateH1", text: message.text });
                port.postMessage({ success: true });
              })
              .catch(error => {
                console.error("Error executing content script:", error);
                port.postMessage({ success: false });
              });
            } else {
              console.error("No active tab found.");
              port.postMessage({ success: false });
            }
          });
        }
      });
    }
  });
  