//LINES 3-8 is example of passing messages between content scripts and background scripts
// Content Script
chrome.runtime.sendMessage({ message: 'Hello from content script!' });

// Background Script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  document.getElementById('content').outerHTML = message;
});
// LINES 11-16 is example of sending messages from the background script to a specific tab
// Background Script
chrome.tabs.sendMessage(tabId, { message: 'Hello from background script!' });

// Content Script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  document.getElementById('content').outerHTML = message;
});
// LINES 19-28 is example of broadcasting messages to all tabs
// Background Script
chrome.tabs.query({}, function(tabs) {
  tabs.forEach(function(tab) {
    chrome.tabs.sendMessage(tab.id, { message: 'Hello from background script!' });
  });
});

// Content Script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  document.getElementById('content').outerHTML = message;
});
// LINES 31-36 passing messages between different content scripts
// Content Script 1
chrome.runtime.sendMessage({ message: 'Hello from content script 1!' });

// Content Script 2
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  document.getElementById('content').outerHTML = message;
});
//LINES 38-43 is example of appending the received message content to a specific element in the document
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.action === "appendToElement") {
    var targetElement = document.getElementById("myElement");
    targetElement.outerHTML += message.content;
  }
});
//LINES 45-50 is example of writing a formatted message to a specific element in the document
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.action === "writeToElement") {
    var targetElement = document.getElementById("myElement");
    targetElement.outerHTML = message.content;
  }
});