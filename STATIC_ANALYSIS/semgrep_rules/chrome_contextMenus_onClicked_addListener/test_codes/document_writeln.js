/*******************
chrome_contextMenus_onClicked_addListener-document_write
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    document.writeln(n.linkUrl); // Expect 1 match here
    document.writeln(n.srcUrl); // Expect 1 match here
    document.writeln(n.pageUrl); // Expect 1 match here
    document.writeln(n.frameUrl); // Expect 1 match here
    document.writeln(n.selectionText); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    document.writeln(x); // Expect 1 match here

    x = n.srcUrl;
    document.writeln(x); // Expect 1 match here

    x = n.pageUrl;
    document.writeln(x); // Expect 1 match here

    x = n.frameUrl;
    document.writeln(x); // Expect 1 match here

    x = n.selectionText;
    document.writeln(x); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n.linkUrl;
document.writeln(x);

chrome.contextMenus.onClicked.addListener(kms);

// case 2
chrome.contextMenus.onClicked.addListener(aaa);

let b = n.linkUrl;
document.writeln(x);

function aaa(n, a) {
    console.log();
    document.writeln(n.linkUrl); // Expect 1 match here
    document.writeln(n.srcUrl); // Expect 1 match here
    document.writeln(n.pageUrl); // Expect 1 match here
    document.writeln(n.frameUrl); // Expect 1 match here
    document.writeln(n.selectionText); // Expect 1 match here

    document.writeln(a.linkUrl);
    console.log();

    let x = n.linkUrl;
    document.writeln(x); // Expect 1 match here

    x = n.srcUrl;
    document.writeln(x); // Expect 1 match here

    x = n.pageUrl;
    document.writeln(x); // Expect 1 match here

    x = n.frameUrl;
    document.writeln(x); // Expect 1 match here

    x = n.selectionText;
    document.writeln(x); // Expect 1 match here
    console.log();
}

// case 3
chrome.contextMenus.onClicked.addListener(function (n, a) {
    console.log();
    document.writeln(n.linkUrl); // Expect 1 match here
    document.writeln(n.srcUrl); // Expect 1 match here
    document.writeln(n.pageUrl); // Expect 1 match here
    document.writeln(n.frameUrl); // Expect 1 match here
    document.writeln(n.selectionText); // Expect 1 match here
    console.log();

    let x = n.linkUrl;
    document.writeln(x); // Expect 1 match here

    x = n.srcUrl;
    document.writeln(x); // Expect 1 match here

    x = n.pageUrl;
    document.writeln(x); // Expect 1 match here

    x = n.frameUrl;
    document.writeln(x); // Expect 1 match here

    x = n.selectionText;
    document.writeln(x); // Expect 1 match here
    console.log();
});

// case 4
chrome.contextMenus.onClicked.addListener(function bbb(n, a) {
    console.log();
    document.writeln(n.linkUrl); // Expect 1 match here
    document.writeln(n.srcUrl); // Expect 1 match here
    document.writeln(n.pageUrl); // Expect 1 match here
    document.writeln(n.frameUrl); // Expect 1 match here
    document.writeln(n.selectionText); // Expect 1 match here
    console.log();

    let x = n.linkUrl;
    document.writeln(x); // Expect 1 match here

    x = n.srcUrl;
    document.writeln(x); // Expect 1 match here

    x = n.pageUrl;
    document.writeln(x); // Expect 1 match here

    x = n.frameUrl;
    document.writeln(x); // Expect 1 match here

    x = n.selectionText;
    document.writeln(x); // Expect 1 match here
    console.log();
});
