chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    console.log("Message received in background script:", request);
    sendResponse("Message received!");
});
