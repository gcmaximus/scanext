//LINES 3-12 is an example of when a message is received with action to update new href value.
// Content script
$(document).ready(function() {
    // Listen for messages from the background script
    chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
      if (message.action === 'changeHref') {
        // Change the href of all anchor tags
        $('a').attr('href', message.newHref);
        sendResponse({ success: true });
      }
    });
  });
  //LINES 15-27 is an example of changing the href of a specific anchor tag by its ID
  // Content script
  $(document).ready(function() {
    // Listen for messages from the background script
    chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
      if (message.action === 'changeHrefById') {
        var anchorId = message.anchorId;
        var newHref = message.newHref || '';
        
        // Change the href of the specified anchor tag
        $('#' + anchorId).attr('href', newHref);
        sendResponse({ success: true });
      }
    });
  });
  //LINES 30-42 is an example of changing the href of multiple anchor tags using a class selector
  // Content script
  $(document).ready(function() {
    // Listen for messages from the background script
    chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
      if (message.action === 'changeHrefByClass') {
        var className = message.className;
        var newHref = message.newHref || '';
        
        // Change the href of all anchor tags with the specified class
        $('a.' + className).attr('href', newHref);
        sendResponse({ success: true });
      }
    });
  });
  //3 matches to be found