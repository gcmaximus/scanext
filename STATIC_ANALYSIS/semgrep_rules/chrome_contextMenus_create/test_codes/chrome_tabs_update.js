// // chrome.tabs.update(
// //   tabId?: number,
// //   updateProperties: object,
// //   callback?: function,
// // )

// let abc = "javascript:" + window.name

// // should not match
// let wrong = { m: abc }
// chrome.tabs.update(cde, wrong, (tab) => { console.log(tab) })

// chrome.tabs.update(cde, { m: abc }, (tab) => { console.log(tab) })

// chrome.tabs.update(wrong)

// chrome.tabs.update({ m: abc })

// let wrong2 = { url: abc }
// chrome.tabs.update(1, 2, wrong2)

// // should match
// let rite = { url: abc }
// chrome.tabs.update(cde, rite, (tab) => { console.log(tab) })

// chrome.tabs.update(cde, { url: abc }, (tab) => { console.log(tab) })

// let rite2 = { url: abc }
// chrome.tabs.update(rite2)

// let rite3 = { url: abc }
// chrome.tabs.update(rite3, (tab) => { console.log(tab) })

// chrome.tabs.update({ url: abc })
