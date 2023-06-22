// Content script
// Listen for messages from the background script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === 'prependText') {
      // prepend the received text to a specific element using jQuery
      $('#myElement').prepend(message.text);
    }
  });
  // Content script
  // Listen for messages from the background script
  chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === 'prependElement') {
      // prepend a new element with the received content using jQuery
      $('<div>').text(message.content).prepend('body');
    }
  });
  //2 matches to be found