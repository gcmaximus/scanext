/*******************
chrome_cookies_get-jQuery_prependTo
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    $(n.linkUrl).prependTo("f"); // Expect 1 match here
    $(n.srcUrl).prependTo("f"); // Expect 1 match here
    $(n.pageUrl).prependTo("f"); // Expect 1 match here
    $(n.frameUrl).prependTo("f"); // Expect 1 match here
    $(n.selectionText).prependTo("f"); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.srcUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.pageUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.frameUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.selectionText;
    $(x).prependTo("f"); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n.linkUrl;
$(x).prependTo("f");

chrome.cookies.get({ name: "" }, kms);

// case 2
chrome.cookies.get({ name: "" }, aaa);

let b = n.linkUrl;
$(x).prependTo("f");

function aaa(n, a) {
    console.log();
    $(n.linkUrl).prependTo("f"); // Expect 1 match here
    $(n.srcUrl).prependTo("f"); // Expect 1 match here
    $(n.pageUrl).prependTo("f"); // Expect 1 match here
    $(n.frameUrl).prependTo("f"); // Expect 1 match here
    $(n.selectionText).prependTo("f"); // Expect 1 match here

    $("f").prependTo(a.linkUrl);
    console.log();

    let x = n.linkUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.srcUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.pageUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.frameUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.selectionText;
    $(x).prependTo("f"); // Expect 1 match here
    console.log();
}

// case 3
chrome.cookies.get({ name: "" }, function (n, a) {
    console.log();
    $(n.linkUrl).prependTo("f"); // Expect 1 match here
    $(n.srcUrl).prependTo("f"); // Expect 1 match here
    $(n.pageUrl).prependTo("f"); // Expect 1 match here
    $(n.frameUrl).prependTo("f"); // Expect 1 match here
    $(n.selectionText).prependTo("f"); // Expect 1 match here
    console.log();

    let x = n.linkUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.srcUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.pageUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.frameUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.selectionText;
    $(x).prependTo("f"); // Expect 1 match here
    console.log();
});

// case 4
chrome.cookies.get({ name: "" }, function bbb(n, a) {
    console.log();
    $(n.linkUrl).prependTo("f"); // Expect 1 match here
    $(n.srcUrl).prependTo("f"); // Expect 1 match here
    $(n.pageUrl).prependTo("f"); // Expect 1 match here
    $(n.frameUrl).prependTo("f"); // Expect 1 match here
    $(n.selectionText).prependTo("f"); // Expect 1 match here
    console.log();

    let x = n.linkUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.srcUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.pageUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.frameUrl;
    $(x).prependTo("f"); // Expect 1 match here

    x = n.selectionText;
    $(x).prependTo("f"); // Expect 1 match here
    console.log();
});
