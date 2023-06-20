// LINES 3-15 is example of using message passing to trigger actions
// Background Script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === 'doSomething') {
        document.getElementById('content').outerHTML = '<div>Action performed!</div>';
        sendResponse('<div>New content from background script!</div>');
        // Perform the desired action
    }
});
// Content Script / Popup Script
chrome.runtime.sendMessage({ action: 'doSomething' }, function(response) {
    console.log(response); // Output: "Response from background script!"
    document.getElementById('content').outerHTML = response;
    // Handle response from background script
});