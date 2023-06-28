/*******************
chrome_contextMenus_onClicked_addListener-jQuery_wrapInner
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    $("f").wrapInner(n.linkUrl); // Expect 1 match here
    $("f").wrapInner(n.srcUrl); // Expect 1 match here
    $("f").wrapInner(n.pageUrl); // Expect 1 match here
    $("f").wrapInner(n.frameUrl); // Expect 1 match here
    $("f").wrapInner(n.selectionText); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n.selectionText;
    $("f").wrapInner(x); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n.linkUrl;
$("f").wrapInner(x);

chrome.contextMenus.onClicked.addListener(kms);

// case 2
chrome.contextMenus.onClicked.addListener(aaa);

let b = n.linkUrl;
$("f").wrapInner(x);

function aaa(n, a) {
    console.log();
    $("f").wrapInner(n.linkUrl); // Expect 1 match here
    $("f").wrapInner(n.srcUrl); // Expect 1 match here
    $("f").wrapInner(n.pageUrl); // Expect 1 match here
    $("f").wrapInner(n.frameUrl); // Expect 1 match here
    $("f").wrapInner(n.selectionText); // Expect 1 match here

    $("f").wrapInner(a.linkUrl);
    console.log();

    let x = n.linkUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n.selectionText;
    $("f").wrapInner(x); // Expect 1 match here
    console.log();
}

// case 3
chrome.contextMenus.onClicked.addListener(function (n, a) {
    console.log();
    $("f").wrapInner(n.linkUrl); // Expect 1 match here
    $("f").wrapInner(n.srcUrl); // Expect 1 match here
    $("f").wrapInner(n.pageUrl); // Expect 1 match here
    $("f").wrapInner(n.frameUrl); // Expect 1 match here
    $("f").wrapInner(n.selectionText); // Expect 1 match here
    console.log();

    let x = n.linkUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n.selectionText;
    $("f").wrapInner(x); // Expect 1 match here
    console.log();
});

// case 4
chrome.contextMenus.onClicked.addListener(function bbb(n, a) {
    console.log();
    $("f").wrapInner(n.linkUrl); // Expect 1 match here
    $("f").wrapInner(n.srcUrl); // Expect 1 match here
    $("f").wrapInner(n.pageUrl); // Expect 1 match here
    $("f").wrapInner(n.frameUrl); // Expect 1 match here
    $("f").wrapInner(n.selectionText); // Expect 1 match here
    console.log();

    let x = n.linkUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n.selectionText;
    $("f").wrapInner(x); // Expect 1 match here
    console.log();

    $(x).wrapInner("f");
});
