var tabs = await chrome.tabs.getAllInWindow(3)

target = tabs[1]

document.getElementById('ass').innerHTML = target.url