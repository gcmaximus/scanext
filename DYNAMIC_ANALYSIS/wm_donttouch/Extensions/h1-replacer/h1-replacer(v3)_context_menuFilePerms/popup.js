// Update the extension text with the selected text
function updateExtensionText(selectedText) {
    const textElement = document.getElementById("extensionText");
    textElement.textContent = selectedText;
  }
  
  // Create a unique ID for the context menu item
  var contextMenuItemId = "myContextMenu";
  
  // Function to create the context menu item
  function createContextMenuItem() {
    chrome.contextMenus.create({
      id: contextMenuItemId,
      title: "My Context Menu",
      contexts: ["page", "selection"],
    });
  }
  
  // Check if the context menu item already exists and remove it if it does
  chrome.contextMenus.remove(contextMenuItemId, () => {
    // Create the context menu item after removing the existing one
    createContextMenuItem();
  });
  
  // Content script function to modify the <h1> elements
  function modifyH1Elements() {
    // Listen for messages from the extension
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
      console.log('being run')
      console.log(message.text)
      if (message.text) {
        // Modify the <h1> elements on the webpage
        const h1Elements = document.getElementsByTagName("h1");
  
        for (let i = 0; i < h1Elements.length; i++) {
          h1Elements[i].innerHTML = message.text;
        }
      }
    });
  }
  
 // Inject the content script to the current tab
  chrome.tabs.query({ active: false, currentWindow: true }, (tabs) => {
    console.log(tabs)
    chrome.scripting.executeScript({
      target: { tabId: tabs[0].id },
      function: modifyH1Elements,
    });
  });
  
  // Add a listener for when the menu item is clicked
  chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === contextMenuItemId) {
      // Update the extension text with the selected text
      updateExtensionText(info.selectionText);
  
      // Send a message to the content script to modify the <h1> elements
      chrome.tabs.sendMessage(tab.id, { text: info.selectionText });
      console.log('sending 1');
    }
  });
  
  // Listen for messages from the extension
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log('being run');
    console.log(message.text);
    if (message.text) {
      // Modify the <h1> elements on the webpage
      const h1Elements = document.getElementsByTagName("h1");
  
      for (let i = 0; i < h1Elements.length; i++) {
        h1Elements[i].innerHTML = message.text;
      }
    }
  });
  