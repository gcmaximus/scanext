chrome.runtime.onMessageExternal.addListener((message, sender, sendResponse) => {
    if (message.action === 'replaceH1') {
        chrome.scripting.executeScript({
            target: { tabId: sender.tab.id },
            function: replaceH1,
            args: [message.text]
        });
    }
});

function replaceH1(text) {
    const h1Element = document.querySelector('h1');
    if (h1Element) {
        h1Element.textContent = text;
    }
}
//Follow below to send message and test
//   const extensionId = 'YOUR_EXTENSION_ID'; // Replace with the ID of the target extension

//   chrome.runtime.sendMessage(extensionId, {
//     action: 'replaceH1',
//     text: 'Hello from external source!'
//   });
