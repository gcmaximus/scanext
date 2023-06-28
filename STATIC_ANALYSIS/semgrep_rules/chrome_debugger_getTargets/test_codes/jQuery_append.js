/*******************
chrome_debugger_getTargets-jQuery_append
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    $("f").append(n[0].linkUrl); // Expect 1 match here
    $("f").append(n[0].srcUrl); // Expect 1 match here
    $("f").append(n[0].pageUrl); // Expect 1 match here
    $("f").append(n[0].frameUrl); // Expect 1 match here
    $("f").append(n[0].selectionText); // Expect 1 match here

    console.log();

    let x = n[0].linkUrl;
    $("f").append(x); // Expect 1 match here

    x = n[0].srcUrl;
    $("f").append(x); // Expect 1 match here

    x = n[0].pageUrl;
    $("f").append(x); // Expect 1 match here

    x = n[0].frameUrl;
    $("f").append(x); // Expect 1 match here

    x = n[0].selectionText;
    $("f").append(x); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n[0].linkUrl;
$("f").append(x);

chrome.debugger.getTargets(kms);

// case 2
chrome.debugger.getTargets(aaa);

let b = n[0].linkUrl;
$("f").append(x);

function aaa(n, a) {
    console.log();
    $("f").append(n[0].linkUrl); // Expect 1 match here
    $("f").append(n[0].srcUrl); // Expect 1 match here
    $("f").append(n[0].pageUrl); // Expect 1 match here
    $("f").append(n[0].frameUrl); // Expect 1 match here
    $("f").append(n[0].selectionText); // Expect 1 match here

    $("f").append(a.linkUrl);
    console.log();

    let x = n[0].linkUrl;
    $("f").append(x); // Expect 1 match here

    x = n[0].srcUrl;
    $("f").append(x); // Expect 1 match here

    x = n[0].pageUrl;
    $("f").append(x); // Expect 1 match here

    x = n[0].frameUrl;
    $("f").append(x); // Expect 1 match here

    x = n[0].selectionText;
    $("f").append(x); // Expect 1 match here
    console.log();
}

// case 3
chrome.debugger.getTargets(function (n, a) {
    console.log();
    $("f").append(n[0].linkUrl); // Expect 1 match here
    $("f").append(n[0].srcUrl); // Expect 1 match here
    $("f").append(n[0].pageUrl); // Expect 1 match here
    $("f").append(n[0].frameUrl); // Expect 1 match here
    $("f").append(n[0].selectionText); // Expect 1 match here
    console.log();

    let x = n[0].linkUrl;
    $("f").append(x); // Expect 1 match here

    x = n[0].srcUrl;
    $("f").append(x); // Expect 1 match here

    x = n[0].pageUrl;
    $("f").append(x); // Expect 1 match here

    x = n[0].frameUrl;
    $("f").append(x); // Expect 1 match here

    x = n[0].selectionText;
    $("f").append(x); // Expect 1 match here
    console.log();
});

// case 4
chrome.debugger.getTargets(function bbb(n, a) {
    console.log();
    $("f").append(n[0].linkUrl); // Expect 1 match here
    $("f").append(n[0].srcUrl); // Expect 1 match here
    $("f").append(n[0].pageUrl); // Expect 1 match here
    $("f").append(n[0].frameUrl); // Expect 1 match here
    $("f").append(n[0].selectionText); // Expect 1 match here
    console.log();

    let x = n[0].linkUrl;
    $("f").append(x); // Expect 1 match here

    x = n[0].srcUrl;
    $("f").append(x); // Expect 1 match here

    x = n[0].pageUrl;
    $("f").append(x); // Expect 1 match here

    x = n[0].frameUrl;
    $("f").append(x); // Expect 1 match here

    x = n[0].selectionText;
    $("f").append(x); // Expect 1 match here
    console.log();

    $(x).append("f");
});
