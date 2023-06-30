const filter = {
    url: [
        {
            hostContains: 'youtube.com',
            pathContains: 'shorts'
        }
    ]
}

chrome.webNavigation.onHistoryStateUpdated.addListener((e) => {
    console.log(e);
    const newURL = e.url.replace('shorts', 'watch');
    chrome.tabs.update(e.tabId, { url: newURL });
}, filter);

// chrome.runtime.onMessage.addListener((request) => {
//     console.log(request.message)
// });

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request.message) {
        console.log('Message received in background.js:', request.message);
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            chrome.scripting.executeScript({
                target: { tabId: tabs[0].id },
                function: replaceH1Text,
                args: [request.message]
            });
        });
    }
});

function replaceH1Text(message) {
    document.querySelector('h1').innerHTML = message;
}
  



