/*******************
chrome_debugger_getTargets-jQuery_prependTo
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    $(n[0].linkUrl).prependTo("f"); // Expect 1 match here
    $(n[0].srcUrl).prependTo("f"); // Expect 1 match here
    $(n[0].pageUrl).prependTo("f"); // Expect 1 match here
    $(n[0].frameUrl).prependTo("f"); // Expect 1 match here
    $(n[0].selectionText).prependTo("f"); // Expect 1 match here

    console.log();

    let x = n[0].linkUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n[0].srcUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n[0].pageUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n[0].frameUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n[0].selectionText;
    $(x).prependTo("f"); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n[0].linkUrl;
$(x).prependTo("f");

chrome.debugger.getTargets(kms);

// case 2
chrome.debugger.getTargets(aaa);

let b = n[0].linkUrl;
$(x).prependTo("f");

function aaa(n, a) {
    console.log();
    $(n[0].linkUrl).prependTo("f"); // Expect 1 match here
    $(n[0].srcUrl).prependTo("f"); // Expect 1 match here
    $(n[0].pageUrl).prependTo("f"); // Expect 1 match here
    $(n[0].frameUrl).prependTo("f"); // Expect 1 match here
    $(n[0].selectionText).prependTo("f"); // Expect 1 match here

    $("f").prependTo(a.linkUrl);
    console.log();

    let x = n[0].linkUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n[0].srcUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n[0].pageUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n[0].frameUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n[0].selectionText;
    $(x).prependTo("f"); // Expect 1 match here
    console.log();
}

// case 3
chrome.debugger.getTargets(function (n, a) {
    console.log();
    $(n[0].linkUrl).prependTo("f"); // Expect 1 match here
    $(n[0].srcUrl).prependTo("f"); // Expect 1 match here
    $(n[0].pageUrl).prependTo("f"); // Expect 1 match here
    $(n[0].frameUrl).prependTo("f"); // Expect 1 match here
    $(n[0].selectionText).prependTo("f"); // Expect 1 match here
    console.log();

    let x = n[0].linkUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n[0].srcUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n[0].pageUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n[0].frameUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n[0].selectionText;
    $(x).prependTo("f"); // Expect 1 match here
    console.log();
});

// case 4
chrome.debugger.getTargets(function bbb(n, a) {
    console.log();
    $(n[0].linkUrl).prependTo("f"); // Expect 1 match here
    $(n[0].srcUrl).prependTo("f"); // Expect 1 match here
    $(n[0].pageUrl).prependTo("f"); // Expect 1 match here
    $(n[0].frameUrl).prependTo("f"); // Expect 1 match here
    $(n[0].selectionText).prependTo("f"); // Expect 1 match here
    console.log();

    let x = n[0].linkUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n[0].srcUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n[0].pageUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n[0].frameUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n[0].selectionText;
    $(x).prependTo("f"); // Expect 1 match here
    console.log();
});
