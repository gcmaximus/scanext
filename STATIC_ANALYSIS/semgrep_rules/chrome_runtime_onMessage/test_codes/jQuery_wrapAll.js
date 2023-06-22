// Content script
// Listen for messages from the background script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === 'wrapAllText') {
      // wrapAll the received text to a specific element using jQuery
      $('#myElement').wrapAll(message.text);
    }
  });
  // Content script
  // Listen for messages from the background script
  chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === 'wrapAllElement') {
      // wrapAll a new element with the received content using jQuery
      $('<div>').text(message.content).wrapAll('body');
    }
  });
  //2 matches to be found