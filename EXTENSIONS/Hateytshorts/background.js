// chrome.runtime.onMessage.addListener((request) => {
//     console.log(request.message)
// });

chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
        console.log('Message received in background.js:', request.message);
        if (request.message) {
            chrome.scripting.executeScript({
                target: { tabId: tabs[0].id },
                function: replaceH1Text,
                args: [request.message]
            });
        }
    })
});

function replaceH1Text(message) {
    document.querySelector('h1').innerHTML = message;
}
  



