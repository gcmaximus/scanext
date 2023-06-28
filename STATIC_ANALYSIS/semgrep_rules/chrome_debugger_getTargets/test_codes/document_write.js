/*******************
chrome_debugger_getTargets-document_write
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    document.write(n[0].linkUrl); // Expect 1 match here
    document.write(n[0].srcUrl); // Expect 1 match here
    document.write(n[0].pageUrl); // Expect 1 match here
    document.write(n[0].frameUrl); // Expect 1 match here
    document.write(n[0].selectionText); // Expect 1 match here

    console.log();

    let x = n[0].linkUrl;
    document.write(x); // Expect 1 match here

    x = n[0].srcUrl;
    document.write(x); // Expect 1 match here

    x = n[0].pageUrl;
    document.write(x); // Expect 1 match here

    x = n[0].frameUrl;
    document.write(x); // Expect 1 match here

    x = n[0].selectionText;
    document.write(x); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n[0].linkUrl;
document.write(x);

chrome.debugger.getTargets(kms);

// case 2
chrome.debugger.getTargets(aaa);

let b = n[0].linkUrl;
document.write(x);

function aaa(n, a) {
    console.log();
    document.write(n[0].linkUrl); // Expect 1 match here
    document.write(n[0].srcUrl); // Expect 1 match here
    document.write(n[0].pageUrl); // Expect 1 match here
    document.write(n[0].frameUrl); // Expect 1 match here
    document.write(n[0].selectionText); // Expect 1 match here

    document.write(a.linkUrl);
    console.log();

    let x = n[0].linkUrl;
    document.write(x); // Expect 1 match here

    x = n[0].srcUrl;
    document.write(x); // Expect 1 match here

    x = n[0].pageUrl;
    document.write(x); // Expect 1 match here

    x = n[0].frameUrl;
    document.write(x); // Expect 1 match here

    x = n[0].selectionText;
    document.write(x); // Expect 1 match here
    console.log();
}

// case 3
chrome.debugger.getTargets(function (n, a) {
    console.log();
    document.write(n[0].linkUrl); // Expect 1 match here
    document.write(n[0].srcUrl); // Expect 1 match here
    document.write(n[0].pageUrl); // Expect 1 match here
    document.write(n[0].frameUrl); // Expect 1 match here
    document.write(n[0].selectionText); // Expect 1 match here
    console.log();

    let x = n[0].linkUrl;
    document.write(x); // Expect 1 match here

    x = n[0].srcUrl;
    document.write(x); // Expect 1 match here

    x = n[0].pageUrl;
    document.write(x); // Expect 1 match here

    x = n[0].frameUrl;
    document.write(x); // Expect 1 match here

    x = n[0].selectionText;
    document.write(x); // Expect 1 match here
    console.log();
});

// case 4
chrome.debugger.getTargets(function bbb(n, a) {
    console.log();
    document.write(n[0].linkUrl); // Expect 1 match here
    document.write(n[0].srcUrl); // Expect 1 match here
    document.write(n[0].pageUrl); // Expect 1 match here
    document.write(n[0].frameUrl); // Expect 1 match here
    document.write(n[0].selectionText); // Expect 1 match here
    console.log();

    let x = n[0].linkUrl;
    document.write(x); // Expect 1 match here

    x = n[0].srcUrl;
    document.write(x); // Expect 1 match here

    x = n[0].pageUrl;
    document.write(x); // Expect 1 match here

    x = n[0].frameUrl;
    document.write(x); // Expect 1 match here

    x = n[0].selectionText;
    document.write(x); // Expect 1 match here
    console.log();
});
