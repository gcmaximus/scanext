async function updateTabUrl(tabId, newUrl) {
  try {
    const tab = await chrome.tabs.getCurrent()
    if (tab) {
      // Update the URL property of the retrieved tab using chrome.tabs.update
      const current = await chrome.tabs.update(tab.id, { url: tab.url });
      console.log("Tab URL updated:", current);
    } else {
      console.log("Tab not found");
    }
  } catch (error) {
    console.error("Error occurred:", error);
  }
}

// Usage: Call the function and pass the tab ID and new URL as arguments
const tabId = 123; // Replace with the actual tab ID
updateTabUrl(tabId, newUrl);
