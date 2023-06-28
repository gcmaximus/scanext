/*******************
chrome_cookies_get-jQuery_insertBefore
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    $(n.linkUrl).insertBefore("f"); // Expect 1 match here
    $(n.srcUrl).insertBefore("f"); // Expect 1 match here
    $(n.pageUrl).insertBefore("f"); // Expect 1 match here
    $(n.frameUrl).insertBefore("f"); // Expect 1 match here
    $(n.selectionText).insertBefore("f"); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n.srcUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n.pageUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n.frameUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n.selectionText;
    $(x).insertBefore("f"); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n.linkUrl;
$(x).insertBefore("f");

chrome.cookies.get({ name: "" }, kms);

// case 2
chrome.cookies.get({ name: "" }, aaa);

let b = n.linkUrl;
$(x).insertBefore("f");

function aaa(n, a) {
    console.log();
    $(n.linkUrl).insertBefore("f"); // Expect 1 match here
    $(n.srcUrl).insertBefore("f"); // Expect 1 match here
    $(n.pageUrl).insertBefore("f"); // Expect 1 match here
    $(n.frameUrl).insertBefore("f"); // Expect 1 match here
    $(n.selectionText).insertBefore("f"); // Expect 1 match here

    $("f").insertBefore(a.linkUrl);
    console.log();

    let x = n.linkUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n.srcUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n.pageUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n.frameUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n.selectionText;
    $(x).insertBefore("f"); // Expect 1 match here
    console.log();
}

// case 3
chrome.cookies.get({ name: "" }, function (n, a) {
    console.log();
    $(n.linkUrl).insertBefore("f"); // Expect 1 match here
    $(n.srcUrl).insertBefore("f"); // Expect 1 match here
    $(n.pageUrl).insertBefore("f"); // Expect 1 match here
    $(n.frameUrl).insertBefore("f"); // Expect 1 match here
    $(n.selectionText).insertBefore("f"); // Expect 1 match here
    console.log();

    let x = n.linkUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n.srcUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n.pageUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n.frameUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n.selectionText;
    $(x).insertBefore("f"); // Expect 1 match here
    console.log();
});

// case 4
chrome.cookies.get({ name: "" }, function bbb(n, a) {
    console.log();
    $(n.linkUrl).insertBefore("f"); // Expect 1 match here
    $(n.srcUrl).insertBefore("f"); // Expect 1 match here
    $(n.pageUrl).insertBefore("f"); // Expect 1 match here
    $(n.frameUrl).insertBefore("f"); // Expect 1 match here
    $(n.selectionText).insertBefore("f"); // Expect 1 match here
    console.log();

    let x = n.linkUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n.srcUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n.pageUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n.frameUrl;
    $(x).insertBefore("f"); // Expect 1 match here

    x = n.selectionText;
    $(x).insertBefore("f"); // Expect 1 match here
    console.log();
});
