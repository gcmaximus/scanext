/*******************
chrome_debugger_getTargets-jQuery_wrapInner
*******************/

// Expected total matches: 40

// case 1
function kms(n) {
    console.log();
    $("f").wrapInner(n[0].linkUrl); // Expect 1 match here
    $("f").wrapInner(n[0].srcUrl); // Expect 1 match here
    $("f").wrapInner(n[0].pageUrl); // Expect 1 match here
    $("f").wrapInner(n[0].frameUrl); // Expect 1 match here
    $("f").wrapInner(n[0].selectionText); // Expect 1 match here

    console.log();

    let x = n[0].linkUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n[0].srcUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n[0].pageUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n[0].frameUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n[0].selectionText;
    $("f").wrapInner(x); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n[0].linkUrl;
$("f").wrapInner(x);

chrome.debugger.getTargets(kms);

// case 2
chrome.debugger.getTargets(aaa);

let b = n[0].linkUrl;
$("f").wrapInner(x);

function aaa(n) {
    console.log();
    $("f").wrapInner(n[0].linkUrl); // Expect 1 match here
    $("f").wrapInner(n[0].srcUrl); // Expect 1 match here
    $("f").wrapInner(n[0].pageUrl); // Expect 1 match here
    $("f").wrapInner(n[0].frameUrl); // Expect 1 match here
    $("f").wrapInner(n[0].selectionText); // Expect 1 match here

    $("f").wrapInner(a.linkUrl);
    console.log();

    let x = n[0].linkUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n[0].srcUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n[0].pageUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n[0].frameUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n[0].selectionText;
    $("f").wrapInner(x); // Expect 1 match here
    console.log();
}

// case 3
chrome.debugger.getTargets(function (n) {
    console.log();
    $("f").wrapInner(n[0].linkUrl); // Expect 1 match here
    $("f").wrapInner(n[0].srcUrl); // Expect 1 match here
    $("f").wrapInner(n[0].pageUrl); // Expect 1 match here
    $("f").wrapInner(n[0].frameUrl); // Expect 1 match here
    $("f").wrapInner(n[0].selectionText); // Expect 1 match here
    console.log();

    let x = n[0].linkUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n[0].srcUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n[0].pageUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n[0].frameUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n[0].selectionText;
    $("f").wrapInner(x); // Expect 1 match here
    console.log();
});

// case 4
chrome.debugger.getTargets(function bbb(n) {
    console.log();
    $("f").wrapInner(n[0].linkUrl); // Expect 1 match here
    $("f").wrapInner(n[0].srcUrl); // Expect 1 match here
    $("f").wrapInner(n[0].pageUrl); // Expect 1 match here
    $("f").wrapInner(n[0].frameUrl); // Expect 1 match here
    $("f").wrapInner(n[0].selectionText); // Expect 1 match here
    console.log();

    let x = n[0].linkUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n[0].srcUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n[0].pageUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n[0].frameUrl;
    $("f").wrapInner(x); // Expect 1 match here

    x = n[0].selectionText;
    $("f").wrapInner(x); // Expect 1 match here
    console.log();

    $(x).wrapInner("f");
});
