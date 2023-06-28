/*******************
chrome_cookies_getAll-jQuery_prepend
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    $("f").prepend(n.linkUrl); // Expect 1 match here
    $("f").prepend(n.srcUrl); // Expect 1 match here
    $("f").prepend(n.pageUrl); // Expect 1 match here
    $("f").prepend(n.frameUrl); // Expect 1 match here
    $("f").prepend(n.selectionText); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    $("f").prepend(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").prepend(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").prepend(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").prepend(x); // Expect 1 match here

    x = n.selectionText;
    $("f").prepend(x); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n.linkUrl;
$("f").prepend(x);

chrome.cookies.getAll({ name: "" }, kms);

// case 2
chrome.cookies.getAll({ name: "" }, aaa);

let b = n.linkUrl;
$("f").prepend(x);

function aaa(n, a) {
    console.log();
    $("f").prepend(n.linkUrl); // Expect 1 match here
    $("f").prepend(n.srcUrl); // Expect 1 match here
    $("f").prepend(n.pageUrl); // Expect 1 match here
    $("f").prepend(n.frameUrl); // Expect 1 match here
    $("f").prepend(n.selectionText); // Expect 1 match here

    $("f").prepend(a.linkUrl);
    console.log();

    let x = n.linkUrl;
    $("f").prepend(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").prepend(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").prepend(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").prepend(x); // Expect 1 match here

    x = n.selectionText;
    $("f").prepend(x); // Expect 1 match here
    console.log();
}

// case 3
chrome.cookies.getAll({ name: "" }, function (n, a) {
    console.log();
    $("f").prepend(n.linkUrl); // Expect 1 match here
    $("f").prepend(n.srcUrl); // Expect 1 match here
    $("f").prepend(n.pageUrl); // Expect 1 match here
    $("f").prepend(n.frameUrl); // Expect 1 match here
    $("f").prepend(n.selectionText); // Expect 1 match here
    console.log();

    let x = n.linkUrl;
    $("f").prepend(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").prepend(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").prepend(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").prepend(x); // Expect 1 match here

    x = n.selectionText;
    $("f").prepend(x); // Expect 1 match here
    console.log();
});

// case 4
chrome.cookies.getAll({ name: "" }, function bbb(n, a) {
    console.log();
    $("f").prepend(n.linkUrl); // Expect 1 match here
    $("f").prepend(n.srcUrl); // Expect 1 match here
    $("f").prepend(n.pageUrl); // Expect 1 match here
    $("f").prepend(n.frameUrl); // Expect 1 match here
    $("f").prepend(n.selectionText); // Expect 1 match here
    console.log();

    let x = n.linkUrl;
    $("f").prepend(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").prepend(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").prepend(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").prepend(x); // Expect 1 match here

    x = n.selectionText;
    $("f").prepend(x); // Expect 1 match here
    console.log();

    $(x).prepend("f");
});
