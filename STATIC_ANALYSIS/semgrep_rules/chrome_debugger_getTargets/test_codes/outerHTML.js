/*******************
chrome_debugger_getTargets-outerHTML
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    document.getElementById("f").outerHTML = n[0].linkUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n[0].srcUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n[0].pageUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n[0].frameUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n[0].selectionText; // Expect 1 match here

    console.log();

    let x = n[0].linkUrl;
    document.getElementById("f").outerHTML = x; // Expect 1 match here

    x = n[0].srcUrl;
    document.getElementById("f").outerHTML = x; // Expect 1 match here

    x = n[0].pageUrl;
    document.getElementById("f").outerHTML = x; // Expect 1 match here

    x = n[0].frameUrl;
    document.getElementById("f").outerHTML = x; // Expect 1 match here

    x = n[0].selectionText;
    document.getElementById("f").outerHTML = x; // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n[0].linkUrl;
document.getElementById("f").outerHTML = x;

chrome.debugger.getTargets(kms);

// case 2
chrome.debugger.getTargets(aaa);

let b = n[0].linkUrl;
document.getElementById("f").outerHTML = x;

function aaa(n, a) {
    console.log();
    document.getElementById("f").outerHTML = n[0].linkUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n[0].srcUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n[0].pageUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n[0].frameUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n[0].selectionText; // Expect 1 match here

    document.getElementById("f").outerHTML = a.linkUrl;
    console.log();

    let x = n[0].linkUrl;
    document.getElementById("f").outerHTML = x; // Expect 1 match here

    x = n[0].srcUrl;
    document.getElementById("f").outerHTML = x; // Expect 1 match here

    x = n[0].pageUrl;
    document.getElementById("f").outerHTML = x; // Expect 1 match here

    x = n[0].frameUrl;
    document.getElementById("f").outerHTML = x; // Expect 1 match here

    x = n[0].selectionText;
    document.getElementById("f").outerHTML = x; // Expect 1 match here
    console.log();
}

// case 3
chrome.debugger.getTargets(function (n, a) {
    console.log();
    document.getElementById("f").outerHTML = n[0].linkUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n[0].srcUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n[0].pageUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n[0].frameUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n[0].selectionText; // Expect 1 match here
    console.log();

    let x = n[0].linkUrl;
    document.getElementById("f").outerHTML = x; // Expect 1 match here

    x = n[0].srcUrl;
    document.getElementById("f").outerHTML = x; // Expect 1 match here

    x = n[0].pageUrl;
    document.getElementById("f").outerHTML = x; // Expect 1 match here

    x = n[0].frameUrl;
    document.getElementById("f").outerHTML = x; // Expect 1 match here

    x = n[0].selectionText;
    document.getElementById("f").outerHTML = x; // Expect 1 match here
    console.log();
});

// case 4
chrome.debugger.getTargets(function bbb(n, a) {
    console.log();
    document.getElementById("f").outerHTML = n[0].linkUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n[0].srcUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n[0].pageUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n[0].frameUrl; // Expect 1 match here
    document.getElementById("f").outerHTML = n[0].selectionText; // Expect 1 match here
    console.log();

    let x = n[0].linkUrl;
    document.getElementById("f").outerHTML = x; // Expect 1 match here

    x = n[0].srcUrl;
    document.getElementById("f").outerHTML = x; // Expect 1 match here

    x = n[0].pageUrl;
    document.getElementById("f").outerHTML = x; // Expect 1 match here

    x = n[0].frameUrl;
    document.getElementById("f").outerHTML = x; // Expect 1 match here

    x = n[0].selectionText;
    document.getElementById("f").outerHTML = x; // Expect 1 match here
    console.log();

    document.getElementById(x).outerHTML = "a";
});
