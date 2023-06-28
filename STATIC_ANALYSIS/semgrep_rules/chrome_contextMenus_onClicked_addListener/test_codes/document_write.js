/*******************
chrome_contextMenus_onClicked_addListener-document_write
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    document.write(n.linkUrl); // Expect 1 match here
    document.write(n.srcUrl); // Expect 1 match here
    document.write(n.pageUrl); // Expect 1 match here
    document.write(n.frameUrl); // Expect 1 match here
    document.write(n.selectionText); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    document.write(x); // Expect 1 match here

    x = n.srcUrl;
    document.write(x); // Expect 1 match here

    x = n.pageUrl;
    document.write(x); // Expect 1 match here

    x = n.frameUrl;
    document.write(x); // Expect 1 match here

    x = n.selectionText;
    document.write(x); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n.linkUrl;
document.write(x);

chrome.contextMenus.onClicked.addListener(kms);

// case 2
chrome.contextMenus.onClicked.addListener(aaa);

let b = n.linkUrl;
document.write(x);

function aaa(n, a) {
    console.log();
    document.write(n.linkUrl); // Expect 1 match here
    document.write(n.srcUrl); // Expect 1 match here
    document.write(n.pageUrl); // Expect 1 match here
    document.write(n.frameUrl); // Expect 1 match here
    document.write(n.selectionText); // Expect 1 match here

    document.write(a.linkUrl);
    console.log();

    let x = n.linkUrl;
    document.write(x); // Expect 1 match here

    x = n.srcUrl;
    document.write(x); // Expect 1 match here

    x = n.pageUrl;
    document.write(x); // Expect 1 match here

    x = n.frameUrl;
    document.write(x); // Expect 1 match here

    x = n.selectionText;
    document.write(x); // Expect 1 match here
    console.log();
}

// case 3
chrome.contextMenus.onClicked.addListener(function (n, a) {
    console.log();
    document.write(n.linkUrl); // Expect 1 match here
    document.write(n.srcUrl); // Expect 1 match here
    document.write(n.pageUrl); // Expect 1 match here
    document.write(n.frameUrl); // Expect 1 match here
    document.write(n.selectionText); // Expect 1 match here
    console.log();

    let x = n.linkUrl;
    document.write(x); // Expect 1 match here

    x = n.srcUrl;
    document.write(x); // Expect 1 match here

    x = n.pageUrl;
    document.write(x); // Expect 1 match here

    x = n.frameUrl;
    document.write(x); // Expect 1 match here

    x = n.selectionText;
    document.write(x); // Expect 1 match here
    console.log();
});

// case 4
chrome.contextMenus.onClicked.addListener(function bbb(n, a) {
    console.log();
    document.write(n.linkUrl); // Expect 1 match here
    document.write(n.srcUrl); // Expect 1 match here
    document.write(n.pageUrl); // Expect 1 match here
    document.write(n.frameUrl); // Expect 1 match here
    document.write(n.selectionText); // Expect 1 match here
    console.log();

    let x = n.linkUrl;
    document.write(x); // Expect 1 match here

    x = n.srcUrl;
    document.write(x); // Expect 1 match here

    x = n.pageUrl;
    document.write(x); // Expect 1 match here

    x = n.frameUrl;
    document.write(x); // Expect 1 match here

    x = n.selectionText;
    document.write(x); // Expect 1 match here
    console.log();
});
