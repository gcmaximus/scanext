function abc() {
    window.addEventListener("message", (event) => {
        console.log(event.data)
        xyz = event.data
        tags = document.getElementsByTagName('h1')
        tags[0].innerHTML = xyz.message_1 + ' abc '
    })
    // PAYLOAD: 
    // postMessage({ message: "<img src=x onerror=alert(1)>" }, location.href)

}


chrome.tabs.query({
    active: true,
    currentWindow: true
}, function (tabs) {
    chrome.scripting.executeScript({
        target: {
            tabId: tabs[0].id
        },
        func: abc,
        args: []
    })
});
