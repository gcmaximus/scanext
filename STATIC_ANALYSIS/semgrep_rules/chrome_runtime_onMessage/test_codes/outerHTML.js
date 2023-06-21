// LINES 3-9 is example of using message passing to trigger actions
// Background Script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === 'doSomething') {
        document.getElementById('content').outerHTML = '<div>Action performed!</div>';
        sendResponse('<div>New content from background script!</div>');
        // Perform the desired action
    }
});
//LINES 11-16 is example of writing a formatted message to a specific element in the document
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === "writeToElement") {
      var targetElement = document.getElementById("myElement");
      targetElement.outerHTML = message.content;
    }
  });
// 2 matches to be found