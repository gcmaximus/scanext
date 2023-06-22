// Content script
// Listen for messages from the background script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === 'wrapText') {
      // wrap the received text to a specific element using jQuery
      $('#myElement').wrap(message.text);
    }
  });
  // Content script
  // Listen for messages from the background script
  chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === 'wrapElement') {
      // wrap a new element with the received content using jQuery
      $('<div>').text(message.content).wrap('body');
    }
  });
  //2 matches to be found