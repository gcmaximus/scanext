// function toDo(tab) {
//     let tags = document.getElementsByTagName("h1");
//     // tags[0].innerHTML = `${tab.url.split("#")[1]}`;
//     tags[0].innerHTML = tab.url;

// }

async function getCurrentTab() {
    let queryOptions = { active: true, currentWindow: true };
    let [tab] = await chrome.tabs.query(queryOptions);
    return tab;
}

getCurrentTab().then((tab) => {
    document.getElementById('saaaa').innerHTML = tab.url
    // chrome.scripting.executeScript({
    //     target: { tabId: tab.id },
    //     func: toDo,
    //     args: [tab],
    // });
});