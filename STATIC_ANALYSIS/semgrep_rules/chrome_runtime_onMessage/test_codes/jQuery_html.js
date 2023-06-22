//LINES 4-9 is an example of injecting HTML from the content script to the current page
// Content Script
// Listen for messages from the background script or popup
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === 'injectHTML') {
      var htmlContent = message.html;
      $('body').html(htmlContent);
    }
  });
  //LINES 13-19 is an example of receiving HTML from the background script and updating a specific element
  // Content Script
  // Listen for messages from the background script or popup
  chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === 'updateElement') {
      var elementSelector = message.selector;
      var htmlContent = message.html;
      $(elementSelector).html(htmlContent);
    }
  });
  //LINES 23-31 is an example of updating multiple elements with HTML content
  // Content Script
  // Listen for messages from the background script or popup
  chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === 'updateElements') {
      var elementSelector = message.selector;
      var htmlContent = message.html;
      $(elementSelector).each(function() {
        $(this).html(htmlContent);
      });
    }
  });
// 3 matches to be found