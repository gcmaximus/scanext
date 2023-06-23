async function getCurrentTab() {
  let queryOptions = { active: true, lastFocusedWindow: true };
  let [tab] = await chrome.tabs.query(queryOptions);
  tabUrl = tab.url  //google.com
  await chrome.tabs.update(tab.id, { url: tabUrl })
  return tab;
}

getCurrentTab().then((tab) => {
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    files: ["contentScript.js"]
  });
})