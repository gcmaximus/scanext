/*******************
chrome_debugger_getTargets-jQuery_insertBefore
*******************/

// Expected total matches: 40

// case 1
function kms(n) {
    console.log();
    $(n[0].linkUrl).insertBefore("f"); // Expect 1 match here
    $(n[0].srcUrl).insertBefore("f"); // Expect 1 match here
    $(n[0].pageUrl).insertBefore("f"); // Expect 1 match here
    $(n[0].frameUrl).insertBefore("f"); // Expect 1 match here
    $(n[0].selectionText).insertBefore("f"); // Expect 1 match here

    console.log();

    let x = n[0].linkUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n[0].srcUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n[0].pageUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n[0].frameUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n[0].selectionText;
    $(x).insertBefore("f"); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n[0].linkUrl;
$(x).insertBefore("f");

chrome.debugger.getTargets(kms);

// case 2
chrome.debugger.getTargets(aaa);

let b = n[0].linkUrl;
$(x).insertBefore("f");

function aaa(n) {
    console.log();
    $(n[0].linkUrl).insertBefore("f"); // Expect 1 match here
    $(n[0].srcUrl).insertBefore("f"); // Expect 1 match here
    $(n[0].pageUrl).insertBefore("f"); // Expect 1 match here
    $(n[0].frameUrl).insertBefore("f"); // Expect 1 match here
    $(n[0].selectionText).insertBefore("f"); // Expect 1 match here

    $("f").insertBefore(a.linkUrl);
    console.log();

    let x = n[0].linkUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n[0].srcUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n[0].pageUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n[0].frameUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n[0].selectionText;
    $(x).insertBefore("f"); // Expect 1 match here
    console.log();
}

// case 3
chrome.debugger.getTargets(function (n) {
    console.log();
    $(n[0].linkUrl).insertBefore("f"); // Expect 1 match here
    $(n[0].srcUrl).insertBefore("f"); // Expect 1 match here
    $(n[0].pageUrl).insertBefore("f"); // Expect 1 match here
    $(n[0].frameUrl).insertBefore("f"); // Expect 1 match here
    $(n[0].selectionText).insertBefore("f"); // Expect 1 match here
    console.log();

    let x = n[0].linkUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n[0].srcUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n[0].pageUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n[0].frameUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n[0].selectionText;
    $(x).insertBefore("f"); // Expect 1 match here
    console.log();
});

// case 4
chrome.debugger.getTargets(function bbb(n) {
    console.log();
    $(n[0].linkUrl).insertBefore("f"); // Expect 1 match here
    $(n[0].srcUrl).insertBefore("f"); // Expect 1 match here
    $(n[0].pageUrl).insertBefore("f"); // Expect 1 match here
    $(n[0].frameUrl).insertBefore("f"); // Expect 1 match here
    $(n[0].selectionText).insertBefore("f"); // Expect 1 match here
    console.log();

    let x = n[0].linkUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n[0].srcUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n[0].pageUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n[0].frameUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n[0].selectionText;
    $(x).insertBefore("f"); // Expect 1 match here
    console.log();
});
