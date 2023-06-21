//LINES 2-8 is an example of sending a message from the background script to the content script and updating the active tab
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    // Perform some actions based on the received message
    if (message === "updateTab") {
      chrome.tabs.update(sender.tab.id, { active: true });
      sendResponse("Tab updated successfully!");
    }
  });
  //LINES 10-17 is an example of sending a message from a popup to the background script and updating a specific tab
  chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    // Perform some actions based on the received message
    if (message.type === "updateTab") {
      const tabId = message.tabId;
      chrome.tabs.update(tabId, { active: true });
      sendResponse("Tab updated successfully!");
    }
  });
  //2 matches to be found