//LINES 3-8 is example of passing messages between content scripts and background scripts
// Content Script
chrome.runtime.sendMessage({ message: 'Hello from content script!' });

// Background Script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  document.getElementById('content').innerHTML = message;
});
// LINES 11-16 is example of sending messages from the background script to a specific tab
// Background Script
chrome.tabs.sendMessage(tabId, { message: 'Hello from background script!' });

// Content Script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  document.getElementById('content').innerHTML = message;
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
  document.getElementById('content').innerHTML = message;
});
// LINES 31-36 passing messages between different content scripts
// Content Script 1
chrome.runtime.sendMessage({ message: 'Hello from content script 1!' });

// Content Script 2
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  document.getElementById('content').innerHTML = message;
});
// LINES is 39-50 example of using message passing to trigger actions
// Background Script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.action === 'doSomething') {
    document.getElementById('content').innerHTML = 'Action performed!';
    sendResponse('Response from background script!');
    // Perform the desired action
  }
});
// Content Script / Popup Script
chrome.runtime.sendMessage({ action: 'doSomething' }, function(response) {
  console.log(response); // Output: "Response from background script!"
  // Handle response from background script
});
//LINES 52-57 is example of appending the received message content to a specific element in the document
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.action === "appendToElement") {
    var targetElement = document.getElementById("myElement");
    targetElement.innerHTML += message.content;
  }
});
//LINES 59-64 is example of writing a formatted message to a specific element in the document
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.action === "writeToElement") {
    var targetElement = document.getElementById("myElement");
    targetElement.innerHTML = message.content;
  }
});