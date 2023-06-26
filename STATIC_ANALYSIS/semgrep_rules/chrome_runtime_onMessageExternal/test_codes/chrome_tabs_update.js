//LINES 2-9 is an example of sending a message from a popup to the background script and updating a specific tab
chrome.runtime.onMessageExternal.addListener(function(message, sender, sendResponse) {
    // Perform some actions based on the received message
    if (message.type === "updateTab") {
      const tabId = message.tabId;
      chrome.tabs.update(tabId, { active: true });
      sendResponse("Tab updated successfully!");
    }
  });
  //1 matches to be found