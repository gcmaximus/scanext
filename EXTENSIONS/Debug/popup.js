function getChromeTarget() {
    chrome.debugger.getTargets((targets) => {
        console.log(targets)
        var target
        for (i = 0; i < targets.length; i++) {
            if (targets[i].title == 'Example Domain') {
                target = targets[i]
                break
            }
        }
        console.log(target)
        const elements = document.getElementsByTagName('h1');
        for (let i = 0; i < elements.length; i++) {
            elements[i].innerHTML = `Your target title is: ${target.title}`
        }
    })
}

async function getCurrentTab() {
    let queryOptions = { active: true, currentWindow: true };
    let [tab] = await chrome.tabs.query(queryOptions);
    // console.log(tab)
    return tab;
}


getCurrentTab().then((tab) => {
    console.log(tab)
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: getChromeTarget,
    });
});