/*******************
chrome_cookies_get-jQuery_after
*******************/

// Expected total matches: 40

// case 1
function kms(n, a) {
    console.log();
    $("f").after(n.linkUrl); // Expect 1 match here
    $("f").after(n.srcUrl); // Expect 1 match here
    $("f").after(n.pageUrl); // Expect 1 match here
    $("f").after(n.frameUrl); // Expect 1 match here
    $("f").after(n.selectionText); // Expect 1 match here

    console.log();

    let x = n.linkUrl;
    $("f").after(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").after(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").after(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").after(x); // Expect 1 match here

    x = n.selectionText;
    $("f").after(x); // Expect 1 match here
    console.log();
}

let n = { linkUrl: "" };
let a = n.linkUrl;
$("f").after(x);

chrome.cookies.get({ name: "" }, kms);

// case 2
chrome.cookies.get({ name: "" }, aaa);

let b = n.linkUrl;
$("f").after(x);

function aaa(n, a) {
    console.log();
    $("f").after(n.linkUrl); // Expect 1 match here
    $("f").after(n.srcUrl); // Expect 1 match here
    $("f").after(n.pageUrl); // Expect 1 match here
    $("f").after(n.frameUrl); // Expect 1 match here
    $("f").after(n.selectionText); // Expect 1 match here

    $("f").after(a.linkUrl);
    console.log();

    let x = n.linkUrl;
    $("f").after(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").after(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").after(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").after(x); // Expect 1 match here

    x = n.selectionText;
    $("f").after(x); // Expect 1 match here
    console.log();
}

// case 3
chrome.cookies.get({ name: "" }, function (n, a) {
    console.log();
    $("f").after(n.linkUrl); // Expect 1 match here
    $("f").after(n.srcUrl); // Expect 1 match here
    $("f").after(n.pageUrl); // Expect 1 match here
    $("f").after(n.frameUrl); // Expect 1 match here
    $("f").after(n.selectionText); // Expect 1 match here
    console.log();

    let x = n.linkUrl;
    $("f").after(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").after(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").after(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").after(x); // Expect 1 match here

    x = n.selectionText;
    $("f").after(x); // Expect 1 match here
    console.log();
});

// case 4
chrome.cookies.get({ name: "" }, function bbb(n, a) {
    console.log();
    $("f").after(n.linkUrl); // Expect 1 match here
    $("f").after(n.srcUrl); // Expect 1 match here
    $("f").after(n.pageUrl); // Expect 1 match here
    $("f").after(n.frameUrl); // Expect 1 match here
    $("f").after(n.selectionText); // Expect 1 match here
    console.log();

    let x = n.linkUrl;
    $("f").after(x); // Expect 1 match here

    x = n.srcUrl;
    $("f").after(x); // Expect 1 match here

    x = n.pageUrl;
    $("f").after(x); // Expect 1 match here

    x = n.frameUrl;
    $("f").after(x); // Expect 1 match here

    x = n.selectionText;
    $("f").after(x); // Expect 1 match here
    console.log();

    $(x).after("f");
});
