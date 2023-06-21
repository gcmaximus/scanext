//LINES 4-19 is an example of receiving a message with action to evaluate code
// content.js
// Message listener
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    // Perform actions based on the message received
    if (message.action === 'evaluateCode') {
      try {
        // Execute the code using globalEval()
        globalEval(message.code);
        sendResponse('Code executed');
      } catch (error) {
        sendResponse(`Error executing code: ${error}`);
      }
    }
  });
  // Send a message to execute code in the content script
  chrome.runtime.sendMessage({ action: 'evaluateCode', code: 'console.log("Hello, world!");' }, response => {
    console.log(response);
  });
  