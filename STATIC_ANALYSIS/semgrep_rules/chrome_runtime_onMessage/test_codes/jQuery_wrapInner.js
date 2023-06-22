// Content script
// Listen for messages from the background script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === 'wrapInnerText') {
      // wrapInner the received text to a specific element using jQuery
      $('#myElement').wrapInner(message.text);
    }
  });
  // Content script
  // Listen for messages from the background script
  chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === 'wrapInnerElement') {
      // wrapInner a new element with the received content using jQuery
      $('<div>').text(message.content).wrapInner('body');
    }
  });
  //2 matches to be found