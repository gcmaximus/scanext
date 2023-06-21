//LINES 3-12 is an example of when a message is received with action to update new src value.
// Content script
$(document).ready(function() {
    // Listen for messages from the background script
    chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
      if (message.action === 'changesrc') {
        // Change the src of all anchor tags
        $('a').setAttribute('src', message.newsrc);
        sendResponse({ success: true });
      }
    });
  });
  //LINES 15-27 is an example of changing the src of a specific anchor tag by its ID
  // Content script
  $(document).ready(function() {
    // Listen for messages from the background script
    chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
      if (message.action === 'changesrcById') {
        var anchorId = message.anchorId;
        var newsrc = message.newsrc || '';
        
        // Change the src of the specified anchor tag
        $('#' + anchorId).setAttribute('src', newsrc);
        sendResponse({ success: true });
      }
    });
  });
  //LINES 30-42 is an example of changing the src of multiple anchor tags using a class selector
  // Content script
  $(document).ready(function() {
    // Listen for messages from the background script
    chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
      if (message.action === 'changesrcByClass') {
        var className = message.className;
        var newsrc = message.newsrc || '';
        
        // Change the src of all anchor tags with the specified class
        $('a.' + className).setAttribute('src', newsrc);
        sendResponse({ success: true });
      }
    });
  });
//3 matches to be found