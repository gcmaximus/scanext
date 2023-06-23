async function updateTabUrl(windowId, newUrl) {
    try {
      const all = await chrome.tabs.getAllInWindow(windowId)
      const def = all[0]
      if (true) {
        // Update the URL property of the retrieved tab using chrome.tabs.update
        const abc = await chrome.tabs.update(all.id, { url: all.url });
        console.log("Tab URL updated:", abc);
      }
    } catch (error) {
      console.error("Error occurred:", error);
    }
  }
  
  // Usage: Call the function and pass the tab ID and new URL as arguments
  const tabId = 123; // Replace with the actual tab ID
  updateTabUrl(tabId, newUrl);
  