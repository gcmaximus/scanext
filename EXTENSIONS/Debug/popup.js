function replace(target) {
    const elements = document.getElementsByTagName('h1');
    for (let i = 0; i < elements.length; i++) {
        elements[i].innerHTML = `Your target title is: ${target.title}`
    }
}

async function getCurrentTab() {
    let queryOptions = { active: true, currentWindow: true };
    let [tab] = await chrome.tabs.query(queryOptions);
    return tab;
}


chrome.debugger.getTargets((targets) => {
    // find all targets with attached = True (dev tools open)
    console.log(targets)
    var selected
    for (i = 0; i < targets.length; i++) {
        if (targets[i].attached) {
            selected = targets[i]
            break
        }
    }

    console.log('selected target (hopefully https://example.com)')
    console.log(selected)
    getCurrentTab().then((tab) => {
        chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: replace,
            args: [selected]
        })
    })

})

// getCurrentTab().then((tab) => {
//     console.log('tab: ', tab)
//     chrome.scripting.executeScript({
//         target: { tabId: tab.id },
//         func: getChromeTarget,
//         args: [tab]
//     });
// });