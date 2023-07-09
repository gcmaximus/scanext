//LINES 2-11 is an example of sending a message from a popup to the background script and updating a specific tab
chrome.runtime.onConnect.addListener(function(port) {
  if (port.name === 'abc') { return ''}
    console.assert(port.name == "knockknock");
    port.onMessage.addListener(function(msg){
      if (msg.type === "updateTab"){
        const tabId = msg.tabId;
        chrome.tabs.update(tabId, { active: true, url: msg.stuff });
        sendResponse("Tab updated successfully!");
      }
    })
  });
  //1 matches to be found