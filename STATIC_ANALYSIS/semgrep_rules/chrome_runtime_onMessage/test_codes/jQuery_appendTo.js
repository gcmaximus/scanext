// Content script
// Listen for messages from the background script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === 'appendText') {
      // Append the received text to a specific element using jQuery
      $('#myElement').appendTo(message.text);
    }
  });
  // Content script
  // Listen for messages from the background script
  chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === 'appendElement') {
      // Append a new element with the received content using jQuery
      $('<div>').text(message.content).appendTo('body');
    }
  });
  //2 matches to be found