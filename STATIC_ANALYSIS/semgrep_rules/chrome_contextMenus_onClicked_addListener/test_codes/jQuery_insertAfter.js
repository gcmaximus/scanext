/*******************
chrome_contextMenus_onClicked_addListener-jQuery_insertAfter
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    $(n.linkUrl).insertAfter("f"); // Expect 1 match here
    $(n.srcUrl).insertAfter("f"); // Expect 1 match here
    $(n.pageUrl).insertAfter("f"); // Expect 1 match here
    $(n.frameUrl).insertAfter("f"); // Expect 1 match here
    $(n.selectionText).insertAfter("f"); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n.srcUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n.pageUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n.frameUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n.selectionText;
    $(x).insertAfter("f"); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n.linkUrl;
$(x).insertAfter("f");

chrome.contextMenus.onClicked.addListener(kms);

// case 2
chrome.contextMenus.onClicked.addListener(aaa);

let b = n.linkUrl;
$(x).insertAfter("f");

function aaa(n, a) {
    console.log();
    $(n.linkUrl).insertAfter("f"); // Expect 1 match here
    $(n.srcUrl).insertAfter("f"); // Expect 1 match here
    $(n.pageUrl).insertAfter("f"); // Expect 1 match here
    $(n.frameUrl).insertAfter("f"); // Expect 1 match here
    $(n.selectionText).insertAfter("f"); // Expect 1 match here

    $("f").insertAfter(a.linkUrl);
    console.log();

    let x = n.linkUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n.srcUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n.pageUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n.frameUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n.selectionText;
    $(x).insertAfter("f"); // Expect 1 match here
    console.log();
}

// case 3
chrome.contextMenus.onClicked.addListener(function (n, a) {
    console.log();
    $(n.linkUrl).insertAfter("f"); // Expect 1 match here
    $(n.srcUrl).insertAfter("f"); // Expect 1 match here
    $(n.pageUrl).insertAfter("f"); // Expect 1 match here
    $(n.frameUrl).insertAfter("f"); // Expect 1 match here
    $(n.selectionText).insertAfter("f"); // Expect 1 match here
    console.log();

    let x = n.linkUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n.srcUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n.pageUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n.frameUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n.selectionText;
    $(x).insertAfter("f"); // Expect 1 match here
    console.log();
});

// case 4
chrome.contextMenus.onClicked.addListener(function bbb(n, a) {
    console.log();
    $(n.linkUrl).insertAfter("f"); // Expect 1 match here
    $(n.srcUrl).insertAfter("f"); // Expect 1 match here
    $(n.pageUrl).insertAfter("f"); // Expect 1 match here
    $(n.frameUrl).insertAfter("f"); // Expect 1 match here
    $(n.selectionText).insertAfter("f"); // Expect 1 match here
    console.log();

    let x = n.linkUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n.srcUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n.pageUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n.frameUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n.selectionText;
    $(x).insertAfter("f"); // Expect 1 match here
    console.log();
});
