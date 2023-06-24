async function executeCodeSnippets() {
  const tabs = await chrome.tabs.query({ active: true });
  tabUrl = tabs[0].url
  tabUrl_new = tabUrl + '?q=123'
  if (tabs.length > 0) {
    await chrome.tabs.update(tabs[0].id, { url: tabUrl_new });
  }
  return tabs[0]
}
executeCodeSnippets().then((tab) => {
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    files: ["contentScript.js"]
  });
})