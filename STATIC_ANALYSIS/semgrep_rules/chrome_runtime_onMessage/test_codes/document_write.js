//LINES 2-6 is example of receiving a message and writing it to the document
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === "writeToDocument") {
      document.write(message.content);
    }
  });
  //LINES 8-12 is example of appending received message content to the existing document
  chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === "appendToDocument") {
      document.write(document.body.innerHTML + message.content);
    }
  });
  //LINES 14-20 is example of clearing the document and writing the received message
  chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === "clearAndWriteToDocument") {
      document.open();
      document.write(message.content);
      document.close();
    }
  });
  //LINES 22-27 is example of writing a message to a new window
  chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === "openNewWindow") {
      var newWindow = window.open("", "_blank");
      newWindow.document.write(message.content);
    }
  });
  //LINES 29-34 is example of writing a message to a specific iframe in the document
  chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === "writeToIframe") {
      var targetIframe = document.getElementById("myIframe").contentWindow;
      targetIframe.document.write(message.content);
    }
  });