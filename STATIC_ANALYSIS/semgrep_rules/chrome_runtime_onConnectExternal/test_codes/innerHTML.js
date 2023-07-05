//LINES 2-12 is an example of background script communication to content script
chrome.runtime.onConnectExternal.addListener(function(port) {
    if (port.name === 'contentScript') {
      port.onMessage.addListener(function(message) {
        // Update the web page's innerHTML
        document.body.innerHTML = '<h1>' + message + '</h1>';
      });
      
      // Send a message to the content script
      port.postMessage('Hello from background script!');
    }
  });
  //LINES 14-24 is an example of possible popup to Background Script communication
  //background script
  chrome.runtime.onConnectExternal.addListener(function(port) {
    if (port.name === 'popup') {
      port.onMessage.addListener(function(message) {
        // Update the web page's innerHTML
        document.body.innerHTML = '<h1>' + message + '</h1>';
      });
      
      // Send a message to the popup script
      port.postMessage('Message received in the background script!');
    }
  });
  //2 matches to be found