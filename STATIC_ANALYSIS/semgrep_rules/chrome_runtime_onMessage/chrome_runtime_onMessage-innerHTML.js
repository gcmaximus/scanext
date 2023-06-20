// Content Script
chrome.runtime.sendMessage({ message: 'Hello from content script!' });

// Background Script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  document.getElementById('content').innerHTML = message;
});
// Background Script
chrome.tabs.sendMessage(tabId, { message: 'Hello from background script!' });

// Content Script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  document.getElementById('content').innerHTML = message;
});
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
// Content Script 1
chrome.runtime.sendMessage({ message: 'Hello from content script 1!' });

// Content Script 2
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  document.getElementById('content').innerHTML = message;
});
// Popup Script
chrome.runtime.sendMessage({ message: 'Hello from popup script!' });

// Background Script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  document.getElementById('content').innerHTML = message;
});
// Background Script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.action === 'doSomething') {
    document.getElementById('content').innerHTML = 'Action performed!';
    // Perform the desired action
  }
});
