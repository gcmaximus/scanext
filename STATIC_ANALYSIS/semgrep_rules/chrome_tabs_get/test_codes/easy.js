async function updateTabUsingGet(tabId) {
    try {
      const tab = await chrome.tabs.get(tabId);
      if (tab) {
        // Update the retrieved tab using chrome.tabs.update
        const updatedTab = await chrome.tabs.update(tab.id, { url: tab.url });
        console.log("Tab updated:", updatedTab);
      } else {
        console.log("Tab not found");
      }
    } catch (error) {
      console.error("Error occurred:", error);
    }
  }
  
  // Usage: Call the function and pass the tab ID as an argument
  const tabId = 123; // Replace with the actual tab ID
  updateTabUsingGet(tabId);
  