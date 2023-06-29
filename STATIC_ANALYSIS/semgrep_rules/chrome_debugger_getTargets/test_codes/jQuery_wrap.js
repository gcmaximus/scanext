/*******************
chrome_debugger_getTargets-jQuery_wrap
*******************/

// Expected total matches: 40

// case 1
function kms(n) {
    console.log();
    $("f").wrap(n[0].linkUrl); // Expect 1 match here
    $("f").wrap(n[0].srcUrl); // Expect 1 match here
    $("f").wrap(n[0].pageUrl); // Expect 1 match here
    $("f").wrap(n[0].frameUrl); // Expect 1 match here
    $("f").wrap(n[0].selectionText); // Expect 1 match here

    console.log();

    let x = n[0].linkUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n[0].srcUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n[0].pageUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n[0].frameUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n[0].selectionText;
    $("f").wrap(x); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n[0].linkUrl;
$("f").wrap(x);

chrome.debugger.getTargets(kms);

// case 2
chrome.debugger.getTargets(aaa);

let b = n[0].linkUrl;
$("f").wrap(x);

function aaa(n) {
    console.log();
    $("f").wrap(n[0].linkUrl); // Expect 1 match here
    $("f").wrap(n[0].srcUrl); // Expect 1 match here
    $("f").wrap(n[0].pageUrl); // Expect 1 match here
    $("f").wrap(n[0].frameUrl); // Expect 1 match here
    $("f").wrap(n[0].selectionText); // Expect 1 match here

    $("f").wrap(a.linkUrl);
    console.log();

    let x = n[0].linkUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n[0].srcUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n[0].pageUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n[0].frameUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n[0].selectionText;
    $("f").wrap(x); // Expect 1 match here
    console.log();
}

// case 3
chrome.debugger.getTargets(function (n) {
    console.log();
    $("f").wrap(n[0].linkUrl); // Expect 1 match here
    $("f").wrap(n[0].srcUrl); // Expect 1 match here
    $("f").wrap(n[0].pageUrl); // Expect 1 match here
    $("f").wrap(n[0].frameUrl); // Expect 1 match here
    $("f").wrap(n[0].selectionText); // Expect 1 match here
    console.log();

    let x = n[0].linkUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n[0].srcUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n[0].pageUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n[0].frameUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n[0].selectionText;
    $("f").wrap(x); // Expect 1 match here
    console.log();
});

// case 4
chrome.debugger.getTargets(function bbb(n) {
    console.log();
    $("f").wrap(n[0].linkUrl); // Expect 1 match here
    $("f").wrap(n[0].srcUrl); // Expect 1 match here
    $("f").wrap(n[0].pageUrl); // Expect 1 match here
    $("f").wrap(n[0].frameUrl); // Expect 1 match here
    $("f").wrap(n[0].selectionText); // Expect 1 match here
    console.log();

    let x = n[0].linkUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n[0].srcUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n[0].pageUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n[0].frameUrl;
    $("f").wrap(x); // Expect 1 match here

    x = n[0].selectionText;
    $("f").wrap(x); // Expect 1 match here
    console.log();

    $(x).wrap("f");
});
