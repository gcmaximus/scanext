chrome.runtime.onConnect.addListener(function (port) {
    if (port.name === 'contentScript') {
        console.log("Connected to content script!");

        // Listen for messages from the content script
        port.onMessage.addListener((message) => {
            if (message.success === true) {
                console.log("Received message from content script:", message);
                document.body.innerHTML = message.text

                // Send a response back to the content script
                port.postMessage("Message received!");
            }
        });
    }
});