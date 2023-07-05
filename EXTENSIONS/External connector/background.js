// chrome.runtime.onConnectExternal.addListener((port) => {
//     if (port.name === 'replaceH1Port') {
//         port.onMessage.addListener((message) => {
//             if (message.action === 'replaceH1') {
//                 chrome.scripting.executeScript({
//                     target: { tabId: port.sender.tab.id },
//                     function: replaceH1,
//                     args: [message.text]
//                 });
//             }
//         });
//     }
// });

// function replaceH1(text) {
//     const h1Element = document.querySelector('h1');
//     if (h1Element) {
//         h1Element.innerHTML = text;
//     }
// }    RIFQI COMMENTED LINE 1 TO 20
// send this from a external extension/console
// const extensionId = 'YOUR_EXTENSION_ID'; // Replace with your extension's ID

// chrome.runtime.connect(extensionId, { name: 'replaceH1Port' }, (port) => {
//     port.postMessage({
//         action: 'replaceH1',
//         text: 'Hello from external source!'
//     });
// });
chrome.scripting.executeScript({
    target: { tabId: port.sender.tab.id },
    function: replaceH1,
    args: [message.text]
});

function replaceH1(text) {
    chrome.runtime.onConnectExternal.addListener((port) => {
    if (port.name === 'replaceH1Port') {
        port.onMessage.addListener((message) => {
            if (message.action === 'replaceH1') {
              const h1Element = document.querySelector('h1');
              if (h1Element) {
                  h1Element.innerHTML = text;
              }
            }
        });
    }
});
}
// RIFQI added lines 30- 50
