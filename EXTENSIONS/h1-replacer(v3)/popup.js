async function getCurrentTab() {
  // let queryOptions = { active: false, lastFocusedWindow: true };
  let queryOptions = { active: true, lastFocusedWindow: true };

  // `tab` will either be a `tabs.Tab` instance or `undefined`.
  let [tab] = await chrome.tabs.query(queryOptions);
  console.log(tab)
  tabUrl = tab.url

  await chrome.tabs.update(tab.id, { url: tabUrl })

  return tab;
}

getCurrentTab().then((tab) => {

  // document.getElementsByTagName("h1")[0].innerHTML = tab.title
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    files: ["contentScript.js"]
    // function: setTabUrl,
  });

})
