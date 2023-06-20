// LINES 3-11 is example of passing messages between content scripts and background scripts
// Content Script
chrome.runtime.sendMessage({ message: 'Hello from content script!' }, function(response) {
    document.getElementById('content').outerHTML = response;
});
  
// Background Script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    console.log(message); // Output: "Hello from content script!"
    sendResponse('<div>New content from background script!</div>');
});
// LINES 14-22 is example of sending messages from the background script to a specific tab
// Background Script
chrome.tabs.sendMessage(tabId, { message: 'Hello from background script!' }, function(response) {
    document.getElementById('content').outerHTML = response;
});
  
// Content Script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    console.log(message); // Output: "Hello from background script!"
    sendResponse('<div>New content from content script!</div>');
});
// LINES 25-38 is example of broadcasting messages to all tabs 
// Background Script
chrome.tabs.query({}, function(tabs) {
    tabs.forEach(function(tab) {
        chrome.tabs.sendMessage(tab.id, { message: 'Hello from background script!' }, function(response) {
            console.log(response); // Output: "Response from content script!"d
            document.getElementById('content').outerHTML = response;
            // Handle response from content script
        });
    });
});
// Content Script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    console.log(message); // Output: "Hello from background script!"
    sendResponse('<div>New content from content script!</div>');
});
// LINE 41-50 is example of communication between popup scripts and background scripts
// Content Script 1
chrome.runtime.sendMessage({ message: 'Hello from content script 1!' }, function(response) {
    console.log(response); // Output: "Response from content script 2!"
    document.getElementById('content').outerHTML = response;
    // Handle response from content script 2
});
// Content Script 2
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    console.log(message); // Output: "Hello from content script 1!"
    sendResponse('<div>New content from content script 2!</div>');
});
// LINES 53-65 is example of using message passing to trigger actions
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
// LINE 68-76 is example of communication between popup scripts and background scripts
// Popup Script
chrome.runtime.sendMessage({ message: 'Hello from popup script!' }, function(response) {
    document.getElementById('content').outerHTML = response;
});  

// Background Script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    console.log(message); // Output: "Hello from popup script!"
    sendResponse('<div>New content from background script!</div>');
});