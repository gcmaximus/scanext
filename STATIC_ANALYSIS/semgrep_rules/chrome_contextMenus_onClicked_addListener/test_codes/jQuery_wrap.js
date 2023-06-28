/*******************
chrome_contextMenus_onClicked_addListener-jQuery_wrap
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    $("f").wrap(n.linkUrl); // Expect 1 match here
    $("f").wrap(n.srcUrl); // Expect 1 match here
    $("f").wrap(n.pageUrl); // Expect 1 match here
    $("f").wrap(n.frameUrl); // Expect 1 match here
    $("f").wrap(n.selectionText); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n.selectionText;
    $("f").wrap(x); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n.linkUrl;
$("f").wrap(x);

chrome.contextMenus.onClicked.addListener(kms);

// case 2
chrome.contextMenus.onClicked.addListener(aaa);

let b = n.linkUrl;
$("f").wrap(x);

function aaa(n, a) {
    console.log();
    $("f").wrap(n.linkUrl); // Expect 1 match here
    $("f").wrap(n.srcUrl); // Expect 1 match here
    $("f").wrap(n.pageUrl); // Expect 1 match here
    $("f").wrap(n.frameUrl); // Expect 1 match here
    $("f").wrap(n.selectionText); // Expect 1 match here

    $("f").wrap(a.linkUrl);
    console.log();

    let x = n.linkUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n.selectionText;
    $("f").wrap(x); // Expect 1 match here
    console.log();
}

// case 3
chrome.contextMenus.onClicked.addListener(function (n, a) {
    console.log();
    $("f").wrap(n.linkUrl); // Expect 1 match here
    $("f").wrap(n.srcUrl); // Expect 1 match here
    $("f").wrap(n.pageUrl); // Expect 1 match here
    $("f").wrap(n.frameUrl); // Expect 1 match here
    $("f").wrap(n.selectionText); // Expect 1 match here
    console.log();

    let x = n.linkUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n.selectionText;
    $("f").wrap(x); // Expect 1 match here
    console.log();
});

// case 4
chrome.contextMenus.onClicked.addListener(function bbb(n, a) {
    console.log();
    $("f").wrap(n.linkUrl); // Expect 1 match here
    $("f").wrap(n.srcUrl); // Expect 1 match here
    $("f").wrap(n.pageUrl); // Expect 1 match here
    $("f").wrap(n.frameUrl); // Expect 1 match here
    $("f").wrap(n.selectionText); // Expect 1 match here
    console.log();

    let x = n.linkUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n.selectionText;
    $("f").wrap(x); // Expect 1 match here
    console.log();

    $(x).wrap("f");
});
