// Listen for messages from the popup or content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    // console.log(message.text);
    if (message.text) {
        // Modify the <h1> elements on the webpage
        chrome.tabs.query({}, (tabs) => {
            tabs.forEach((tab) => {
                chrome.scripting.executeScript({
                    target: {
                        tabId: tab.id
                    },
                    function: (
                    selectedText) => {
                        const h1Elements =
                            document
                            .getElementsByTagName(
                                "h1");
                        for (let i = 0; i <
                            h1Elements
                            .length; i++) {
                            h1Elements[i]
                                .innerHTML =
                                selectedText;
                        }
                    },
                    args: [message.text],
                });
            });
        });
    }
});
