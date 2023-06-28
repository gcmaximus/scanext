/*******************
chrome_cookies_getAll-jQuery_wrapAll
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    $("f").wrapAll(n.linkUrl); // Expect 1 match here
    $("f").wrapAll(n.srcUrl); // Expect 1 match here
    $("f").wrapAll(n.pageUrl); // Expect 1 match here
    $("f").wrapAll(n.frameUrl); // Expect 1 match here
    $("f").wrapAll(n.selectionText); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    $("f").wrapAll(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").wrapAll(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").wrapAll(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").wrapAll(x); // Expect 1 match here

    x = n.selectionText;
    $("f").wrapAll(x); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n.linkUrl;
$("f").wrapAll(x);

chrome.cookies.getAll({ name: "" }, kms);

// case 2
chrome.cookies.getAll({ name: "" }, aaa);

let b = n.linkUrl;
$("f").wrapAll(x);

function aaa(n, a) {
    console.log();
    $("f").wrapAll(n.linkUrl); // Expect 1 match here
    $("f").wrapAll(n.srcUrl); // Expect 1 match here
    $("f").wrapAll(n.pageUrl); // Expect 1 match here
    $("f").wrapAll(n.frameUrl); // Expect 1 match here
    $("f").wrapAll(n.selectionText); // Expect 1 match here

    $("f").wrapAll(a.linkUrl);
    console.log();

    let x = n.linkUrl;
    $("f").wrapAll(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").wrapAll(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").wrapAll(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").wrapAll(x); // Expect 1 match here

    x = n.selectionText;
    $("f").wrapAll(x); // Expect 1 match here
    console.log();
}

// case 3
chrome.cookies.getAll({ name: "" }, function (n, a) {
    console.log();
    $("f").wrapAll(n.linkUrl); // Expect 1 match here
    $("f").wrapAll(n.srcUrl); // Expect 1 match here
    $("f").wrapAll(n.pageUrl); // Expect 1 match here
    $("f").wrapAll(n.frameUrl); // Expect 1 match here
    $("f").wrapAll(n.selectionText); // Expect 1 match here
    console.log();

    let x = n.linkUrl;
    $("f").wrapAll(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").wrapAll(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").wrapAll(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").wrapAll(x); // Expect 1 match here

    x = n.selectionText;
    $("f").wrapAll(x); // Expect 1 match here
    console.log();
});

// case 4
chrome.cookies.getAll({ name: "" }, function bbb(n, a) {
    console.log();
    $("f").wrapAll(n.linkUrl); // Expect 1 match here
    $("f").wrapAll(n.srcUrl); // Expect 1 match here
    $("f").wrapAll(n.pageUrl); // Expect 1 match here
    $("f").wrapAll(n.frameUrl); // Expect 1 match here
    $("f").wrapAll(n.selectionText); // Expect 1 match here
    console.log();

    let x = n.linkUrl;
    $("f").wrapAll(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").wrapAll(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").wrapAll(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").wrapAll(x); // Expect 1 match here

    x = n.selectionText;
    $("f").wrapAll(x); // Expect 1 match here
    console.log();

    $(x).wrapAll("f");
});
