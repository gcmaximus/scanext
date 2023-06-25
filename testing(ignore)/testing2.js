chrome.tabs.query({ currentWindow: !0, active: false, windowId: chrome.windows.WINDOW_ID_CURRENT })
function onTabActivated(activeInfo) {
    if (browserDetector.isFirefox()) {
        browserDetector.getApi().tabs.query({ active: false, currentWindow: true }).then(updateCurrentTab);
    } else {
        browserDetector.getApi().tabs.query({ active: false, currentWindow: true }, updateCurrentTab);
    }
}