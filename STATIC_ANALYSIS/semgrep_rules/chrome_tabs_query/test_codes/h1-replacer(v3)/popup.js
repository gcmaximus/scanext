function toDo(tab) {
    let tags = document.getElementsByTagName("h1");
    tags[0].innerHTML = `${tab.url.split("#")[1]}`;
}

async function getCurrentTab() {
    let queryOptions = { active: true, currentWindow: true };
    // let queryOptions = { active: true, lastFocusedWindow: true };

    // `tab` will either be a `tabs.Tab` instance or `undefined`.
    let [tab] = await chrome.tabs.query(queryOptions);
    return tab;
}

getCurrentTab().then((tab) => {
    // document.getElementsByTagName("h1")[0].innerHTML = tab.title
    console.log(tab);
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: toDo,
        args: [tab],
    });
});

// getCurrentTab().then((tab) => {
//     // document.getElementsByTagName("h1")[0].innerHTML = tab.title

//     chrome.scripting.executeScript({
//         target: { tabId: tab.id },
//         files: ["contentScript.js"],
//     });
// });
