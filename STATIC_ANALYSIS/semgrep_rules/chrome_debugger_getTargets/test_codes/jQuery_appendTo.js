/*******************
chrome_debugger_getTargets-jQuery_appendTo
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    $(n[0].linkUrl).appendTo("f"); // Expect 1 match here
    $(n[0].srcUrl).appendTo("f"); // Expect 1 match here
    $(n[0].pageUrl).appendTo("f"); // Expect 1 match here
    $(n[0].frameUrl).appendTo("f"); // Expect 1 match here
    $(n[0].selectionText).appendTo("f"); // Expect 1 match here

    console.log();

    let x = n[0].linkUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n[0].srcUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n[0].pageUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n[0].frameUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n[0].selectionText;
    $(x).appendTo("f"); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n[0].linkUrl;
$(x).appendTo("f");

chrome.debugger.getTargets(kms);

// case 2
chrome.debugger.getTargets(aaa);

let b = n[0].linkUrl;
$(x).appendTo("f");

function aaa(n, a) {
    console.log();
    $(n[0].linkUrl).appendTo("f"); // Expect 1 match here
    $(n[0].srcUrl).appendTo("f"); // Expect 1 match here
    $(n[0].pageUrl).appendTo("f"); // Expect 1 match here
    $(n[0].frameUrl).appendTo("f"); // Expect 1 match here
    $(n[0].selectionText).appendTo("f"); // Expect 1 match here

    $("f").appendTo(a.linkUrl);
    console.log();

    let x = n[0].linkUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n[0].srcUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n[0].pageUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n[0].frameUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n[0].selectionText;
    $(x).appendTo("f"); // Expect 1 match here
    console.log();
}

// case 3
chrome.debugger.getTargets(function (n, a) {
    console.log();
    $(n[0].linkUrl).appendTo("f"); // Expect 1 match here
    $(n[0].srcUrl).appendTo("f"); // Expect 1 match here
    $(n[0].pageUrl).appendTo("f"); // Expect 1 match here
    $(n[0].frameUrl).appendTo("f"); // Expect 1 match here
    $(n[0].selectionText).appendTo("f"); // Expect 1 match here
    console.log();

    let x = n[0].linkUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n[0].srcUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n[0].pageUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n[0].frameUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n[0].selectionText;
    $(x).appendTo("f"); // Expect 1 match here
    console.log();
});

// case 4
chrome.debugger.getTargets(function bbb(n, a) {
    console.log();
    $(n[0].linkUrl).appendTo("f"); // Expect 1 match here
    $(n[0].srcUrl).appendTo("f"); // Expect 1 match here
    $(n[0].pageUrl).appendTo("f"); // Expect 1 match here
    $(n[0].frameUrl).appendTo("f"); // Expect 1 match here
    $(n[0].selectionText).appendTo("f"); // Expect 1 match here
    console.log();

    let x = n[0].linkUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n[0].srcUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n[0].pageUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n[0].frameUrl;
    $(x).appendTo("f"); // Expect 1 match here

    x = n[0].selectionText;
    $(x).appendTo("f"); // Expect 1 match here
    console.log();
});
