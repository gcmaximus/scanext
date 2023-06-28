/*******************
chrome_contextMenus_onClicked_addListener-jQuery_prependTo
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    $(n.linkUrl).prependTo("f"); // Expect 1 match here
    $(n.srcUrl).prependTo("f"); // Expect 1 match here
    $(n.pageUrl).prependTo("f"); // Expect 1 match here
    $(n.frameUrl).prependTo("f"); // Expect 1 match here
    $(n.selectionText).prependTo("f"); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.srcUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.pageUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.frameUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.selectionText;
    $(x).prependTo("f"); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n.linkUrl;
$(x).prependTo("f");

chrome.contextMenus.onClicked.addListener(kms);

// case 2
chrome.contextMenus.onClicked.addListener(aaa);

let b = n.linkUrl;
$(x).prependTo("f");

function aaa(n, a) {
    console.log();
    $(n.linkUrl).prependTo("f"); // Expect 1 match here
    $(n.srcUrl).prependTo("f"); // Expect 1 match here
    $(n.pageUrl).prependTo("f"); // Expect 1 match here
    $(n.frameUrl).prependTo("f"); // Expect 1 match here
    $(n.selectionText).prependTo("f"); // Expect 1 match here

    $("f").prependTo(a.linkUrl);
    console.log();

    let x = n.linkUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.srcUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.pageUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.frameUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.selectionText;
    $(x).prependTo("f"); // Expect 1 match here
    console.log();
}

// case 3
chrome.contextMenus.onClicked.addListener(function (n, a) {
    console.log();
    $(n.linkUrl).prependTo("f"); // Expect 1 match here
    $(n.srcUrl).prependTo("f"); // Expect 1 match here
    $(n.pageUrl).prependTo("f"); // Expect 1 match here
    $(n.frameUrl).prependTo("f"); // Expect 1 match here
    $(n.selectionText).prependTo("f"); // Expect 1 match here
    console.log();

    let x = n.linkUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.srcUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.pageUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.frameUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.selectionText;
    $(x).prependTo("f"); // Expect 1 match here
    console.log();
});

// case 4
chrome.contextMenus.onClicked.addListener(function bbb(n, a) {
    console.log();
    $(n.linkUrl).prependTo("f"); // Expect 1 match here
    $(n.srcUrl).prependTo("f"); // Expect 1 match here
    $(n.pageUrl).prependTo("f"); // Expect 1 match here
    $(n.frameUrl).prependTo("f"); // Expect 1 match here
    $(n.selectionText).prependTo("f"); // Expect 1 match here
    console.log();

    let x = n.linkUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.srcUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.pageUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.frameUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.selectionText;
    $(x).prependTo("f"); // Expect 1 match here
    console.log();
});
