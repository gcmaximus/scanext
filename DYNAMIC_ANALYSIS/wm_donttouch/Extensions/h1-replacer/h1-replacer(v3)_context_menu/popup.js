// Update the extension text with the selected text
function updateExtensionText(selectedText) {
  const textElement = document.getElementById("extensionText");
  textElement.innerHTML = selectedText;
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

// Add a listener for when the menu item is clicked
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === contextMenuItemId) {
    // Update the extension text with the selected text
    updateExtensionText(info.pageUrl);
    console.log("INFO: ", info)
    console.log("TAB: ", tab)

    // Send a message to the background script to modify the <h1> elements
    chrome.runtime.sendMessage({ text: info.selectionText });
    console.log('sendMessage');
  }
});
