/*******************
chrome_debugger_getTargets-jQuery_insertAfter
*******************/

// Expected total matches: 40

// case 1
function kms(n) {
    console.log();
    $(n[0].linkUrl).insertAfter("f"); // Expect 1 match here
    $(n[0].srcUrl).insertAfter("f"); // Expect 1 match here
    $(n[0].pageUrl).insertAfter("f"); // Expect 1 match here
    $(n[0].frameUrl).insertAfter("f"); // Expect 1 match here
    $(n[0].selectionText).insertAfter("f"); // Expect 1 match here

    console.log();

    let x = n[0].linkUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n[0].srcUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n[0].pageUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n[0].frameUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n[0].selectionText;
    $(x).insertAfter("f"); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n[0].linkUrl;
$(x).insertAfter("f");

chrome.debugger.getTargets(kms);

// case 2
chrome.debugger.getTargets(aaa);

let b = n[0].linkUrl;
$(x).insertAfter("f");

function aaa(n) {
    console.log();
    $(n[0].linkUrl).insertAfter("f"); // Expect 1 match here
    $(n[0].srcUrl).insertAfter("f"); // Expect 1 match here
    $(n[0].pageUrl).insertAfter("f"); // Expect 1 match here
    $(n[0].frameUrl).insertAfter("f"); // Expect 1 match here
    $(n[0].selectionText).insertAfter("f"); // Expect 1 match here

    $("f").insertAfter(a.linkUrl);
    console.log();

    let x = n[0].linkUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n[0].srcUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n[0].pageUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n[0].frameUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n[0].selectionText;
    $(x).insertAfter("f"); // Expect 1 match here
    console.log();
}

// case 3
chrome.debugger.getTargets(function (n) {
    console.log();
    $(n[0].linkUrl).insertAfter("f"); // Expect 1 match here
    $(n[0].srcUrl).insertAfter("f"); // Expect 1 match here
    $(n[0].pageUrl).insertAfter("f"); // Expect 1 match here
    $(n[0].frameUrl).insertAfter("f"); // Expect 1 match here
    $(n[0].selectionText).insertAfter("f"); // Expect 1 match here
    console.log();

    let x = n[0].linkUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n[0].srcUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n[0].pageUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n[0].frameUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n[0].selectionText;
    $(x).insertAfter("f"); // Expect 1 match here
    console.log();
});

// case 4
chrome.debugger.getTargets(function bbb(n) {
    console.log();
    $(n[0].linkUrl).insertAfter("f"); // Expect 1 match here
    $(n[0].srcUrl).insertAfter("f"); // Expect 1 match here
    $(n[0].pageUrl).insertAfter("f"); // Expect 1 match here
    $(n[0].frameUrl).insertAfter("f"); // Expect 1 match here
    $(n[0].selectionText).insertAfter("f"); // Expect 1 match here
    console.log();

    let x = n[0].linkUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n[0].srcUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n[0].pageUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n[0].frameUrl;
    $(x).insertAfter("f"); // Expect 1 match here

    x = n[0].selectionText;
    $(x).insertAfter("f"); // Expect 1 match here
    console.log();
});
