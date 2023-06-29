/*******************
chrome_debugger_getTargets-jQuery_html
*******************/

// Expected total matches: 40

// case 1
function kms(n) {
    console.log();
    $("f").html(n[0].linkUrl); // Expect 1 match here
    $("f").html(n[0].srcUrl); // Expect 1 match here
    $("f").html(n[0].pageUrl); // Expect 1 match here
    $("f").html(n[0].frameUrl); // Expect 1 match here
    $("f").html(n[0].selectionText); // Expect 1 match here

    console.log();

    let x = n[0].linkUrl;
    $("f").html(x); // Expect 1 match here

    x = n[0].srcUrl;
    $("f").html(x); // Expect 1 match here

    x = n[0].pageUrl;
    $("f").html(x); // Expect 1 match here

    x = n[0].frameUrl;
    $("f").html(x); // Expect 1 match here

    x = n[0].selectionText;
    $("f").html(x); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n[0].linkUrl;
$("f").html(x);

chrome.debugger.getTargets(kms);

// case 2
chrome.debugger.getTargets(aaa);

let b = n[0].linkUrl;
$("f").html(x);

function aaa(n) {
    console.log();
    $("f").html(n[0].linkUrl); // Expect 1 match here
    $("f").html(n[0].srcUrl); // Expect 1 match here
    $("f").html(n[0].pageUrl); // Expect 1 match here
    $("f").html(n[0].frameUrl); // Expect 1 match here
    $("f").html(n[0].selectionText); // Expect 1 match here

    $("f").html(a.linkUrl);
    console.log();

    let x = n[0].linkUrl;
    $("f").html(x); // Expect 1 match here

    x = n[0].srcUrl;
    $("f").html(x); // Expect 1 match here

    x = n[0].pageUrl;
    $("f").html(x); // Expect 1 match here

    x = n[0].frameUrl;
    $("f").html(x); // Expect 1 match here

    x = n[0].selectionText;
    $("f").html(x); // Expect 1 match here
    console.log();
}

// case 3
chrome.debugger.getTargets(function (n) {
    console.log();
    $("f").html(n[0].linkUrl); // Expect 1 match here
    $("f").html(n[0].srcUrl); // Expect 1 match here
    $("f").html(n[0].pageUrl); // Expect 1 match here
    $("f").html(n[0].frameUrl); // Expect 1 match here
    $("f").html(n[0].selectionText); // Expect 1 match here
    console.log();

    let x = n[0].linkUrl;
    $("f").html(x); // Expect 1 match here

    x = n[0].srcUrl;
    $("f").html(x); // Expect 1 match here

    x = n[0].pageUrl;
    $("f").html(x); // Expect 1 match here

    x = n[0].frameUrl;
    $("f").html(x); // Expect 1 match here

    x = n[0].selectionText;
    $("f").html(x); // Expect 1 match here
    console.log();
});

// case 4
chrome.debugger.getTargets(function bbb(n) {
    console.log();
    $("f").html(n[0].linkUrl); // Expect 1 match here
    $("f").html(n[0].srcUrl); // Expect 1 match here
    $("f").html(n[0].pageUrl); // Expect 1 match here
    $("f").html(n[0].frameUrl); // Expect 1 match here
    $("f").html(n[0].selectionText); // Expect 1 match here
    console.log();

    let x = n[0].linkUrl;
    $("f").html(x); // Expect 1 match here

    x = n[0].srcUrl;
    $("f").html(x); // Expect 1 match here

    x = n[0].pageUrl;
    $("f").html(x); // Expect 1 match here

    x = n[0].frameUrl;
    $("f").html(x); // Expect 1 match here

    x = n[0].selectionText;
    $("f").html(x); // Expect 1 match here
    console.log();

    $(x).html("f");
});
