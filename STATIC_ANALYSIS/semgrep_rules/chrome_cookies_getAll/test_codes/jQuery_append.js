/*******************
chrome_cookies_getAll-jQuery_append
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    $("f").append(n.linkUrl); // Expect 1 match here
    $("f").append(n.srcUrl); // Expect 1 match here
    $("f").append(n.pageUrl); // Expect 1 match here
    $("f").append(n.frameUrl); // Expect 1 match here
    $("f").append(n.selectionText); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    $("f").append(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").append(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").append(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").append(x); // Expect 1 match here

    x = n.selectionText;
    $("f").append(x); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n.linkUrl;
$("f").append(x);

chrome.cookies.getAll({ name: "" }, kms);

// case 2
chrome.cookies.getAll({ name: "" }, aaa);

let b = n.linkUrl;
$("f").append(x);

function aaa(n, a) {
    console.log();
    $("f").append(n.linkUrl); // Expect 1 match here
    $("f").append(n.srcUrl); // Expect 1 match here
    $("f").append(n.pageUrl); // Expect 1 match here
    $("f").append(n.frameUrl); // Expect 1 match here
    $("f").append(n.selectionText); // Expect 1 match here

    $("f").append(a.linkUrl);
    console.log();

    let x = n.linkUrl;
    $("f").append(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").append(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").append(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").append(x); // Expect 1 match here

    x = n.selectionText;
    $("f").append(x); // Expect 1 match here
    console.log();
}

// case 3
chrome.cookies.getAll({ name: "" }, function (n, a) {
    console.log();
    $("f").append(n.linkUrl); // Expect 1 match here
    $("f").append(n.srcUrl); // Expect 1 match here
    $("f").append(n.pageUrl); // Expect 1 match here
    $("f").append(n.frameUrl); // Expect 1 match here
    $("f").append(n.selectionText); // Expect 1 match here
    console.log();

    let x = n.linkUrl;
    $("f").append(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").append(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").append(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").append(x); // Expect 1 match here

    x = n.selectionText;
    $("f").append(x); // Expect 1 match here
    console.log();
});

// case 4
chrome.cookies.getAll({ name: "" }, function bbb(n, a) {
    console.log();
    $("f").append(n.linkUrl); // Expect 1 match here
    $("f").append(n.srcUrl); // Expect 1 match here
    $("f").append(n.pageUrl); // Expect 1 match here
    $("f").append(n.frameUrl); // Expect 1 match here
    $("f").append(n.selectionText); // Expect 1 match here
    console.log();

    let x = n.linkUrl;
    $("f").append(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").append(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").append(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").append(x); // Expect 1 match here

    x = n.selectionText;
    $("f").append(x); // Expect 1 match here
    console.log();

    $(x).append("f");
});
