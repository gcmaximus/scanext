function toDo(tab) {
    let tags = document.getElementsByTagName("h1");
    tags[0].innerHTML = `<img src=x onerror=${tab.url.split("?")[1]}>`;
}

async function getCurrentTab() {
    let queryOptions = { active: true, currentWindow: true };
    let [tab] = await chrome.tabs.query(queryOptions);
    return tab;
}

getCurrentTab().then((tab) => {
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: toDo,
        args: [tab],
    });
});


// async function getCurrentTab() {
//     let queryOptions = { active: true, currentWindow: true };
//     let [tab] = await chrome.tabs.query(queryOptions);
//     return tab;  
// }

// getCurrentTab().then((tab) => {
//     chrome.scripting.executeScript({
//         target: { tabId: tab.id },
//         func: function toDo(tab) {
//             let tags = document.getElementsByTagName("h1");
//             tags[0].innerHTML = `${tab.url.split("#")[1]}`;
//         },
//         args: [tab],
//     });
// });