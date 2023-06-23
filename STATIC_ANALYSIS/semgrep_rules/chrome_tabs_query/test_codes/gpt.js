async function executeCodeSnippets() {
    // Code snippet 1: Updating the URL of the first tab matching a specific URL pattern
    const tabs1 = await chrome.tabs.query({ url: "https://example.com/*" });
    if (tabs1.length > 0) {
      await chrome.tabs.update(tabs1[0].id, { url: "https://newurl.com/" });
    }
  
    // Code snippet 2: Updating the title of all tabs matching a specific URL pattern
    const tabs2 = await chrome.tabs.query({ url: "https://example.com/*" });
    for (const tab of tabs2) {
      await chrome.tabs.update(tab.id, { title: "Updated Title" });
    }
  
    // Code snippet 3: Updating the pinned status of all tabs in the current window
    const tabs3 = await chrome.tabs.query({ currentWindow: true });
    for (const tab of tabs3) {
      await chrome.tabs.update(tab.id, { pinned: true });
    }
  
    // Code snippet 4: Updating the active tab's URL to a predefined value
    const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });
    await chrome.tabs.update(activeTab.id, { url: "https://newurl.com/" });
  
    // Code snippet 5: Updating the zoom level of all tabs in the current window
    const tabs5 = await chrome.tabs.query({ currentWindow: true });
    for (const tab of tabs5) {
      await chrome.tabs.update(tab.id, { zoom: 1.5 });
    }
  
    // Code snippet 6: Updating the muted status of the last tab opened
    const [lastFocusedWindow] = await chrome.tabs.query({ lastFocusedWindow: true });
    const lastTab = lastFocusedWindow.tabs[lastFocusedWindow.tabs.length - 1];
    await chrome.tabs.update(lastTab.id, { muted: true });
  
    // Code snippet 7: Updating the highlighted status of all tabs matching a specific URL pattern
    const tabs7 = await chrome.tabs.query({ url: "https://example.com/*" });
    const tabIds = tabs7.map(tab => tab.id);
    await chrome.tabs.update(tabIds, { highlighted: true });
  
    // Code snippet 8: Updating the position of the second tab in the current window
    const tabs8 = await chrome.tabs.query({ currentWindow: true });
    if (tabs8.length > 1) {
      const secondTab = tabs8[1];
      await chrome.tabs.update(secondTab.id, { index: 0 });
    }
  
    // Code snippet 9: Updating the pinned status of a specific tab by its ID
    const tabId = 123; // Replace with the actual tab ID
    await chrome.tabs.update(tabId, { pinned: true });
  
    // Code snippet 10: Updating the URL and title of the active tab simultaneously
    const [activeTab10] = await chrome.tabs.query({ active: true, currentWindow: true });
    await chrome.tabs.update(activeTab10.id, { url: "https://newurl.com/", title: "Updated Title" });
  }
  
  executeCodeSnippets();
  